import type { SettingValue } from '../registry/types';

type BrowserDecisionMode = 'llm' | 'shadow' | 'hybrid';
type BrowserDecisionProvider = 'openrouter' | 'typesafe' | 'custom';

export type BrowserSettingsState = {
  chrome_path: string;
  headless: boolean;
  decision_mode: BrowserDecisionMode;
  decision_provider: BrowserDecisionProvider;
  decision_model: string;
  decision_display_name: string;
  decision_api_base: string;
  // Read-only: path.get reports whether the provider's key is set, never the key.
  jev_key_configured: boolean;
  'opencli.enabled': boolean;
  'opencli.worker_page': 'sidebar' | 'hidden';
  opencli_status: Record<string, unknown>;
};

const BROWSER_DECISION_MODES: readonly unknown[] = ['llm', 'shadow', 'hybrid'];
const BROWSER_DECISION_PROVIDERS: readonly unknown[] = ['openrouter', 'typesafe', 'custom'];
const DECISION_FIELDS = new Set([
  'decision_mode',
  'decision_provider',
  'decision_model',
  'decision_display_name',
  'decision_api_base',
]);

/**
 * Accepts both the server payload (nested `opencli`) and the page's own flat
 * state (`opencli.enabled`), since local patches re-normalize the current state.
 */
export function normalizeBrowserState(value: Record<string, unknown> | undefined): BrowserSettingsState {
  const options = value?.opencli as Record<string, unknown> | undefined;
  const enabled = options && 'enabled' in options ? options.enabled : value?.['opencli.enabled'];
  const workerPage = options && 'worker_page' in options ? options.worker_page : value?.['opencli.worker_page'];
  return {
    chrome_path: typeof value?.chrome_path === 'string' ? value.chrome_path : '',
    headless: value?.headless === undefined ? true : value.headless === true,
    decision_mode: BROWSER_DECISION_MODES.includes(value?.decision_mode)
      ? (value?.decision_mode as BrowserDecisionMode)
      : 'llm',
    decision_provider: BROWSER_DECISION_PROVIDERS.includes(value?.decision_provider)
      ? (value?.decision_provider as BrowserDecisionProvider)
      : 'typesafe',
    jev_key_configured: value?.jev_key_configured === true,
    decision_model: typeof value?.decision_model === 'string' ? value.decision_model : '',
    decision_display_name: typeof value?.decision_display_name === 'string' ? value.decision_display_name : '',
    decision_api_base: typeof value?.decision_api_base === 'string' ? value.decision_api_base : '',
    'opencli.enabled': enabled === true,
    'opencli.worker_page': workerPage === 'hidden' ? 'hidden' : 'sidebar',
    opencli_status:
      value?.opencli_status && typeof value.opencli_status === 'object'
        ? (value.opencli_status as Record<string, unknown>)
        : { state: 'off' },
  };
}

/** Send only edited fields; browser.opencli and enabled_sites are merged on the server. */
export function buildBrowserSettingsPatch(updates: Record<string, SettingValue>): Record<string, unknown> {
  const patch: Record<string, unknown> = {};
  const opencli: Record<string, SettingValue> = {};
  for (const [key, value] of Object.entries(updates)) {
    if (key === 'chrome_path' || key === 'headless' || DECISION_FIELDS.has(key)) patch[key] = value;
    else if (key === 'opencli.enabled' || key === 'opencli.worker_page') opencli[key.slice('opencli.'.length)] = value;
    else throw new Error(`Unsupported browser setting: ${key}`);
  }
  if (Object.keys(opencli).length) patch.opencli = opencli;
  return patch;
}
