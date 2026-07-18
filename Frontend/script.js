/* ==========================================================================
   Real Estate Property Portal — Frontend JavaScript
   Fetch API integration with the Django REST backend + bonus features
   ========================================================================== */

const API_BASE = "http://127.0.0.1:8000";

/* ----- API client ----- */
const api = {
  async request(method, path, body = null, query = null) {
    const url = new URL(API_BASE + path);
    if (query) {
      Object.entries(query).forEach(([k, v]) => {
        if (v !== "" && v !== null && v !== undefined) url.searchParams.set(k, v);
      });
    }
    const opts = { method, headers: { "Content-Type": "application/json" } };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(url, opts);
    let data;
    try { data = await res.json(); }
    catch { data = null; }
    if (!res.ok) {
      const msg = (data && data.error) || `Request failed (${res.status})`;
      throw new Error(msg);
    }
    return data;
  },
  get: (p, q) => api.request("GET", p, null, q),
  post: (p, b) => api.request("POST", p, b),
  put: (p, b) => api.request("PUT", p, b),
  del: (p) => api.request("DELETE", p),
};

/* ----- Auth (localStorage based) ----- */
const auth = {
  register(customer) { return api.post("/customers/add/", customer); },
  login(email, password) {
    return api.get("/customers/").then((list) => {
      const user = list.find(
        (c) => c.email === email && c.password === password
      );
      if (!user) throw new Error("Invalid email or password");
      localStorage.setItem("realestate_user", JSON.stringify(user));
      return user;
    });
  },
  logout() { localStorage.removeItem("realestate_user"); },
  current() {
    try { return JSON.parse(localStorage.getItem("realestate_user")); }
    catch { return null; }
  },
  isAdmin() {
    return auth.current()?.email === "admin@realestate.com";
  },
};

/* ----- Favorites (wishlist) ----- */
const favorites = {
  all() {
    try { return JSON.parse(localStorage.getItem("realestate_favs")) || []; }
    catch { return []; }
  },
  isFav(id) { return favorites.all().includes(Number(id)); },
  toggle(id) {
    const favs = favorites.all();
    const idx = favs.indexOf(Number(id));
    if (idx >= 0) favs.splice(idx, 1);
    else favs.push(Number(id));
    localStorage.setItem("realestate_favs", JSON.stringify(favs));
    return idx < 0;
  },
};

/* ----- Compare ----- */
const compare = {
  all() {
    try { return JSON.parse(localStorage.getItem("realestate_compare")) || []; }
    catch { return []; }
  },
  toggle(id) {
    const list = compare.all();
    const idx = list.indexOf(Number(id));
    if (idx >= 0) list.splice(idx, 1);
    else {
      if (list.length >= 3) throw new Error("You can compare up to 3 properties");
      list.push(Number(id));
    }
    localStorage.setItem("realestate_compare", JSON.stringify(list));
    return idx < 0;
  },
  clear() { localStorage.removeItem("realestate_compare"); },
};

/* ----- UI helpers ----- */
const ui = {
  toast(msg, type = "success") {
    let container = document.querySelector(".toast-container");
    if (!container) {
      container = document.createElement("div");
      container.className = "toast-container";
      document.body.appendChild(container);
    }
    const t = document.createElement("div");
    t.className = `toast ${type}`;
    t.textContent = msg;
    container.appendChild(t);
    setTimeout(() => t.remove(), 3200);
  },
  money(n) {
    if (n >= 10000000) return "₹" + (n / 10000000).toFixed(2) + " Cr";
    if (n >= 100000) return "₹" + (n / 100000).toFixed(2) + " Lakh";
    return "₹" + n.toLocaleString("en-IN");
  },
  statusClass(status) {
    const s = (status || "").toLowerCase();
    if (["available", "scheduled", "responded", "pending"].includes(s)) {
      if (s === "available") return "badge-available";
      if (s === "scheduled") return "chip-primary";
      if (s === "responded") return "chip-success";
      if (s === "pending") return "chip-warning";
    }
    if (s === "sold") return "badge-sold";
    if (s === "rented") return "badge-rented";
    if (s === "completed") return "chip-success";
    if (s === "cancelled") return "chip-error";
    if (s === "closed") return "chip-error";
    return "";
  },
  chip(status) {
    return `<span class="chip ${ui.statusClass(status)}">${status}</span>`;
  },
  escape(s) {
    return String(s ?? "").replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  },
  qs(name) {
    return new URLSearchParams(location.search).get(name);
  },
};

/* ----- Navbar render ----- */
function renderNavbar() {
  const navEl = document.getElementById("navbar");
  if (!navEl) return;
  const user = auth.current();
  const isAdmin = auth.isAdmin();
  navEl.innerHTML = `
    <div class="container">
      <a href="index.html" class="brand">
        <span class="brand-mark">RE</span>
        <span>EstateHub</span>
      </a>
      <nav class="nav-links" id="navLinks">
        <a href="index.html">Home</a>
        <a href="properties.html">Properties</a>
        <a href="properties.html?type=Apartment">Apartments</a>
        <a href="properties.html?type=Villa">Villas</a>
        <a href="properties.html?status=Available">Available</a>
        ${user ? '<a href="customer_dashboard.html">My Dashboard</a>' : ""}
        ${isAdmin ? '<a href="admin_dashboard.html">Admin</a>' : ""}
      </nav>
      <div class="nav-actions">
        ${user
          ? `<span class="text-sm text-muted" style="margin-right:.5rem">Hi, ${ui.escape(user.full_name.split(" ")[0])}</span>
             <button class="btn btn-secondary btn-sm" id="logoutBtn">Logout</button>`
          : `<a href="login.html" class="btn btn-ghost btn-sm">Login</a>
             <a href="register.html" class="btn btn-primary btn-sm">Register</a>`}
        <button class="nav-toggle" id="navToggle" aria-label="Menu">&#9776;</button>
      </div>
    </div>
  `;
  const toggle = document.getElementById("navToggle");
  if (toggle) toggle.addEventListener("click", () => {
    document.getElementById("navLinks").classList.toggle("open");
  });
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) logoutBtn.addEventListener("click", () => {
    auth.logout();
    ui.toast("Logged out");
    setTimeout(() => location.href = "index.html", 600);
  });
  window.addEventListener("scroll", () => {
    document.querySelector(".navbar")?.classList.toggle("scrolled", window.scrollY > 10);
  });
}

/* ----- Footer render ----- */
function renderFooter() {
  const el = document.getElementById("footer");
  if (!el) return;
  el.innerHTML = `
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="brand" style="color:white;margin-bottom:1rem">
            <span class="brand-mark">RE</span><span>EstateHub</span>
          </div>
          <p>Your trusted partner for finding, buying, renting, and managing residential and commercial properties across India.</p>
        </div>
        <div>
          <h4>Explore</h4>
          <ul style="display:flex;flex-direction:column;gap:.5rem">
            <li><a href="properties.html">All Properties</a></li>
            <li><a href="properties.html?type=Apartment">Apartments</a></li>
            <li><a href="properties.html?type=Villa">Villas</a></li>
            <li><a href="properties.html?type=Plot">Plots</a></li>
          </ul>
        </div>
        <div>
          <h4>Account</h4>
          <ul style="display:flex;flex-direction:column;gap:.5rem">
            <li><a href="login.html">Login</a></li>
            <li><a href="register.html">Register</a></li>
            <li><a href="customer_dashboard.html">Dashboard</a></li>
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul style="display:flex;flex-direction:column;gap:.5rem">
            <li>info@estatehub.com</li>
            <li>+91 98765 43210</li>
            <li>Bangalore, India</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        &copy; ${new Date().getFullYear()} EstateHub. Built for the Real Estate Property Portal project.
      </div>
    </div>
  `;
}

/* ----- Property card ----- */
function propertyCard(p) {
  const fav = favorites.isFav(p.property_id);
  const badgeClass = ui.statusClass(p.status);
  return `
    <article class="property-card">
      <div class="property-image">
        <span class="badge ${badgeClass}">${ui.escape(p.status)}</span>
        <button class="fav-btn ${fav ? "active" : ""}" data-fav="${p.property_id}" title="Save to wishlist">${fav ? "♥" : "♡"}</button>
        <img src="${ui.escape(p.image_url || "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg")}" alt="${ui.escape(p.property_title)}" loading="lazy">
      </div>
      <div class="property-body">
        <span class="property-type">${ui.escape(p.property_type)}</span>
        <h3 class="property-title">${ui.escape(p.property_title)}</h3>
        <div class="property-location">📍 ${ui.escape(p.location)}</div>
        <div class="property-specs">
          ${p.bedrooms ? `<span>🛏 ${p.bedrooms} Beds</span>` : ""}
          ${p.bathrooms ? `<span>🛁 ${p.bathrooms} Baths</span>` : ""}
          <span>📐 ${p.area_sqft} sqft</span>
        </div>
      </div>
      <div class="property-footer">
        <span class="property-price">${ui.money(p.price)}</span>
        <a href="property_details.html?id=${p.property_id}" class="btn btn-primary btn-sm">View</a>
      </div>
    </article>
  `;
}

/* ----- Compare bar ----- */
function renderCompareBar() {
  let bar = document.getElementById("compareBar");
  if (!bar) {
    bar = document.createElement("div");
    bar.id = "compareBar";
    bar.className = "compare-bar";
    document.body.appendChild(bar);
  }
  const list = compare.all();
  if (list.length === 0) { bar.classList.remove("show"); return; }
  bar.classList.add("show");
  bar.innerHTML = `
    <span class="text-sm">Comparing ${list.length} of 3</span>
    ${list.map((id) => `<span class="chip chip-primary">#${id}</span>`).join("")}
    <button class="btn btn-primary btn-sm" onclick="location.href='properties.html?compare=1'">Compare</button>
    <button class="btn btn-secondary btn-sm" onclick="compare.clear();renderCompareBar()">Clear</button>
  `;
}

/* ----- Init ----- */
document.addEventListener("DOMContentLoaded", () => {
  renderNavbar();
  renderFooter();
  renderCompareBar();
});
