/* Settings — per-device preferences. Theme, accent, and planning options live
   in localStorage (see the App.applyTheme / pref helpers), so each housemate's
   phone keeps its own setup without touching shared household data. */

App.registerView('settings', {
  title: 'Settings',
  icon: 'sliders',

  async render(container) {
    const rerender = () => App.renderCurrent();

    /* ----- Appearance: theme + accent ----- */

    const themeBtn = (value, label) => h('button', {
      class: 'btn' + (App.themeSetting() === value ? ' btn-primary' : ''),
      onclick: () => { App.applyTheme(value); rerender(); },
    }, label);

    const accentBtn = (key, def) => h('button', {
      class: 'accent-swatch' + (App.accentSetting() === key ? ' active' : ''),
      title: def.label,
      'aria-label': def.label + ' accent',
      style: { background: def.swatch },
      onclick: () => { App.applyAccent(key); rerender(); },
    }, App.accentSetting() === key ? App.icon('check', 15) : null);

    const themeCard = h('div', { class: 'card', style: { marginBottom: '18px' } },
      h('h3', {}, 'Appearance'),
      h('p', { class: 'muted small' }, '"System" follows your phone’s light/dark setting.'),
      h('div', { style: { display: 'flex', gap: '10px', flexWrap: 'wrap' } },
        themeBtn('system', 'System'),
        themeBtn('light', 'Light'),
        themeBtn('dark', 'Dark')),
      h('p', { class: 'muted small', style: { marginTop: '16px', marginBottom: '8px' } }, 'Accent color'),
      h('div', { style: { display: 'flex', gap: '12px', flexWrap: 'wrap' } },
        Object.entries(App.ACCENTS).map(([key, def]) => accentBtn(key, def))));

    /* ----- Calendar ----- */

    const weekBtn = (value, label) => h('button', {
      class: 'btn' + (App.weekStart() === value ? ' btn-primary' : ''),
      onclick: () => { App.setWeekStart(value); rerender(); },
    }, label);

    const leftoverToggle = h('label', { class: 'leftover-toggle', style: { marginTop: '14px' } },
      h('input', {
        type: 'checkbox',
        checked: App.leftoverDefault(),
        onchange: (e) => { App.setLeftoverDefault(e.target.checked); },
      }),
      h('span', {}, App.icon('repeat', 14),
        ' Suggest saving dinner leftovers as tomorrow’s lunch'));

    const calendarCard = h('div', { class: 'card', style: { marginBottom: '18px' } },
      h('h3', {}, 'Calendar'),
      h('p', { class: 'muted small' }, 'Week starts on'),
      h('div', { style: { display: 'flex', gap: '10px' } },
        weekBtn(0, 'Sunday'),
        weekBtn(1, 'Monday')),
      leftoverToggle);

    /* ----- Meals to plan ----- */

    const prefs = App.slotPrefs();
    const slotToggle = (mt) => h('label', { class: 'leftover-toggle', style: { marginTop: '10px' } },
      h('input', {
        type: 'checkbox',
        checked: prefs[mt],
        onchange: (e) => {
          const next = Object.assign({}, App.slotPrefs(), { [mt]: e.target.checked });
          if (!App.MEAL_TYPES.some((t) => next[t])) {
            App.toast('Keep at least one meal type visible', 'error');
            rerender();
            return;
          }
          App.setSlotPref(mt, e.target.checked);
          rerender();
        },
      }),
      h('span', {}, 'Plan ' + ({ breakfast: 'breakfasts', lunch: 'lunches', dinner: 'dinners' })[mt]));

    const slotsCard = h('div', { class: 'card', style: { marginBottom: '18px' } },
      h('h3', {}, 'Meals to plan'),
      h('p', { class: 'muted small' },
        'Pick which meals you actually plan. Cook dinners and eat leftovers for lunch? '
        + 'Turn breakfast off and the calendar gets that much simpler. '
        + 'Anything already planned in a hidden slot stays visible.'),
      App.MEAL_TYPES.map(slotToggle));

    /* ----- Dietary focus ----- */

    const dietToggle = (slug) => {
      const meta = App.DIETS[slug];
      const active = App.dietPrefs().includes(slug);
      return h('label', { class: 'leftover-toggle', style: { marginTop: '10px' } },
        h('input', {
          type: 'checkbox',
          checked: active,
          onchange: (e) => {
            const prefs = App.dietPrefs().filter((d) => d !== slug);
            if (e.target.checked) prefs.push(slug);
            App.setDietPrefs(prefs);
            rerender();
          },
        }),
        h('span', {}, meta.label,
          h('span', { class: 'muted small', style: { display: 'block', fontWeight: 400 } }, meta.explain)));
    };

    const dietCard = h('div', { class: 'card', style: { marginBottom: '18px' } },
      h('h3', {}, 'Dietary focus'),
      h('p', { class: 'muted small' },
        'Pre-selects these filters in the recipe box, the meal picker, and the week builder, '
        + 'and shows the numbers that matter to you on recipes and the Today page.'),
      Object.keys(App.DIETS).map(dietToggle),
      h('p', { class: 'muted small', style: { marginTop: '14px', marginBottom: 0 } },
        App.NUTRITION_DISCLAIMER));

    /* ----- About ----- */

    const aboutCard = h('div', { class: 'card' },
      h('h3', {}, 'About these settings'),
      h('p', { class: 'muted small', style: { margin: 0 } },
        'Saved on this device only — each housemate’s phone keeps its own preferences. '
        + 'Household-wide things (members, budget, invite code) live under House.'));

    container.replaceChildren(
      h('div', { class: 'view-head' },
        h('div', {},
          h('div', { class: 'view-title' }, 'Settings'),
          h('div', { class: 'view-sub' }, 'Make Stay Ready fit how you actually cook.'))),
      themeCard,
      dietCard,
      calendarCard,
      slotsCard,
      aboutCard);
  },
});
