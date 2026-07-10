/* Shopping List view: everything to buy for the planned meals in a date range,
   pantry already subtracted. Mark items bought to restock the pantry in place. */

App.registerView('shopping', {
  title: 'Shopping List',
  icon: 'cart',

  async render(container) {
    const range = {
      start: App.fmtDate(App.today()),
      end: App.fmtDate(App.addDays(App.today(), 29)), // next month of meal prep
    };
    let data = await App.api('/api/shopping?start=' + range.start + '&end=' + range.end);

    const statsWrap = h('div', { class: 'stat-row', style: { marginBottom: '18px' } });
    const budgetWrap = h('div', { style: { marginBottom: '18px' } });
    const listWrap = h('div', { class: 'shopping-list' });

    /* ---------- range controls ---------- */

    const startInput = h('input', {
      class: 'input', type: 'date', value: range.start, style: { width: 'auto' },
      onchange: (e) => { if (!e.target.value) return; range.start = e.target.value; load(); },
    });
    const endInput = h('input', {
      class: 'input', type: 'date', value: range.end, style: { width: 'auto' },
      onchange: (e) => { if (!e.target.value) return; range.end = e.target.value; load(); },
    });

    const load = async () => {
      listWrap.replaceChildren(h('div', { class: 'card' },
        h('div', { class: 'empty-state' }, App.spinner(), 'Building your list…')));
      try {
        data = await App.api('/api/shopping?start=' + range.start + '&end=' + range.end);
      } catch (err) {
        App.toast(err.message, 'error');
      }
      drawStats();
      drawBudget();
      drawList();
    };

    const setRange = (startDate, endDate) => {
      range.start = App.fmtDate(startDate);
      range.end = App.fmtDate(endDate);
      startInput.value = range.start;
      endInput.value = range.end;
      load();
    };

    const presets = [
      { label: 'Next 7 days', get: () => [App.today(), App.addDays(App.today(), 6)] },
      { label: 'Next 30 days', get: () => [App.today(), App.addDays(App.today(), 29)] },
      {
        label: 'This month',
        get: () => {
          const t = App.today();
          return [new Date(t.getFullYear(), t.getMonth(), 1),
            new Date(t.getFullYear(), t.getMonth() + 1, 0)];
        },
      },
    ];

    const rangeCard = h('div', { class: 'card shopping-range', style: { marginBottom: '18px' } },
      h('div', { class: 'field-row', style: { alignItems: 'flex-end', flexWrap: 'wrap' } },
        h('div', { class: 'field', style: { marginBottom: 0, flex: '0 0 auto' } },
          h('label', {}, 'From'), startInput),
        h('div', { class: 'field', style: { marginBottom: 0, flex: '0 0 auto' } },
          h('label', {}, 'To'), endInput),
        h('div', { class: 'field', style: { marginBottom: 0, flex: '1 1 auto' } },
          h('label', {}, 'Quick ranges'),
          h('div', { style: { display: 'flex', gap: '8px', flexWrap: 'wrap' } },
            presets.map((p) => h('button', {
              class: 'btn btn-sm',
              onclick: () => setRange(...p.get()),
            }, p.label))))));

    /* ---------- stats ---------- */

    const stat = (label, value) => h('div', { class: 'stat' },
      h('div', { class: 'stat-label' }, label),
      h('div', { class: 'stat-value' }, value));

    const drawStats = () => {
      statsWrap.replaceChildren(
        stat('Meals planned', data.meals_count),
        stat('Items to buy', data.items.filter((i) => !i.done).length),
        stat('Est. days covered', data.days));
    };

    /* ---------- cost & budget ---------- */

    const drawBudget = () => {
      if (!data.meals_count) { budgetWrap.replaceChildren(); return; }
      const est = data.estimated_cost || 0;
      const people = Math.max(data.members_count || 1, 1);
      const perPerson = est / people;
      const weekly = data.weekly_budget || 0;
      const weeks = Math.max((data.days || 7) / 7, 0.1);
      const budgetForRange = weekly * weeks;

      const line = (label, sub, value) => h('div', { class: 'rowline' },
        h('div', { class: 'grow' },
          h('div', { class: 'bold' }, label),
          h('div', { class: 'muted small' }, sub)),
        h('div', { class: 'bold', style: { fontSize: '18px', whiteSpace: 'nowrap' } }, value));

      let budgetBlock;
      if (weekly > 0) {
        const over = est > budgetForRange;
        const pct = budgetForRange > 0 ? Math.min(100, (est / budgetForRange) * 100) : 100;
        budgetBlock = h('div', { style: { marginTop: '10px' } },
          h('div', { style: { display: 'flex', justifyContent: 'space-between', gap: '10px', marginBottom: '6px', flexWrap: 'wrap' } },
            h('span', { class: 'bold', style: over ? { color: 'var(--red-deep)' } : {} },
              over ? 'Over budget' : 'Within budget'),
            h('span', { class: 'muted small' },
              App.fmtMoney(est) + ' of ' + App.fmtMoney(budgetForRange) +
              '  ·  ' + App.fmtMoney(weekly) + '/wk × ' + weeks.toFixed(1) + ' wk')),
          h('div', { class: 'money-bar' },
            h('div', { class: 'money-bar-fill' + (over ? ' over' : ''), style: { width: pct + '%' } })),
          over
            ? h('div', { class: 'small', style: { color: 'var(--red-deep)', marginTop: '7px', fontWeight: '700' } },
                'Over by ' + App.fmtMoney(est - budgetForRange) + ' — swap in cheaper dinners to get back under.')
            : null);
      } else {
        budgetBlock = h('div', { class: 'muted small', style: { marginTop: '8px' } },
          'No weekly budget set yet. ',
          h('a', { href: '#/household', style: { color: 'var(--red)', fontWeight: '700' } },
            'Set one on the Household page'),
          ' to track under/over.');
      }

      budgetWrap.replaceChildren(h('div', { class: 'card' },
        h('h3', {}, 'Cost & budget'),
        line('Estimated cost of planned meals',
          'Based on recipe costs for ' + data.meals_count + ' planned meal' + (data.meals_count === 1 ? '' : 's'),
          App.fmtMoney(est)),
        line("Each person's share", 'Split ' + people + ' way' + (people === 1 ? '' : 's'),
          App.fmtMoney(perPerson)),
        budgetBlock,
        h('div', { class: 'muted small', style: { marginTop: '12px' } },
          h('a', { href: '#/balance', style: { color: 'var(--red)', fontWeight: '700' } },
            'Track what you actually spent on the Balance tab →'))));
    };

    /* ---------- list ---------- */

    const markBought = async (item) => {
      if (item.done) return; // in-flight or already bought — ignore repeat clicks
      item.done = true; // optimistic — local state only, no full refetch
      drawStats();
      drawList();
      try {
        const res = await App.api('/api/shopping/purchase', 'POST', {
          name: item.name, quantity: item.to_buy, unit: item.unit, category: item.category,
        });
        App.toast(item.name + ' added to pantry', 'success', {
          label: 'Undo',
          onClick: async () => {
            try {
              if (res.created) {
                await App.api('/api/pantry/' + res.id, 'DELETE');
              } else {
                await App.api('/api/pantry/' + res.id, 'PUT', { quantity: res.previous_quantity });
              }
              item.done = false;
              drawStats();
              drawList();
              App.toast(item.name + ' — undone');
            } catch (err) { App.toast(err.message, 'error'); }
          },
        });
      } catch (err) {
        item.done = false;
        drawStats();
        drawList();
        App.toast(err.message, 'error');
      }
    };

    const itemRow = (item) => {
      const unitSuffix = item.unit ? ' ' + item.unit : '';
      return h('div', { class: 'rowline' + (item.done ? ' row-done' : '') },
        h('div', { class: 'grow' },
          h('div', { class: 'bold truncate item-name' }, item.name),
          item.recipes.length
            ? h('div', { class: 'muted small truncate' }, 'for: ' + item.recipes.join(', '))
            : null),
        item.done
          ? h('span', { class: 'chip chip-green' }, App.icon('check', 13), 'In pantry')
          : [
            h('span', { class: 'chip' }, 'need ' + App.fmtQty(item.needed) + unitSuffix),
            item.have > 0 ? h('span', { class: 'chip chip-green' }, 'have ' + App.fmtQty(item.have)) : null,
            h('span', { class: 'bold', style: { whiteSpace: 'nowrap' } },
              'buy ' + App.fmtQty(item.to_buy) + unitSuffix),
            h('button', { class: 'btn btn-sm btn-primary', onclick: () => markBought(item) }, 'Bought'),
          ]);
    };

    const drawList = () => {
      if (!data.meals_count) {
        listWrap.replaceChildren(h('div', { class: 'card' },
          h('div', { class: 'empty-state' },
            h('div', { class: 'big' }, App.icon('cart', 32)),
            h('div', { class: 'headline' }, 'Plan some meals first — your list builds itself.'),
            'Nothing is planned between ' + App.fmtHuman(range.start) + ' and ' + App.fmtHuman(range.end) + '.',
            h('div', { style: { marginTop: '14px' } },
              h('button', { class: 'btn btn-primary', onclick: () => App.navigate('plan') },
                'Go plan some meals')))));
        return;
      }
      if (!data.items.length) {
        listWrap.replaceChildren(h('div', { class: 'card' },
          h('div', { class: 'empty-state' },
            h('div', { class: 'big' }, App.icon('check', 32)),
            h('div', { class: 'headline' }, 'You have everything you need.'),
            'Your pantry already covers every ingredient for ' + data.meals_count +
              ' planned meal' + (data.meals_count === 1 ? '' : 's') + '.')));
        return;
      }
      const catOf = (i) => (App.PANTRY_CATEGORIES.includes(i.category) ? i.category : 'other');
      const groups = App.PANTRY_CATEGORIES
        .map((cat) => ({ cat, rows: data.items.filter((i) => catOf(i) === cat) }))
        .filter((g) => g.rows.length);
      listWrap.replaceChildren(...groups.map(({ cat, rows }) => {
        const meta = App.CATEGORY_META[cat];
        return h('div', { class: 'card', style: { marginBottom: '14px' } },
          h('h3', {}, meta.label + ' ', h('span', { class: 'chip' }, rows.length)),
          rows.map(itemRow));
      }));
    };

    /* ---------- assemble ---------- */

    container.replaceChildren(
      h('div', { class: 'view-head' },
        h('div', {},
          h('div', { class: 'view-title' }, 'Shopping List'),
          h('div', { class: 'view-sub' },
            "Everything you need to buy for the meals you've planned — your pantry is already subtracted.")),
        h('div', { class: 'view-actions' },
          h('button', { class: 'btn', onclick: () => window.print() }, App.icon('print', 15), 'Print'))),
      rangeCard,
      statsWrap,
      budgetWrap,
      listWrap);

    drawStats();
    drawBudget();
    drawList();
  },
});
