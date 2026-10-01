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

  loadAdSense();
})();
