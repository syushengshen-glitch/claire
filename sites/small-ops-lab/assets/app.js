// SignalShelf 前端互動：搜尋、篩選、排序、行動選單與 AdSense 載入。
(() => {
  // 廣告儲存預設為拒絕；Google CMP 會在需要的地區取得同意並更新訊號。
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });

  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-site-nav]');
  navToggle?.addEventListener('click', () => {
    const open = nav?.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(Boolean(open)));
  });

  const searchForm = document.querySelector('[data-search-form]');
  searchForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const input = searchForm.querySelector('input');
    const value = input?.value.trim();
    const target = searchForm.dataset.searchTarget || '/directory.html';
    if (value) window.location.href = `${target}?q=${encodeURIComponent(value)}`;
  });

  const directory = document.querySelector('[data-directory]');
  if (directory) {
    const params = new URLSearchParams(window.location.search);
    const searchInput = directory.querySelector('[data-filter-search]');
    const sortSelect = directory.querySelector('[data-sort]');
    const chips = [...directory.querySelectorAll('[data-filter-category]')];
    const rows = [...directory.querySelectorAll('[data-tool-row]')];
    const count = directory.querySelector('[data-result-count]');
    const empty = directory.querySelector('[data-empty-state]');
    let activeCategory = params.get('category') || 'all';

    if (searchInput && params.get('q')) searchInput.value = params.get('q');

    const applyFilters = () => {
      const query = searchInput?.value.trim().toLowerCase() || '';
      let visible = 0;
      rows.forEach((row) => {
        const haystack = row.dataset.search || '';
        const matchQuery = !query || haystack.includes(query);
        const matchCategory = activeCategory === 'all' || row.dataset.category === activeCategory;
        const show = matchQuery && matchCategory;
        row.hidden = !show;
        if (show) visible += 1;
      });
      if (count) count.textContent = `${visible} tool${visible === 1 ? '' : 's'}`;
      if (empty) empty.style.display = visible ? 'none' : 'block';
      empty?.setAttribute('aria-hidden', String(Boolean(visible)));
    };

    const applySort = () => {
      if (!sortSelect) return;
      const mode = sortSelect.value;
      const sorted = [...rows].sort((a, b) => {
        if (mode === 'name') return a.dataset.name.localeCompare(b.dataset.name);
        if (mode === 'category') return a.dataset.category.localeCompare(b.dataset.category) || a.dataset.name.localeCompare(b.dataset.name);
        return Number(b.dataset.featured) - Number(a.dataset.featured) || a.dataset.name.localeCompare(b.dataset.name);
      });
      sorted.forEach((row) => row.parentElement?.appendChild(row));
    };

    chips.forEach((chip) => {
      const category = chip.dataset.filterCategory;
      chip.setAttribute('aria-pressed', String(category === activeCategory));
      chip.addEventListener('click', () => {
        activeCategory = category;
        chips.forEach((item) => item.setAttribute('aria-pressed', String(item === chip)));
        applyFilters();
      });
    });

    searchInput?.addEventListener('input', applyFilters);
    sortSelect?.addEventListener('change', applySort);
    applySort();
    applyFilters();
  }

  const copyButton = document.querySelector('[data-copy-link]');
  copyButton?.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      copyButton.textContent = 'Link copied';
      setTimeout(() => { copyButton.textContent = 'Copy link'; }, 1600);
    } catch {
      copyButton.textContent = 'Copy failed';
    }
  });

  let adScriptLoaded = false;
  const loadAdSense = () => {
    if (!window.SIGNALSHELF_ADSENSE_CLIENT || adScriptLoaded) return;
    adScriptLoaded = true;
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(window.SIGNALSHELF_ADSENSE_CLIENT)}`;
    script.crossOrigin = 'anonymous';
    document.head.appendChild(script);
  };

  document.querySelector('[data-manage-consent]')?.addEventListener('click', () => {
    if (window.googlefc?.showRevocationMessage) {
      window.googlefc.showRevocationMessage();
      return;
    }
    window.open('https://adssettings.google.com/', '_blank', 'noopener');
  });

  document.querySelectorAll('[data-year]').forEach((node) => {
    node.textContent = String(new Date().getFullYear());
  });

  // AI 工具成本計算器：只用瀏覽器中的數字估算，不傳送資料。
  const costForm = document.querySelector('[data-cost-form]');
  if (costForm) {
    const numberValue = (selector) => Number(costForm.querySelector(selector)?.value || 0);
    const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
    const renderCost = () => {
      const tasks = numberValue('[data-cost-tasks]');
      const baseMinutes = numberValue('[data-cost-base-minutes]');
      const freeCorrection = numberValue('[data-cost-free-correction]');
      const paidCorrection = numberValue('[data-cost-paid-correction]');
      const hourly = numberValue('[data-cost-hourly]');
      const subscription = numberValue('[data-cost-subscription]');
      const seats = numberValue('[data-cost-seats]');
      const freeHours = tasks * (baseMinutes + freeCorrection) / 60;
      const paidHours = tasks * (baseMinutes + paidCorrection) / 60;
      const freeCost = freeHours * hourly;
      const paidCost = subscription * seats + paidHours * hourly;
      const difference = freeCost - paidCost;
      const savedHours = freeHours - paidHours;
      const result = costForm.parentElement?.querySelector('[data-cost-result]') || document.querySelector('[data-cost-result]');
      if (!result) return;
      const verdict = difference > 0
        ? 'The paid plan is cheaper under these assumptions. Verify quality and privacy before subscribing.'
        : 'The free plan is cheaper under these assumptions. A paid trial needs a quality or capacity reason that is not captured here.';
      result.innerHTML = '<h3>Monthly comparison</h3><div class="result-grid"><div><strong>' + money.format(freeCost) + '</strong><span>Free plan effort cost</span></div><div><strong>' + money.format(paidCost) + '</strong><span>Paid plan total</span></div><div><strong>' + money.format(Math.abs(difference)) + '</strong><span>' + (difference >= 0 ? 'Estimated saving with paid plan' : 'Estimated extra cost with paid plan') + '</span></div></div><p><strong>' + savedHours.toFixed(1) + ' hours</strong> of correction effort are estimated to be saved each month. ' + verdict + '</p>';
    };
    costForm.addEventListener('input', renderCost);
    costForm.addEventListener('submit', (event) => { event.preventDefault(); renderCost(); });
    renderCost();
  }

  // 評估計分板：把主觀印象轉成可重複比較的七項分數。
  const scoreForm = document.querySelector('[data-scorecard-form]');
  if (scoreForm) {
    const scoreInputs = [...scoreForm.querySelectorAll('[data-score]')];
    const syncScores = () => scoreInputs.forEach((input) => {
      const output = input.parentElement?.querySelector('output');
      if (output) output.textContent = input.value;
    });
    const renderScore = (event) => {
      if (event) event.preventDefault();
      syncScores();
      const total = scoreInputs.reduce((sum, input) => sum + Number(input.value), 0);
      const max = scoreInputs.length * 4;
      const band = total < 14 ? 'Do not subscribe yet' : total <= 21 ? 'Needs a narrower trial' : 'Paid-trial candidate';
      const result = scoreForm.parentElement?.querySelector('[data-scorecard-result]') || document.querySelector('[data-scorecard-result]');
      if (!result) return;
      result.innerHTML = '<p><span class="score-band">' + band + '</span></p><h3>' + total + ' / ' + max + '</h3><p>This score is only valid for the task you tested. Record the date, input, correction time, and privacy review before making a purchase decision.</p>';
    };
    scoreInputs.forEach((input) => input.addEventListener('input', () => { syncScores(); }));
    scoreForm.addEventListener('submit', renderScore);
    scoreForm.addEventListener('reset', () => window.setTimeout(syncScores, 0));
    syncScores();
  }

  loadAdSense();
})();
