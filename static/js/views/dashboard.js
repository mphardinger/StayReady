/* Dashboard ("Today") view — the landing page. Greets the cook, shows today's
   three meal slots, the week ahead at a glance, and smart recipe picks. */

App.registerView('dashboard', {
  title: 'Today',
  icon: 'today',

  async render(container) {
    const t = App.today();
    const todayStr = App.fmtDate(t);
    const [plan, recipes, shopping] = await Promise.all([
      App.api('/api/plan?start=' + todayStr + '&end=' + App.fmtDate(App.addDays(t, 6))),
      App.api('/api/recipes'),
      App.api('/api/shopping?start=' + todayStr + '&end=' + App.fmtDate(App.addDays(t, 29))),
    ]);

    const hour = new Date().getHours();
    const daypart = hour < 12 ? 'morning' : hour < 18 ? 'afternoon' : 'evening';
    const dateLine = new Date().toLocaleDateString(undefined,
      { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    /* ----- Today card ----- */

    const todayEntries = {};
    plan.filter((e) => e.date === todayStr).forEach((e) => { todayEntries[e.meal_type] = e; });

    const markCooked = async (entry) => {
      try {
        const res = await App.api('/api/plan/' + entry.id + '/cooked', 'POST');
        const n = ((res && res.deducted) || []).length;
        App.toast(n
          ? 'Marked cooked — used up ' + n + ' pantry item' + (n === 1 ? '' : 's')
          : 'Marked cooked');
        App.renderCurrent();
      } catch (err) { App.toast(err.message, 'error'); }
    };

    const mealRow = (mt) => {
      const meta = App.MEAL_META[mt];
      const entry = todayEntries[mt];
      return h('div', { class: 'rowline' },
        h('span', { class: 'chip tag-' + mt, style: { width: '96px', justifyContent: 'center', flexShrink: 0 } },
          meta.label),
        entry
          ? h('div', { class: 'grow' },
              h('div', { class: 'bold truncate' }, entry.recipe.name),
              h('div', { class: 'muted small' }, App.fmtMinutes(entry.recipe.time_minutes)))
          : h('div', { class: 'grow muted' }, 'Nothing planned'),
        entry && entry.cook
          ? h('span', { class: 'chip' },
              h('span', { class: 'cook-dot', style: { background: entry.cook.color } }),
              entry.cook.name)
          : null,
        entry
          ? (entry.cooked
              ? h('span', { class: 'chip chip-green' }, App.icon('check', 13), 'Cooked')
              : h('button', { class: 'btn btn-primary btn-sm', onclick: () => markCooked(entry) }, 'Mark cooked'))
          : h('a', { class: 'btn btn-ghost btn-sm', href: '#/plan' }, '+ Plan it'));
    };

    const todayCard = h('div', { class: 'card' },
      h('h3', {}, "Today's meals"),
      // Slot types hidden in Settings still show when something is planned.
      App.MEAL_TYPES.filter((mt) => App.visibleMealTypes().includes(mt) || todayEntries[mt])
        .map(mealRow));

    /* ----- Next 7 days card ----- */

    const weekRows = [];
    for (let i = 1; i <= 6; i++) {
      const ds = App.fmtDate(App.addDays(t, i));
      const dayEntries = plan.filter((e) => e.date === ds)
        .sort((a, b) => App.MEAL_TYPES.indexOf(a.meal_type) - App.MEAL_TYPES.indexOf(b.meal_type));
      if (!dayEntries.length) continue;
      weekRows.push(h('div', { class: 'rowline' },
        h('div', { class: 'bold small', style: { width: '92px', flexShrink: 0 } }, App.fmtHuman(ds)),
        h('div', { class: 'grow', style: { display: 'flex', flexWrap: 'wrap', gap: '6px' } },
          dayEntries.map((e) => h('span', {
            class: 'chip tag-' + e.meal_type,
            title: App.MEAL_META[e.meal_type].label,
          }, e.recipe.name)))));
    }

    const weekCard = h('div', { class: 'card' },
      h('h3', {}, 'Next 7 days'),
      weekRows.length ? weekRows : h('div', { class: 'empty-state' },
        h('div', { class: 'big' }, App.icon('calendar', 32)),
        h('div', { class: 'headline' }, 'The week is wide open'),
        h('div', {}, 'Nothing on the menu yet — ',
          h('a', { href: '#/plan', style: { color: 'var(--red)', fontWeight: '700' } }, 'plan some meals →'))));

    /* ----- Smart picks card ----- */

    const pickSection = (cat) => h('div', {},
      h('div', { class: 'bold small', style: { marginBottom: '4px' } }, cat.label),
      App.recommend(recipes, cat.key, null, 2).map((r) => h('div', { class: 'rowline' },
        h('div', { class: 'grow truncate' }, r.name),
        App.statChip(cat.key, r))));

    const picksCard = h('div', { class: 'card' },
      h('h3', {}, 'Smart picks'),
      h('div', { class: 'muted small', style: { marginTop: '2px', marginBottom: '10px' } },
        'Ranked by time to make, nutrition, and cost.'),
      recipes.length
        ? h('div', { style: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))', gap: '16px' } },
            App.REC_CATS.map(pickSection))
        : h('div', { class: 'empty-state' },
            h('div', { class: 'big' }, App.icon('book', 32)),
            h('div', { class: 'headline' }, 'No recipes yet'),
            h('div', {}, 'Fill your ',
              h('a', { href: '#/recipes', style: { color: 'var(--red)', fontWeight: '700' } }, 'recipe box'),
              ' and top picks will show up here.')));

    /* ----- Stat row ----- */

    const stat = (label, value, view) => h('div', {
      class: 'stat',
      style: { cursor: 'pointer' },
      onclick: () => App.navigate(view),
    },
      h('div', { class: 'stat-label' }, label),
      h('div', { class: 'stat-value' }, value));

    container.replaceChildren(
      h('div', { class: 'view-head' },
        h('div', {},
          h('div', { class: 'view-title' },
            'Good ' + daypart + ', ' + App.state.user.display_name + '.'),
          h('div', { class: 'view-sub' }, dateLine)),
        h('div', { class: 'view-actions' },
          h('a', {
            class: 'btn btn-sm', href: '/api/calendar/export.ics',
            title: 'Download your meal plan (.ics) for Google Calendar',
          }, App.icon('download', 15), 'Export to calendar'))),
      h('div', { class: 'stat-row', style: { marginBottom: '16px' } },
        stat('Meals planned this week', plan.length, 'plan'),
        stat('Recipes in the box', recipes.length, 'recipes'),
        stat('Shopping items needed', ((shopping && shopping.items) || []).length, 'shopping')),
      h('div', { style: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(330px, 1fr))', gap: '16px', marginBottom: '16px' } },
        todayCard, weekCard),
      picksCard);
  },
});
