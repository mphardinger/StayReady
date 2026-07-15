/* Recipes view: the household recipe box — browse, search, and filter recipes,
   see pantry readiness at a glance, and add/edit/delete via modals. */

App.registerView('recipes', {
  title: 'Recipes',
  icon: 'book',

  async render(container) {
    const recipes = await App.api('/api/recipes');
    let search = '';
    let mealFilter = 'all';   // all | breakfast | lunchdinner | any
    let sortBy = 'name';      // name | time | cost | nutrition
    // Need-based filters (ANDed): 'quick' (≤15 min), 'budget' (≤$2/serving),
    // plus diet tag slugs. Dietary focus from Settings starts pre-selected.
    const needs = new Set(App.dietPrefs());

    const passesNeeds = (r) => {
      for (const n of needs) {
        if (n === 'quick' && !App.isQuick(r)) return false;
        if (n === 'budget' && !App.isBudget(r)) return false;
        if (App.DIETS[n] && !(r.tags || []).includes(n)) return false;
      }
      return true;
    };

    const SORTERS = {
      name: (a, b) => a.name.localeCompare(b.name),
      time: (a, b) => a.time_minutes - b.time_minutes,
      cost: (a, b) => a.cost_per_serving - b.cost_per_serving,
      nutrition: (a, b) => b.nutrition_score - a.nutrition_score,
    };
    // Sections used when viewing "All" — lunch & dinner grouped together since
    // people mix them.
    const SECTIONS = [
      { label: 'Breakfast', match: (r) => r.meal_type === 'breakfast' },
      { label: 'Lunch & Dinner', match: (r) => r.meal_type === 'lunch' || r.meal_type === 'dinner' },
      { label: 'Anytime', match: (r) => r.meal_type === 'any' },
    ];
    const matchesFilter = (r) => {
      if (mealFilter === 'all') return true;
      if (mealFilter === 'lunchdinner') return r.meal_type === 'lunch' || r.meal_type === 'dinner';
      if (mealFilter === 'any') return r.meal_type === 'any';
      return r.meal_type === mealFilter;
    };

    /* Same normalization the backend uses: lowercase, trimmed, collapsed spaces. */
    const norm = (s) => (s || '').trim().toLowerCase().split(/\s+/).join(' ');

    const MEAL_CHOICES = ['breakfast', 'lunch', 'dinner', 'any'];
    const mealLabel = (mt) => (mt === 'any' ? 'Any meal' : App.MEAL_META[mt].label);

    const gridWrap = h('div', {});

    /* ---------- Card grid ---------- */

    const pantryChip = (r) => {
      if (r.have_count === r.ingredient_count && r.ingredient_count > 0) {
        return h('span', { class: 'chip chip-green' },
          App.icon('check', 13), 'Have all ' + r.ingredient_count + ' ingredients');
      }
      return h('span', { class: 'chip' },
        'have ' + r.have_count + '/' + r.ingredient_count + ' ingredients');
    };

    const card = (r) => h('div', { class: 'card recipe-card', onclick: () => detailModal(r) },
      h('div', { class: 'recipe-head' },
        App.monogram(r.name),
        h('div', { class: 'recipe-name' }, r.name)),
      h('div', { class: 'recipe-chips' },
        App.mealTag(r.meal_type),
        (r.tags || []).map((t) => App.dietChip(t))),
      h('div', { class: 'recipe-chips' },
        App.statChip('time', r),
        App.statChip('cost', r),
        App.statChip('nutrition', r)),
      h('div', { class: 'recipe-chips' }, pantryChip(r)));

    const drawGrid = () => {
      const q = search.toLowerCase();
      const filtered = recipes
        .filter((r) => matchesFilter(r) && passesNeeds(r) && r.name.toLowerCase().includes(q))
        .sort(SORTERS[sortBy] || SORTERS.name);
      if (!filtered.length) {
        gridWrap.replaceChildren(h('div', { class: 'card' },
          h('div', { class: 'empty-state' },
            h('div', { class: 'big' }, App.icon(recipes.length ? 'search' : 'book', 32)),
            h('div', { class: 'headline' }, recipes.length ? 'Nothing matches' : 'No recipes yet'),
            recipes.length
              ? 'Try a different search, meal filter, or fewer "Only show" chips.'
              : 'Add your first recipe and the meal plan practically writes itself.')));
        return;
      }
      // Grouped into sections in the "All" view; a flat grid when a filter is active.
      if (mealFilter === 'all') {
        const sections = SECTIONS
          .map((s) => ({ label: s.label, rows: filtered.filter((r) => s.match(r)) }))
          .filter((s) => s.rows.length);
        gridWrap.replaceChildren(...sections.map((s) => h('div', { class: 'recipe-section' },
          h('div', { class: 'recipe-section-head' }, s.label, ' ',
            h('span', { class: 'chip' }, s.rows.length)),
          h('div', { class: 'grid-cards' }, s.rows.map(card)))));
      } else {
        gridWrap.replaceChildren(h('div', { class: 'grid-cards' }, filtered.map(card)));
      }
    };

    /* ---------- Detail modal ---------- */

    const detailModal = async (summary) => {
      let full, pantry;
      try {
        [full, pantry] = await Promise.all([
          App.api('/api/recipes/' + summary.id),
          App.api('/api/pantry'),
        ]);
      } catch (err) { App.toast(err.message, 'error'); return; }

      const haveSet = new Set(pantry.filter((p) => p.quantity > 0).map((p) => norm(p.name)));
      const steps = (full.instructions || '').split('\n').map((s) => s.trim()).filter(Boolean);

      const macro = (label, value) => h('div', { class: 'stat' },
        h('div', { class: 'stat-label' }, label),
        h('div', { class: 'stat-value' }, value));

      const ingLine = (ing) => {
        const have = haveSet.has(norm(ing.name));
        const amount = ((ing.quantity ? App.fmtQty(ing.quantity) + ' ' : '') + (ing.unit || '')).trim();
        return h('div', { class: 'rowline' },
          h('span', {
            class: 'bold',
            title: have ? 'In the pantry' : 'Need to buy',
            style: { color: have ? 'var(--ink)' : 'var(--red)', width: '18px', textAlign: 'center', display: 'inline-flex', justifyContent: 'center' },
          }, App.icon(have ? 'check' : 'close', 15)),
          h('div', { class: 'grow' }, ing.name),
          amount ? h('span', { class: 'muted small' }, amount) : null);
      };

      const modal = App.modal({
        title: full.name,
        wide: true,
        body: h('div', {},
          h('div', { class: 'recipe-chips', style: { marginBottom: '14px' } },
            App.mealTag(full.meal_type),
            App.statChip('time', full),
            h('span', { class: 'chip' }, App.icon('users', 13), full.servings + ' serving' + (full.servings === 1 ? '' : 's')),
            App.statChip('cost', full),
            App.statChip('nutrition', full)),
          full.description ? h('p', { class: 'muted', style: { marginTop: 0 } }, full.description) : null,
          (full.tags || []).length
            ? h('div', { class: 'recipe-chips', style: { marginBottom: '12px' } },
                full.tags.map((t) => App.dietChip(t)))
            : null,
          h('div', { class: 'muted small', style: { fontWeight: 700, marginBottom: '6px' } }, 'Per serving (estimated)'),
          h('div', { class: 'stat-row', style: { marginBottom: '10px' } },
            macro('Calories', full.calories),
            macro('Protein', App.fmtQty(full.protein_g) + 'g'),
            macro('Carbs', App.fmtQty(full.carbs_g) + 'g'),
            macro('Fat', App.fmtQty(full.fat_g) + 'g')),
          h('div', { class: 'stat-row', style: { marginBottom: '8px' } },
            macro('Fiber', full.fiber_g ? App.fmtQty(full.fiber_g) + 'g' : '—'),
            macro('Sugar', full.sugar_g ? App.fmtQty(full.sugar_g) + 'g' : '—'),
            macro('Sodium', full.sodium_mg ? full.sodium_mg + 'mg' : '—'),
            macro('Potassium', full.potassium_mg ? full.potassium_mg + 'mg' : '—'),
            macro('Phosphorus', full.phosphorus_mg ? full.phosphorus_mg + 'mg' : '—')),
          h('div', { class: 'muted small', style: { marginBottom: '18px' } }, App.NUTRITION_DISCLAIMER),
          h('h3', {}, 'Ingredients ',
            h('span', { class: 'chip' }, full.have_count + '/' + full.ingredient_count + ' on hand')),
          full.ingredients.length
            ? h('div', { style: { marginBottom: '16px' } }, full.ingredients.map(ingLine))
            : h('div', { class: 'muted small', style: { padding: '8px 0 16px' } }, 'No ingredients listed yet.'),
          h('h3', {}, 'Instructions'),
          steps.length
            ? h('ol', { class: 'recipe-steps' }, steps.map((s) => h('li', {}, s)))
            : h('div', { class: 'muted small', style: { padding: '8px 0' } }, 'No instructions written yet.'),
          h('div', { style: { display: 'flex', gap: '10px', marginTop: '18px' } },
            h('button', { class: 'btn', onclick: () => { modal.close(); formModal(full); } }, App.icon('edit', 15), 'Edit'),
            h('button', { class: 'btn btn-danger', onclick: () => removeRecipe(full, modal.close) }, App.icon('trash', 15), 'Delete'))),
      });
    };

    /* ---------- Delete ---------- */

    const removeRecipe = async (r, closeModal) => {
      if (!confirm('Delete "' + r.name + '"? Any planned meals using it will be removed too.')) return;
      try {
        await App.api('/api/recipes/' + r.id, 'DELETE');
        App.toast('Deleted ' + r.name);
        if (closeModal) closeModal();
        App.renderCurrent();
      } catch (err) { App.toast(err.message, 'error'); }
    };

    /* ---------- Add / edit form modal ----------
       recipe: null = blank create; with id = edit; without id = import DRAFT
       (prefilled create — review, then save as a new recipe). */

    const formModal = (recipe) => {
      const isEdit = Boolean(recipe && recipe.id);

      const numField = (label, name, value, step) => h('div', { class: 'field' },
        h('label', {}, label),
        h('input', { class: 'input', name, type: 'number', step, min: 0, value }));

      const ingWrap = h('div', {});
      const ingRow = (ing) => {
        const row = h('div', { class: 'recipe-ing-row' },
          h('input', { class: 'input ing-name', placeholder: 'e.g. eggs', maxlength: 60, value: ing ? ing.name : '' }),
          h('input', { class: 'input ing-qty', type: 'number', step: 'any', min: 0, placeholder: 'Qty', value: ing ? ing.quantity : '' }),
          h('input', { class: 'input ing-unit', placeholder: 'unit', maxlength: 20, value: ing ? ing.unit : '' }),
          h('button', {
            class: 'btn btn-ghost btn-sm btn-icon', type: 'button', title: 'Remove ingredient',
            onclick: () => row.remove(),
          }, App.icon('close', 14)));
        ingWrap.appendChild(row);
      };
      ((recipe && recipe.ingredients.length) ? recipe.ingredients : [null]).forEach(ingRow);

      const form = h('form', {
        onsubmit: async (e) => {
          e.preventDefault();
          const btn = e.target.querySelector('button[type="submit"]');
          if (btn.disabled) return;
          btn.disabled = true;
          const payload = Object.fromEntries(new FormData(e.target).entries());
          payload.tags = [...e.target.querySelectorAll('.diet-tag-box:checked')].map((c) => c.value);
          payload.ingredients = [...ingWrap.querySelectorAll('.recipe-ing-row')].map((row) => ({
            name: row.querySelector('.ing-name').value.trim(),
            quantity: row.querySelector('.ing-qty').value,
            unit: row.querySelector('.ing-unit').value.trim(),
          })).filter((i) => i.name);
          try {
            if (isEdit) {
              await App.api('/api/recipes/' + recipe.id, 'PUT', payload);
              App.toast('Saved ' + payload.name);
            } else {
              await App.api('/api/recipes', 'POST', payload);
              App.toast('Added ' + payload.name);
            }
            modal.close();
            App.renderCurrent();
          } catch (err) {
            btn.disabled = false;
            App.toast(err.message, 'error');
          }
        },
      },
        h('div', { class: 'field' },
          h('label', {}, 'Name'),
          h('input', { class: 'input', name: 'name', required: true, maxlength: 80, placeholder: 'e.g. Veggie Scramble', value: recipe ? recipe.name : '' })),
        h('div', { class: 'field-row' },
          h('div', { class: 'field' },
            h('label', {}, 'Meal type'),
            h('select', { class: 'select', name: 'meal_type' },
              MEAL_CHOICES.map((mt) => h('option', {
                value: mt,
                selected: mt === (recipe ? recipe.meal_type : 'dinner'),
              }, mealLabel(mt))))),
          numField('Time (minutes)', 'time_minutes', recipe ? recipe.time_minutes : 30, 1),
          numField('Servings', 'servings', recipe ? recipe.servings : 4, 1),
          numField('Total cost ($)', 'cost_total', recipe && recipe.cost_total ? recipe.cost_total : '', 'any')),
        h('div', { class: 'field' },
          h('label', {}, 'Description'),
          h('input', { class: 'input', name: 'description', maxlength: 200, placeholder: 'A one-liner to sell it', value: recipe ? recipe.description : '' })),
        h('div', { class: 'field-row' },
          numField('Calories / serving', 'calories', recipe ? (recipe.calories || '') : '', 1),
          numField('Protein (g)', 'protein_g', recipe ? (recipe.protein_g || '') : '', 'any'),
          numField('Carbs (g)', 'carbs_g', recipe ? (recipe.carbs_g || '') : '', 'any'),
          numField('Fat (g)', 'fat_g', recipe ? (recipe.fat_g || '') : '', 'any')),
        h('div', { class: 'field-row' },
          numField('Fiber (g)', 'fiber_g', recipe ? (recipe.fiber_g || '') : '', 'any'),
          numField('Sugar (g)', 'sugar_g', recipe ? (recipe.sugar_g || '') : '', 'any'),
          numField('Sodium (mg)', 'sodium_mg', recipe ? (recipe.sodium_mg || '') : '', 1),
          numField('Potassium (mg)', 'potassium_mg', recipe ? (recipe.potassium_mg || '') : '', 1),
          numField('Phosphorus (mg)', 'phosphorus_mg', recipe ? (recipe.phosphorus_mg || '') : '', 1)),
        h('div', { class: 'field' },
          h('label', {}, 'Diet tags (only tag what genuinely qualifies)'),
          h('div', { style: { display: 'flex', gap: '14px', flexWrap: 'wrap' } },
            Object.entries(App.DIETS).map(([slug, meta]) =>
              h('label', { class: 'leftover-toggle', style: { marginTop: 0 }, title: meta.explain },
                h('input', {
                  type: 'checkbox', class: 'diet-tag-box', value: slug,
                  checked: Boolean(recipe) && (recipe.tags || []).includes(slug),
                }),
                h('span', {}, meta.label))))),
        h('div', { class: 'field' },
          h('label', {}, 'Ingredients'),
          ingWrap,
          h('button', {
            class: 'btn btn-sm', type: 'button', style: { alignSelf: 'flex-start' },
            onclick: () => ingRow(null),
          }, '+ ingredient')),
        h('div', { class: 'field' },
          h('label', {}, 'Instructions (one step per line)'),
          h('textarea', { class: 'input', name: 'instructions', rows: 6, placeholder: 'Crack the eggs…\nWhisk with a pinch of salt…\nScramble low and slow.', value: recipe ? recipe.instructions : '' })),
        h('button', { class: 'btn btn-primary', type: 'submit', style: { width: '100%', justifyContent: 'center' } },
          isEdit ? 'Save recipe' : 'Add recipe'));

      const modal = App.modal({ title: isEdit ? 'Edit ' + recipe.name : (recipe ? 'Review imported recipe' : 'New recipe'), body: form, wide: true });
    };

    /* ---------- Import from link / pasted text ---------- */

    const importModal = () => {
      const urlInput = h('input', {
        class: 'input', type: 'url', placeholder: 'https://www.allrecipes.com/recipe/…',
      });
      const textArea = h('textarea', {
        class: 'input', rows: 7,
        placeholder: 'Chicken Fried Rice\n\nIngredients\n2 cups rice\n2 eggs\n…\n\nInstructions\nCook the rice…',
      });
      const goBtn = h('button', {
        class: 'btn btn-primary', style: { width: '100%', justifyContent: 'center' },
      }, 'Import');
      goBtn.onclick = async () => {
        if (goBtn.disabled) return;
        const url = urlInput.value.trim();
        const text = textArea.value.trim();
        if (!url && !text) { App.toast('Paste a link or the recipe text first', 'error'); return; }
        goBtn.disabled = true;
        goBtn.textContent = 'Importing…';
        try {
          const res = await App.api('/api/recipes/import', 'POST', url ? { url } : { text });
          modal.close();
          formModal(res.draft);
          App.toast('Imported — give it a once-over.  Sites never include cost, so add yours.');
        } catch (err) {
          goBtn.disabled = false;
          goBtn.textContent = 'Import';
          App.toast(err.message, 'error');
        }
      };
      const modal = App.modal({
        title: 'Import a recipe',
        body: h('div', {},
          h('div', { class: 'field' },
            h('label', {}, 'Recipe link'),
            urlInput),
          h('div', { class: 'muted small', style: { margin: '2px 0 12px' } },
            'Works with most recipe sites.  If a site can’t be reached, use the box below.'),
          h('div', { class: 'field' },
            h('label', {}, '…or paste the recipe text'),
            textArea),
          goBtn),
      });
      urlInput.focus();
    };

    /* ---------- Header controls ---------- */

    const TABS = [['all', 'All'], ['breakfast', 'Breakfast'], ['lunchdinner', 'Lunch & Dinner'], ['any', 'Anytime']];
    const tabs = h('div', { class: 'tabs' }, TABS.map(([key, label]) =>
      h('button', {
        class: key === mealFilter ? 'active' : '',
        onclick: (e) => {
          mealFilter = key;
          [...tabs.children].forEach((b) => b.classList.toggle('active', b === e.currentTarget));
          drawGrid();
        },
      }, label)));

    // Need chips: time/budget constraints + diet tags, all ANDed together.
    const NEED_CHOICES = [
      ['quick', '15 min or less'],
      ['budget', 'Under $2/serving'],
      ...Object.entries(App.DIETS).map(([slug, meta]) => [slug, meta.label]),
    ];
    const needChips = h('div', { style: { display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '16px', alignItems: 'center' } },
      h('span', { class: 'muted small', style: { fontWeight: 700 } }, 'Only show:'),
      NEED_CHOICES.map(([key, label]) => h('button', {
        class: 'btn btn-sm' + (needs.has(key) ? ' btn-primary' : ''),
        onclick: (e) => {
          needs.has(key) ? needs.delete(key) : needs.add(key);
          e.currentTarget.classList.toggle('btn-primary', needs.has(key));
          drawGrid();
        },
      }, label)));

    const SORTS = [['name', 'Name (A–Z)'], ['time', 'Quickest'], ['cost', 'Cheapest'], ['nutrition', 'Healthiest']];
    const sortSelect = h('select', {
      class: 'select', style: { width: 'auto' }, title: 'Sort recipes',
      onchange: (e) => { sortBy = e.target.value; drawGrid(); },
    }, SORTS.map(([v, l]) => h('option', { value: v }, 'Sort: ' + l)));

    const searchBox = h('input', {
      class: 'input', placeholder: 'Search recipes…', style: { maxWidth: '200px' },
      oninput: (e) => { search = e.target.value; drawGrid(); },
    });

    container.replaceChildren(
      h('div', { class: 'view-head' },
        h('div', {},
          h('div', { class: 'view-title' }, 'Recipes'),
          h('div', { class: 'view-sub' },
            recipes.length + ' recipe' + (recipes.length === 1 ? '' : 's') + ' in the box')),
        h('div', { class: 'view-actions' },
          searchBox,
          tabs,
          sortSelect,
          h('button', { class: 'btn', onclick: importModal }, App.icon('download', 15), 'Import'),
          h('button', { class: 'btn btn-primary', onclick: () => formModal(null) }, '+ New recipe'))),
      needChips,
      gridWrap);

    drawGrid();
  },
});
