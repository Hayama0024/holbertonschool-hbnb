console.log("✅ place.js is loaded");

// -------------------- 共通ヘルパー --------------------
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let c of cookies) {
    const [key, value] = c.trim().split('=');
    if (key === name) return decodeURIComponent(value || '');
  }
  return null;
}
function getToken() {
  return (
    getCookie('access_token') ||
    getCookie('token') ||
    localStorage.getItem('access_token') ||
    null
  );
}
function authHeader() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

// 候補キーから最初に値があるものを拾う（ドット記法対応）
function pick(obj, candidates, fallback) {
  for (const path of candidates) {
    const val = path.split('.').reduce((acc, k) => (acc ? acc[k] : undefined), obj);
    if (val !== undefined && val !== null) return val;
  }
  return fallback;
}

// 単純エスケープ（XSS対策）
function escapeHTML(s) {
  if (s === null || s === undefined) return '';
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// 価格のゆれに対応（通貨記号付き文字列・ネスト対応）
function resolvePrice(obj) {
  if (!obj || typeof obj !== 'object') return null;

  let price = pick(obj, [
    'price_by_night',
    'price_per_night',
    'price',
    'nightly_price',
    'cost',
    'amount',
    'pricing.price',
    'pricing.amount',
    'rates.nightly',
    'rates.price',
  ], null);

  if (price && typeof price === 'object') {
    price = pick(price, ['amount', 'value', 'price'], null);
  }

  if (typeof price === 'string') {
    const cleaned = price
      .replace(/[^\d.,\-]/g, '')
      .replace(',', '.');
    const num = Number(cleaned);
    if (Number.isFinite(num)) return num;
    return null;
  }

  const num = Number(price);
  return Number.isFinite(num) ? num : null;
}

// 緯度経度（任意）
function resolveCoords(obj) {
  const lat = pick(obj, ['latitude', 'lat'], null);
  const lng = pick(obj, ['longitude', 'lon', 'lng'], null);
  if (lat == null || lng == null) return null;
  return { lat, lng };
}

// 配列/ラッパー正規化（[], {results:[]}, {reviews:[]})
function normalizeArray(data) {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.results)) return data.results;
  if (data && Array.isArray(data.reviews)) return data.reviews;
  return [];
}

// -------------------- 画面イベント --------------------
window.addEventListener('DOMContentLoaded', () => {
  console.log("🍩 DOM fully loaded");

  const token = getToken();
  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  const addReviewBtn = document.getElementById('add-review-btn');

  // ヘッダー表示切替
  if (token) {
    if (loginLink) loginLink.style.display = 'none';
    if (logoutLink) logoutLink.style.display = 'inline';
    if (addReviewBtn) addReviewBtn.style.display = 'inline';
  } else {
    if (loginLink) loginLink.style.display = 'inline';
    if (logoutLink) logoutLink.style.display = 'none';
    if (addReviewBtn) addReviewBtn.style.display = 'none';
  }

  if (logoutLink) {
    logoutLink.addEventListener('click', () => {
      // Token削除（Cookie + localStorage）
      document.cookie = 'access_token=; path=/; max-age=0';
      document.cookie = 'token=; path=/; max-age=0';
      localStorage.removeItem('access_token');
      // 既存構成に合わせたまま
      window.location.href = '/static/html/login.html';
    });
  }

  // URLの ?id=... を取得
  const placeId = new URLSearchParams(window.location.search).get('id');
  if (!placeId) {
    alert("❌ No place ID provided in the URL.");
    return;
  }

  fetchPlaceDetails(placeId);
  fetchReviews(placeId);

  if (addReviewBtn) {
    addReviewBtn.addEventListener('click', () => {
      if (!getToken()) {
        window.location.href = '/static/html/login.html';
        return;
      }
      window.location.href = `/static/html/add_review.html?place_id=${encodeURIComponent(placeId)}`;
    });
  }
});

// -------------------- データ取得＆描画 --------------------
async function fetchPlaceDetails(placeId) {
  console.log("📡 Fetching place details...");

  try {
    const res = await fetch(`/api/v1/places/${encodeURIComponent(placeId)}`, {
      headers: { ...authHeader() }
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(`HTTP ${res.status} ${text}`);
    }
    const place = await res.json();
    console.log("📦 place payload keys:", Object.keys(place));
    window.__place = place; // Console用

    const section = document.getElementById('place-details');
    if (!section) return;

    const title = pick(place, ['title', 'name'], 'Place');
    const description = pick(place, ['description', 'details', 'summary'], 'No description provided.');
    const price = resolvePrice(place);
    const coords = resolveCoords(place);

    // ホスト名（Safari 互換のため段階的に組み立て）
    let host = pick(place, ['host.name', 'owner.name', 'user.name'], null);
    if (host == null) {
      const first = pick(place, ['host.first_name', 'owner.first_name', 'user.first_name'], '');
      const last  = pick(place, ['host.last_name',  'owner.last_name',  'user.last_name'],  '');
      const combined = [first, last].filter(Boolean).join(' ').trim();
      host = combined !== '' ? combined : null;
    }

    // アメニティ（配列/オブジェクト配列 both 対応）
    let amenities = pick(place, ['amenities'], []);
    if (Array.isArray(amenities) && amenities.length && typeof amenities[0] === 'object') {
      amenities = amenities.map(a => (a && (a.name || a.title)) ? (a.name || a.title) : '').filter(Boolean);
    } else if (!Array.isArray(amenities)) {
      amenities = [];
    }

    // ★ 画像URLを決める（DBに image_url があればそれを優先、なければ ID.jpg）
    const imageUrl = (place.image_url && String(place.image_url).trim())
      ? place.image_url
      : `/static/images/places/${encodeURIComponent(place.id || '')}.jpg`;

    section.innerHTML = `
      <img src="${imageUrl}" alt="${escapeHTML(title)}"
           onerror="this.onerror=null;this.src='/static/images/placeholder.jpg';"
           style="width:100%;max-height:360px;object-fit:cover;border-radius:10px;margin-bottom:12px;">
      <h1>${escapeHTML(title)}</h1>
      <p><strong>Price:</strong> ${price == null ? '$N/A' : `$${price}`}</p>
      <p>${escapeHTML(description)}</p>
      ${coords ? `<p><strong>Location:</strong> ${escapeHTML(coords.lat)}, ${escapeHTML(coords.lng)}</p>` : ''}
      ${host ? `<p><strong>Host:</strong> ${escapeHTML(host)}</p>` : ''}
      <p><strong>Amenities:</strong> ${amenities.length ? amenities.map(escapeHTML).join(', ') : '—'}</p>
    `;
  } catch (err) {
    console.error("❌ Failed to fetch place:", err);
    const section = document.getElementById('place-details');
    if (section) section.innerHTML = '<p>Failed to load place details.</p>';
  }
}

function fetchReviews(placeId) {
  console.log("📡 Fetching reviews...", placeId);

  const headers = { ...authHeader() };
  const urls = [
    `/api/v1/reviews/places/${encodeURIComponent(placeId)}/reviews`,
    `/api/v1/reviews/places/${encodeURIComponent(placeId)}/reviews/`,
    `/api/v1/places/${encodeURIComponent(placeId)}/reviews`,
    `/api/v1/places/${encodeURIComponent(placeId)}/reviews/`,
  ];

  const tryNext = async (i = 0, tried = []) => {
    if (i >= urls.length) {
      throw new Error('No reviews endpoint matched. Tried: ' + tried.join(', '));
    }
    const url = urls[i];
    const res = await fetch(url, { headers });
    if (!res.ok) {
      if (res.status === 404) {
        return tryNext(i + 1, tried.concat(url));
      }
      const text = await res.text();
      throw new Error(`HTTP ${res.status} ${text}`);
    }
    return res.json();
  };

  tryNext()
    .then(raw => {
      const list = document.getElementById('review-list');
      if (!list) return;
      list.innerHTML = '';

      const reviews = normalizeArray(raw);
      window.__reviews = reviews; // Console用

      if (!reviews.length) {
        list.innerHTML = '<p>No reviews yet.</p>';
        return;
      }

      reviews.forEach(review => {
        const text = pick(review, ['text', 'comment', 'content'], '');
        const rating = pick(review, ['rating', 'stars', 'score'], 'N/A');

        // ユーザー名候補（first/last or name/username）
        let userName = '';
        const first = pick(review, ['user.first_name', 'author.first_name'], '');
        const last  = pick(review, ['user.last_name',  'author.last_name'],  '');
        const combined = [first, last].filter(Boolean).join(' ').trim();
        if (combined) userName = combined;
        if (!userName) userName = pick(review, ['user.name', 'author.name'], '');
        if (!userName) userName = pick(review, ['user.username', 'author.username'], '');
        if (!userName) userName = pick(review, ['user', 'author'], '');
        if (!userName) userName = 'Anonymous';

        const div = document.createElement('div');
        div.className = 'review';
        div.innerHTML = `
          <p><strong>${escapeHTML(userName)}:</strong> ${escapeHTML(text)}</p>
          <p>Rating: ${escapeHTML(rating)}/5</p>
        `;
        list.appendChild(div);
      });
    })
    .catch(err => {
      console.error("❌ Failed to fetch reviews:", err);
      const list = document.getElementById('review-list');
      if (list) list.innerHTML = '<p>Failed to load reviews.</p>';
    });
}
