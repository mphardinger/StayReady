/* Sign in / create account / reset password screen (not a nav view — rendered
   full screen). New accounts see their recovery codes ONCE before entering. */

App.renderAuth = function renderAuth() {
  let mode = 'login';          // 'login' | 'register' | 'reset'
  let joinMode = 'create';     // 'create' | 'join'
  let error = '';

  const root = document.getElementById('app');

  function finish(res) {
    App.state.user = res.user;
    location.hash = '#/dashboard';
    App.renderShell();
    App.toast('Welcome, ' + res.user.display_name + '.');
  }

  /* One-time recovery-codes screen after signup. The codes exist in this
     response only — they are never shown again. */
  function showCodes(res) {
    const codes = res.recovery_codes;
    const copyBtn = h('button', {
      class: 'btn',
      onclick: () => {
        navigator.clipboard.writeText(codes.join('\n'))
          .then(() => App.toast('Codes copied — paste them somewhere safe'))
          .catch(() => App.toast('Could not copy — screenshot them instead', 'error'));
      },
    }, App.icon('copy', 15), 'Copy all');

    root.replaceChildren(
      h('div', { class: 'auth-wrap' },
        h('div', { class: 'auth-card' },
          h('div', { class: 'auth-form', style: { maxWidth: '460px', margin: '0 auto' } },
            h('h2', {}, 'Save your recovery codes'),
            h('p', { class: 'muted small' },
              'Stay Ready never asks for an email, so these codes are the ONLY way back '
              + 'into your account if you forget your password.  Screenshot them or copy '
              + 'them somewhere safe.  Each code works once.'),
            h('div', {
              style: {
                display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px',
                fontFamily: 'Consolas, Menlo, monospace', fontWeight: '700',
                fontSize: '15px', letterSpacing: '1px', margin: '16px 0',
                padding: '14px', background: 'var(--bg-soft)', borderRadius: '10px',
              },
            }, codes.map((c) => h('div', {}, c))),
            h('div', { style: { display: 'flex', gap: '10px', flexWrap: 'wrap' } },
              copyBtn,
              h('button', {
                class: 'btn btn-primary', style: { flex: '1', justifyContent: 'center' },
                onclick: () => finish(res),
              }, "I saved them — let's cook"))))));
  }

  function submit(form) {
    error = '';
    const data = Object.fromEntries(new FormData(form).entries());
    const fail = (err) => { error = err.message; draw(); };
    if (mode === 'login') {
      App.api('/api/auth/login', 'POST', data).then(finish).catch(fail);
    } else if (mode === 'reset') {
      App.api('/api/auth/reset_password', 'POST', data).then((res) => {
        App.toast('Password reset — ' + res.codes_left + ' recovery code'
          + (res.codes_left === 1 ? '' : 's') + ' left.  Make new ones from the House tab.');
        finish(res);
      }).catch(fail);
    } else {
      if (joinMode === 'create') delete data.invite_code;
      else delete data.household_name;
      App.api('/api/auth/register', 'POST', data).then((res) => {
        try { localStorage.setItem('sr-welcome', '1'); } catch { /* private mode */ }
        showCodes(res);
      }).catch(fail);
    }
  }

  function draw() {
    const isLogin = mode === 'login';
    const isReset = mode === 'reset';

    // Preserve whatever the user already typed across redraws (error/toggle re-renders).
    const prev = {};
    root.querySelectorAll('input[name]').forEach((i) => { prev[i.name] = i.value; });

    const fields = [];
    if (mode === 'register') {
      fields.push(
        h('div', { class: 'field' },
          h('label', {}, 'Your name'),
          h('input', { class: 'input', name: 'display_name', placeholder: 'e.g. Matt', required: true, maxlength: 40, value: prev.display_name || '' })));
    }
    fields.push(
      h('div', { class: 'field' },
        h('label', {}, 'Username'),
        h('input', { class: 'input', name: 'username', placeholder: 'username', required: true, autocomplete: 'username', maxlength: 40, value: prev.username || '' })));

    if (isReset) {
      fields.push(
        h('div', { class: 'field' },
          h('label', {}, 'One of your recovery codes'),
          h('input', { class: 'input', name: 'code', placeholder: 'XXXX-XXXX', required: true, maxlength: 12, style: { textTransform: 'uppercase' }, value: prev.code || '' })),
        h('div', { class: 'field' },
          h('label', {}, 'New password'),
          h('input', { class: 'input', name: 'new_password', type: 'password', required: true, minlength: 6, autocomplete: 'new-password', value: prev.new_password || '' })));
    } else {
      fields.push(
        h('div', { class: 'field' },
          h('label', {}, 'Password'),
          h('input', { class: 'input', name: 'password', type: 'password', required: true, minlength: isLogin ? undefined : 6, autocomplete: isLogin ? 'current-password' : 'new-password', value: prev.password || '' })));
    }

    if (mode === 'register') {
      fields.push(
        h('div', { class: 'choice-row' },
          h('button', { type: 'button', class: joinMode === 'create' ? 'active' : '', onclick: () => { joinMode = 'create'; draw(); } }, 'New household'),
          h('button', { type: 'button', class: joinMode === 'join' ? 'active' : '', onclick: () => { joinMode = 'join'; draw(); } }, 'Join with a code')));
      if (joinMode === 'create') {
        fields.push(
          h('div', { class: 'field' },
            h('label', {}, 'Household name'),
            h('input', { class: 'input', name: 'household_name', placeholder: 'e.g. The Hardingers', required: true, maxlength: 60, value: prev.household_name || '' })));
      } else {
        fields.push(
          h('div', { class: 'field' },
            h('label', {}, 'Invite code'),
            h('input', { class: 'input', name: 'invite_code', placeholder: '6-letter code from a housemate', required: true, maxlength: 6, style: { textTransform: 'uppercase' }, value: prev.invite_code || '' })));
      }
    }

    const heading = isLogin ? 'Welcome back' : (isReset ? 'Reset your password' : 'Create your account');
    const submitLabel = isLogin ? 'Sign in' : (isReset ? 'Reset password' : 'Create account');

    const form = h('form', {
      onsubmit: (e) => { e.preventDefault(); submit(e.target); },
    },
      error ? h('div', { class: 'form-error' }, error) : null,
      isReset ? h('p', { class: 'muted small', style: { marginTop: 0 } },
        'Enter one of the recovery codes you saved when you signed up.') : null,
      fields,
      h('button', { class: 'btn btn-primary', type: 'submit', style: { width: '100%', justifyContent: 'center', marginTop: '4px' } },
        submitLabel));

    root.replaceChildren(
      h('div', { class: 'auth-wrap' },
        h('div', { class: 'auth-card' },
          h('div', { class: 'auth-hero' },
            h('div', { class: 'hero-logo' }, 'SR'),
            h('h1', {}, 'Stay Ready'),
            h('p', {}, 'Plan the month. Stock the pantry. Never wonder what’s for dinner.'),
            h('ul', {},
              h('li', {}, 'Month-at-a-glance meal calendar'),
              h('li', {}, 'Pantry that talks to your recipes'),
              h('li', {}, 'Smart picks: quickest, healthiest, cheapest'),
              h('li', {}, 'Shopping list + Google Calendar export'))),
          h('div', { class: 'auth-form' },
            h('h2', {}, heading),
            form,
            h('div', { class: 'auth-switch' },
              isLogin ? 'New here? ' : 'Already have an account? ',
              h('a', {
                onclick: () => { mode = isLogin ? 'register' : 'login'; error = ''; draw(); },
              }, isLogin ? 'Create an account' : 'Sign in')),
            isLogin ? h('div', { class: 'auth-switch', style: { marginTop: '8px' } },
              h('a', { onclick: () => { mode = 'reset'; error = ''; draw(); } }, 'Forgot your password?')) : null,
            h('div', { class: 'auth-switch', style: { marginTop: '8px' } },
              h('a', { href: '/privacy', target: '_blank' }, 'Privacy policy'))))));
  }

  draw();
};
