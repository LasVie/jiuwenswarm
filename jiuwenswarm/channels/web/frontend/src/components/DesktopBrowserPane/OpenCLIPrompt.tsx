import { ShieldAlert, ShieldCheck } from 'lucide-react';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import type { ElectronBrowserState } from '../../types/electron';

/** Handled by App: sends ``content`` as an ordinary user message in ``sessionId``. */
export const SEND_CHAT_MESSAGE_EVENT = 'jiuwen:send-chat-message';

/**
 * OpenCLI worker page prompts: the write confirmation bar and the
 * "awaiting user" banner (captcha / login). Decisions only come from these
 * buttons, never from the model.
 */
export function OpenCLIPrompt({ panel, sessionId }: { panel?: ElectronBrowserState; sessionId: string }) {
  const { t } = useTranslation();
  const desktop = window.jiuwenDesktop;
  const confirm = panel?.pendingConfirm ?? null;
  const hold = panel?.hold ?? null;
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    if (!confirm) return;
    setNow(Date.now());
    const timer = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, [confirm]);

  if (!desktop || !panel) return null;

  if (confirm) {
    const seconds = Math.max(0, Math.ceil((confirm.expiresAt - now) / 1000));
    const respond = (decision: 'approve' | 'reject') => {
      void desktop.browser.respondConfirm?.(confirm.requestId, decision);
    };
    return (
      <div className="desktop-browser-opencli-prompt" role="alertdialog" data-testid="desktop-browser-opencli-confirm">
        <div className="desktop-browser-opencli-heading">
          <ShieldAlert aria-hidden size={16} />
          <strong data-testid="desktop-browser-opencli-confirm-title">{t('browser.opencli.confirmTitle')}</strong>
          <span className="desktop-browser-opencli-countdown" data-testid="desktop-browser-opencli-countdown">
            {t('browser.opencli.secondsLeft', { seconds })}
          </span>
        </div>
        <code className="desktop-browser-opencli-command" data-testid="desktop-browser-opencli-command">
          {[confirm.command, ...confirm.args].join(' ')}
        </code>
        {confirm.warnings.map((warning) => (
          <p key={warning} className="desktop-browser-opencli-warning" data-testid="desktop-browser-opencli-warning">
            {warning}
          </p>
        ))}
        <div className="desktop-browser-opencli-actions">
          <button
            type="button"
            className="desktop-browser-opencli-primary"
            data-testid="desktop-browser-opencli-approve"
            onClick={() => respond('approve')}
          >
            {t('browser.opencli.confirmApprove')}
          </button>
          <button type="button" data-testid="desktop-browser-opencli-reject" onClick={() => respond('reject')}>
            {t('browser.opencli.confirmReject')}
          </button>
        </div>
      </div>
    );
  }

  if (hold) {
    const decide = async (decision: 'resolved' | 'abandoned') => {
      const applied = await desktop.browser.decideHold?.(panel.panelId, hold.blockId, decision);
      if (applied && decision === 'resolved') {
        window.dispatchEvent(
          new CustomEvent(SEND_CHAT_MESSAGE_EVENT, {
            detail: { sessionId, content: t('browser.opencli.continueMessage') },
          }),
        );
      }
    };
    return (
      <div className="desktop-browser-opencli-prompt" role="alert" data-testid="desktop-browser-opencli-hold">
        <div className="desktop-browser-opencli-heading">
          <ShieldCheck aria-hidden size={16} />
          <strong data-testid="desktop-browser-opencli-hold-title">{t('browser.opencli.holdTitle')}</strong>
          <span data-testid="desktop-browser-opencli-hold-reason">
            {t(`browser.opencli.reason.${hold.reason}`, { defaultValue: hold.reason })}
          </span>
        </div>
        {hold.instructions ? (
          <p className="desktop-browser-opencli-instructions" data-testid="desktop-browser-opencli-instructions">
            {hold.instructions}
          </p>
        ) : null}
        <div className="desktop-browser-opencli-actions">
          <button
            type="button"
            className="desktop-browser-opencli-primary"
            data-testid="desktop-browser-opencli-done"
            onClick={() => void decide('resolved')}
          >
            {t('browser.opencli.holdDone')}
          </button>
          <button type="button" data-testid="desktop-browser-opencli-abandon" onClick={() => void decide('abandoned')}>
            {t('browser.opencli.holdAbandon')}
          </button>
        </div>
      </div>
    );
  }

  return null;
}
