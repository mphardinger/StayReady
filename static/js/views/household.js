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

      h('div', { class: 'card', style: { marginBottom: '18px' } },
        h('h3', {}, 'Members & cooks'),
        h('p', { class: 'muted small' }, 'Assign any of these people as the cook on a planned meal. Colors show up on the calendar.'),
        members.length ? memberRows : h('div', { class: 'empty-state' },
          h('div', { class: 'big' }, App.icon('users', 32)),
          h('div', { class: 'headline' }, 'No members yet'),
          'Add the people in your household below.'),
        addForm),

      h('div', { class: 'card' },
        h('h3', {}, 'Account'),
        h('div', { class: 'rowline', style: { borderBottom: 'none', paddingBottom: '0' } },
          h('div', { class: 'grow' },
            h('div', { style: { fontWeight: '700' } }, user.display_name),
            h('div', { class: 'muted small' }, '@' + user.username)),
          h('button', { class: 'btn', onclick: () => App.logout() }, 'Sign out'),
          h('button', { class: 'btn', onclick: () => recoveryCodesModal() }, 'Recovery codes'),
          h('button', { class: 'btn btn-danger', onclick: () => deleteAccountModal() }, 'Delete account')),
        h('p', { class: 'muted small', style: { marginBottom: 0 } },
          h('a', { href: '/privacy', target: '_blank', style: { color: 'var(--red)', fontWeight: '700' } },
            'Privacy policy'),
          '  ·  Deleting your account is permanent.  If yours is the last account in the '
          + 'household, all household data is erased too.')));

    function recoveryCodesModal() {
      const pwInput = h('input', {
        class: 'input', type: 'password', autocomplete: 'current-password',
        placeholder: 'Your password',
      });
      const resultWrap = h('div', {});
      const genBtn = h('button', { class: 'btn btn-primary', style: { width: '100%', justifyContent: 'center' } },
        'Generate new codes');
      genBtn.onclick = async () => {
        if (genBtn.disabled) return;
        if (!pwInput.value) { App.toast('Enter your password first', 'error'); return; }
        genBtn.disabled = true;
        try {
          const res = await App.api('/api/auth/recovery_codes', 'POST', { password: pwInput.value });
          resultWrap.replaceChildren(
            h('div', {
              style: {
                display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px',
                fontFamily: 'Consolas, Menlo, monospace', fontWeight: '700',
                fontSize: '15px', letterSpacing: '1px', margin: '14px 0',
                padding: '14px', background: 'var(--bg-soft)', borderRadius: '10px',
              },
            }, res.recovery_codes.map((c) => h('div', {}, c))),
            h('button', {
              class: 'btn', style: { width: '100%', justifyContent: 'center' },
              onclick: () => {
                navigator.clipboard.writeText(res.recovery_codes.join('\n'))
                  .then(() => App.toast('Codes copied — paste them somewhere safe'))
                  .catch(() => App.toast('Could not copy — screenshot them instead', 'error'));
              },
            }, App.icon('copy', 15), 'Copy all'));
        } catch (err) {
          genBtn.disabled = false;
          App.toast(err.message, 'error');
        }
      };
      App.modal({
        title: 'Recovery codes',
        body: h('div', {},
          h('p', { class: 'muted small', style: { marginTop: 0 } },
            'Recovery codes are the only way back into your account if you forget your '
            + 'password (there is no email on file).  Generating a new set replaces ALL '
            + 'of your old codes — save the new ones before closing this.'),
          h('div', { class: 'field' },
            h('label', {}, 'Confirm with your password'),
            pwInput),
          genBtn,
          resultWrap),
      });
      pwInput.focus();
    }

    function deleteAccountModal() {
      const pwInput = h('input', {
        class: 'input', type: 'password', autocomplete: 'current-password',
        placeholder: 'Your password',
      });
      const confirmBtn = h('button', { class: 'btn btn-danger', style: { width: '100%', justifyContent: 'center' } },
        'Permanently delete my account');
      confirmBtn.onclick = async () => {
        if (confirmBtn.disabled) return;
        if (!pwInput.value) { App.toast('Enter your password to confirm', 'error'); return; }
        confirmBtn.disabled = true;
        try {
          const res = await App.api('/api/auth/delete_account', 'POST', { password: pwInput.value });
          modal.close();
          App.state.user = null;
          App.renderAuth();
          App.toast(res.household_deleted
            ? 'Account and household data deleted.  Take care.'
            : 'Account deleted.  Your housemates keep the household.');
        } catch (err) {
          confirmBtn.disabled = false;
          App.toast(err.message, 'error');
        }
      };
      const modal = App.modal({
        title: 'Delete account',
        body: h('div', {},
          h('p', {}, 'This permanently deletes your login.  There is no undo.'),
          h('p', { class: 'muted small' },
            'If you are the last account in this household, every recipe, planned meal, '
            + 'pantry item, and expense record is erased with it.  If housemates remain, '
            + 'the shared household stays with them.'),
          h('div', { class: 'field' },
            h('label', {}, 'Confirm with your password'),
            pwInput),
          confirmBtn),
      });
      pwInput.focus();
    }
  },
});
