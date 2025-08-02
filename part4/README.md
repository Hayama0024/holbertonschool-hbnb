# HBnB – Part 4: Simple Web Client

This repository contains the front‑end **Simple Web Client** for the HBnB application (Part 4), together with a minimal Flask API used for local testing. The client is built with **HTML5, CSS3, and JavaScript (ES6)** and communicates with the back‑end via **Fetch** using **JWT** for authentication. CORS is enabled for local development.

> **Scope of this README**
> - How to install/run (single command)
> - Project structure
> - How the pages work (Login / Index / Place Details / Add Review)
> - API expectations (JWT, headers, endpoints)
> - How to test each task
> - Known deviations from the rubric (fix list)

---

## Quick Start

### 1) Create and activate a virtualenv (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Run the app
```bash
python3 part4/run.py
```
By default the Flask dev server runs on `http://127.0.0.1:5000/`.

> The client pages are served under `/` and `/static/html/*` while the API lives under `/api/v1/*`.

---

## Project Layout

```
part4/
├── run.py
├── config.py
├── requirements.txt
├── app/
│   ├── __init__.py            # Flask app factory (CORS enabled, JWT setup)
│   ├── models/                # SQLAlchemy models (User, Place, Amenity, Review, associations)
│   ├── services/facade.py     # Service layer
│   ├── persistence/           # Repositories
│   ├── api/v1/                # REST API (auth, places, reviews, users, admin)
│   ├── templates/
│   │   ├── index.html         # Places list (served at / or /index.html)
│   │   └── login.html         # Login page
│   └── static/
│       ├── css/               # base.css, page‑specific CSS (index/place/review/login)
│       ├── js/                # index.js, place.js, add_review.js, login.js
│       ├── images/            # logo and sample images
│       └── html/
│           ├── place.html     # Place details page
│           └── add_review.html# Add review page
└── ER-diagram.png
```

---

## Configuration

`part4/config.py` defines dev settings:
- SQLite DB: `sqlite:///development.db`
- `JWT_SECRET_KEY` for signing tokens
- `JWT_ACCESS_TOKEN_EXPIRES = 2h`

CORS is enabled in `app/__init__.py`:
```python
from flask_cors import CORS
CORS(app)  # allows cross‑origin requests in dev
```

---

## Pages & Behavior

### 1) **Login** (`/login.html`)
- Form posts to `POST /api/v1/auth/login` with `{ email, password }`.
- On success, the **JWT** is stored as a cookie `token` (also `access_token`) and in `localStorage` for convenience.
- Then we redirect back (same‑origin referrer) or to `/index.html`.
- Errors are shown inline (`#login-error`).

**Code:** `static/js/login.js`, `templates/login.html`

---

### 2) **Places List (Index)** (`/` or `/index.html`)
- Shows header with **logo** (`.logo`) and **Login/Logout** controls.
- Fetches places from `GET /api/v1/places/` (JWT added if present).
- Renders each place as a **card** with class `.place-card` (title, price, short description) and a “View Details” button.
- Client‑side **price filter** via the `#price-filter` dropdown: `10`, `50`, `100`, `All`.
- If a JWT is absent, the page **shows the Login link** and still lists public places (see “Deviations” below if your rubric expects a hard redirect).

**Code:** `static/js/index.js`, `templates/index.html`, `static/css/index.css`

---

### 3) **Place Details** (`/static/html/place.html?id=<PLACE_ID>`)
- Reads `id` from the query string.
- Fetches a single place: `GET /api/v1/places/<id>`.
- Displays **name, price, description, amenities** and **reviews**.
- If authenticated, shows an **“Add Review”** button that links to `/static/html/add_review.html?id=<PLACE_ID>`.

**Code:** `static/js/place.js`, `static/html/place.html`, `static/css/place.css`

---

### 4) **Add Review** (`/static/html/add_review.html?id=<PLACE_ID>`)
- Requires auth: if no JWT, redirects to the **login** page.
- Submits to:  
  - `POST /api/v1/places/<id>/reviews` (preferred), or
  - `POST /api/v1/reviews/` with `{ place_id, text, rating }`.
- On success, shows a message and navigates back to the **place details** page.

**Code:** `static/js/add_review.js`, `static/html/add_review.html`, `static/css/review.css`

---

## API Expectations

### Authentication
- **Login:** `POST /api/v1/auth/login`
  - body: `{ "email": "<email>", "password": "<password>" }`
  - response: `{ "access_token": "<JWT>" }`
- **Auth header:** `Authorization: Bearer <token>`

### Places
- **List:** `GET /api/v1/places/`
- **Detail:** `GET /api/v1/places/<place_id>`
  - returns `title`, `price_by_night`, `description`, `owner`, `amenities`, and possibly `reviews` (or reviews are fetched separately).

### Reviews
- **List by place:** `GET /api/v1/places/<place_id>/reviews`
- **Create:**  
  - `POST /api/v1/places/<place_id>/reviews` (body: `{ text, rating }`), or  
  - `POST /api/v1/reviews/` (body: `{ place_id, text, rating }`).

> Server code for these endpoints resides under `app/api/v1/` and uses the service layer in `app/services/facade.py`.

---

## How to Test (Manual QA)

1) **Start server**  
   `python3 part4/run.py`

2) **Login**  
   - Open `http://127.0.0.1:5000/login.html`  
   - Use the seeded admin (see `seed_users()` in `app/__init__.py`) or create a user via the API.
   - On success, confirm cookies: `token`/`access_token` are set.

3) **Index (Places)**  
   - Visit `/index.html`.
   - Confirm **Login** is hidden and **Logout** is visible when authenticated.
   - Confirm places are listed as **.place-card**, and the **price filter** works (`10 / 50 / 100 / All`).

4) **Place Details**  
   - Click **View Details** to open `/static/html/place.html?id=<id>`.
   - Confirm price, description, amenities, and reviews are displayed.

5) **Add Review**  
   - From Place Details, click **Add Review** (must be logged in).
   - Submit a review and verify it appears in the details page.

6) **CORS**  
   - If you load the client from another origin, CORS must be enabled on the API (`CORS(app)` is active in dev).

---

## Accessibility & Validation

- Semantic HTML5 is used on each page.
- Forms expose `aria-live` regions for error/success messages where relevant.
- All pages should pass the **W3C Validator**; if the validator flags a page, fix any missing `alt`, `label-for`, or `lang` attributes.

---

## Known Deviations vs. Rubric / To‑Do

> This section lists items to adjust if you need *strict* compliance with the project rubric.

1. **Index redirect when unauthenticated**  
   - *Current behavior:* If there’s no JWT, we **show the Login link** but still fetch and render places.  
   - *Rubric (Tasks/Index) may require:* **Redirect to the login page** when unauthenticated.  
   - *Fix:* In `static/js/index.js`, if `!getToken()`, set `window.location.href = '/login.html'` before fetching places.

2. **Add Review redirect target when unauthenticated**  
   - *Current behavior:* The add review page redirects unauthenticated users to **/login.html**.  
   - *Rubric requests:* Redirect unauthenticated users to the **index page**.  
   - *Fix:* Change the redirect target in `static/js/add_review.js` from `/login.html` to `/index.html` to match the text of the rubric (if required).

3. **Required class names**  
   - *Rubric:* Review cards must use class **`review-card`**, and details sections should include **`place-details`** and **`place-info`**.  
   - *Current behavior:* Place details uses `.place-details`; rendered reviews use `.review` (not `.review-card`); `.place-info` is not used.  
   - *Fix:* In `static/js/place.js`, change `div.className = 'review';` to `div.className = 'review-card';`. Optionally wrap the primary info in a container with class `place-info` for full spec alignment. Ensure margins/padding/border match the fixed params.

4. **Card spacing**  
   - *Rubric fixed param:* *Margin: 20px for place and review cards.*  
   - *Current CSS:* `.place-card` has padding/border/radius, but spacing is primarily via `gap`.  
   - *Fix:* Add `margin: 20px;` to `.place-card` and `.review-card` (already present for review‑card in CSS; ensure it’s exactly `20px`).

5. **Navigation bar**  
   - *Rubric:* “Navigation Bar must include relevant links (e.g., index.html and login.html).”  
   - *Current behavior:* The header has logo + Login/Logout links; a dedicated `<nav>` with explicit links is optional.  
   - *Fix (if required):* Add a `<nav>` element with links to `/index.html` and `/login.html` and give it a class for styling.

6. **Templates vs. Static HTML**  
   - Place Details and Add Review are currently served from `/static/html/...`. This is fine for a static client, but if your grader expects *all* pages under `templates/`, move them to `app/templates/` and expose Flask routes (e.g., `/place.html`, `/add_review.html`).

---

## Security Notes

- JWT is stored in a **cookie (`SameSite=Lax`)** and duplicated to `localStorage` for convenience. For production, prefer **HTTP‑only cookies** and avoid duplicating tokens into `localStorage`.
- Always send `Authorization: Bearer <token>` for protected endpoints.
- Sanitize any dynamic text before inserting into the DOM (see `escapeHTML` helpers).

---

## License

This project is for educational purposes as part of the HBnB curriculum. If you plan to reuse outside the course context, please ensure image and asset licenses are respected.
