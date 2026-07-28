# Copyright (c) Huawei Technologies Co., Ltd. 2026. All rights reserved.

"""Structured OpenCLI execution guarded by progressive Skill disclosure."""

from __future__ import annotations

from importlib import import_module
from typing import Any

_EXPORTS = {
    "OPENCLI_WEB_SKILL_NAME": (
        "jiuwenswarm.agents.harness.common.opencli.contracts",
        "OPENCLI_WEB_SKILL_NAME",
    ),
    "DisclosureReceiptStore": (
        "jiuwenswarm.agents.harness.common.opencli.disclosure",
        "DisclosureReceiptStore",
    ),
    "get_opencli_disclosure_store": (
        "jiuwenswarm.agents.harness.common.opencli.disclosure",
        "get_opencli_disclosure_store",
    ),
    "OpenCLIDisclosureRail": (
        "jiuwenswarm.agents.harness.common.opencli.rail",
        "OpenCLIDisclosureRail",
    ),
    "OPENCLI_EXECUTE_TOOL_NAME": (
        "jiuwenswarm.agents.harness.common.opencli.tool",
        "OPENCLI_EXECUTE_TOOL_NAME",
    ),
    "OpenCLIExecuteTool": (
        "jiuwenswarm.agents.harness.common.opencli.tool",
        "OpenCLIExecuteTool",
    ),
}

__all__ = [
    "DisclosureReceiptStore",
    "OPENCLI_EXECUTE_TOOL_NAME",
    "OPENCLI_WEB_SKILL_NAME",
    "OpenCLIDisclosureRail",
    "OpenCLIExecuteTool",
    "get_opencli_disclosure_store",
]


def __getattr__(name: str) -> Any:
    """Resolve the existing public API without eager runtime side effects."""

    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attribute_name = target
    value = getattr(import_module(module_name), attribute_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Include lazily exported names in interactive module discovery."""

    return sorted(set(globals()) | set(__all__))
