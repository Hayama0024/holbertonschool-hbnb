console.log("✅ add_review.js is loaded");

// ---- token helpers ----
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
  return t ? { 'Authorization': `Bearer ${t}` } : {};
}

document.addEventListener('DOMContentLoaded', () => {
  const token = getToken();
  const loginLink  = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  const form = document.getElementById('review-form');
  const msg  = document.getElementById('review-msg');

  if (!token) {
    // 未ログインならログインへ
    window.location.href = '/login.html';
    return;
  }

  // ヘッダー切り替え
  if (loginLink)  loginLink.style.display  = 'none';
  if (logoutLink) {
    logoutLink.style.display = 'inline';
    logoutLink.addEventListener('click', (e) => {
      e.preventDefault();
      document.cookie = 'access_token=; path=/; max-age=0';
      document.cookie = 'token=; path=/; max-age=0';
      localStorage.removeItem('access_token');
      window.location.href = '/login.html';
    });
  }

  // URL から place_id を取得
  const urlParams = new URLSearchParams(window.location.search);
  const placeId = urlParams.get('place_id');
  if (!placeId) {
    alert("❌ No place_id provided in URL!");
    return;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (msg) msg.textContent = '';

    // 入力値
    const rating = Number(document.getElementById('rating').value);
    const text   = String(document.getElementById('review-text').value || '').trim();

    // 簡易バリデーション
    if (!Number.isInteger(rating) || rating < 0 || rating > 5) {
      if (msg) msg.textContent = '❌ Rating must be an integer between 0 and 5.';
      return;
    }
    if (!text) {
      if (msg) msg.textContent = '❌ Review text is required.';
      return;
    }

    // --- POST 先は互換エンドポイントに統一 ---
    // /api/v1/reviews/places/:place_id/reviews へ送る（bodyに place_id は不要）
    const url = `/api/v1/reviews/places/${encodeURIComponent(placeId)}/reviews`;
    const body = { text, rating };

    console.log("📡 Submitting review:", { url, body });

    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeader() },
        body: JSON.stringify(body)
      });

      const textBody = await res.text();
      if (!res.ok) {
        console.error(`❌ Failed with status ${res.status}: ${textBody}`);
        throw new Error(textBody || res.statusText);
      }

      if (msg) msg.textContent = '✅ Review submitted successfully!';
      form.reset();

      // 0.5秒後に place 詳細へ戻る（id クエリ！）
      setTimeout(() => {
        window.location.href = `/static/html/place.html?id=${encodeURIComponent(placeId)}`;
      }, 500);
    } catch (error) {
      console.error('❌ Failed to submit review:', error);
      if (msg) msg.textContent = '❌ Failed to submit review. ' + (error.message || '');
      else alert('❌ Failed to submit review.');
    }
  });
});
