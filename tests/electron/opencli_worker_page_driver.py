"""JSON-lines driver for the real desktop-host OpenCLI integration test."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from jiuwenswarm.extensions.opencli.catalog import Catalog
from jiuwenswarm.extensions.opencli.pending import PendingStore
from jiuwenswarm.extensions.opencli.sources.opencli import OpenCLISource, prepare_runtime
from jiuwenswarm.extensions.opencli.tools import OpenCLIDescribeTool, OpenCLIRunTool, OpenCLIToolContext
from jiuwenswarm.extensions.opencli.worker_page import HostBinding, get_slot


def emit(payload):
    print(json.dumps(payload, ensure_ascii=False, default=str), flush=True)


def prepare():
    runtime = prepare_runtime(os.environ['SMOKE_ELECTRON'], user_workspace_dir=Path(os.environ['SMOKE_WORKSPACE']))
    emit({'cli_path': str(runtime.cli_path), 'home_dir': str(runtime.home_dir), 'node_version': runtime.node_version})


async def agent_task(request, runtime, catalog, binding, workspace):
    """Run the real Browser Agent/rails with scripted model decisions, no model API.

    Only the model and fixture catalog are substituted. Swarm contribution,
    Core factory, MCP, tool execution and authoritative finalization are real.
    """
    from openjiuwen.core.foundation.llm import AssistantMessage, Model, ToolCall
    from openjiuwen.core.foundation.llm.schema.config import ModelClientConfig, ModelRequestConfig
    from openjiuwen.core.foundation.tool import McpServerConfig
    from openjiuwen.core.runner import Runner
    from openjiuwen.core.session.agent import create_agent_session
    from openjiuwen.harness.subagents.browser_agent import build_browser_agent_config, create_browser_agent
    from openjiuwen.harness.tools.browser_move.playwright_runtime.config import BrowserRunGuardrails, RuntimeSettings
    from jiuwenswarm.extensions.opencli import apply_opencli_contribution

    command = request.get('command', 'read')
    decisions = [
        ('opencli_describe', {'site': 'fixture'}),
        ('opencli_run', {'site': 'fixture', 'command': command}),
    ]
    if command == 'hybrid':
        decisions = [
            ('opencli_describe', {'site': 'fixture'}),
            ('opencli_run', {'site': 'fixture', 'command': 'read'}),
            ('browser_navigate', {'url': os.environ['SMOKE_FIXTURE_ORIGIN'] + '/playwright-fallback'}),
            ('opencli_run', {'site': 'fixture', 'command': 'read'}),
        ]
    elif command == 'multiple':
        decisions = [('opencli_describe', {'site': 'fixture'})] + [
            ('opencli_run', {'site': 'fixture', 'command': 'read', 'args': {'page': page}})
            for page in (1, 2, 3)
        ]
    model_calls = []
    executed_calls = []

    async def scripted_invoke(self, *, messages, **kwargs):
        index = len(model_calls)
        model_calls.append([str(message) for message in messages])
        if index < len(decisions):
            name, args = decisions[index]
            names = [getattr(tool, 'name', '') if not isinstance(tool, dict) else tool.get('name', '')
                     for tool in kwargs.get('tools') or []]
            candidates = [visible for visible in names if visible.endswith(name)]
            if len(candidates) != 1:
                raise AssertionError(f'{name} must be visible exactly once, got {candidates}')
            name = candidates[0]
            executed_calls.append(name)
            return AssistantMessage(content='', tool_calls=[ToolCall(
                id=f'fixture-{index}', type='function', name=name, arguments=json.dumps(args))])
        if command not in {'read', 'hybrid', 'multiple'}:
            raise AssertionError('a blocked task must stop before another model call')
        return AssistantMessage(content='The first two titles are First item and Second item.')

    env = {
        'PLAYWRIGHT_MCP_TARGET_RESOLVER': binding.resolver,
        'PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN': binding.token,
        'PLAYWRIGHT_MCP_CDP_ENDPOINT': os.environ['SMOKE_CDP_ENDPOINT'],
        'PLAYWRIGHT_MCP_SESSION_ID': binding.session_id,
        'PLAYWRIGHT_MCP_MEMBER_ID': binding.member_id,
        'JIUWENSWARM_ELECTRON_NODE': runtime.node_command,
        'ELECTRON_RUN_AS_NODE': '1',
        'PATH': os.environ['SMOKE_MCP_PATH'],
    }
    settings = RuntimeSettings(provider='OpenAI', api_key='fixture-key',
        api_base='https://example.invalid/v1', model_name='fixture-model',
        mcp_cfg=McpServerConfig(server_id='fixture-browser-task', server_name='fixture-browser-task',
            server_path='stdio://fixture-browser', client_type='stdio',
            params={'command': runtime.node_command, 'args': [os.environ['SMOKE_MCP_WRAPPER']],
                    'env': env, 'cwd': str(workspace)}),
        guardrails=BrowserRunGuardrails(timeout_s=120))
    model = Model(ModelClientConfig(client_provider='OpenAI', api_key='fixture-key',
                  api_base='https://example.invalid/v1'), ModelRequestConfig(model='fixture-model'))
    agent = None
    try:
        await Runner.start()
        with patch.object(Model, 'invoke', scripted_invoke), \
                patch('jiuwenswarm.extensions.opencli.sources.opencli.prepare_runtime',
                      return_value=replace(runtime, catalog=catalog)), \
                patch('jiuwenswarm.common.utils.get_user_workspace_dir', return_value=workspace):
            spec = build_browser_agent_config(model, settings=settings, workspace=str(workspace), language='en')
            assert apply_opencli_contribution(spec, {'browser': {'opencli': {'enabled': True}}})
            agent = create_browser_agent(spec.model, settings=settings, tools=spec.tools,
                system_prompt=spec.system_prompt, workspace=str(workspace), language='en',
                max_iterations=6, enable_model_anomaly_detection_rail=False, enable_sys_operation=False)
            query = ('List the first 2 item titles.' if command in {'read', 'hybrid', 'multiple'}
                     else 'Read items that require captcha verification.')
            session = create_agent_session(session_id=f'fixture-{command}', card=agent.card)
            await session.pre_run(inputs={'query': query})
            result = await agent.invoke({'query': query}, session)
            task_state = session.get_state('__browser_phase_budget_state__')
            await session.post_run()
            return {'result': result, 'model_calls': len(model_calls),
                    'executed_calls': executed_calls,
                    'local_core': sys.modules['openjiuwen'].__file__, 'task_state': task_state,
                    'rails': [type(rail).__name__ for rail in agent.configured_rails()]}
    finally:
        if agent is not None:
            await agent.cleanup_task_resources()
        await Runner.stop()


async def serve():
    workspace = Path(os.environ['SMOKE_WORKSPACE'])
    runtime = prepare_runtime(os.environ['SMOKE_ELECTRON'], user_workspace_dir=workspace)
    catalog = Catalog.from_payload({'commands': [
        {'site': 'fixture', 'command': command, 'access': 'write' if command.startswith('write') else 'read',
         'needs_browser': True,
         'args': [{'name': 'page', 'type': 'int', 'default': 1}] if command == 'read' else []}
        for command in ['read', 'write', 'write-lost', 'write-slow', 'captcha', 'slow']
    ]}, source='opencli')
    binding = HostBinding(resolver=os.environ['SMOKE_RESOLVER'], token=os.environ['SMOKE_TOKEN'],
                          session_id='session-one')
    # The settings UI exercises the real config adapter against an isolated
    # YAML file, never the user's application configuration.
    from jiuwenswarm.common import config as config_module
    from jiuwenswarm.common.schema.agent import AgentRequest
    from jiuwenswarm.common.schema.message import ReqMethod
    from jiuwenswarm.extensions.opencli import browser_agent_contribution
    from jiuwenswarm.extensions.opencli.gate import read_settings
    from jiuwenswarm.server.runtime.gateway_adapter.config_adapter import ConfigAdapter
    from types import SimpleNamespace
    import yaml
    config_path = workspace / 'browser-settings.yaml'
    config_path.write_text('browser:\n  chrome_path: ""\n  headless: true\n  opencli:\n'
                          '    enabled: false\n    worker_page: sidebar\n    enabled_sites: [bilibili]\n', encoding='utf-8')
    def read_config():
        return yaml.safe_load(config_path.read_text(encoding='utf-8'))
    settings_env = {
        'PLAYWRIGHT_MCP_TARGET_RESOLVER': binding.resolver,
        'PLAYWRIGHT_MCP_TARGET_RESOLVER_TOKEN': binding.token,
        'PLAYWRIGHT_MCP_SESSION_ID': binding.session_id,
        'JIUWENSWARM_ELECTRON_NODE': runtime.node_command,
        'JIUWENSWARM_ELECTRON_NODE_VERSION': runtime.node_version,
    }
    context = OpenCLIToolContext(source=OpenCLISource(runtime), catalog=catalog,
        slot=get_slot(binding), pending=PendingStore(workspace/'pending'),
        session_id=binding.session_id, member_id=binding.member_id, work_dir=workspace,
        language='en', command_timeout_s=15, confirm_timeout_s=20)
    tools = {'run': OpenCLIRunTool(context), 'describe': OpenCLIDescribeTool(context)}
    running = {}

    async def handle(request):
        request_id = request['id']
        try:
            action = request.get('action', 'run')
            if action == 'pending':
                data = [record.public() for record in context.pending.find(
                    session_id=binding.session_id, member_id=binding.member_id, site='fixture')]
            elif action == 'config':
                method = ReqMethod.PATH_GET if request['method'] == 'path.get' else ReqMethod.PATH_SET
                with patch.object(config_module, 'CONFIG_YAML_PATH', config_path), \
                     patch.object(config_module, 'get_config', read_config), \
                     patch.dict(os.environ, {'BROWSER_DRIVER': 'remote', 'JIUWENSWARM_BROWSER_FORCE_MANAGED': '0',
                         'PLAYWRIGHT_MCP_TARGET_RESOLVER': binding.resolver,
                         'PLAYWRIGHT_MCP_ENV_JSON': json.dumps(settings_env)}):
                    response = await ConfigAdapter().handle(AgentRequest(request_id=str(request_id), channel_id='web',
                        req_method=method, params=request.get('params', {})))
                if not response.ok:
                    raise ValueError(response.payload.get('error', 'settings update failed'))
                data = {'payload': response.payload, 'metadata': response.metadata}
            elif action == 'assembly':
                from jiuwenswarm.common.browser_config import resolve_browser_path
                settings = SimpleNamespace(mcp_cfg=SimpleNamespace(params={'env': settings_env}))
                if resolve_browser_path(read_config().get('browser', {})):
                    settings = SimpleNamespace(mcp_cfg=SimpleNamespace(params={'env': {}}))
                with patch('jiuwenswarm.common.utils.get_user_workspace_dir', lambda: workspace):
                    contribution = browser_agent_contribution(settings, read_config(), language='en', workspace=workspace)
                data = {'tools': [tool.card.name for tool in contribution.tools] if contribution else [],
                        'prompt': contribution.prompt_text if contribution else '', 'config': read_config()}
            elif action == 'task':
                data = await agent_task(request, runtime, catalog, binding, workspace)
            elif action == 'site':
                # Optional real-site READ ONLY check. Never open a write command.
                spec = runtime.catalog.get('bilibili', request['command'])
                if spec is None or spec.access != 'read':
                    raise ValueError('the real-site check requires a bundled Bilibili read command')
                site_context = OpenCLIToolContext(source=OpenCLISource(runtime), catalog=runtime.catalog,
                    slot=context.slot, pending=context.pending, session_id=binding.session_id,
                    member_id=binding.member_id, work_dir=workspace, language='en')
                site_tool = OpenCLIDescribeTool(site_context) if request.get('operation') == 'describe' else OpenCLIRunTool(site_context)
                data = (await site_tool.invoke({
                    'site': 'bilibili', 'command': request['command'], 'args': request.get('args', {})})).data
            else:
                tool = tools[action]
                if action == 'run':
                    options = read_settings(read_config())
                    tool = OpenCLIRunTool(replace(context,
                        slot=get_slot(replace(binding, visibility=options.worker_page)),
                        confirm_timeout_s=request.get('confirm_timeout_s', context.confirm_timeout_s)))
                data = (await tool.invoke({'site': 'fixture', 'command': request.get('command', ''),
                                          'args': request.get('args', {})})).data
            emit({'id': request_id, 'data': data})
        except asyncio.CancelledError:
            emit({'id': request_id, 'cancelled': True})
        except Exception as exc:
            emit({'id': request_id, 'error': str(exc)})
        finally:
            running.pop(request_id, None)

    while line := await asyncio.to_thread(sys.stdin.readline):
        request = json.loads(line)
        if request.get('action') == 'cancel':
            task = running.get(request['target'])
            if task is not None:
                task.cancel()
            emit({'id': request['id'], 'data': {'requested': task is not None}})
        else:
            running[request['id']] = asyncio.create_task(handle(request))
    await asyncio.gather(*list(running.values()), return_exceptions=True)


if __name__ == '__main__':
    if sys.argv[1] == 'prepare':
        prepare()
    else:
        asyncio.run(serve())
