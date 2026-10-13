import { useEffect, useState } from 'react';
import type { ElectronBrowserAttention, ElectronBrowserState } from '../../types/electron';
import { requestDesktopBrowserTab } from '../../features/desktopBrowserFile';

/** Mount in the app shell so a collapsed/unmounted browser pane can be opened. */
export function useDesktopBrowserAttention(sessionId: string, onReveal: () => void) {
  const [attention, setAttention] = useState<ElectronBrowserAttention | null>(null);

  useEffect(() => {
    const browser = window.jiuwenDesktop?.browser;
    if (!browser || !sessionId) return;
    let active = true;
    let lastPendingKey = '';
    const reveal = (request: ElectronBrowserAttention) => {
      if (!active || request.sessionId !== sessionId) return;
      requestDesktopBrowserTab(sessionId);
      setAttention(request);
      onReveal();
    };
    const recover = (panels: ElectronBrowserState[]) => {
      const pending = panels.find((panel) => panel.sessionId === sessionId && (panel.pendingConfirm || panel.hold));
      if (!pending) {
        lastPendingKey = '';
        setAttention(null);
        return;
      }
      const key = pending.pendingConfirm?.requestId || pending.hold?.blockId || '';
      if (!key || key === lastPendingKey) return;
      lastPendingKey = key;
      reveal({
        sessionId,
        panelId: pending.panelId,
        kind: pending.pendingConfirm ? 'confirm' : 'human',
        visibility: pending.visibility,
      });
    };
    const offAttention = browser.onAttention?.(reveal);
    const offPanels = browser.onPanelsChanged(recover);
    void browser
      .listPanels(sessionId)
      .then(recover)
      .catch(() => {});
    return () => {
      active = false;
      offAttention?.();
      offPanels();
    };
  }, [sessionId, onReveal]);

  return attention?.sessionId === sessionId ? attention : null;
}
