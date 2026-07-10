/* Balance view: what the meal plan costs, grocery spending over time, and who
   owes what. The money home for a household splitting groceries. */

App.registerView('balance', {
  title: 'Balance',
  icon: 'cost',
  period: null, // 'week' | 'month'

  async render(container) {
    if (!this.period) this.period = 'month';
    const t = App.today();
    const range = periodRange(this.period, t);
    const data = await App.api('/api/balance?start=' + range.start + '&end=' + range.end);
    const p = data.period;
    const money = App.fmtMoney;

    /* ---------- 1. Meal plan cost (the headline) ---------- */

    const weekly = data.weekly_budget || 0;
    const overBudget = weekly > 0 && p.meal_plan_cost > p.budget_for_period;
    const pct = (weekly > 0 && p.budget_for_period > 0)
      ? Math.min(100, (p.meal_plan_cost / p.budget_for_period) * 100) : 0;

    const budgetBlock = weekly > 0
      ? h('div', { style: { marginTop: '12px' } },
          h('div', { style: { display: 'flex', justifyContent: 'space-between', gap: '10px', marginBottom: '6px', flexWrap: 'wrap' } },
            h('span', { class: 'bold', style: overBudget ? { color: 'var(--red-deep)' } : {} },
              overBudget ? 'Over budget' : 'Within budget'),
            h('span', { class: 'muted small' },
              money(p.meal_plan_cost) + ' of ' + money(p.budget_for_period) + ' budget')),
          h('div', { class: 'money-bar' },
            h('div', { class: 'money-bar-fill' + (overBudget ? ' over' : ''), style: { width: pct + '%' } })),
          overBudget
            ? h('div', { class: 'small', style: { color: 'var(--red-deep)', marginTop: '7px', fontWeight: '700' } },
                'Over by ' + money(p.meal_plan_cost - p.budget_for_period) + ' — swap in cheaper dinners.')
            : null)
      : h('div', { class: 'muted small', style: { marginTop: '10px' } },
          'No weekly budget set. ',
          h('a', { href: '#/household', style: { color: 'var(--red)', fontWeight: '700' } }, 'Set one on Household'),
          ' to track under/over.');

    const costCard = h('div', { class: 'card balance-hero' },
      h('div', { class: 'muted small bold', style: { textTransform: 'uppercase', letterSpacing: '0.5px' } },
        'Meal plan cost · ' + range.label),
      h('div', { class: 'balance-big' }, money(p.meal_plan_cost)),
      h('div', { class: 'muted small' },
        p.meal_plan_cost > 0
          ? money(p.per_person_meal_share) + ' per person (÷ ' + data.members_count + ')  ·  '
          : '',
        h('a', { href: '#/shopping', style: { color: 'var(--red)', fontWeight: '700' } }, 'See the shopping list')),
      p.groceries_spent > 0
        ? h('div', { class: 'muted small', style: { marginTop: '4px' } },
            'You actually logged ' + money(p.groceries_spent) + ' in grocery trips this ' + this.period + '.')
        : null,
      budgetBlock);

    /* ---------- 2. Who owes what ---------- */

    let owesCard;
    if (data.members_count < 2) {
      owesCard = h('div', { class: 'card' },
        h('h3', {}, 'Who owes what'),
        h('div', { class: 'muted small' },
          'Add your roommates on the ',
          h('a', { href: '#/household', style: { color: 'var(--red)', fontWeight: '700' } }, 'Household page'),
          ' to split grocery costs and see who owes whom.'));
    } else {
      const anySpend = data.balances.some((b) => b.paid > 0);
      const anyOwing = data.balances.some((b) => Math.abs(b.net) > 0.005);
      const settleBtn = h('button', { class: 'btn btn-sm', onclick: () => settleUp() }, App.icon('check', 14), 'Settle up');
      const settleUp = async () => {
        if (settleBtn.disabled) return;
        if (!confirm('Mark everyone as paid up? This resets balances to zero — your spending history and chart stay.')) return;
        settleBtn.disabled = true;
        try {
          await App.api('/api/expenses/settle', 'POST');
          App.toast('Settled up — balances reset');
          App.renderCurrent();
        } catch (err) {
          settleBtn.disabled = false;
          App.toast(err.message, 'error');
        }
      };
      owesCard = h('div', { class: 'card' },
        h('div', { style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '8px', flexWrap: 'wrap' } },
          h('h3', {}, 'Who owes what'),
          anyOwing ? settleBtn : null),
        h('div', { class: 'muted small', style: { margin: '2px 0 4px' } },
          anySpend ? 'Across unsettled grocery trips, split evenly.' : 'Log a grocery trip below and balances show up here.'),
        data.balances.map((b) => {
          let statusText, statusColor;
          if (b.net > 0.005) { statusText = 'gets back ' + money(b.net); statusColor = 'var(--ink)'; }
          else if (b.net < -0.005) { statusText = 'owes ' + money(-b.net); statusColor = 'var(--red-deep)'; }
          else { statusText = 'all square'; statusColor = 'var(--ink-soft)'; }
          return h('div', { class: 'rowline' },
            h('span', { class: 'cook-dot', style: { background: b.color, width: '13px', height: '13px' } }),
            h('div', { class: 'grow' },
              h('span', { class: 'bold' }, b.name),
              h('span', { class: 'muted small', style: { marginLeft: '8px' } }, 'paid ' + money(b.paid))),
            h('span', { class: 'bold', style: { color: statusColor, whiteSpace: 'nowrap' } }, statusText));
        }));
    }

    /* ---------- 3. Spending over time ---------- */

    const maxSpend = Math.max(1, ...data.weekly_spending.map((w) => w.total));
    const spendCard = h('div', { class: 'card' },
      h('h3', {}, 'Spending over time'),
      h('div', { class: 'muted small', style: { marginBottom: '12px' } }, 'Grocery money logged, by week (last 8 weeks).'),
      h('div', { class: 'spend-chart' }, data.weekly_spending.map((w) => {
        const ws = App.parseDate(w.week_start);
        const label = (ws.getMonth() + 1) + '/' + ws.getDate();
        return h('div', { class: 'spend-col', title: money(w.total) + ' week of ' + label },
          h('div', { class: 'spend-val' }, w.total > 0 ? money(w.total) : ''),
          h('div', { class: 'spend-bar', style: { height: (w.total / maxSpend * 100) + '%' } }),
          h('div', { class: 'spend-lbl' }, label));
      })));

    /* ---------- 4. Log a grocery trip ---------- */

    const logForm = h('form', {
      onsubmit: async (e) => {
        e.preventDefault();
        const btn = e.target.querySelector('button[type="submit"]');
        if (btn.disabled) return;
        const fd = Object.fromEntries(new FormData(e.target).entries());
        if (!fd.amount) {
          App.toast('Enter an amount to log the trip.', 'error');
          return;
        }
        btn.disabled = true;
        try {
          await App.api('/api/expenses', 'POST', fd);
          App.toast('Logged ' + App.fmtMoney(fd.amount));
          App.renderCurrent();
        } catch (err) {
          btn.disabled = false;
          App.toast(err.message, 'error');
        }
      },
    },
      h('div', { class: 'field-row', style: { alignItems: 'flex-end', flexWrap: 'wrap' } },
        h('div', { class: 'field', style: { marginBottom: 0 } },
          h('label', {}, 'Date'),
          h('input', { class: 'input', name: 'date', type: 'date', value: App.fmtDate(t) })),
        h('div', { class: 'field', style: { marginBottom: 0 } },
          h('label', {}, 'Amount ($)'),
          h('input', { class: 'input', name: 'amount', type: 'number', step: 'any', min: 0, placeholder: '0.00', required: true })),
        h('div', { class: 'field', style: { marginBottom: 0 } },
          h('label', {}, 'Who paid?'),
          h('select', { class: 'select', name: 'paid_by' },
            h('option', { value: '' }, '— nobody / shared —'),
            data.members.map((m) => h('option', { value: m.id }, m.name)))),
        h('div', { class: 'field', style: { marginBottom: 0, flex: 2 } },
          h('label', {}, 'Note (optional)'),
          h('input', { class: 'input', name: 'note', maxlength: 120, placeholder: 'e.g. Costco run' })),
        h('button', { class: 'btn btn-primary', type: 'submit', style: { marginBottom: 0 } }, 'Log trip')));

    const tripRow = (ex) => h('div', { class: 'rowline' },
      h('div', { class: 'grow' },
        h('span', { class: 'bold' }, App.fmtMoney(ex.amount)),
        ex.note ? h('span', { class: 'muted small', style: { marginLeft: '8px' } }, ex.note) : null),
      h('span', { class: 'muted small' },
        App.fmtHuman(ex.date) + (ex.paid_by_name ? '  ·  ' + ex.paid_by_name : '')),
      h('button', {
        class: 'btn btn-ghost btn-sm btn-icon', title: 'Delete',
        onclick: (e) => {
          const btn = e.currentTarget;
          if (btn.disabled) return;
          btn.disabled = true;
          App.api('/api/expenses/' + ex.id, 'DELETE')
            .then(() => { App.toast('Trip deleted'); App.renderCurrent(); })
            .catch((err) => { btn.disabled = false; App.toast(err.message, 'error'); });
        },
      }, App.icon('trash', 15)));

    const logCard = h('div', { class: 'card' },
      h('h3', {}, 'Grocery trips'),
      h('div', { class: 'muted small', style: { marginBottom: '12px' } },
        'Log what you actually spent so balances and spending stay accurate.'),
      logForm,
      data.expenses.length
        ? h('div', { style: { marginTop: '8px' } }, data.expenses.map(tripRow))
        : h('div', { class: 'muted small', style: { marginTop: '12px' } }, 'No grocery trips logged yet.'));

    /* ---------- header + assemble ---------- */

    const periodTab = (key, label) => h('button', {
      class: this.period === key ? 'active' : '',
      onclick: () => { this.period = key; App.renderCurrent(); },
    }, label);

    container.replaceChildren(
      h('div', { class: 'view-head' },
        h('div', {},
          h('div', { class: 'view-title' }, 'Balance'),
          h('div', { class: 'view-sub' }, "What your meal plan costs, and who's paid for what.")),
        h('div', { class: 'view-actions' },
          h('div', { class: 'tabs' }, periodTab('week', 'This week'), periodTab('month', 'This month')))),
      costCard,
      h('div', { class: 'balance-grid' }, owesCard, spendCard),
      logCard);
  },
});

/* Sunday-start week or calendar month containing `t`. Returns {start,end,label}. */
function periodRange(period, t) {
  if (period === 'week') {
    const start = App.addDays(t, -t.getDay());
    const end = App.addDays(start, 6);
    return { start: App.fmtDate(start), end: App.fmtDate(end), label: 'this week' };
  }
  const start = new Date(t.getFullYear(), t.getMonth(), 1);
  const end = new Date(t.getFullYear(), t.getMonth() + 1, 0);
  return { start: App.fmtDate(start), end: App.fmtDate(end), label: App.monthLabel(t) };
}
