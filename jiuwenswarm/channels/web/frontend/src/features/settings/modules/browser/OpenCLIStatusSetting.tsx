import { useTranslation } from 'react-i18next';
import { SettingRow } from '../../components/SettingRow';
import { useSettingsSource } from '../../services/SettingsSourceProvider';

const STATUS_KEYS: Record<string, string> = {
  off: 'settingsPanel.browser.opencli.states.off',
  available: 'settingsPanel.browser.opencli.states.available',
  unsupported_browser_mode: 'settingsPanel.browser.opencli.states.unsupportedBrowser',
  runtime_missing: 'settingsPanel.browser.opencli.states.runtimeMissing',
  electron_node_unavailable: 'settingsPanel.browser.opencli.states.electronUnavailable',
  no_sites_enabled: 'settingsPanel.browser.opencli.states.noSites',
};

export function OpenCLIStatusSetting() {
  const { t } = useTranslation();
  const { values } = useSettingsSource();
  const status = values.opencli_status as Record<string, unknown> | undefined;
  const state = values['opencli.enabled'] === true ? String(status?.state || 'runtime_missing') : 'off';
  return (
    <SettingRow
      title={<span data-testid="settings-opencli-status-title">{t('settingsPanel.browser.opencli.status')}</span>}
      description={
        <span role="status" data-testid="settings-opencli-status" data-variant={state}>
          {t(STATUS_KEYS[state] || STATUS_KEYS.runtime_missing, {
            count: typeof status?.site_count === 'number' ? status.site_count : 0,
            version: String(status?.version || ''),
          })}
        </span>
      }
    />
  );
}
