(function() {
  const SESSION_KEY = 'wordsense_session_id';

  function sessionId() {
    try {
      let value = localStorage.getItem(SESSION_KEY);
      if (!value) {
        value = `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
        localStorage.setItem(SESSION_KEY, value);
      }
      return value;
    } catch (error) {
      return `session-${Date.now()}`;
    }
  }

  function wordFromUrl() {
    try {
      return new URLSearchParams(window.location.search).get('word') || '';
    } catch (error) {
      return '';
    }
  }

  function track(event, properties = {}) {
    if (!window.location.protocol.startsWith('http')) return;
    const payload = {
      event,
      sessionId: sessionId(),
      page: window.location.pathname + window.location.search,
      properties,
      word: properties.word || wordFromUrl()
    };
    const body = JSON.stringify(payload);
    if (navigator.sendBeacon) {
      const blob = new Blob([body], { type: 'application/json' });
      navigator.sendBeacon('/api/events', blob);
      return;
    }
    fetch('/api/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
      keepalive: true
    }).catch(() => {});
  }

  window.WordSenseEvents = { track };

  document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const word = wordFromUrl();

    if (path.endsWith('/word-sense-home_9.html') || path === '/') {
      track('home_view');
      document.addEventListener('click', event => {
        const item = event.target.closest?.('.word-item');
        if (item) {
          track('word_click', {
            word: item.querySelector('.word-item-name')?.textContent?.trim() || item.dataset.word || '',
            level: document.querySelector('.level-tab.active')?.dataset.level || ''
          });
        }
        const link = event.target.closest?.('.preview-more-link');
        if (link) {
          track('preview_continue_click', { word: new URL(link.href).searchParams.get('word') || '' });
        }
        const tab = event.target.closest?.('.level-tab');
        if (tab) {
          track('level_tab_click', { level: tab.dataset.level || '' });
        }
      });
      document.getElementById('senseSearchForm')?.addEventListener('submit', () => {
        track('search_submit', {
          word: document.getElementById('senseWordInput')?.value?.trim() || '',
          hasSource: Boolean(document.getElementById('senseSourceInput')?.value?.trim()),
          hasSentence: Boolean(document.getElementById('senseSentenceInput')?.value?.trim()),
          hasApiKey: Boolean(document.getElementById('searchApiKeyInput')?.value?.trim())
        });
      }, { capture: true });
      document.getElementById('installPwaButton')?.addEventListener('click', () => track('install_click'));
      document.getElementById('mailingListForm')?.addEventListener('submit', () => track('subscribe_submit'), { capture: true });
      return;
    }

    if (path.endsWith('/word-sense-result_10.html')) {
      track('result_view', { word });
      document.getElementById('saveWordButton')?.addEventListener('click', () => track('save_click', { word }));
      document.getElementById('shareWordButton')?.addEventListener('click', () => track('share_click', { word, style: 'direct' }));
      document.addEventListener('click', event => {
        const shareStyle = event.target.closest?.('[data-share-style]');
        if (shareStyle) track('share_click', { word, style: shareStyle.dataset.shareStyle || '' });
        if (event.target.closest?.('[data-generated-copy]')) track('generated_copy_click', { word });
        if (event.target.closest?.('[data-generated-download]')) track('generated_download_click', { word });
      });
      return;
    }

    if (path.endsWith('/word-sense-review.html')) {
      track('review_view', { word });
      return;
    }

    if (path.endsWith('/word-sense-about.html')) {
      track('about_view');
      return;
    }

    if (path.endsWith('/word-sense-author.html')) {
      track('author_view');
      document.querySelectorAll('a[href^="http"]').forEach(link => {
        link.addEventListener('click', () => track('author_link_click', { href: link.href }));
      });
    }
  });
})();
