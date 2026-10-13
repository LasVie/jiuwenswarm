import React, { useCallback, useEffect, useState } from '../../jiuwenswarm/channels/web/frontend/node_modules/react';
import { createRoot } from '../../jiuwenswarm/channels/web/frontend/node_modules/react-dom/client';
import i18n from '../../jiuwenswarm/channels/web/frontend/node_modules/i18next';
import { initReactI18next } from '../../jiuwenswarm/channels/web/frontend/node_modules/react-i18next';
import { DesktopBrowserPane } from '../../jiuwenswarm/channels/web/frontend/src/components/DesktopBrowserPane';
import { useDesktopBrowserAttention } from '../../jiuwenswarm/channels/web/frontend/src/components/DesktopBrowserPane/useDesktopBrowserAttention';
import { SEND_CHAT_MESSAGE_EVENT } from '../../jiuwenswarm/channels/web/frontend/src/components/DesktopBrowserPane/OpenCLIPrompt';
import en from '../../jiuwenswarm/channels/web/frontend/src/i18n/locales/en.json';
import zh from '../../jiuwenswarm/channels/web/frontend/src/i18n/locales/zh.json';
import { SettingsPage } from '../../jiuwenswarm/channels/web/frontend/src/features/settings/SettingsPage';
import { createSettingsPageDefinition } from '../../jiuwenswarm/channels/web/frontend/src/features/settings/registry/createSettingsPageDefinition';
import { openSourceSettingsAccessPolicy } from '../../jiuwenswarm/channels/web/frontend/src/features/settings/registry/accessPolicy';
import { browserModule } from '../../jiuwenswarm/channels/web/frontend/src/features/settings/modules/browser/definition';
import { generalModule } from '../../jiuwenswarm/channels/web/frontend/src/features/settings/modules/general/definition';
import '../../jiuwenswarm/channels/web/frontend/src/styles/foundation.css';
import '../../jiuwenswarm/channels/web/frontend/src/styles/themes/default/light.css';

// The shell stays mounted while the production browser pane is unmounted.
const settingsDefinition = createSettingsPageDefinition({
  id: 'fixture-settings', compositionMode: 'base', accessPolicy: openSourceSettingsAccessPolicy,
  modules: [browserModule, generalModule],
});

async function settingsRequest(method: string, params?: unknown) {
  if (method === 'locale.set_conf') return {};
  const response = await fetch('/settings', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ method, params }),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error);
  return result;
}

function Fixture() {
  const [open, setOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const reveal = useCallback(() => { setSettingsOpen(false); setOpen(true); }, []);
  const attention = useDesktopBrowserAttention('session-one', reveal);
  useEffect(() => {
    const listener = (event: Event) => setMessage((event as CustomEvent).detail.content);
    window.addEventListener(SEND_CHAT_MESSAGE_EVENT, listener);
    return () => window.removeEventListener(SEND_CHAT_MESSAGE_EVENT, listener);
  }, []);
  return (
    <div className={`fixture-shell${settingsOpen ? ' fixture-shell--settings' : ''}`}>
      <aside className="fixture-controls">
        <button data-testid="fixture-collapse" onClick={() => setOpen(false)}>Other tab</button>
        <button data-testid="fixture-settings" onClick={() => { setOpen(false); setSettingsOpen(true); }}>Settings</button>
        <button data-testid="fixture-browser" onClick={() => { setSettingsOpen(false); setOpen(true); }}>Browser</button>
        <output data-testid="fixture-message">{message}</output>
      </aside>
      {settingsOpen ? (
        <SettingsPage definition={settingsDefinition} initialModuleId="browser" isConnected connectionState="ready" request={settingsRequest} />
      ) : open ? <DesktopBrowserPane sessionId="session-one" attention={attention} /> : <p data-testid="fixture-other-tab">Planning</p>}
    </div>
  );
}

void i18n.use(initReactI18next).init({ lng: 'en', resources: { en: { translation: en }, zh: { translation: zh } } }).then(() => {
  createRoot(document.getElementById('root')!).render(<Fixture />);
});
