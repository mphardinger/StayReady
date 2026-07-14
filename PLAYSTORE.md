# Publishing Stay Ready to Google Play

The app ships as a Trusted Web Activity (TWA): a thin Android wrapper around
the live PWA at https://stayready.pythonanywhere.com.  No Android SDK needed
locally — PWABuilder generates the package in the browser.

Everything code-side is already done: privacy policy at `/privacy`, in-app
account deletion (House ▸ Account ▸ Delete account), and the Digital Asset
Links file at `/.well-known/assetlinks.json` (one placeholder to fill in at
step 5).

## 1. Play Console account (you)

https://play.google.com/console — personal developer account, one-time $25.
Identity verification can take a day or two.

## 2. Generate the Android package (PWABuilder)

1. Go to https://www.pwabuilder.com and enter `https://stayready.pythonanywhere.com`.
2. Package for stores → **Android**.  Settings:
   - Package ID: `com.mphardinger.stayready` (must match assetlinks.json — it does)
   - App name: Stay Ready · Version: 1.0.0 / code 1
   - Signing: **let PWABuilder create a new signing key**
3. Download the zip.  KEEP IT SOMEWHERE SAFE — it contains your upload key
   (`signing.keystore` + passwords in `signing-key-info.txt`).  Losing it makes
   future updates painful.

## 3. Create the app in Play Console

Create app → name "Stay Ready", App (not game), Free.  Then in the dashboard
work through "Set up your app":
- **Privacy policy**: `https://stayready.pythonanywhere.com/privacy`
- **App access**: "All functionality is available without special access" is
  NOT true (login required) → choose "All or some functionality is restricted"
  and add a demo account: create a fresh account in the app for Google's
  reviewers (e.g. username `playreview`, household "Review Kitchen") and give
  them those credentials.
- **Ads**: No ads.
- **Content rating**: questionnaire → Utility/Productivity → everything "No" →
  rated Everyone.
- **Target audience**: 18+ (or 13+; do not select under-13).
- **Data safety**: see the answers below.
- **Account deletion**: it asks for a URL →
  `https://stayready.pythonanywhere.com/privacy#delete`

## 4. Data safety form answers

- Does your app collect or share user data? **Yes, collects.  Shares: No.**
- Data types collected:
  - Personal info → **User IDs** (username) and **Name** (display name).
    Required, collected (not shared), for App functionality + Account
    management.  Not processed ephemerally.
  - App activity → **Other user-generated content** (recipes, meal plans,
    pantry, expenses).  Required, App functionality only.
- Everything else (location, financial info, email, contacts, photos, health,
  device IDs, browsing): **not collected**.  (Expense amounts are user-entered
  content, not payment info — the app never touches payment instruments.)
- Is all user data encrypted in transit? **Yes** (HTTPS).
- Do you provide a way for users to request deletion? **Yes** (in-app + the
  /privacy#delete URL).

## 5. Upload, then fix the signing fingerprint (the step people miss)

1. Testing → **Internal testing** → create release → upload the `.aab` from
   the PWABuilder zip → add yourself as a tester → roll out.
2. Play Console → **Test and release → Setup → App signing**: copy the
   **SHA-256 certificate fingerprint** of the *App signing key certificate*
   (Google re-signs your app — this is the fingerprint that matters).
3. Edit `static/.well-known/assetlinks.json` in the repo: replace
   `REPLACE_WITH_SHA256_FROM_PLAY_CONSOLE_APP_SIGNING_PAGE` with that
   fingerprint (keep the quotes; you can list the PWABuilder upload key's
   fingerprint as a second array entry too).
4. Deploy it: commit/push, then on PythonAnywhere `git pull` + Reload.
5. Verify: https://stayready.pythonanywhere.com/.well-known/assetlinks.json
   shows the real fingerprint.  Install the internal-testing build — it must
   open full-screen with NO browser address bar.  An address bar means the
   fingerprint doesn't match yet.

## 6. Store listing + release

- Screenshots: at least 2 phone screenshots (settle for the Today page, the
  meal plan, and the week builder — dark mode looks sharp).  512×512 icon
  (`static/icons/icon-512.png` works) + a 1024×500 feature graphic.
- Short description (max 80 chars):
  "Plan meals with your house: budgets, diets, one shared list."
- Promote the internal release to **Production** when it feels right.
  First review typically takes a few days.

## Ongoing

- App updates: shipping web changes needs NO new Play release — the TWA loads
  the live site.  Only manifest-level changes (name, icon, colors) need a new
  .aab (PWABuilder again, bump version code).
- The free PythonAnywhere tier needs its "Run until 3 months from today"
  button clicked quarterly, and sleeps are possible under heavy load.  For a
  public store app, the $5/month plan (no expiry, more capacity) is strongly
  recommended once real strangers start installing.
- iOS/App Store is a different, harder path (Apple rejects thin wrappers) —
  out of scope here.
