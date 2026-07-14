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

    /* ----- First-run welcome (set at registration, dismissed once) ----- */

    let welcome = false;
    try { welcome = localStorage.getItem('sr-welcome') === '1'; } catch { /* private mode */ }
    const dismissWelcome = () => {
      try { localStorage.removeItem('sr-welcome'); } catch { /* private mode */ }
      App.renderCurrent();
    };
    const welcomeCard = !welcome ? null : h('div', { class: 'card', style: { marginBottom: '16px' } },
      h('h3', {}, 'Welcome to Stay Ready 🥕'),
      h('p', { class: 'muted small' }, 'Two moves and dinner is handled for the week:'),
      h('div', { class: 'rowline' },
        h('div', { class: 'grow' },
          h('div', { class: 'bold' }, '1.  Get your housemates in'),
          h('div', { class: 'muted small' }, 'Everyone shares one plan, pantry, and grocery split.')),
        h('button', {
          class: 'btn btn-sm',
          onclick: () => {
            navigator.clipboard.writeText(App.state.user.invite_code)
              .then(() => App.toast('Invite code ' + App.state.user.invite_code + ' copied — text it to them'))
              .catch(() => App.toast('Your invite code: ' + App.state.user.invite_code, 'error'));
          },
        }, App.icon('copy', 14), 'Copy invite code')),
      h('div', { class: 'rowline' },
        h('div', { class: 'grow' },
          h('div', { class: 'bold' }, '2.  Let it plan your week'),
          h('div', { class: 'muted small' }, 'Pick a budget and max cook time — it drafts 7 dinners you can shuffle.')),
        h('button', {
          class: 'btn btn-accent btn-sm',
          onclick: () => {
            try { sessionStorage.setItem('sr-open-builder', '1'); } catch { /* private mode */ }
            dismissWelcome();
            App.navigate('plan');
          },
        }, App.icon('shuffle', 14), 'Build my week')),
      h('div', { class: 'rowline', style: { borderBottom: 'none', paddingBottom: 0 } },
        h('div', { class: 'grow muted small' },
          'Then the Shopping tab knows exactly what to buy.'),
        h('button', { class: 'btn btn-ghost btn-sm', onclick: dismissWelcome }, 'Got it')));

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
            style: { maxWidth: '100%' },
            title: App.MEAL_META[e.meal_type].label + ': ' + e.recipe.name,
          }, h('span', {
            class: 'truncate',
            style: { display: 'inline-block', maxWidth: '100%' },
          }, e.recipe.name))))));
    }

    const weekCard = h('div', { class: 'card' },
      h('h3', {}, 'Next 7 days'),
      weekRows.length ? weekRows : h('div', { class: 'empty-state' },
        h('div', { class: 'big' }, App.icon('calendar', 32)),
        h('div', { class: 'headline' }, 'The week is wide open'),
        h('div', {}, 'Nothing on the menu yet — ',
          h('a', { href: '#/plan', style: { color: 'var(--red)', fontWeight: '700' } }, 'plan some meals →'))));

    /* ----- Today's nutrition card ----- */

    const recipesById = {};
    recipes.forEach((r) => { recipesById[r.id] = r; });
    const todayList = plan.filter((e) => e.date === todayStr);
    const nut = App.dayNutrition(todayList, recipesById);
    const prefs = App.dietPrefs();

    const nutStat = (label, value, sub) => h('div', { class: 'stat' },
      h('div', { class: 'stat-label' }, label),
      h('div', { class: 'stat-value' }, value),
      sub ? h('div', { class: 'muted small' }, sub) : null);

    const fmtMg = (v) => (v ? Math.round(v) + 'mg' : '—');
    const fmtG = (v) => (v ? App.fmtQty(Math.round(v * 10) / 10) + 'g' : '—');

    const nutritionCard = h('div', { class: 'card' },
      h('h3', {}, "Today's nutrition"),
      h('div', { class: 'muted small', style: { marginTop: '2px', marginBottom: '10px' } },
        nut.meals
          ? 'Per person, across today’s ' + nut.meals + ' planned meal' + (nut.meals === 1 ? '' : 's') + ' (one serving each).'
          : 'Plan today’s meals and their combined nutrition shows up here.'),
      nut.meals ? h('div', {},
        h('div', { class: 'stat-row', style: { marginBottom: '8px' } },
          nutStat('Calories', nut.calories || '—'),
          nutStat('Protein', fmtG(nut.protein_g)),
          nutStat('Carbs', fmtG(nut.carbs_g),
            (nut.fiber_g || nut.sugar_g) ? fmtG(nut.fiber_g) + ' fiber · ' + fmtG(nut.sugar_g) + ' sugar' : null),
          nutStat('Fat', fmtG(nut.fat_g))),
        h('div', { class: 'stat-row', style: { marginBottom: '8px' } },
          nutStat('Sodium', fmtMg(nut.sodium_mg)),
          nutStat('Potassium', fmtMg(nut.potassium_mg)),
          nutStat('Phosphorus', fmtMg(nut.phosphorus_mg))),
        prefs.includes('kidney')
          ? h('div', { class: 'muted small', style: { marginBottom: '6px' } },
              'Common renal-diet daily targets are ~2,000mg sodium, ~2,000mg potassium, '
              + '~900mg phosphorus — yours may differ, so use the numbers your care team gave you.')
          : null,
        prefs.includes('diabetic')
          ? h('div', { class: 'muted small', style: { marginBottom: '6px' } },
              'Carb counts are per serving of each planned meal — handy for spotting heavy days, '
              + 'not a substitute for reading labels when dosing.')
          : null,
        h('div', { class: 'muted small' }, App.NUTRITION_DISCLAIMER)) : null);

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
      welcomeCard,
      h('div', { class: 'stat-row', style: { marginBottom: '16px' } },
        stat('Meals planned this week', plan.length, 'plan'),
        stat('Recipes in the box', recipes.length, 'recipes'),
        stat('Shopping items needed', ((shopping && shopping.items) || []).length, 'shopping')),
      h('div', { style: { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(330px, 1fr))', gap: '16px', marginBottom: '16px' } },
        todayCard, weekCard),
      h('div', { style: { marginBottom: '16px' } }, nutritionCard),
      picksCard);
  },
});
