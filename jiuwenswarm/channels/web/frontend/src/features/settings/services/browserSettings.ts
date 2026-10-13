import type { SettingValue } from '../registry/types';

export type BrowserSettingsState = {
  chrome_path: string;
  headless: boolean;
  'opencli.enabled': boolean;
  'opencli.worker_page': 'sidebar' | 'hidden';
  opencli_status: Record<string, unknown>;
};

export function normalizeBrowserState(value: Record<string, unknown> | undefined): BrowserSettingsState {
  const options = value?.opencli as Record<string, unknown> | undefined;
  return {
    chrome_path: typeof value?.chrome_path === 'string' ? value.chrome_path : '',
    headless: value?.headless === undefined ? true : value.headless === true,
    'opencli.enabled': options?.enabled === true,
    'opencli.worker_page': options?.worker_page === 'hidden' ? 'hidden' : 'sidebar',
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
    if (key === 'chrome_path' || key === 'headless') patch[key] = value;
    else if (key === 'opencli.enabled' || key === 'opencli.worker_page') opencli[key.slice('opencli.'.length)] = value;
    else throw new Error(`Unsupported browser setting: ${key}`);
  }
  if (Object.keys(opencli).length) patch.opencli = opencli;
  return patch;
}
