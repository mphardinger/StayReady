/* Stay Ready — app shell: API client, DOM builder, router, modal, toast, helpers.
   Views register themselves via App.registerView(name, def) and are rendered
   into the #view container by the hash router (#/plan, #/pantry, ...). */

/** DOM builder. Strings/numbers become text nodes (XSS-safe by construction).
 *  h('div', {class: 'card', onclick: fn}, 'hello', h('b', {}, '!'))            */
function h(tag, attrs, ...children) {
  const el = document.createElement(tag);
  for (const [key, val] of Object.entries(attrs || {})) {
    if (val === null || val === undefined || val === false) continue;
    if (key.startsWith('on') && typeof val === 'function') {
      el.addEventListener(key.slice(2).toLowerCase(), val);
    } else if (key === 'class') {
      el.className = val;
    } else if (key === 'style' && typeof val === 'object') {
      Object.assign(el.style, val);
    } else if (key === 'value') {
      el.value = val;
    } else if (key === 'checked' || key === 'disabled' || key === 'selected') {
      el[key] = Boolean(val);
    } else {
      el.setAttribute(key, val);
    }
  }
  const append = (child) => {
    if (child === null || child === undefined || child === false) return;
    if (Array.isArray(child)) { child.forEach(append); return; }
    el.appendChild(child instanceof Node ? child : document.createTextNode(String(child)));
  };
  children.forEach(append);
  return el;
}

/* ---- Inline line-icon system (monochrome, currentColor stroke) ---- */
const SVG_NS = 'http://www.w3.org/2000/svg';
function svgNode(tag, attrs) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}
const ICON_DEFS = {
  today: [['circle', { cx: 12, cy: 12, r: 4 }], ['line', { x1: 12, y1: 2, x2: 12, y2: 4 }],
    ['line', { x1: 12, y1: 20, x2: 12, y2: 22 }], ['line', { x1: 4.2, y1: 4.2, x2: 5.6, y2: 5.6 }],
    ['line', { x1: 18.4, y1: 18.4, x2: 19.8, y2: 19.8 }], ['line', { x1: 2, y1: 12, x2: 4, y2: 12 }],
    ['line', { x1: 20, y1: 12, x2: 22, y2: 12 }], ['line', { x1: 4.2, y1: 19.8, x2: 5.6, y2: 18.4 }],
    ['line', { x1: 18.4, y1: 5.6, x2: 19.8, y2: 4.2 }]],
  calendar: [['rect', { x: 3, y: 4, width: 18, height: 18, rx: 2 }], ['line', { x1: 16, y1: 2, x2: 16, y2: 6 }],
    ['line', { x1: 8, y1: 2, x2: 8, y2: 6 }], ['line', { x1: 3, y1: 10, x2: 21, y2: 10 }]],
  book: [['path', { d: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20' }],
    ['path', { d: 'M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z' }]],
  box: [['path', { d: 'M21 8v13H3V8' }], ['rect', { x: 1, y: 3, width: 22, height: 5, rx: 1 }],
    ['line', { x1: 10, y1: 12, x2: 14, y2: 12 }]],
  cart: [['circle', { cx: 9, cy: 21, r: 1 }], ['circle', { cx: 20, cy: 21, r: 1 }],
    ['path', { d: 'M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6' }]],
  home: [['path', { d: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z' }],
    ['polyline', { points: '9 22 9 12 15 12 15 22' }]],
  search: [['circle', { cx: 11, cy: 11, r: 7 }], ['line', { x1: 21, y1: 21, x2: 16.65, y2: 16.65 }]],
  plus: [['line', { x1: 12, y1: 5, x2: 12, y2: 19 }], ['line', { x1: 5, y1: 12, x2: 19, y2: 12 }]],
  check: [['polyline', { points: '20 6 9 17 4 12' }]],
  close: [['line', { x1: 18, y1: 6, x2: 6, y2: 18 }], ['line', { x1: 6, y1: 6, x2: 18, y2: 18 }]],
  chevronLeft: [['polyline', { points: '15 18 9 12 15 6' }]],
  chevronRight: [['polyline', { points: '9 18 15 12 9 6' }]],
  trash: [['polyline', { points: '3 6 5 6 21 6' }],
    ['path', { d: 'M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2' }]],
  edit: [['path', { d: 'M12 20h9' }], ['path', { d: 'M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z' }]],
  copy: [['rect', { x: 9, y: 9, width: 13, height: 13, rx: 2 }],
    ['path', { d: 'M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1' }]],
  download: [['path', { d: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4' }],
    ['polyline', { points: '7 10 12 15 17 10' }], ['line', { x1: 12, y1: 15, x2: 12, y2: 3 }]],
  print: [['polyline', { points: '6 9 6 2 18 2 18 9' }],
    ['path', { d: 'M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2' }],
    ['rect', { x: 6, y: 14, width: 12, height: 8 }]],
  clock: [['circle', { cx: 12, cy: 12, r: 9 }], ['polyline', { points: '12 7 12 12 15 14' }]],
  cost: [['line', { x1: 12, y1: 1, x2: 12, y2: 23 }],
    ['path', { d: 'M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6' }]],
  score: [['polyline', { points: '22 12 18 12 15 21 9 3 6 12 2 12' }]],
  users: [['path', { d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' }], ['circle', { cx: 9, cy: 7, r: 4 }],
    ['path', { d: 'M23 21v-2a4 4 0 0 0-3-3.87' }], ['path', { d: 'M16 3.13a4 4 0 0 1 0 7.75' }]],
  logout: [['path', { d: 'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4' }],
    ['polyline', { points: '16 17 21 12 16 7' }], ['line', { x1: 21, y1: 12, x2: 9, y2: 12 }]],
  alert: [['path', { d: 'M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z' }],
    ['line', { x1: 12, y1: 9, x2: 12, y2: 13 }], ['line', { x1: 12, y1: 17, x2: 12.01, y2: 17 }]],
  shuffle: [['polyline', { points: '16 3 21 3 21 8' }], ['line', { x1: 4, y1: 20, x2: 21, y2: 3 }],
    ['polyline', { points: '21 16 21 21 16 21' }], ['line', { x1: 15, y1: 15, x2: 21, y2: 21 }],
    ['line', { x1: 4, y1: 4, x2: 9, y2: 9 }]],
  repeat: [['polyline', { points: '17 1 21 5 17 9' }], ['path', { d: 'M3 11V9a4 4 0 0 1 4-4h14' }],
    ['polyline', { points: '7 23 3 19 7 15' }], ['path', { d: 'M21 13v2a4 4 0 0 1-4 4H3' }]],
};

const App = {
  state: { user: null },
  views: {},
  NAV_ORDER: ['dashboard', 'plan', 'recipes', 'pantry', 'shopping', 'balance', 'household'],
  // Nav labels must fit a 7-slot bottom tab bar on a 375px phone (~9 chars max).
  NAV_SHORT: { shopping: 'Shopping' },
  MEAL_TYPES: ['breakfast', 'lunch', 'dinner'],
  MEAL_META: {
    breakfast: { label: 'Breakfast' },
    lunch: { label: 'Lunch' },
    dinner: { label: 'Dinner' },
  },
  PANTRY_CATEGORIES: ['produce', 'meat', 'dairy', 'grains', 'canned', 'frozen', 'spices', 'snacks', 'other'],
  CATEGORY_META: {
    produce: { label: 'Produce' },
    meat: { label: 'Meat & Fish' },
    dairy: { label: 'Dairy & Eggs' },
    grains: { label: 'Grains & Pasta' },
    canned: { label: 'Canned & Jarred' },
    frozen: { label: 'Frozen' },
    spices: { label: 'Spices & Oils' },
    snacks: { label: 'Snacks' },
    other: { label: 'Other' },
  },
  // Common grocery items per category, powering the pantry add-item autocomplete.
  PANTRY_SUGGESTIONS: {
    produce: ['tomato', 'tomatillo', 'onion', 'red onion', 'garlic', 'potato', 'sweet potato',
      'carrot', 'celery', 'broccoli', 'cauliflower', 'spinach', 'lettuce', 'romaine lettuce',
      'kale', 'bell pepper', 'jalapeño', 'cucumber', 'zucchini', 'mushroom', 'avocado', 'lemon',
      'lime', 'apple', 'banana', 'orange', 'strawberries', 'blueberries', 'grapes', 'ginger',
      'cilantro', 'parsley', 'basil', 'green onion', 'corn', 'peas', 'green beans'],
    meat: ['chicken breast', 'chicken thighs', 'ground beef', 'ground turkey', 'steak',
      'pork chops', 'bacon', 'sausage', 'salmon', 'tuna', 'shrimp', 'tilapia', 'cod', 'ham',
      'sliced turkey', 'hot dogs'],
    dairy: ['milk', 'eggs', 'butter', 'cheddar cheese', 'mozzarella', 'parmesan cheese',
      'cream cheese', 'sour cream', 'greek yogurt', 'yogurt', 'heavy cream', 'half and half',
      'cottage cheese', 'feta cheese'],
    grains: ['rice', 'jasmine rice', 'brown rice', 'pasta', 'spaghetti', 'penne', 'bread',
      'tortillas', 'rolled oats', 'quinoa', 'flour', 'couscous', 'bagels', 'breadcrumbs', 'noodles'],
    canned: ['canned diced tomatoes', 'tomato sauce', 'tomato paste', 'black beans',
      'kidney beans', 'chickpeas', 'canned corn', 'canned tuna', 'chicken broth',
      'vegetable broth', 'coconut milk', 'marinara sauce', 'salsa', 'olives', 'green chiles'],
    frozen: ['frozen peas', 'frozen corn', 'frozen broccoli', 'frozen berries', 'frozen pizza',
      'ice cream', 'frozen chicken', 'frozen shrimp', 'frozen fries', 'frozen waffles'],
    spices: ['salt', 'pepper', 'garlic powder', 'onion powder', 'paprika', 'cumin', 'chili powder',
      'oregano', 'thyme', 'cinnamon', 'olive oil', 'vegetable oil', 'sesame oil', 'soy sauce',
      'vinegar', 'honey', 'sugar', 'brown sugar', 'baking soda', 'baking powder', 'vanilla extract'],
    snacks: ['chips', 'crackers', 'popcorn', 'granola bars', 'pretzels', 'cookies', 'nuts',
      'peanut butter', 'trail mix', 'dried fruit'],
    other: [],
  },
  REC_CATS: [
    { key: 'time', label: 'Quickest', explain: 'shortest time to make' },
    { key: 'nutrition', label: 'Healthiest', explain: 'best nutrition score' },
    { key: 'cost', label: 'Cheapest', explain: 'lowest cost per serving' },
  ],

  /* ---------- API ---------- */

  async api(path, method = 'GET', body) {
    const opts = { method, headers: {} };
    if (body !== undefined) {
      opts.headers['Content-Type'] = 'application/json';
      opts.body = JSON.stringify(body);
    }
    let res;
    try {
      res = await fetch(path, opts);
    } catch {
      throw new Error('Cannot reach the server — is it running?');
    }
    if (res.status === 401 && !path.startsWith('/api/auth/')) {
      App.state.user = null;
      App.renderAuth();
      throw new Error('Signed out');
    }
    let data = null;
    try { data = await res.json(); } catch { /* non-JSON response */ }
    if (!res.ok) throw new Error((data && data.error) || 'Request failed (' + res.status + ')');
    return data;
  },

  /* ---------- Views & routing ---------- */

  registerView(name, def) { this.views[name] = def; },

  route() {
    const name = (location.hash || '').replace(/^#\/?/, '').split('?')[0];
    return this.views[name] ? name : 'dashboard';
  },

  navigate(name) { location.hash = '#/' + name; },

  async renderCurrent() {
    const name = this.route();
    document.querySelectorAll('.navlink').forEach((a) => {
      a.classList.toggle('active', a.dataset.view === name);
    });
    const container = document.getElementById('view');
    if (!container) return;
    // Generation token: if the user navigates again before this render's await
    // resolves, the stale render's replaceChildren calls become no-ops.
    const token = (this._renderToken = (this._renderToken || 0) + 1);
    const guarded = { replaceChildren: (...kids) => {
      if (token === this._renderToken) container.replaceChildren(...kids);
    } };
    guarded.replaceChildren(
      h('div', { class: 'empty-state' }, this.spinner(), 'Loading…'));
    try {
      await this.views[name].render(guarded);
    } catch (err) {
      if (err.message === 'Signed out') return;
      guarded.replaceChildren(
        h('div', { class: 'empty-state' },
          h('div', { class: 'big' }, this.icon('alert', 32)),
          h('div', { class: 'headline' }, 'Could not load this page'),
          h('div', {}, err.message)));
    }
  },

  renderShell() {
    const user = this.state.user;
    const nav = this.NAV_ORDER.filter((n) => this.views[n]).map((name) => {
      const v = this.views[name];
      return h('a', { class: 'navlink', href: '#/' + name, 'data-view': name, 'aria-label': v.title },
        h('span', { class: 'nav-icon' }, App.icon(v.icon, 20)),
        h('span', { class: 'nav-label' }, this.NAV_SHORT[name] || v.title),
        h('span', { class: 'nav-tip' }, v.title));
    });
    document.getElementById('app').replaceChildren(
      h('div', { class: 'layout' },
        h('nav', { class: 'sidebar' },
          h('div', { class: 'brand' },
            h('span', { class: 'brand-mark' }, 'SR'),
            h('span', { class: 'brand-text' }, 'Stay Ready')),
          nav,
          h('div', { class: 'sidebar-foot' },
            h('div', { class: 'who' }, user.display_name),
            h('div', { class: 'hh' }, user.household_name),
            h('button', { class: 'btn btn-ghost btn-sm', style: { marginTop: '8px' }, onclick: () => App.logout() }, 'Sign out'))),
        h('main', { class: 'main', id: 'view' })));
    this.renderCurrent();
  },

  async logout() {
    try { await this.api('/api/auth/logout', 'POST'); } catch { /* ignore */ }
    this.state.user = null;
    this.renderAuth();
  },

  async boot() {
    window.addEventListener('hashchange', () => { if (App.state.user) App.renderCurrent(); });
    try {
      const me = await this.api('/api/auth/me');
      this.state.user = me.user;
      this.renderShell();
    } catch (err) {
      if (err.message !== 'Signed out') this.renderAuth();
    }
  },

  /* ---------- Modal ---------- */

  /** App.modal({title, body, wide}) -> {el, close}. body is a Node. */
  modal({ title, body, wide }) {
    const close = () => { overlay.remove(); document.removeEventListener('keydown', onEsc); };
    let downOnOverlay = false;
    const overlay = h('div', {
      class: 'modal-overlay',
      onmousedown: (e) => { downOnOverlay = e.target === overlay; },
      onclick: (e) => { if (e.target === overlay && downOnOverlay) close(); },
    },
      h('div', { class: 'modal' + (wide ? ' modal-wide' : '') },
        h('div', { class: 'modal-head' },
          h('h2', {}, title),
          h('button', { class: 'modal-close', onclick: close }, App.icon('close', 18))),
        h('div', { class: 'modal-body' }, body)));
    const onEsc = (e) => { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', onEsc);
    document.body.appendChild(overlay);
    return { el: overlay, close };
  },

  /* ---------- Toast ---------- */

  /** App.toast(msg), App.toast(msg,'error'), or App.toast(msg,'success',{label,onClick})
   *  for an action button (e.g. Undo). Action toasts linger longer. */
  toast(message, type = 'success', action) {
    let wrap = document.querySelector('.toast-wrap');
    if (!wrap) {
      wrap = h('div', { class: 'toast-wrap' });
      document.body.appendChild(wrap);
    }
    const t = h('div', { class: 'toast toast-' + type },
      h('span', { class: 'grow' }, message),
      action ? h('button', {
        class: 'toast-action',
        onclick: () => { clearTimeout(timer); t.remove(); action.onClick(); },
      }, action.label) : null);
    wrap.appendChild(t);
    const timer = setTimeout(() => t.remove(), action ? 6500 : 3200);
    return t;
  },

  /* ---------- Date helpers (all LOCAL time — never toISOString for dates) ---------- */

  fmtDate(d) {
    const p = (n) => String(n).padStart(2, '0');
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
  },
  parseDate(str) {
    const [y, m, day] = str.split('-').map(Number);
    return new Date(y, m - 1, day);
  },
  addDays(d, n) {
    const copy = new Date(d);
    copy.setDate(copy.getDate() + n);
    return copy;
  },
  today() {
    const now = new Date();
    return new Date(now.getFullYear(), now.getMonth(), now.getDate());
  },
  fmtHuman(dateStr) {
    return this.parseDate(dateStr).toLocaleDateString(undefined,
      { weekday: 'short', month: 'short', day: 'numeric' });
  },
  monthLabel(d) {
    return d.toLocaleDateString(undefined, { month: 'long', year: 'numeric' });
  },

  /* ---------- Misc helpers ---------- */

  fmtMoney(x) { return '$' + (Number(x) || 0).toFixed(2); },

  fmtQty(x) {
    const n = Number(x) || 0;
    return Number.isInteger(n) ? String(n) : String(Math.round(n * 100) / 100);
  },

  fmtMinutes(mins) {
    if (mins >= 60) {
      const hrs = Math.floor(mins / 60), rest = mins % 60;
      return rest ? hrs + 'h ' + rest + 'm' : hrs + 'h';
    }
    return mins + ' min';
  },

  /** Top picks from a recipe list for a recommendation category ('time'|'nutrition'|'cost').
   *  mealType filters to that meal (+ 'any' recipes); pass null for all. */
  recommend(recipes, category, mealType, limit = 5) {
    let list = recipes.slice();
    if (mealType) list = list.filter((r) => this.mealMatches(r.meal_type, mealType));
    const sorters = {
      time: (a, b) => a.time_minutes - b.time_minutes,
      nutrition: (a, b) => b.nutrition_score - a.nutrition_score,
      cost: (a, b) => a.cost_per_serving - b.cost_per_serving,
    };
    list.sort(sorters[category] || sorters.time);
    return list.slice(0, limit);
  },

  mealTag(mealType) {
    const meta = this.MEAL_META[mealType];
    if (!meta) return h('span', { class: 'chip' }, 'Any meal');
    return h('span', { class: 'chip tag-' + mealType }, meta.label);
  },

  /** Whether a recipe of `recipeType` fits a `slot`. Lunch & dinner are treated
   *  as interchangeable (people mix them); 'any' recipes fit every slot. */
  mealMatches(recipeType, slot) {
    if (recipeType === 'any') return true;
    if (slot === 'lunch' || slot === 'dinner') return recipeType === 'lunch' || recipeType === 'dinner';
    return recipeType === slot;
  },

  /** Build an inline SVG line icon (currentColor stroke). size in px, default 18. */
  icon(name, size) {
    const svg = svgNode('svg', {
      viewBox: '0 0 24 24', width: size || 18, height: size || 18,
      fill: 'none', stroke: 'currentColor', 'stroke-width': 1.8,
      'stroke-linecap': 'round', 'stroke-linejoin': 'round', class: 'icon',
    });
    (ICON_DEFS[name] || []).forEach(([tag, attrs]) => svg.appendChild(svgNode(tag, attrs)));
    return svg;
  },

  /** A lettered square standing in for a recipe (first letter of its name). */
  monogram(name, cls) {
    const letter = (((name || '').trim()[0]) || '?').toUpperCase();
    return h('span', { class: 'monogram' + (cls ? ' ' + cls : '') }, letter);
  },

  /** A stat chip (icon + value) for a recipe: key is 'time' | 'cost' | 'nutrition'. */
  statChip(key, r) {
    if (key === 'time') return h('span', { class: 'chip' }, this.icon('clock', 13), this.fmtMinutes(r.time_minutes));
    if (key === 'cost') return h('span', { class: 'chip' }, this.icon('cost', 13), this.fmtMoney(r.cost_per_serving) + '/serving');
    return h('span', { class: 'chip' }, this.icon('score', 13), r.nutrition_score + '/100');
  },

  spinner() { return h('div', { class: 'spinner' }); },
};
