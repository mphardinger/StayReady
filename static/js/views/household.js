/* Household view: invite code + the members who can be assigned as cooks. */

App.registerView('household', {
  title: 'Household',
  icon: 'home',

  async render(container) {
    const [members, household] = await Promise.all([
      App.api('/api/members'),
      App.api('/api/household'),
    ]);
    const user = App.state.user;

    const memberRows = members.map((m) => h('div', { class: 'rowline' },
      h('span', { class: 'cook-dot', style: { background: m.color, width: '14px', height: '14px' } }),
      h('span', { class: 'grow bold' }, m.name),
      h('input', {
        type: 'color', value: m.color, title: 'Calendar color',
        style: { width: '34px', height: '28px', border: 'none', background: 'none', cursor: 'pointer' },
        onchange: async (e) => {
          try {
            await App.api('/api/members/' + m.id, 'PUT', { color: e.target.value });
            App.toast('Color updated');
            App.renderCurrent();
          } catch (err) { App.toast(err.message, 'error'); }
        },
      }),
      h('button', {
        class: 'btn btn-ghost btn-sm btn-icon', title: 'Rename',
        onclick: () => {
          const name = prompt('Rename ' + m.name + ' to:', m.name);
          if (!name || !name.trim()) return;
          App.api('/api/members/' + m.id, 'PUT', { name: name.trim() })
            .then(() => { App.toast('Renamed'); App.renderCurrent(); })
            .catch((err) => App.toast(err.message, 'error'));
        },
      }, App.icon('edit', 15)),
      h('button', {
        class: 'btn btn-danger btn-sm',
        onclick: () => {
          if (!confirm('Remove ' + m.name + '? Meals they were cooking stay planned, just without a cook.')) return;
          App.api('/api/members/' + m.id, 'DELETE')
            .then(() => { App.toast('Member removed'); App.renderCurrent(); })
            .catch((err) => App.toast(err.message, 'error'));
        },
      }, 'Remove')));

    const addForm = h('form', {
      class: 'field-row', style: { marginTop: '14px' },
      onsubmit: (e) => {
        e.preventDefault();
        const input = e.target.querySelector('input');
        const name = input.value.trim();
        if (!name) return;
        App.api('/api/members', 'POST', { name })
          .then(() => { App.toast('Added ' + name); App.renderCurrent(); })
          .catch((err) => App.toast(err.message, 'error'));
      },
    },
      h('input', { class: 'input', placeholder: 'Add a household member (they can be a cook)', maxlength: 40 }),
      h('button', { class: 'btn btn-primary', type: 'submit' }, '+ Add'));

    const budgetCard = h('div', { class: 'card', style: { marginBottom: '18px' } },
      h('h3', {}, 'Weekly grocery budget'),
      h('p', { class: 'muted small' },
        'Set a target and the shopping list shows whether your plan is under or over — and splits the cost across everyone.'),
      h('form', {
        onsubmit: async (e) => {
          e.preventDefault();
          const btn = e.target.querySelector('button[type="submit"]');
          if (btn.disabled) return;
          btn.disabled = true;
          const amount = e.target.querySelector('input').value;
          try {
            await App.api('/api/household', 'PUT', { weekly_budget: amount });
            App.toast('Weekly budget saved');
            App.renderCurrent();
          } catch (err) {
            btn.disabled = false;
            App.toast(err.message, 'error');
          }
        },
      },
        h('div', { class: 'field-row', style: { alignItems: 'flex-end', maxWidth: '360px' } },
          h('div', { class: 'field', style: { marginBottom: 0 } },
            h('label', {}, 'Amount per week ($)'),
            h('input', {
              class: 'input', type: 'number', step: 'any', min: 0,
              value: household.weekly_budget || 0, placeholder: '0',
            })),
          h('button', { class: 'btn btn-primary', type: 'submit' }, 'Save'))));

    container.replaceChildren(
      h('div', { class: 'view-head' },
        h('div', {},
          h('div', { class: 'view-title' }, user.household_name),
          h('div', { class: 'view-sub' }, 'Everyone in your household shares this pantry, recipe box, and meal plan.'))),

      h('div', { class: 'card', style: { marginBottom: '18px' } },
        h('h3', {}, 'Invite a housemate'),
        h('p', { class: 'muted small' }, 'They create an account with this code and land in your household:'),
        h('div', { style: { display: 'flex', gap: '10px', alignItems: 'center' } },
          h('span', {
            class: 'chip chip-green',
            style: { fontSize: '20px', padding: '8px 18px', letterSpacing: '3px' },
          }, user.invite_code),
          h('button', {
            class: 'btn btn-sm',
            onclick: () => {
              navigator.clipboard.writeText(user.invite_code)
                .then(() => App.toast('Invite code copied'))
                .catch(() => App.toast('Could not copy — code: ' + user.invite_code, 'error'));
            },
          }, App.icon('copy', 15), 'Copy'))),

      budgetCard,

      h('div', { class: 'card' },
        h('h3', {}, 'Members & cooks'),
        h('p', { class: 'muted small' }, 'Assign any of these people as the cook on a planned meal. Colors show up on the calendar.'),
        members.length ? memberRows : h('div', { class: 'empty-state' },
          h('div', { class: 'big' }, App.icon('users', 32)),
          h('div', { class: 'headline' }, 'No members yet'),
          'Add the people in your household below.'),
        addForm));
  },
});
