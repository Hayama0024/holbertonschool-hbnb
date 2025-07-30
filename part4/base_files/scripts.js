// scripts.js

// ─── Utilities ────────────────────────────────────────────────────────────────

function getCookie(name) {
  const v = `; ${document.cookie}`;
  const parts = v.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function getJwtPayload(token) {
  if (!token) return null;
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch {
    return null;
  }
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id') || params.get('place_id');
}

// ─── Authentication ───────────────────────────────────────────────────────────

function setupLoginForm() {
  const form = document.getElementById('login-form');
  if (!form) return;
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    try {
      const res = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, password})
      });
      if (res.ok) {
        const { access_token } = await res.json();
        document.cookie = `token=${access_token}; path=/`;
        window.location.href = 'index.html';
      } else {
        const txt = await res.text();
        alert(`Login failed (${res.status}): ${txt}`);
      }
    } catch (err) {
      alert('Login error: ' + err.message);
    }
  });
}

function setupLogout() {
  const btn = document.getElementById('logout-link');
  if (!btn) return;
  btn.addEventListener('click', e => {
    e.preventDefault();
    document.cookie = 'token=; Max-Age=0; path=/';
    window.location.href = 'login.html';
  });
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');
  if (loginLink)  loginLink.style.display  = token ? 'none' : 'block';
  if (logoutLink) logoutLink.style.display = token ? 'block': 'none';
  return token;
}

// ─── INDEX ───────────────────────────────────────────────────────────────────

async function fetchPlaces(token) {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/v1/places', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      const places = await res.json();
      displayPlaces(places, token);
    }
  } catch (err) {
    console.error('fetchPlaces failed', err);
  }
}

function displayPlaces(places, token) {
  const container = document.getElementById('places-list');
  container.innerHTML = '';
  const me = getJwtPayload(token)?.sub;
  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price);
    card.innerHTML = `
      <h3>${place.title}</h3>
      <p>€${place.price} per night</p>
      <a href="place.html?id=${place.id}">View Details</a>
    `;
    // fetch my review for this place
    if (me) {
      fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${place.id}/reviews`)
        .then(r => r.json())
        .then(revs => {
          const mine = revs.find(r => r.user.id === me);
          if (mine) {
            const p = document.createElement('p');
            p.textContent = `Your rating: ${mine.rating}`;
            card.appendChild(p);
          }
        });
    }
    container.appendChild(card);
  });
}

function setupPriceFilter() {
  const sel = document.getElementById('price-filter');
  if (!sel) return;
  sel.addEventListener('change', () => {
    const max = sel.value;
    document.querySelectorAll('.place-card').forEach(card => {
      const price = parseFloat(card.dataset.price);
      card.style.display = (max === 'All' || price <= parseFloat(max))
        ? 'block' : 'none';
    });
  });
}

// ─── PLACE DETAILS ────────────────────────────────────────────────────────────

async function fetchPlaceDetails(placeId, token) {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      displayPlaceDetails(await res.json());
    }
  } catch (err) {
    console.error('fetchPlaceDetails failed', err);
  }
}

function displayPlaceDetails(place) {
  const sec = document.querySelector('.place-info');
  sec.innerHTML = `
    <h2>${place.title}</h2>
    <p><strong>Hosted by:</strong> ${place.owner.first_name}</p>
    <p><strong>Price:</strong> €${place.price} per night</p>
    <p><strong>Description:</strong> ${place.description}</p>
    <p><strong>Amenities:</strong> ${place.amenities.map(a => a.name).join(', ')}</p>
  `;
}

async function fetchPlaceReviews(placeId, token) {
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`);
    if (res.ok) {
      displayPlaceReviews(await res.json(), token, placeId);
    }
  } catch (err) {
    console.error('fetchPlaceReviews failed', err);
  }
}

function displayPlaceReviews(reviews, token, placeId) {
  const container = document.querySelector('.reviews');
  const me = getJwtPayload(token)?.sub;
  container.innerHTML = '<h2>Reviews</h2>';
  reviews.forEach(r => {
    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = `
      <p>"${r.text}"</p>
      <p><strong>By:</strong> ${r.user.first_name}</p>
      <p><strong>Rating:</strong> ${r.rating}</p>
    `;
    if (me && r.user.id === me) {
      const btn = document.createElement('button');
      btn.textContent = 'Edit';
      btn.className = 'edit-review-btn';
      btn.addEventListener('click', () => {
        window.location.href = `edit_review.html?review_id=${r.id}&place_id=${placeId}`;
      });
      card.appendChild(btn);
    }
    container.appendChild(card);
  });
  const addCtn = document.querySelector('.add-review-container');
  if (me) addCtn.style.display = 'block';
}

// ─── ADD REVIEW ───────────────────────────────────────────────────────────────

function setupAddReviewPage() {
  const form = document.getElementById('review-form');
  if (!form) return;
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();
  const userId = getJwtPayload(token)?.sub;

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const text   = document.getElementById('review').value;
    const rating = parseInt(document.getElementById('rating').value, 10);
    try {
      const res = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type':  'application/json'
        },
        body: JSON.stringify({ user_id: userId, place_id: placeId, text, rating })
      });
      if (res.ok) {
        window.location.href = `place.html?id=${placeId}`;
      } else {
        const err = await res.json();
        alert(err.message || 'Failed to submit review.');
      }
    } catch (err) {
      alert('Error submitting review: ' + err.message);
    }
  });
}

// ─── EDIT REVIEW ──────────────────────────────────────────────────────────────

function setupEditReviewPage() {
  const form = document.getElementById('edit-form');
  if (!form) return;
  const token    = getCookie('token');
  const params   = new URLSearchParams(window.location.search);
  const reviewId = params.get('review_id');
  const placeId  = params.get('place_id');

  // load existing
  fetch(`http://127.0.0.1:5000/api/v1/reviews/${reviewId}`)
    .then(r => r.json())
    .then(data => {
      document.getElementById('review-text').value   = data.text;
      document.getElementById('review-rating').value = data.rating;
    });

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const text   = document.getElementById('review-text').value;
    const rating = parseInt(document.getElementById('review-rating').value, 10);
    try {
      const res = await fetch(`http://127.0.0.1:5000/api/v1/reviews/${reviewId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type':  'application/json'
        },
        body: JSON.stringify({ text, rating })
      });
      if (res.ok) {
        window.location.href = `place.html?id=${placeId}`;
      } else {
        alert('Update failed');
      }
    } catch (err) {
      alert('Error updating review: ' + err.message);
    }
  });
}

// ─── Initialize ──────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  setupLoginForm();
  setupLogout();
  const token = checkAuthentication();

  // index page
  if (document.getElementById('places-list')) {
    setupPriceFilter();
    fetchPlaces(token);
  }

  // place details page
  const placeId = getPlaceIdFromURL();
  if (placeId && document.querySelector('.place-info')) {
    fetchPlaceDetails(placeId, token);
    fetchPlaceReviews(placeId, token);
  }

  // add review page
  if (document.getElementById('review-form')) {
    setupAddReviewPage();
  }

  // edit review page
  if (document.getElementById('edit-form')) {
    setupEditReviewPage();
  }
});
