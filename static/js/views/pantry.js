/* Pantry view: everything you have on hand, grouped by category.
   Quantities feed the shopping list (needed - have = to buy). */

App.registerView('pantry', {
  title: 'Pantry',
  icon: 'box',

  async render(container) {
    const items = await App.api('/api/pantry');
    let search = '';

    const listWrap = h('div', {});

    const setQty = async (item, qty) => {
      const prev = item.quantity;
      item.quantity = qty; // optimistic — so rapid clicks read the latest value, not stale server state
      drawList();
      try {
        const updated = await App.api('/api/pantry/' + item.id, 'PUT', { quantity: qty });
        item.quantity = updated.quantity;
        drawList();
      } catch (err) {
        item.quantity = prev;
        drawList();
        App.toast(err.message, 'error');
      }
    };

    const itemRow = (item) => h('div', { class: 'rowline' },
      h('div', { class: 'grow' },
        h('div', { class: 'bold truncate' }, item.name),
        item.unit ? h('div', { class: 'muted small' }, item.unit) : null),
      h('span', { class: 'stepper' },
        h('button', { onclick: () => setQty(item, Math.max(0, item.quantity - 1)) }, '−'),
        h('span', { class: 'qty' }, App.fmtQty(item.quantity)),
        h('button', { onclick: () => setQty(item, item.quantity + 1) }, '+')),
      item.quantity === 0 ? h('span', { class: 'chip chip-tomato' }, 'Out') : null,
      h('button', {
        class: 'btn btn-ghost btn-sm btn-icon', title: 'Edit',
        onclick: () => editModal(item),
      }, App.icon('edit', 15)),
      h('button', {
        class: 'btn btn-danger btn-sm btn-icon', title: 'Remove',
        onclick: () => {
          if (!confirm('Remove ' + item.name + ' from the pantry?')) return;
          App.api('/api/pantry/' + item.id, 'DELETE')
            .then(() => { App.toast('Removed ' + item.name); App.renderCurrent(); })
            .catch((err) => App.toast(err.message, 'error'));
        },
      }, App.icon('trash', 15)));

    const drawList = () => {
      const outCount = items.filter((i) => i.quantity === 0).length;
      sub.textContent = items.length + ' item' + (items.length === 1 ? '' : 's') + ' on hand' +
        (outCount ? ' · ' + outCount + ' out of stock' : '');
      const q = search.toLowerCase();
      const filtered = items.filter((i) => i.name.toLowerCase().includes(q));
      if (!filtered.length) {
        listWrap.replaceChildren(h('div', { class: 'card' },
          h('div', { class: 'empty-state' },
            h('div', { class: 'big' }, App.icon(items.length ? 'search' : 'box', 32)),
            h('div', { class: 'headline' }, items.length ? 'Nothing matches' : 'Your pantry is empty'),
            items.length ? 'Try a different search.' : 'Add what you have on hand — the shopping list subtracts it automatically.')));
        return;
      }
      const groups = App.PANTRY_CATEGORIES
        .map((cat) => ({ cat, rows: filtered.filter((i) => i.category === cat) }))
        .filter((g) => g.rows.length);
      listWrap.replaceChildren(...groups.map(({ cat, rows }) => {
        const meta = App.CATEGORY_META[cat];
        return h('div', { class: 'card', style: { marginBottom: '14px' } },
          h('h3', {}, meta.label + ' ', h('span', { class: 'chip' }, rows.length)),
          rows.map(itemRow));
      }));
    };

    const editModal = (item) => {
      const form = h('form', {
        onsubmit: async (e) => {
          e.preventDefault();
          const data = Object.fromEntries(new FormData(e.target).entries());
          try {
            await App.api('/api/pantry/' + item.id, 'PUT', data);
            modal.close();
            App.toast('Saved');
            App.renderCurrent();
          } catch (err) { App.toast(err.message, 'error'); }
        },
      },
        h('div', { class: 'field' }, h('label', {}, 'Name'),
          h('input', { class: 'input', name: 'name', value: item.name, required: true, maxlength: 60 })),
        h('div', { class: 'field-row' },
          h('div', { class: 'field' }, h('label', {}, 'Quantity'),
            h('input', { class: 'input', name: 'quantity', type: 'number', step: 'any', min: 0, value: item.quantity })),
          h('div', { class: 'field' }, h('label', {}, 'Unit (optional)'),
            h('input', { class: 'input', name: 'unit', value: item.unit, placeholder: 'cups, lb, cans…', maxlength: 20 }))),
        h('div', { class: 'field' }, h('label', {}, 'Category'),
          h('select', { class: 'select', name: 'category' },
            App.PANTRY_CATEGORIES.map((c) =>
              h('option', { value: c, selected: c === item.category }, App.CATEGORY_META[c].label)))),
        h('button', { class: 'btn btn-primary', type: 'submit', style: { width: '100%', justifyContent: 'center' } }, 'Save'));
      const modal = App.modal({ title: 'Edit ' + item.name, body: form });
    };

    // Category-aware autocomplete: the name field suggests common items for the
    // selected category (plus items already in that category of your pantry).
    const suggList = h('datalist', { id: 'pantry-sugg' });
    const updateSuggestions = (category) => {
      const seen = new Set();
      const opts = [];
      const add = (name) => {
        const key = (name || '').trim().toLowerCase();
        if (key && !seen.has(key)) { seen.add(key); opts.push(name); }
      };
      (App.PANTRY_SUGGESTIONS[category] || []).forEach(add);
      items.filter((i) => i.category === category).forEach((i) => add(i.name));
      opts.sort((a, b) => a.localeCompare(b));
      suggList.replaceChildren(...opts.map((name) => h('option', { value: name })));
    };

    const nameInput = h('input', {
      class: 'input', name: 'name', placeholder: 'start typing… e.g. tomato, chicken, rice',
      maxlength: 60, list: 'pantry-sugg', autocomplete: 'off',
    });
    const catSelect = h('select', {
      class: 'select', name: 'category',
      onchange: (e) => { updateSuggestions(e.target.value); nameInput.focus(); },
    }, App.PANTRY_CATEGORIES.map((c) => h('option', { value: c }, App.CATEGORY_META[c].label)));

    const addForm = h('form', {
      class: 'card', style: { marginBottom: '18px' },
      onsubmit: async (e) => {
        e.preventDefault();
        const btn = e.target.querySelector('button[type="submit"]');
        if (btn.disabled) return;
        const data = Object.fromEntries(new FormData(e.target).entries());
        if (!data.name.trim()) return;
        btn.disabled = true;
        try {
          await App.api('/api/pantry', 'POST', data);
          App.toast('Added ' + data.name.trim());
          App.renderCurrent();
        } catch (err) {
          btn.disabled = false;
          App.toast(err.message, 'error');
        }
      },
    },
      h('div', { class: 'field-row', style: { alignItems: 'flex-end' } },
        h('div', { class: 'field', style: { flex: 2, marginBottom: 0 } },
          h('label', {}, 'Add an item'),
          nameInput),
        h('div', { class: 'field', style: { marginBottom: 0 } },
          h('label', {}, 'Qty'),
          h('input', { class: 'input', name: 'quantity', type: 'number', step: 'any', min: 0, value: 1 })),
        h('div', { class: 'field', style: { marginBottom: 0 } },
          h('label', {}, 'Unit'),
          h('input', { class: 'input', name: 'unit', placeholder: 'cups, lb…', maxlength: 20 })),
        h('div', { class: 'field', style: { marginBottom: 0 } },
          h('label', {}, 'Category'),
          catSelect),
        h('button', { class: 'btn btn-primary', type: 'submit', style: { marginBottom: 0 } }, '+ Add')),
      suggList);
    updateSuggestions(App.PANTRY_CATEGORIES[0]);

    const searchBox = h('input', {
      class: 'input', placeholder: 'Search the pantry…', style: { maxWidth: '260px' },
      oninput: (e) => { search = e.target.value; drawList(); },
    });

    const sub = h('div', { class: 'view-sub' });

    container.replaceChildren(
      h('div', { class: 'view-head' },
        h('div', {},
          h('div', { class: 'view-title' }, 'Pantry'),
          sub),
        h('div', { class: 'view-actions' }, searchBox)),
      addForm,
      listWrap);

    drawList();
  },
});
