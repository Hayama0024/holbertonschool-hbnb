// static/js/login.js
console.log('✅ login.js loaded');

function setCookie(name, val, days=7) {
  const d = new Date();
  d.setTime(d.getTime() + days*24*60*60*1000);
  document.cookie = `${name}=${encodeURIComponent(val)}; expires=${d.toUTCString()}; path=/; SameSite=Lax`;
}

function safeRedirectAfterLogin() {
  try {
    const ref = document.referrer || '';
    const sameOrigin = ref.startsWith(location.origin);
    if (sameOrigin && ref !== location.href) {
      return location.replace(ref);
    }
  } catch (_) {
    // noop
  }
  // ✅ テンプレート構成に合わせて /index.html を優先
  // 環境によっては / にマップされている場合もあるため、二段フォールバック
  try {
    location.replace('/index.html');
  } catch (_) {
    location.replace('/');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const err  = document.getElementById('login-error');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (err) err.textContent = '';

    const email = form.email.value.trim();
    const password = form.password.value;

    try {
      const res = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        const msg = data.error || data.msg || res.statusText;
        throw new Error(msg);
      }

      const token = data.access_token || data.token || data.jwt;
      if (!token) throw new Error('No token in response');

      // Cookie / localStorage へ保存（両方）
      setCookie('token', token, 7);
      setCookie('access_token', token, 7);
      localStorage.setItem('access_token', token);

      safeRedirectAfterLogin();
    } catch (e2) {
      console.error('Login error:', e2);
      if (err) err.textContent = '❌ ' + (e2.message || 'Login failed');
      else alert('❌ ' + (e2.message || 'Login failed'));
    }
  });
});
