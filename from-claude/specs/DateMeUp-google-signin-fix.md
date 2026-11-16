# Fix: Google sign-in blocked ("Error 400: origin_mismatch")

**Priority:** must fix before store submission. Every new user who taps "Continue with Google" is blocked.
**Reported:** Sun 15 Nov 2026, while creating a new account with a new Google account on datemeup.app.

## What the user sees
> **Access blocked: Authorization Error**
> You can't sign in to this app because it doesn't comply with Google's OAuth 2.0 policy.
> If you're the app developer, register the JavaScript origin in the Google Cloud Console.
> **Error 400: origin_mismatch**

## Cause
The address of the page that started Google sign-in isn't in the Google OAuth web client's **Authorized JavaScript origins**. It most likely still lists the old togetherplans.app domain, or is missing a variant (`www.` vs bare domain, staging or preview addresses).

This is **not** caused by the consent screen being in "Testing". Testing mode gives **Error 403: access_denied** for anyone not on the test-user list. That's checked in step 3 so it doesn't become the next blocker.

---

## Fix steps

### 1. Google Cloud: web OAuth client
Console → APIs & Services → **Credentials** → the **Web application** OAuth client used by datemeup.app (match its Client ID to the site's config, e.g. `GOOGLE_CLIENT_ID`).

**Authorized JavaScript origins.** Add every address the login page can be served from: scheme and host only, no path or trailing slash.
```
https://datemeup.app
https://www.datemeup.app
https://api.datemeup.app        (only if the Google button or a popup starts from the API host)
https://<staging/preview hosts>  (e.g. staging.datemeup.app, preview deployments)
http://localhost:3000            (local dev, optional)
```
Remove the `togetherplans.app` entries once nothing uses them.

**Authorized redirect URIs.** Needed if sign-in goes through a server redirect (OAuth code flow, NextAuth, Supabase, Firebase and so on). List the exact callback URLs on the new domain, for example:
```
https://datemeup.app/api/auth/callback/google
https://api.datemeup.app/auth/google/callback
```
Use whatever path the auth library actually calls. A wrong one gives **Error 400: redirect_uri_mismatch**.

Save. Changes can take **5 minutes to a few hours** to apply.

### 2. Check the app's own config
- The site's environment variables use the right Client ID and the **new domain** for anything like `NEXTAUTH_URL`, `AUTH_URL`, `SITE_URL`, `BASE_URL`, `GOOGLE_REDIRECT_URI` or `OAUTH_CALLBACK_URL`.
- If an auth provider is involved, update its settings too:
  - **Supabase:** Auth → URL Configuration → Site URL and Redirect URLs set to `https://datemeup.app/**`. Supabase's own callback (`https://<project>.supabase.co/auth/v1/callback`) must be in Google's redirect URIs.
  - **Firebase:** Authentication → Settings → Authorized domains: add `datemeup.app` and `www.datemeup.app`.
  - **Auth0 / Clerk:** Allowed Callback URLs, Allowed Web Origins and Allowed Logout URLs set to the new domain.
- Pick one canonical host (`datemeup.app` or `www.datemeup.app`) and redirect the other to it, so sign-in always starts from a known address.

### 3. OAuth consent screen
Console → APIs & Services → **OAuth consent screen** (Branding / Audience):
- **App name:** DateMeUp. Upload the logo.
- **Home page:** `https://datemeup.app`. **Privacy policy:** `https://datemeup.app/privacy`. **Terms:** `https://datemeup.app/terms`.
- **Authorized domains:** `datemeup.app`. Remove `togetherplans.app` when it's no longer used.
- **Support and developer contact email:** an @datemeup.app address if one exists.
- **Publishing status:** if it says **Testing**, click **Publish app** (go to Production).
  - With only basic scopes (`openid`, `email`, `profile`), no Google verification review is needed.
  - Brand verification may still be required for the name and logo to show; follow any prompt in the console.

### 4. Mobile apps (iOS and Android)
Google blocks sign-in inside embedded web views (**Error 403: disallowed_useragent**), so:
- The apps must use **native Google Sign-In** (Google Sign-In SDK / Credential Manager, or `expo-auth-session` / `@react-native-google-signin`), not the website's login page in an in-app browser.
- Credentials needed:
  - **iOS OAuth client:** bundle ID `app.togetherplans.datenight` (or the new bundle ID if it changes). Put the reversed client ID URL scheme in Info.plist.
  - **Android OAuth client:** package `datemeup.app`, with the **SHA-1** of the debug key, the upload key, **and** the Play App Signing key (from Play Console → Setup → App integrity).
  - The backend accepts ID tokens whose `aud` is any of the web, iOS or Android client IDs.
- Related from the v1.5.0 test: "Pick an invite card" on iOS opens the website's login page in an in-app browser. Pass the user's session or open the picker inside the app, so users never hit Google sign-in in a web view.

### 5. Other sign-in providers: same domain change
- **Facebook Login** (developers.facebook.com → the app):
  - App Domains: `datemeup.app`
  - Valid OAuth Redirect URIs: the new callback URLs
  - Site URL, Privacy Policy URL, Terms URL and Data Deletion URL on datemeup.app
  - App in **Live** mode
- **Sign in with Apple** (developer.apple.com → Identifiers → Services ID): Domains and Return URLs on datemeup.app. Upload any domain-association file it asks for.

---

## Acceptance tests
Run each in a **private window** with a Google account that has **never** signed in to DateMeUp:

| # | Test | Expected |
|---|---|---|
| 1 | https://datemeup.app → Continue with Google | Google consent screen titled **DateMeUp**, then signed in and a new account created |
| 2 | Same from https://www.datemeup.app | Redirects to the canonical host, then signs in |
| 3 | Existing Google user (e.g. the reviewer account) | Signs in to the same account; no duplicate user |
| 4 | iOS app → Continue with Google | Native Google sheet, signed in; no web page, no 403 |
| 5 | Android app → Continue with Google (Play internal test build) | Native account picker, signed in |
| 6 | Facebook and Apple buttons, web and apps | Sign in with no domain or redirect errors |
| 7 | Sign out, then sign in again | Works; onboarding is not shown again |

Report back: the screenshot of the Authorized JavaScript origins and redirect URIs, the consent screen status (Production), and the results of tests 1–7.
