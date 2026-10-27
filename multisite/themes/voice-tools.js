// VoiceSignal Lab 工具：計算與文字生成都在瀏覽器端完成，不傳送輸入資料。
(() => {
  const q = (selector) => document.querySelector(selector);
  const val = (selector) => q(selector)?.value ?? '';
  const num = (selector) => Number(val(selector) || 0);
  const set = (selector, html) => { const node = q(selector); if (node) node.innerHTML = html; };
  const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

  const casting = q('[data-casting-form]');
  if (casting) {
    const render = () => {
      const checks = ['[data-casting-clarity]','[data-casting-emotion]','[data-casting-accent]','[data-casting-pronunciation]','[data-casting-editability]'];
      const total = checks.reduce((sum, selector) => sum + num(selector), 0);
      const band = total < 13 ? 'Do not cast yet' : total <= 19 ? 'Test in context' : 'Strong candidate';
      set('[data-casting-result]', '<h3>Voice casting score</h3><p><strong>' + total + ' / 25</strong> — ' + band + '</p><p>Listen again over the real music, visuals, and phone speaker. A high score does not replace a usage-rights review.</p>');
    };
    casting.addEventListener('input', render);
    casting.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }

  const pacing = q('[data-pacing-form]');
  if (pacing) {
    const render = () => {
      const speech = num('[data-pacing-wpm]') > 0 ? num('[data-pacing-words]') / num('[data-pacing-wpm]') * 60 : 0;
      const pauses = num('[data-pacing-sections]') * num('[data-pacing-pause]');
      const total = Math.max(0, speech + pauses);
      const mins = Math.floor(total / 60);
      const secs = Math.round(total % 60);
      set('[data-pacing-result]', '<h3>Estimated runtime</h3><div class="result-grid"><div><strong>' + mins + 'm ' + secs + 's</strong><span>Estimated voice runtime</span></div><div><strong>' + Math.round(speech) + 's</strong><span>Speech time</span></div><div><strong>' + Math.round(pauses) + 's</strong><span>Planned pauses</span></div></div><p>Measure a real paragraph and adjust the pace before recording the full script.</p>');
    };
    pacing.addEventListener('input', render);
    pacing.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }

  const dubbing = q('[data-dubbing-form]');
  if (dubbing) {
    const render = () => {
      const perLanguage = num('[data-dubbing-minutes]') * num('[data-dubbing-rate]') * (1 + num('[data-dubbing-buffer]') / 100);
      const total = perLanguage * num('[data-dubbing-languages]');
      set('[data-dubbing-result]', '<h3>Dubbing budget estimate</h3><div class="result-grid"><div><strong>' + money.format(perLanguage) + '</strong><span>Per language</span></div><div><strong>' + money.format(total) + '</strong><span>All languages</span></div><div><strong>' + num('[data-dubbing-languages]') + '</strong><span>Languages</span></div></div><p>This is a planning range, not a vendor quote. Separate translation, adaptation, casting, recording, mixing, and native QC when you request proposals.</p>');
    };
    dubbing.addEventListener('input', render);
    dubbing.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }

  const cps = q('[data-cps-form]');
  if (cps) {
    const render = () => {
      const duration = num('[data-cps-duration]');
      const rate = duration > 0 ? num('[data-cps-characters]') / duration : 0;
      const verdict = rate <= 15 ? 'Comfortable' : rate <= 20 ? 'Check on a phone' : 'Too fast for many viewers';
      set('[data-cps-result]', '<h3>Subtitle reading speed</h3><p><strong>' + rate.toFixed(1) + ' characters per second</strong> — ' + verdict + '</p><p>Split the caption by meaning, shorten non-essential words, or extend the duration. Do not solve it by shrinking the font.</p>');
    };
    cps.addEventListener('input', render);
    cps.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }

  const consent = q('[data-consent-form]');
  if (consent) {
    const render = () => {
      const owner = val('[data-consent-owner]') || 'Voice owner';
      const project = val('[data-consent-project]') || 'the project';
      const permitted = val('[data-consent-permitted]') || 'the agreed scope';
      const excluded = val('[data-consent-excluded]') || 'uses outside the agreed scope';
      const territory = val('[data-consent-territory]') || 'the agreed territory';
      const duration = val('[data-consent-duration]') || 'the agreed duration';
      const review = val('[data-consent-review]') || 'the review date';
      set('[data-consent-result]', '<h3>Consent draft</h3><div class="result-lines"><p><strong>Voice owner:</strong> ' + owner + '</p><p>I consent to the creation and use of a synthetic voice model based on my voice for ' + project + '. Permitted uses: ' + permitted + '. Excluded uses: ' + excluded + '. Territory: ' + territory + '. Duration: ' + duration + '. Review date: ' + review + '.</p></div><p>This is a draft, not legal advice. Use a separate signature, attach the approved scope, and have qualified counsel review material commercial uses.</p>');
    };
    consent.addEventListener('input', render);
    consent.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }

  const disclosure = q('[data-disclosure-form]');
  if (disclosure) {
    const render = () => {
      const content = val('[data-disclosure-content]') || 'this content';
      const type = val('[data-disclosure-type]');
      const placement = val('[data-disclosure-placement]');
      const voiceLabel = type === 'cloned' ? 'a cloned human voice' : type === 'mixed' ? 'a mix of human and synthetic voices' : 'a synthetic voice';
      const placementText = placement === 'visual' ? 'Display a clear on-screen label and include the disclosure in the description.' : placement === 'both' ? 'Place the disclosure at the start and end of the audio, and repeat it in the description.' : placement === 'end' ? 'Place the disclosure at the end of the audio and repeat it in the description.' : 'Place the disclosure at the start of the audio and repeat it in the description.';
      set('[data-disclosure-result]', '<h3>Disclosure draft</h3><div class="result-lines"><p>“This ' + content + ' uses ' + voiceLabel + '.”</p></div><p>' + placementText + ' Check the current platform and market requirements before publishing.</p>');
    };
    disclosure.addEventListener('input', render);
    disclosure.addEventListener('submit', (event) => { event.preventDefault(); render(); });
    render();
  }
})();
