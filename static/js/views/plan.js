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

    const [entries, recipes, members] = await Promise.all([
      App.api('/api/plan?start=' + startStr + '&end=' + endStr),
      App.api('/api/recipes'),
      App.api('/api/members'),
    ]);
    const byKey = {};
    entries.forEach((e) => { byKey[e.date + '|' + e.meal_type] = e; });
    const shownTypes = App.visibleMealTypes();

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

      const saveBtn = h('button', {
        class: 'btn btn-primary', disabled: !selectedId, onclick: () => save(),
      }, 'Save meal');

      // "Suggest one" — picks a recipe biased toward the quick/cheap/healthy
      // recommendations for this slot, so a busy user can accept or shuffle.
      const suggestBtn = h('button', {
        class: 'btn suggest-btn', type: 'button',
        onclick: () => {
          const pool = [...new Set([
            ...App.recommend(recipes, 'time', meal, 5),
            ...App.recommend(recipes, 'cost', meal, 5),
            ...App.recommend(recipes, 'nutrition', meal, 5),
          ])].filter((r) => r.id !== selectedId);
          const src = pool.length ? pool : matching.filter((r) => r.id !== selectedId);
          if (!src.length) {
            App.toast('No other recipes for this meal yet — add more in Recipes.', 'error');
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
            h('span', {
              class: 'chip' + (r.ingredient_count > 0 && r.have_count === r.ingredient_count ? ' chip-green' : ''),
            }, 'have ' + r.have_count + '/' + r.ingredient_count))));

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

      const drawRows = () => {
        searchInput.style.display = tab === 'all' ? '' : 'none';
        let list;
        if (tab === 'all') {
          const q = search.trim().toLowerCase();
          list = matching.filter((r) => r.name.toLowerCase().includes(q));
        } else {
          list = App.recommend(recipes, tab, meal, 6);
        }
        if (!list.length) {
          listWrap.replaceChildren(h('div', { class: 'empty-state', style: { padding: '28px 16px' } },
            h('div', { class: 'big' }, App.icon('book', 30)),
            h('div', { class: 'headline' }, matching.length ? 'Nothing matches' : 'No recipes for this meal yet'),
            matching.length ? 'Try a different search.' : 'Add a few in the Recipes tab, then come plan them here.'));
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
  },
});
