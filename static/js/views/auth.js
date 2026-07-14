/* Sign in / create account screen (not a nav view — rendered full screen). */

App.renderAuth = function renderAuth() {
  let mode = 'login';          // 'login' | 'register'
  let joinMode = 'create';     // 'create' | 'join'
  let error = '';

  const root = document.getElementById('app');

  function submit(form) {
    error = '';
    const data = Object.fromEntries(new FormData(form).entries());
    const done = (res) => {
      App.state.user = res.user;
      location.hash = '#/dashboard';
      App.renderShell();
      App.toast('Welcome, ' + res.user.display_name + '.');
    };
    const fail = (err) => { error = err.message; draw(); };
    if (mode === 'login') {
      App.api('/api/auth/login', 'POST', data).then(done).catch(fail);
    } else {
      if (joinMode === 'create') delete data.invite_code;
      else delete data.household_name;
      App.api('/api/auth/register', 'POST', data).then(done).catch(fail);
    }
  }

  function draw() {
    const isLogin = mode === 'login';

    // Preserve whatever the user already typed across redraws (error/toggle re-renders).
    const prev = {};
    root.querySelectorAll('input[name]').forEach((i) => { prev[i.name] = i.value; });

    const fields = [];
    if (!isLogin) {
      fields.push(
        h('div', { class: 'field' },
          h('label', {}, 'Your name'),
          h('input', { class: 'input', name: 'display_name', placeholder: 'e.g. Matt', required: true, maxlength: 40, value: prev.display_name || '' })));
    }
    fields.push(
      h('div', { class: 'field' },
        h('label', {}, 'Username'),
        h('input', { class: 'input', name: 'username', placeholder: 'username', required: true, autocomplete: 'username', maxlength: 40, value: prev.username || '' })),
      h('div', { class: 'field' },
        h('label', {}, 'Password'),
        h('input', { class: 'input', name: 'password', type: 'password', required: true, minlength: isLogin ? undefined : 6, autocomplete: isLogin ? 'current-password' : 'new-password', value: prev.password || '' })));

    if (!isLogin) {
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

    const form = h('form', {
      onsubmit: (e) => { e.preventDefault(); submit(e.target); },
    },
      error ? h('div', { class: 'form-error' }, error) : null,
      fields,
      h('button', { class: 'btn btn-primary', type: 'submit', style: { width: '100%', justifyContent: 'center', marginTop: '4px' } },
        isLogin ? 'Sign in' : 'Create account'));

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
            h('h2', {}, isLogin ? 'Welcome back' : 'Create your account'),
            form,
            h('div', { class: 'auth-switch' },
              isLogin ? 'New here? ' : 'Already have an account? ',
              h('a', {
                onclick: () => { mode = isLogin ? 'register' : 'login'; error = ''; draw(); },
              }, isLogin ? 'Create an account' : 'Sign in')),
            h('div', { class: 'auth-switch', style: { marginTop: '8px' } },
              h('a', { href: '/privacy', target: '_blank' }, 'Privacy policy'))))));
  }

  draw();
};
