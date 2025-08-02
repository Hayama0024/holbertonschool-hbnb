// static/js/index.js
console.log("✅ index.js is loaded");

// ---- Token/Cookie helpers ----
function getCookie(name) {
  const m = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/[-[\]{}()*+?.,\\^$|#\\s]/g, '\\$&') + '=([^;]+)'));
  return m ? decodeURIComponent(m[1]) : null;
}
function getToken() {
  return (
    getCookie('token') ||
    getCookie('access_token') ||
    localStorage.getItem('access_token') ||
    null
  );
}
function authHeader() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

let PLACES_CACHE = []; // 取得済み一覧を保持

window.addEventListener('DOMContentLoaded', () => {
  console.log("🍩 DOM fully loaded");

  const token = getToken();
  console.log("🔑 token:", token ? "[present]" : "[absent]");

  const loginLink  = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  const priceFilter = document.getElementById('price-filter');

  // 認証チェックとUI制御
  if (token) {
    if (loginLink)  loginLink.style.display  = 'none';
    if (logoutLink) logoutLink.style.display = 'inline';
  } else {
    if (loginLink)  loginLink.style.display  = 'inline';
    if (logoutLink) logoutLink.style.display = 'none';
    console.warn("⛔ No token found. Redirecting to login...");
    window.location.href = '/login.html';
    return;
  }

  if (logoutLink) {
    logoutLink.addEventListener('click', (e) => {
      e.preventDefault();
      document.cookie = 'access_token=; path=/; max-age=0';
      document.cookie = 'token=; path=/; max-age=0';
      localStorage.removeItem('access_token');
      window.location.href = '/login.html';
    });
  }

  // 初回読み込み
  fetchPlaces()
    .then(places => {
      PLACES_CACHE = Array.isArray(places) ? places : (places.results || []);
      renderPlacesFiltered();
    })
    .catch(err => {
      console.error('❌ Error fetching places:', err);
      const container = document.getElementById('places-list');
      if (container) container.innerHTML = `<p class="error">Failed to load places.</p>`;
    });

  // フィルター変更時は再描画のみ
  if (priceFilter) {
    priceFilter.addEventListener('change', renderPlacesFiltered);
  }
});

async function fetchPlaces() {
  console.log("📡 Fetching places...");
  // 308回避のため末尾スラッシュ
  const res = await fetch('/api/v1/places/', { headers: { ...authHeader() } });
  console.log("📥 Response status:", res.status);
  if (!res.ok) throw new Error('Failed to fetch places: ' + res.status);
  return res.json();
}

function renderPlacesFiltered() {
  const container = document.getElementById('places-list');
  const priceSelect = document.getElementById('price-filter');

  if (!container || !priceSelect) {
    console.error("🚫 Missing container or price filter");
    return;
  }

  const selected = priceSelect.value;
  const max = selected === 'All' ? Infinity : Number(selected);

  container.innerHTML = '';

  // price_by_night or price のどちらでも
  const filtered = PLACES_CACHE.filter(p => {
    const price = Number(p.price_by_night ?? p.price ?? 0);
    return price <= max;
  });

  if (!filtered.length) {
    container.innerHTML = '<p>No places found for the selected price range.</p>';
    return;
  }

  filtered.forEach(p => {
    const card = document.createElement('div');
    card.className = 'place-card';

    const price = p.price_by_night ?? p.price ?? 'N/A';
    // サムネイルURL（DBに image_url があればそれを優先）
    const img = (p.image_url && String(p.image_url).trim())
      ? p.image_url
      : `/static/images/places/${encodeURIComponent(p.id)}.jpg`;

    card.innerHTML = `
      <img class="place-thumb" src="${img}"
           alt="${escapeHTML(p.title || p.name || 'Place')}"
           onerror="this.onerror=null;this.src='/static/images/placeholder.jpg';"
           style="width:100%;height:160px;object-fit:cover;border-radius:10px;margin-bottom:8px;">
      <h2><a href="/static/html/place.html?id=${encodeURIComponent(p.id)}">${escapeHTML(p.title || p.name || 'Place')}</a></h2>
      <p>Price: $${escapeHTML(price)}</p>
      <p>${escapeHTML(p.description || 'No description provided.')}</p>
    `;
    container.appendChild(card);
  });
}

// 簡易サニタイズ
function escapeHTML(s) {
  if (s === null || s === undefined) return '';
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
