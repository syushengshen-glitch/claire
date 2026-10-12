// Small Ops Lab 工具頁互動：所有計算都在瀏覽器端完成，不傳送使用者輸入。
(() => {
  const root = document;
  const val = (selector) => root.querySelector(selector)?.value ?? '';
  const num = (selector) => Number(val(selector) || 0);
  const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  const set = (selector, html) => { const node = root.querySelector(selector); if (node) node.innerHTML = html; };

  const quoteForm = root.querySelector('[data-quote-form]');
  if (quoteForm) {
    const render = () => {
      const base = num('[data-quote-hours]') * num('[data-quote-rate]');
      const withBuffer = (base + num('[data-quote-expenses]')) * (1 + num('[data-quote-buffer]') / 100);
      const low = Math.max(0, withBuffer * 0.92);
      const high = withBuffer * 1.1;
      const deposit = withBuffer * (num('[data-quote-deposit]') / 100);
      set('[data-quote-result]', '<h3>Suggested quote range</h3><div class="result-grid"><div><strong>' + money.format(low) + ' – ' + money.format(high) + '</strong><span>Quote range</span></div><div><strong>' + money.format(deposit) + '</strong><span>Deposit</span></div><div><strong>' + money.format(withBuffer - deposit) + '</strong><span>Balance after deposit</span></div></div><p>Round the range to a clean number and check it against the value the client receives, not only your hours.</p>');
    };
    quoteForm.addEventListener('input', render);
    quoteForm.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }

  const paymentForm = root.querySelector('[data-payment-form]');
  if (paymentForm) {
    const render = () => {
      const total = num('[data-payment-total]');
      const deposit = total * (num('[data-payment-deposit]') / 100);
      const milestones = Math.max(1, Math.round(num('[data-payment-milestones]')));
      const rest = total - deposit;
      const rows = Array.from({ length: milestones }, (_, index) => '<p><strong>Milestone ' + (index + 1) + ':</strong> ' + money.format(rest / milestones) + '</p>').join('');
      set('[data-payment-result]', '<h3>Payment schedule</h3><div class="result-lines"><p><strong>Deposit:</strong> ' + money.format(deposit) + '</p>' + rows + '<p><strong>Total:</strong> ' + money.format(total) + '</p></div><p>Tie each milestone to a visible deliverable, not only a calendar date.</p>');
    };
    paymentForm.addEventListener('input', render);
    paymentForm.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }

  const followupForm = root.querySelector('[data-followup-form]');
  if (followupForm) {
    const render = () => {
      const client = val('[data-followup-client]') || 'there';
      const invoice = val('[data-followup-invoice]') || 'INV-000';
      const amount = val('[data-followup-amount]') || 'the balance';
      const due = val('[data-followup-due]') || 'the due date';
      const tone = val('[data-followup-tone]');
      const intro = tone === 'final' ? 'This is a final notice before the next agreed step.' : tone === 'firm' ? 'I have not received payment or a processing note yet.' : 'I wanted to check whether the invoice reached the right queue.';
      const subject = 'Invoice ' + invoice + ' — ' + (tone === 'final' ? 'final notice' : 'payment reminder');
      const body = 'Hi ' + client + ', Invoice ' + invoice + ' for ' + amount + ' was due on ' + due + '. ' + intro + ' Could you confirm the payment date, or tell me what is needed to process it? Invoice details are unchanged.';
      set('[data-followup-result]', '<h3>Email draft</h3><div class="result-lines"><p><strong>Subject:</strong> ' + subject + '</p><p>' + body + '</p></div><p>Check the amount, dates, and recipient before sending. Keep the final notice factual and consistent with your written policy.</p>');
    };
    followupForm.addEventListener('input', render);
    followupForm.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }

  const sopForm = root.querySelector('[data-sop-form]');
  if (sopForm) {
    const render = () => {
      const lines = [
        '# ' + (val('[data-sop-name]') || 'Process'),
        '**Trigger:** ' + (val('[data-sop-trigger]') || 'TBD'),
        '**Owner:** ' + (val('[data-sop-owner]') || 'TBD'),
        '**Inputs:** ' + (val('[data-sop-inputs]') || 'TBD'),
        '**Steps:**',
        ...(val('[data-sop-steps]') || '').split('\n').filter(Boolean).map((step, index) => (index + 1) + '. ' + step),
        '**Exceptions:** ' + (val('[data-sop-exceptions]') || 'TBD'),
        '**Done:** ' + (val('[data-sop-done]') || 'TBD')
      ];
      set('[data-sop-result]', '<h3>SOP draft</h3><div class="result-lines"><p>' + lines.join('<br>') + '</p></div><p>Copy this into your document or task tool, then test it on a real task before publishing.</p>');
    };
    sopForm.addEventListener('input', render);
    sopForm.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }

  const onboardingForm = root.querySelector('[data-onboarding-form]');
  if (onboardingForm) {
    const render = () => {
      const client = val('[data-onboarding-client]') || 'client';
      const owner = val('[data-onboarding-owner]') || 'owner';
      const inputs = val('[data-onboarding-inputs]') || 'inputs';
      const checkpoints = (val('[data-onboarding-checkpoints]') || '').split('\n').filter(Boolean);
      const steps = ['Signed agreement and deposit received → create project record and assign ' + owner + '.', 'Intake form sent → collect ' + inputs + '.', 'Workspace created for ' + client + ' with a consistent folder and task structure.', 'Access requested through a secure channel and tracked with owners and dates.', 'Checkpoints scheduled: ' + checkpoints.join('; ') + '.'];
      set('[data-onboarding-result]', '<h3>Onboarding flow</h3><ol>' + steps.map((step) => '<li>' + step + '</li>').join('') + '</ol><p>Keep the kickoff conversation human. Automate preparation, not judgment.</p>');
    };
    onboardingForm.addEventListener('input', render);
    onboardingForm.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }
})();
