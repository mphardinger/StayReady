/* Meal Plan view: a month calendar of breakfast/lunch/dinner slots.
   Click any slot to pick a recipe (with quickest/healthiest/cheapest picks), assign a cook,
   mark it cooked (auto-deducts pantry), or clear it. */

App.registerView('plan', {
  title: 'Meal Plan',
  icon: 'calendar',
  month: null, // Date of the 1st of the month being shown (survives re-renders)
  selectedDate: null, // 'YYYY-MM-DD' the user has clicked to focus (survives re-renders)

  async render(container) {
    if (!this.month) {
      const t = App.today();
      this.month = new Date(t.getFullYear(), t.getMonth(), 1);
    }
    const month = this.month;
    const monthEnd = new Date(month.getFullYear(), month.getMonth() + 1, 0);
    const ws = App.weekStart(); // 0 = Sunday, 1 = Monday (Settings)
    const first = App.addDays(month, -((month.getDay() - ws + 7) % 7));         // week start on/before the 1st
    const last = App.addDays(monthEnd, (ws + 6 - monthEnd.getDay() + 7) % 7);   // week end on/after month end
    const startStr = App.fmtDate(first);
    const endStr = App.fmtDate(last);
    const todayStr = App.fmtDate(App.today());

    const [entries, recipes, members, sales] = await Promise.all([
      App.api('/api/plan?start=' + startStr + '&end=' + endStr),
      App.api('/api/recipes'),
      App.api('/api/members'),
      App.api('/api/sales'),
    ]);
    const byKey = {};
    entries.forEach((e) => { byKey[e.date + '|' + e.meal_type] = e; });
    const shownTypes = App.visibleMealTypes();
    const saleNames = sales.map((s) => s.name);
    const onSale = (r) => App.saleMatches(r, saleNames).length > 0;

    const setMonth = (d) => { this.month = d; App.renderCurrent(); };

    // Toggle a focused day. Pure UI highlight — updates classes directly (no
    // refetch) and works across both the month grid and the mobile agenda.
    const selectDay = (dateStr) => {
      document.querySelectorAll('.day-cell.day-selected, .agenda-day.day-selected')
        .forEach((c) => c.classList.remove('day-selected'));
      if (this.selectedDate === dateStr) { this.selectedDate = null; return; }
      this.selectedDate = dateStr;
      document.querySelectorAll('[data-date="' + dateStr + '"]')
        .forEach((c) => c.classList.add('day-selected'));
    };

    /* ----- slot picker modal ----- */

    const openPicker = (dateStr, meal) => {
      const entry = byKey[dateStr + '|' + meal] || null;
      const meta = App.MEAL_META[meal];
      const matching = recipes.filter((r) => App.mealMatches(r.meal_type, meal));
      let tab = 'all';
      let search = '';
      let selectedId = entry ? entry.recipe.id : null;
      // Need filters (quick/budget/diet), pre-selected from Settings ▸ Dietary focus.
      const needs = new Set(App.dietPrefs());
      const passesNeeds = (r) => {
        for (const n of needs) {
          if (n === 'quick' && !App.isQuick(r)) return false;
          if (n === 'budget' && !App.isBudget(r)) return false;
          if (App.DIETS[n] && !(r.tags || []).includes(n)) return false;
        }
        return true;
      };

      const saveBtn = h('button', {
        class: 'btn btn-primary', disabled: !selectedId, onclick: () => save(),
      }, 'Save meal');

      // "Suggest one" — picks a recipe biased toward the quick/cheap/healthy
      // recommendations for this slot, so a busy user can accept or shuffle.
      const suggestBtn = h('button', {
        class: 'btn suggest-btn', type: 'button',
        onclick: () => {
          const base = matching.filter(passesNeeds);
          let pool = [...new Set([
            ...App.recommend(base, 'time', meal, 5),
            ...App.recommend(base, 'cost', meal, 5),
            ...App.recommend(base, 'nutrition', meal, 5),
          ])].filter((r) => r.id !== selectedId);
          // Bias the shuffle toward recipes using this week's sale items.
          pool = pool.concat(pool.filter(onSale));
          // Fallback also respects the active filter chips — suggesting a
          // recipe the filtered list can't even show would look broken.
          const src = pool.length ? pool : base.filter((r) => r.id !== selectedId);
          if (!src.length) {
            App.toast(needs.size
              ? 'Nothing fits the active filter chips — turn one off or add recipes.'
              : 'No other recipes for this meal yet — add more in Recipes.', 'error');
            return;
          }
          selectedId = src[Math.floor(Math.random() * src.length)].id;
          saveBtn.disabled = false;
          tab = 'all';
          search = '';
          searchInput.value = '';
          drawTabs();
          drawRows();
          const sel = listWrap.querySelector('.pick-row.selected');
          if (sel) sel.scrollIntoView({ block: 'nearest' });
        },
      }, App.icon('shuffle', 15), 'Suggest a ' + meta.label.toLowerCase());

      // Default to on for a fresh dinner, but not when tomorrow's lunch is
      // already planned — the backend won't overwrite it anyway, so reflect
      // that up front instead of offering a checkbox that would silently no-op.
      const nextDateStr = App.fmtDate(App.addDays(App.parseDate(dateStr), 1));
      const nextLunchOccupied = Boolean(byKey[nextDateStr + '|lunch']);
      const leftoverToggle = meal === 'dinner' && App.visibleMealTypes().includes('lunch')
        ? h('label', { class: 'leftover-toggle' + (nextLunchOccupied ? ' leftover-toggle-disabled' : '') },
            h('input', {
              type: 'checkbox',
              checked: !nextLunchOccupied && App.leftoverDefault(),
              disabled: nextLunchOccupied,
            }),
            h('span', {}, App.icon('repeat', 14),
              nextLunchOccupied
                ? " Tomorrow's lunch is already planned, so it won't be overwritten"
                : " Also save tomorrow's lunch as leftovers"))
        : null;

      // Per-row nutrient line for the diets the user tracks (Settings).
      const dietLine = (r) => {
        const prefs = App.dietPrefs();
        const bits = [];
        if (prefs.includes('kidney')) {
          bits.push('Na ' + (r.sodium_mg || '—') + ' · K ' + (r.potassium_mg || '—')
            + ' · P ' + (r.phosphorus_mg || '—') + ' mg');
        }
        if (prefs.includes('diabetic')) {
          bits.push('carbs ' + App.fmtQty(r.carbs_g) + 'g · sugar '
            + (r.sugar_g ? App.fmtQty(r.sugar_g) + 'g' : '—') + ' · fiber '
            + (r.fiber_g ? App.fmtQty(r.fiber_g) + 'g' : '—'));
        }
        return bits.length
          ? h('div', { class: 'muted small', style: { marginTop: '2px' } }, bits.join('   ·   '))
          : null;
      };

      const recipeRow = (r) => h('div', {
        class: 'rowline pick-row' + (r.id === selectedId ? ' selected' : ''),
        onclick: () => { selectedId = r.id; saveBtn.disabled = false; drawRows(); },
      },
        App.monogram(r.name, 'monogram-sm'),
        h('div', { class: 'grow' },
          h('div', { class: 'bold truncate' }, r.name),
          h('div', { style: { display: 'flex', gap: '5px', flexWrap: 'wrap', marginTop: '3px' } },
            App.statChip('time', r),
            App.statChip('cost', r),
            App.statChip('nutrition', r),
            onSale(r) ? h('span', { class: 'chip chip-gold' }, 'on sale') : null,
            (r.tags || []).filter((t) => needs.has(t)).map((t) => App.dietChip(t)),
            h('span', {
              class: 'chip' + (r.ingredient_count > 0 && r.have_count === r.ingredient_count ? ' chip-green' : ''),
            }, 'have ' + r.have_count + '/' + r.ingredient_count)),
          dietLine(r)));

      const searchInput = h('input', {
        class: 'input', placeholder: 'Search recipes…', style: { marginBottom: '10px' },
        oninput: (e) => { search = e.target.value; drawRows(); },
      });
      const listWrap = h('div', { style: { maxHeight: '320px', overflowY: 'auto' } });
      const tabsWrap = h('div', { class: 'tabs', style: { marginBottom: '12px' } });

      const drawTabs = () => {
        const defs = [{ key: 'all', label: 'All' }].concat(App.REC_CATS);
        tabsWrap.replaceChildren(...defs.map((c) =>
          h('button', {
            class: tab === c.key ? 'active' : '',
            onclick: () => { tab = c.key; drawTabs(); drawRows(); },
          }, c.label)));
      };

      // Quick-filter chips (time/budget/diet); active ones AND together.
      const needChips = h('div', { style: { display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '10px' } },
        [['quick', '≤15 min'], ['budget', '<$2/serv'],
          ...Object.entries(App.DIETS).map(([slug, m]) => [slug, m.label])].map(([key, label]) =>
          h('button', {
            class: 'btn btn-sm' + (needs.has(key) ? ' btn-primary' : ''), type: 'button',
            onclick: (e) => {
              needs.has(key) ? needs.delete(key) : needs.add(key);
              e.currentTarget.classList.toggle('btn-primary', needs.has(key));
              drawRows();
            },
          }, label)));

      const drawRows = () => {
        searchInput.style.display = tab === 'all' ? '' : 'none';
        const base = matching.filter(passesNeeds);
        let list;
        if (tab === 'all') {
          const q = search.trim().toLowerCase();
          list = base.filter((r) => r.name.toLowerCase().includes(q));
          // Recipes using this week's sale items float to the top.
          if (saleNames.length) list = [...list.filter(onSale), ...list.filter((r) => !onSale(r))];
        } else {
          list = App.recommend(base, tab, meal, 6);
        }
        if (!list.length) {
          listWrap.replaceChildren(h('div', { class: 'empty-state', style: { padding: '28px 16px' } },
            h('div', { class: 'big' }, App.icon('book', 30)),
            h('div', { class: 'headline' }, matching.length ? 'Nothing matches' : 'No recipes for this meal yet'),
            matching.length ? 'Try a different search or turn off a filter chip.' : 'Add a few in the Recipes tab, then come plan them here.'));
          return;
        }
        listWrap.replaceChildren(...list.map(recipeRow));
      };

      const cookSelect = h('select', { class: 'select' },
        h('option', { value: '' }, '— nobody yet —'),
        members.map((m) => h('option', {
          value: m.id,
          selected: Boolean(entry && entry.cook && entry.cook.id === m.id),
        }, m.name)));

      const save = async () => {
        if (!selectedId || saveBtn.disabled) return;
        saveBtn.disabled = true;
        try {
          const saved = await App.api('/api/plan', 'PUT', {
            date: dateStr,
            meal_type: meal,
            recipe_id: selectedId,
            cook_member_id: cookSelect.value ? Number(cookSelect.value) : null,
            leftover_lunch: leftoverToggle ? leftoverToggle.querySelector('input').checked : false,
          });
          modal.close();
          App.toast(saved.recipe.name + ' planned for ' + meta.label.toLowerCase()
            + (saved.leftover_added ? " · tomorrow's lunch set as leftovers" : ''));
          App.renderCurrent();
        } catch (err) {
          saveBtn.disabled = false;
          App.toast(err.message, 'error');
        }
      };

      const markCookedBtn = h('button', { class: 'btn', onclick: () => markCooked() }, 'Mark cooked');
      const markCooked = async () => {
        if (markCookedBtn.disabled) return;
        markCookedBtn.disabled = true;
        try {
          const res = await App.api('/api/plan/' + entry.id + '/cooked', 'POST');
          modal.close();
          App.toast('Marked cooked — pantry updated: ' + res.deducted.length + ' items deducted');
          App.renderCurrent();
        } catch (err) {
          markCookedBtn.disabled = false;
          App.toast(err.message, 'error');
        }
      };

      const clearBtn = h('button', { class: 'btn btn-danger', onclick: () => clearSlot() }, 'Clear slot');
      const clearSlot = async () => {
        if (clearBtn.disabled) return;
        clearBtn.disabled = true;
        try {
          await App.api('/api/plan?date=' + encodeURIComponent(dateStr) +
            '&meal_type=' + encodeURIComponent(meal), 'DELETE');
          modal.close();
          App.toast('Slot cleared');
          App.renderCurrent();
        } catch (err) {
          clearBtn.disabled = false;
          App.toast(err.message, 'error');
        }
      };

      const footer = h('div', {
        style: { display: 'flex', gap: '10px', marginTop: '16px', flexWrap: 'wrap', alignItems: 'center' },
      },
        saveBtn,
        entry ? (entry.cooked
          ? h('span', { class: 'chip chip-green' }, App.icon('check', 13), 'Cooked')
          : markCookedBtn) : null,
        entry ? clearBtn : null);

      const modal = App.modal({
        title: meta.label + ' · ' + App.fmtHuman(dateStr),
        wide: true,
        body: h('div', {},
          h('div', { style: { display: 'flex', justifyContent: 'flex-end', marginBottom: '10px' } }, suggestBtn),
          tabsWrap,
          needChips,
          searchInput,
          listWrap,
          h('div', { class: 'field', style: { marginTop: '14px', marginBottom: 0 } },
            h('label', {}, "Who's cooking?"),
            cookSelect),
          leftoverToggle,
          footer),
      });
      drawTabs();
      drawRows();
    };

    /* ----- week builder: draft 7 dinners around budget / time / diet ----- */

    const openBuilder = async () => {
      const days = [];
      for (let i = 0; i < 7; i++) days.push(App.fmtDate(App.addDays(App.today(), i)));
      // The builder's window is always today+7, which can extend past (or sit
      // entirely outside) the month range this view fetched into byKey — so it
      // fetches its own week. Anything less risks silently overwriting meals.
      let planned;
      try {
        const weekPlan = await App.api('/api/plan?start=' + days[0] + '&end=' + days[6]);
        planned = {};
        weekPlan.forEach((e) => { planned[e.date + '|' + e.meal_type] = e; });
      } catch (err) { App.toast(err.message, 'error'); return; }
      const recipesById = {};
      recipes.forEach((r) => { recipesById[r.id] = r; });

      const budgetInput = h('input', {
        class: 'input', type: 'number', step: 'any', min: 0, value: '5.00',
        style: { maxWidth: '110px' },
      });
      const timeSelect = h('select', { class: 'select', style: { width: 'auto' } },
        [['', 'Any time'], ['15', '15 min or less'], ['30', '30 min or less'], ['45', '45 min or less']]
          .map(([v, l]) => h('option', { value: v }, l)));
      const dietNeeds = new Set(App.dietPrefs().filter((d) => App.DIETS[d]));
      const dietChips = h('div', { style: { display: 'flex', gap: '6px', flexWrap: 'wrap' } },
        Object.entries(App.DIETS).map(([slug, m]) => h('button', {
          class: 'btn btn-sm' + (dietNeeds.has(slug) ? ' btn-primary' : ''), type: 'button',
          onclick: (e) => {
            dietNeeds.has(slug) ? dietNeeds.delete(slug) : dietNeeds.add(slug);
            e.currentTarget.classList.toggle('btn-primary', dietNeeds.has(slug));
          },
        }, m.label)));
      const salesBox = h('input', { type: 'checkbox', checked: saleNames.length > 0, disabled: !saleNames.length });
      const leftoverBox = h('input', {
        type: 'checkbox',
        checked: App.leftoverDefault() && App.visibleMealTypes().includes('lunch'),
        disabled: !App.visibleMealTypes().includes('lunch'),
      });

      const draftWrap = h('div', {});
      let draft = {}; // dateStr -> recipe (only for days being filled)

      // Empty budget field = no cap; 0 or negative = a strict cap the user
      // typed (which honestly filters everything out, rather than silently
      // meaning "unlimited").
      const budgetVal = () => {
        const raw = budgetInput.value.trim();
        if (raw === '') return null;
        const n = parseFloat(raw);
        return Number.isFinite(n) ? Math.max(n, 0) : null;
      };

      const candidatesFor = () => {
        const maxMin = Number(timeSelect.value) || 0;
        const budget = budgetVal();
        // With leftover lunches each dinner serving gets eaten twice per day
        // (tonight + tomorrow's lunch), so a day's dinner spend is ~2 servings.
        // Without leftovers, dinner gets ~60% of the day's food money.
        const capPerServing = budget === null ? null
          : (leftoverBox.checked ? budget / 2 : budget * 0.6);
        return recipes.filter((r) =>
          App.mealMatches(r.meal_type, 'dinner')
          && (!maxMin || r.time_minutes <= maxMin)
          && [...dietNeeds].every((d) => (r.tags || []).includes(d))
          && (capPerServing === null || r.cost_per_serving <= capPerServing));
      };

      const score = (r) => {
        let s = r.cost_per_serving;
        if (salesBox.checked && onSale(r)) s -= 0.75;
        if (r.ingredient_count > 0) s -= 0.4 * (r.have_count / r.ingredient_count);
        return s;
      };

      // The recipe a given day will serve: drafted, or already planned ("kept").
      const recipeOn = (dateStr) => {
        if (draft[dateStr]) return draft[dateStr];
        const kept = planned[dateStr + '|dinner'];
        return kept ? (recipesById[kept.recipe.id] || null) : null;
      };

      const pickFor = (dateStr, exclude) => {
        // Repeat caps and the no-back-to-back rule count BOTH drafted and kept
        // dinners, and ignore the day being (re)picked itself.
        const used = {};
        for (const d of days) {
          if (d === dateStr) continue;
          const r = recipeOn(d);
          if (r) used[r.id] = (used[r.id] || 0) + 1;
        }
        const neighborIds = [-1, 1]
          .map((off) => recipeOn(App.fmtDate(App.addDays(App.parseDate(dateStr), off))))
          .filter(Boolean)
          .map((r) => r.id);
        const pool = candidatesFor()
          .filter((r) => r.id !== exclude && (used[r.id] || 0) < 2 && !neighborIds.includes(r.id))
          .sort((a, b) => score(a) - score(b))
          .slice(0, 8);
        if (!pool.length) return null;
        return pool[Math.floor(Math.random() * Math.min(pool.length, 4))];
      };

      const drawDraft = () => {
        const rows = days.map((dateStr) => {
          const existing = planned[dateStr + '|dinner'];
          if (existing) {
            return h('div', { class: 'rowline' },
              h('div', { class: 'bold small', style: { width: '86px', flexShrink: 0 } }, App.fmtHuman(dateStr)),
              h('div', { class: 'grow truncate' }, existing.recipe.name),
              h('span', { class: 'chip' }, 'already planned — kept'));
          }
          const r = draft[dateStr];
          if (!r) {
            return h('div', { class: 'rowline' },
              h('div', { class: 'bold small', style: { width: '86px', flexShrink: 0 } }, App.fmtHuman(dateStr)),
              h('div', { class: 'grow muted' }, 'No recipe fits these limits'));
          }
          return h('div', { class: 'rowline' },
            h('div', { class: 'bold small', style: { width: '86px', flexShrink: 0 } }, App.fmtHuman(dateStr)),
            h('div', { class: 'grow' },
              h('div', { class: 'bold truncate' }, r.name),
              h('div', { style: { display: 'flex', gap: '5px', flexWrap: 'wrap', marginTop: '2px' } },
                App.statChip('cost', r),
                App.statChip('time', r),
                salesBox.checked && onSale(r) ? h('span', { class: 'chip chip-gold' }, 'on sale') : null,
                (r.tags || []).filter((t) => dietNeeds.has(t)).map((t) => App.dietChip(t)))),
            h('button', {
              class: 'btn btn-sm btn-icon', title: 'Shuffle this day', type: 'button',
              onclick: () => {
                const next = pickFor(dateStr, r.id);
                if (!next) { App.toast('No other recipe fits these limits', 'error'); return; }
                draft[dateStr] = next;
                drawDraft();
              },
            }, App.icon('shuffle', 14)));
        });

        const drafted = Object.values(draft);
        let summary = null;
        if (drafted.length) {
          // Per the builder's own model: with leftovers on, each dinner
          // serving is eaten twice (dinner + next-day lunch), so a person's
          // real cost is 2 servings per dinner-day. Days with no dinner at
          // all don't dilute the average.
          const factor = leftoverBox.checked ? 2 : 1;
          const dinnerDays = days.filter((d) => recipeOn(d));
          const totalCost = dinnerDays.reduce((sum, d) => sum + recipeOn(d).cost_per_serving, 0) * factor;
          const perDay = dinnerDays.length ? totalCost / dinnerDays.length : 0;
          const budget = budgetVal();
          const mealsCovered = dinnerDays.length + ' dinner' + (dinnerDays.length === 1 ? '' : 's')
            + (leftoverBox.checked ? ' + their leftover lunches' : '');
          summary = h('div', { style: { marginTop: '12px' } },
            h('div', { class: 'bold' },
              'Est. ' + App.fmtMoney(perDay) + '/person/day — ' + mealsCovered + ' for '
              + App.fmtMoney(totalCost) + '/person this week'),
            budget !== null ? h('div', {
              class: 'small',
              style: { fontWeight: 700, color: perDay <= budget ? 'var(--ink-soft)' : 'var(--red-deep)', marginTop: '3px' },
            }, perDay <= budget
              ? 'Under your ' + App.fmtMoney(budget) + '/day target'
              : 'Over your ' + App.fmtMoney(budget) + '/day target — shuffle the pricey days or raise the cap') : null,
            h('div', { class: 'muted small', style: { marginTop: '3px' } },
              'Recipe costs are estimates; breakfasts aren’t counted. Nothing is saved until you accept.'));
        }

        acceptBtn.style.display = drafted.length ? '' : 'none';
        draftWrap.replaceChildren(
          h('div', { class: 'card', style: { marginTop: '14px', padding: '12px 14px' } }, rows, summary));
      };

      const generate = () => {
        draft = {};
        const open = days.filter((d) => !planned[d + '|dinner']);
        if (!open.length) {
          App.toast('Every dinner this week is already planned', 'error');
          return;
        }
        for (const d of open) {
          const r = pickFor(d, null);
          if (r) draft[d] = r;
        }
        if (!Object.keys(draft).length) {
          draftWrap.replaceChildren(h('div', { class: 'card', style: { marginTop: '14px' } },
            h('div', { class: 'empty-state', style: { padding: '20px 14px' } },
              h('div', { class: 'headline' }, 'Nothing fits those limits'),
              'Try raising the budget, allowing more time, or removing a diet filter.')));
          acceptBtn.style.display = 'none';
          return;
        }
        drawDraft();
      };

      const acceptBtn = h('button', {
        class: 'btn btn-primary', type: 'button', style: { display: 'none' },
        onclick: async () => {
          if (acceptBtn.disabled) return;
          acceptBtn.disabled = true;
          const entries2 = Object.entries(draft);
          let saved = 0;
          try {
            for (const [dateStr, r] of entries2) {
              await App.api('/api/plan', 'PUT', {
                date: dateStr, meal_type: 'dinner', recipe_id: r.id,
                cook_member_id: null,
                leftover_lunch: leftoverBox.checked,
              });
              saved++;
            }
            modal.close();
            App.toast(saved + ' dinner' + (saved === 1 ? '' : 's') + ' planned'
              + (leftoverBox.checked ? ' · leftover lunches queued' : '')
              + ' — assign cooks from the calendar');
            App.renderCurrent();
          } catch (err) {
            acceptBtn.disabled = false;
            App.toast(err.message + (saved ? ' — ' + saved + ' saved before the error' : ''), 'error');
          }
        },
      }, 'Accept & plan it');

      const modal = App.modal({
        title: 'Build my week',
        wide: true,
        body: h('div', {},
          h('p', { class: 'muted small', style: { marginTop: 0 } },
            'Drafts the next 7 dinners around your budget, time, and diet limits. '
            + 'You review every pick before anything is saved.'),
          h('div', { class: 'field-row', style: { alignItems: 'flex-end' } },
            h('div', { class: 'field', style: { marginBottom: 0 } },
              h('label', {}, 'Budget per person per day ($)'),
              h('div', { style: { display: 'flex', gap: '6px', alignItems: 'center' } },
                budgetInput,
                h('button', {
                  class: 'btn btn-sm', type: 'button',
                  onclick: () => { budgetInput.value = '5.00'; },
                }, '$5 strict'),
                h('button', {
                  class: 'btn btn-sm', type: 'button', title: 'No budget cap',
                  onclick: () => { budgetInput.value = ''; },
                }, 'No cap'))),
            h('div', { class: 'field', style: { marginBottom: 0 } },
              h('label', {}, 'Max cook time'), timeSelect)),
          h('div', { class: 'field', style: { marginTop: '12px' } },
            h('label', {}, 'Diet limits (from your Settings — tap to change)'), dietChips),
          h('label', { class: 'leftover-toggle', style: { marginTop: '4px' } },
            salesBox, h('span', {}, 'Favor this week’s sale items'
              + (saleNames.length ? '' : ' (none listed — add some on the Shopping tab)'))),
          h('label', { class: 'leftover-toggle', style: { marginTop: '8px' } },
            leftoverBox, h('span', {}, App.icon('repeat', 14), ' Each dinner also covers the next day’s lunch as leftovers')),
          h('div', { style: { display: 'flex', gap: '10px', marginTop: '14px', flexWrap: 'wrap' } },
            h('button', { class: 'btn btn-accent', type: 'button', onclick: generate },
              App.icon('shuffle', 15), 'Draft my week'),
            acceptBtn),
          draftWrap),
      });
    };

    /* ----- month grid ----- */

    const slotBtn = (dateStr, meal) => {
      const entry = byKey[dateStr + '|' + meal];
      const meta = App.MEAL_META[meal];
      if (!entry) {
        return h('button', {
          class: 'slot slot-empty',
          title: 'Plan ' + meta.label.toLowerCase(),
          onclick: () => openPicker(dateStr, meal),
        }, '+');
      }
      return h('button', {
        class: 'slot slot-' + meal + (entry.leftover ? ' is-leftover' : ''),
        title: (entry.leftover ? 'Leftovers — ' : '') + meta.label + ': ' + entry.recipe.name
          + (entry.cook ? ' — ' + entry.cook.name + ' cooks' : ''),
        onclick: () => openPicker(dateStr, meal),
      },
        entry.leftover ? App.icon('repeat', 11) : null,
        h('span', { class: 'slot-name' }, entry.recipe.name),
        entry.cook
          ? h('span', { class: 'cook-dot', style: { background: entry.cook.color }, title: entry.cook.name })
          : null,
        entry.cooked ? App.icon('check', 11) : null);
    };

    const cells = [];
    for (let d = first; d <= last; d = App.addDays(d, 1)) {
      const dateStr = App.fmtDate(d);
      cells.push(h('div', {
        class: 'day-cell'
          + (d.getMonth() !== month.getMonth() ? ' day-out' : '')
          + (dateStr === todayStr ? ' day-today' : '')
          + (dateStr === this.selectedDate ? ' day-selected' : ''),
        'data-date': dateStr,
      },
        h('button', {
          class: 'day-num', title: 'Focus this day',
          onclick: () => selectDay(dateStr),
        }, d.getDate()),
        // Hidden slot types (Settings) stay rendered when occupied, so
        // hiding breakfast never makes an already-planned meal vanish.
        App.MEAL_TYPES.filter((meal) => shownTypes.includes(meal) || byKey[dateStr + '|' + meal])
          .map((meal) => slotBtn(dateStr, meal))));
    }

    const DOW = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const grid = h('div', { class: 'month-grid' },
      DOW.slice(ws).concat(DOW.slice(0, ws)).map((dow) => h('div', { class: 'month-dow' }, dow)),
      cells);
    const gridWrap = h('div', { class: 'month-grid-wrap' }, grid);

    /* ----- mobile agenda (one full-width card per day of the month) ----- */

    const agendaSlot = (dateStr, meal) => {
      const entry = byKey[dateStr + '|' + meal];
      const meta = App.MEAL_META[meal];
      if (!entry) {
        return h('button', {
          class: 'agenda-slot agenda-slot-empty', onclick: () => openPicker(dateStr, meal),
        },
          h('span', { class: 'agenda-slot-label' }, meta.label),
          h('span', { class: 'muted small' }, '+ Add'));
      }
      return h('button', {
        class: 'agenda-slot slot-' + meal + (entry.leftover ? ' is-leftover' : ''),
        onclick: () => openPicker(dateStr, meal),
      },
        h('span', { class: 'agenda-slot-label' },
          entry.leftover ? App.icon('repeat', 12) : null, meta.label),
        h('span', { class: 'agenda-slot-recipe' },
          entry.leftover ? 'Leftovers: ' + entry.recipe.name : entry.recipe.name,
          entry.cook
            ? h('span', { class: 'cook-dot', style: { background: entry.cook.color }, title: entry.cook.name })
            : null,
          entry.cooked ? App.icon('check', 12) : null));
    };

    const agendaDays = [];
    for (let d = new Date(month); d <= monthEnd; d = App.addDays(d, 1)) {
      const dateStr = App.fmtDate(d);
      agendaDays.push(h('div', {
        class: 'agenda-day' + (dateStr === todayStr ? ' agenda-today' : '')
          + (dateStr === this.selectedDate ? ' day-selected' : ''),
        'data-date': dateStr,
      },
        h('button', {
          class: 'agenda-date', onclick: () => selectDay(dateStr),
        }, d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })),
        h('div', { class: 'agenda-slots' },
          App.MEAL_TYPES.filter((meal) => shownTypes.includes(meal) || byKey[dateStr + '|' + meal])
            .map((meal) => agendaSlot(dateStr, meal)))));
    }
    const agenda = h('div', { class: 'month-agenda' }, agendaDays);

    /* ----- header + legend ----- */

    const inMonth = entries.filter((e) => {
      const d = App.parseDate(e.date);
      return d.getMonth() === month.getMonth() && d.getFullYear() === month.getFullYear();
    });
    const cookedCount = inMonth.filter((e) => e.cooked).length;
    const sub = inMonth.length
      ? inMonth.length + ' meal' + (inMonth.length === 1 ? '' : 's') + ' planned'
        + (cookedCount ? ' · ' + cookedCount + ' cooked' : '')
      : 'Nothing planned yet — click any slot to get cooking';

    const legend = h('div', {
      class: 'card',
      style: { marginTop: '16px', display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap', padding: '12px 16px' },
    },
      shownTypes.map((mt) => App.mealTag(mt)),
      h('span', { style: { display: 'inline-flex', alignItems: 'center', gap: '6px' } },
        h('span', { class: 'cook-dot', style: { background: 'var(--tomato)' } }),
        h('span', { class: 'muted small' }, "= who's cooking")),
      h('span', { class: 'muted small' }, 'Tip: click any slot to plan it. Recommendations are ranked by time, nutrition, or cost.'));

    container.replaceChildren(
      h('div', { class: 'view-head' },
        h('div', {},
          h('div', { class: 'view-title' }, 'Meal Plan'),
          h('div', { class: 'view-sub' }, sub)),
        h('div', { class: 'view-actions' },
          h('button', { class: 'btn btn-accent', onclick: openBuilder },
            App.icon('shuffle', 15), 'Build my week'),
          h('div', { class: 'bold', style: { fontSize: '17px', minWidth: '160px', textAlign: 'center' } },
            App.monthLabel(month)),
          h('button', {
            class: 'btn btn-icon', title: 'Previous month',
            onclick: () => setMonth(new Date(month.getFullYear(), month.getMonth() - 1, 1)),
          }, App.icon('chevronLeft', 16)),
          h('button', {
            class: 'btn',
            onclick: () => { const t = App.today(); setMonth(new Date(t.getFullYear(), t.getMonth(), 1)); },
          }, 'Today'),
          h('button', {
            class: 'btn btn-icon', title: 'Next month',
            onclick: () => setMonth(new Date(month.getFullYear(), month.getMonth() + 1, 1)),
          }, App.icon('chevronRight', 16)),
          h('div', { style: { display: 'flex', flexDirection: 'column', gap: '3px', alignItems: 'flex-end' } },
            h('a', { class: 'btn', href: '/api/calendar/export.ics?start=' + startStr + '&end=' + endStr },
              App.icon('download', 15), 'Export to Google Calendar'),
            h('div', { class: 'muted small' }, 'Downloads an .ics file — import it at calendar.google.com')))),
      gridWrap,
      agenda,
      legend);

    // First-run onboarding hands off here: "Build my week" on the welcome
    // card sets this flag, we open the builder on arrival.
    try {
      if (sessionStorage.getItem('sr-open-builder')) {
        sessionStorage.removeItem('sr-open-builder');
        openBuilder();
      }
    } catch { /* private mode */ }
  },
});
