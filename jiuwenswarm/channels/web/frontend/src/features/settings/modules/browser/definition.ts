import { settingsNavigationIcons } from '../../../../assets/settings';
import type { SettingsModuleDefinition } from '../../registry/types';
import { OpenCLIStatusSetting } from './OpenCLIStatusSetting';

export const browserModule: SettingsModuleDefinition = {
  id: 'browser',
  titleKey: 'settingsPanel.categories.browser',
  icon: settingsNavigationIcons.browser,
  source: 'browser',
  sections: [
    {
      id: 'browser-runtime',
      items: [
        { id: 'browser-path', component: 'input', key: 'chrome_path' },
        {
          id: 'browser-run-mode',
          component: 'select',
          key: 'headless',
          options: [
            { value: false, labelKey: 'settingsPanel.browser.headed' },
            { value: true, labelKey: 'settingsPanel.browser.headless' },
          ],
        },
      ],
    },
    {
      id: 'browser-opencli',
      titleKey: 'settingsPanel.browser.opencli.title',
      items: [
        {
          id: 'browser-opencli-enabled',
          component: 'switch',
          key: 'opencli.enabled',
          subItems: {
            show: 'when-parent-checked',
            disabled: 'when-parent-unchecked',
            items: [
              {
                id: 'browser-opencli-worker-page',
                component: 'select',
                key: 'opencli.worker_page',
                options: [
                  { value: 'sidebar', labelKey: 'settingsPanel.browser.opencli.sidebar' },
                  { value: 'hidden', labelKey: 'settingsPanel.browser.opencli.hidden' },
                ],
              },
            ],
          },
        },
        { id: 'browser-opencli-status', component: 'custom', render: OpenCLIStatusSetting },
      ],
    },
  ],
};
