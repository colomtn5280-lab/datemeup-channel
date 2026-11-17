# DateMeUp: ads and privacy setup (2026-11-16)

Claude completed the web-console side tonight with Jake's OK. This file lists the code-side work for Hermes. Everything here is a public ID, not a secret.

## 1. Done in consoles (no action needed)

**AdMob** (publisher `pub-9071368122045876`)
- Registered 2 apps, 4 ad units.
- Published 3 Privacy & messaging messages:
  - **European regulations (GDPR):** both apps, privacy URL https://datemeup.app/privacy, "Do not consent" button ON for all countries.
  - **US state regulations:** both apps.
  - **IDFA explainer:** iOS. Google's default copy is shown before Apple's ATT alert.

**App Store Connect → App Privacy** (published)
- 12 data types:
  - Name, Email, Phone, Photos, Other User Content, User ID → App Functionality, linked, no tracking.
  - **Coarse Location** → App Functionality + Analytics + Third-Party Advertising, not linked, **tracking**.
  - **Device ID, Product Interaction, Advertising Data** → Analytics + Third-Party Advertising, not linked, **tracking**.
  - Crash Data → App Functionality + Analytics. Performance Data → Analytics + Third-Party Advertising. Neither is tracking.
  - **Precise Location removed.** See §3, which is required for that answer to be true.
- Marketing URL is https://datemeup.app (app-ads.txt is crawled from there).

**Google Play**
- Data safety already matched the AdMob data (shared: approximate location, crash logs, diagnostics, app interactions, device IDs).
- Ads = "contains ads" and Advertising ID = "uses" were already declared.
- App-level trader status saved with Terms URL https://datemeup.app/terms. It sits in Publishing overview, waiting to be sent for review (Jake).
- Website is https://datemeup.app.

## 2. Swap test IDs for real IDs

`mobile/app.json` (react-native-google-mobile-ads plugin):
```
"androidAppId": "ca-app-pub-9071368122045876~2156075729",
"iosAppId":     "ca-app-pub-9071368122045876~3469157397",
```

`mobile/src/services/admob.ts`, `AD_UNIT_IDS`:
```
BANNER:       ios 'ca-app-pub-9071368122045876/6740132656'   android 'ca-app-pub-9071368122045876/9842994056'
INTERSTITIAL: ios 'ca-app-pub-9071368122045876/4462674866'   android 'ca-app-pub-9071368122045876/9787153735'
```
Keep Google's **test** unit IDs for `__DEV__` and simulator builds (`TestIds.BANNER` / `TestIds.INTERSTITIAL`). Never tap or load real ads on your own devices; AdMob flags invalid traffic.

**SKAdNetwork:** `skAdNetworkItems` currently has only `cstr6suwn9`. Replace it with Google's full list from https://developers.google.com/admob/ios/3p-skadnetworks. Without the full list, iOS ad revenue is lower.

## 3. Location must actually be approximate (blocking: privacy labels now say coarse only)
- Android: remove `ACCESS_FINE_LOCATION` from `android.permissions` and keep `ACCESS_COARSE_LOCATION`. The Android prompt then offers Approximate only.
- iOS: add `"NSLocationDefaultAccuracyReduced": true` to `ios.infoPlist`.
- Request `Location.Accuracy.Low` (or Lowest).
- Server side: round lat/lng to 2 decimals (~1 km) before storing or logging.
- If you can't do this, tell Jake. Precise Location then has to be re-declared in App Store Connect and Play Data safety.

## 4. Consent (UMP) and ATT flow
AdMob's messages only show once the UMP SDK is called. With `react-native-google-mobile-ads`:
```ts
import mobileAds, { AdsConsent } from 'react-native-google-mobile-ads';
// at startup, before loading any ad:
await AdsConsent.requestInfoUpdate();
await AdsConsent.loadAndShowConsentFormIfRequired(); // shows GDPR / US-state form, and on iOS the IDFA explainer → ATT
const { canRequestAds } = await AdsConsent.getConsentInfo();
if (canRequestAds) await mobileAds().initialize();
```
- **Remove the separate `requestATT()` call.** The published IDFA explainer makes UMP show the explainer and then the system ATT alert, and calling ATT yourself as well would double-prompt. Keep `expo-tracking-transparency` in plugins so the plist key ships.
- **Privacy options entry point (required):** in Profile → Account, add "Privacy choices". Show it when `AdsConsent.getConsentInfo()` reports `privacyOptionsRequirementStatus === 'REQUIRED'`, and on tap call `AdsConsent.showPrivacyOptionsForm()`.
- **New ATT string** (`NSUserTrackingUsageDescription`). The current one says the app "may show ads in the future" and never shares data with advertisers, which is inaccurate now:
  > "DateMeUp is free because of ads. Allowing tracking lets us show you ads that are more relevant. Your choice doesn't change how the app works."
- Keep `maxAdContentRating: PG`. Don't place ads on After Dark screens.

## 5. Web (datemeup.app)
- **`web/public/app-ads.txt`** with exactly this line, served at https://datemeup.app/app-ads.txt:
  ```
  google.com, pub-9071368122045876, DIRECT, f08c47fec0942fa0
  ```
- **Privacy policy (`LegalPages.tsx`):** it still says "We do not use your data to serve targeted advertising". Replace that with an Advertising section covering:
  - the app shows ads via Google AdMob
  - data shared: device advertising ID, approximate location from IP, ad interactions, diagnostics
  - personalized ads only with consent (ATT on iOS; consent form in EU/UK/CH; opt-out in US states via Privacy choices)
  - link to https://policies.google.com/technologies/partner-sites
- **Homepage:** change "Free, no ads" to "Free".
- **`/delete-account` page:** Play needs a dedicated URL showing the steps (in app: Profile → Delete account; or email support@datemeup.app) and what's deleted or kept. Jake/Claude will then swap the Play Data safety URL from `/support` to it.
- **Android App Links:** Play Console reports "one deep link may be failing because your web domains aren't associated with your app". Serve `https://datemeup.app/.well-known/assetlinks.json` with package `datemeup.app` and the app-signing SHA-256 from Play Console → App integrity → App signing.

## 6. Launch order
1. Build with real IDs, UMP, and `ads_enabled` still **false**.
2. Ship that build.
3. Once the apps are live, Claude/Jake link the store listings in AdMob ("Add store"), which lifts AdMob's "limited ad serving".
4. Flip `ads_enabled` to true remotely.
