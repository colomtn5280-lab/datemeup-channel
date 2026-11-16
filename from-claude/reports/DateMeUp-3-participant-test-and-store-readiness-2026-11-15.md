# DateMeUp — 3-Participant Group Test + Store-Readiness Plan
**For:** Hermes  **Date:** 2026-11-15  **Build tested:** iOS + Android "v1.5.0" (Appetize: iPhone 14 Pro / iOS 17.2, Pixel 7 / Android 13) and web (datemeup.app, api.datemeup.app)

---

## 0. TL;DR

The core loop works: create a group, invite people, propose options, everyone votes, and a unanimous Yes locks in a winner. It ran correctly across iOS, Android and web for three people at once, and changing a vote correctly flips a plan to "matched".

It is **not store-ready yet**. Blockers, in priority order:

1. **"Save note" deletes the user's vote** (web and iOS confirmed), and notes are never stored (`comment` is always `null`).
2. **Dates are wrong and inconsistent everywhere.**
   - "Tonight near me" returns events from 2 days ago.
   - Past-dated plans can be sent and even "locked in".
   - The proposal date, header chip, title and option dates all disagree.
3. **Add to calendar fails on both iOS and Android** ("Could not add to calendar"), with no permission prompt.
4. **Invites don't work end-to-end.**
   - The web client sends a lowercase `method` → 400.
   - USERNAME has no input field.
   - EMAIL/USERNAME invites never reach the invitee.
   - Links are single-use, open in the browser rather than the app, and require re-login.
5. **Counter-propose is broken on every platform.**
   - Web: it just redirects to the group page.
   - iOS: it opens a blank new plan that isn't linked (`parentId: null`).
   - The original plan stays OPEN forever.
6. **No-consensus has no resolution.**
   - The banner promises "Lock in a Maybe … or start over", but only Counter-propose exists.
   - There is no vote deadline (`voteDeadline: null`), so a plan can sit OPEN indefinitely.
7. **Group-size wording and counters are wrong.**
   - Copy like "You both said yes" and "Your partner votes by link" assumes two people.
   - Mobile group cards show "0 / 3 voted" when 2–3 people have voted.
   - The header shows 2 avatars for 3 members.
8. **Notifications only cover matches.** There's nothing for a new plan, a comment, a friend request or a group invite, which is a retention problem for a voting app.

Store-submission requirements are in §6. Several of them (Sign in with Apple, UGC report/block, an account-deletion URL, the Play 12-tester closed test) are **gating items independent of bugs**.

---

## 1. Test setup

| Role | Platform | Account | Notes |
|---|---|---|---|
| G R (group **owner**) | Web | horsepunch2013 (new account) | Created the group and sent invites |
| Jake (Yahoo) | iOS (Appetize) | existing test account | Joined via link |
| Demo Reviewer | Android (Appetize) | existing test account | Joined via link |

- **Group:** "Trio Date Club" (`655e798f-5338-413d-9ebb-dddc51609c06`), 3 members.
- **Proposals created:**

| Round | Proposal | Created by | Options | Outcome |
|---|---|---|---|---|
| R1 | "R1 web 3-way" `f1a9d322…` | G R (web) | Giant Rooks, Wizards v Rockets, Amber Autry | **DECIDED**: Amber Autry (unanimous) ✔ |
| R2 | "R2 android no-consensus" `cd37c626…` | Demo (Android) | Nurse Blake, National Conference Center Dining, Ethiopian Buffet | **No consensus**, still OPEN with no way to resolve ✖ |
| R3 | "Date night · Friday" `5ed9b1bd…` | Jake (iOS, via "Counter-propose") | WBB v. North Carolina Central, Eyes of the Nile | Demo changed No→Yes → **DECIDED**: WBB ✔ (but the event was in the past) ✖ |

**Vote matrices:**

R1:

| Option | G R | Jake | Demo |
|---|---|---|---|
| Giant Rooks | Yes | Maybe | Yes |
| Wizards v Rockets | Yes | Yes | No |
| Amber Autry | Yes | Yes | Yes → winner |

R2:

| Option | Demo | G R | Jake |
|---|---|---|---|
| Nurse Blake | Yes | No | Yes |
| Conference Center Dining | Yes | Yes | Maybe |
| Ethiopian Buffet | Yes | Maybe | No |

R3:

| Option | G R | Jake | Demo |
|---|---|---|---|
| WBB | Yes | Yes | No → **Yes** → winner |
| Eyes of the Nile | No | Yes | No |

---

## 2. What works well (keep it)
- The R1 three-way vote resolved correctly. It didn't lock early at 2 of 3 and chose the only unanimous option.
- Changing a vote (No → Yes) immediately triggers the match and decides the plan (R3), and the API state is correct (`status: DECIDED`, `winnerId` set).
- The match screen's per-person breakdown ("G ✓Yes / Jake ~Maybe / Demo ✗No") is clear and delightful.
- iOS shows a "So close! No unanimous choice yet." banner when everyone has voted without consensus. That's the right instinct.
- Android swipe mode (from the "Swipe to vote" button) works with buttons and has a nice "All options voted!" end state.
- The discussion thread syncs across platforms (a web comment appeared on iOS).
- Web invite-card designs: all 32 now render with the real plan title and venue (a big improvement), apart from the date and sample-name leftovers in §3.9.
- The Android invite-card picker now opens (it was broken before).
- Web notifications list "It's a match!" for both decided plans.

---

## 3. Issues: function / flow / feel

Severity: **P0** = blocks release; **P1** = fix before launch; **P2** = polish.

### 3.1 Voting & notes
| # | Sev | Platform | Issue | Repro / evidence | Fix |
|---|---|---|---|---|---|
| V1 | **P0** | Web + iOS | **"Save note" deletes the user's vote.** | Vote Maybe → type a note → Save note. The card collapses (web) and the API shows the user's vote gone. On iOS the UI still shows "Yes ✓" but the server has no vote (verified via `GET /api/proposals/{id}`). | Save note is probably re-POSTing the same sentiment and hitting toggle-off logic. Use a separate `PATCH /votes/{id} {comment}`, or make the vote upsert idempotent (same sentiment = no-op, not delete). |
| V2 | **P0** | All | **Notes never persist.** `comment` is `null` on every vote after saving notes on web, iOS and Android. | API dump after notes saved | Save the `comment` field; show notes in the vote breakdown. |
| V3 | P1 | Web + mobile | Tapping a selected vote again silently un-votes it. That's surprising, and combined with layout shifts it causes accidental vote loss. | Web card collapses or expands when voting, so the next tap lands on a different button. | Either remove toggle-off or confirm it ("Clear vote?"). Reserve fixed height for the note area so buttons don't move. |
| V4 | P1 | iOS/Android | Per-option "N votes" lags or is wrong (showed "2 votes" when 3 had voted, then corrected later). | R2 Nurse Blake on iOS | Recompute from server state after each vote. |
| V5 | P1 | iOS/Android | Group card says **"0 / 3 voted"** when 2–3 have voted; the proposal header showed "2 of 3 voted" after the third vote. | R2 and R3 group cards | Count distinct voters from server tally; refresh on focus. |
| V6 | P2 | All | Vote counts are visible on options before you've voted on them, which can bias the vote. | — | Hide counts until you've voted (or make it a group setting). |
| V7 | P2 | All | "A member voted · waiting on you" is vague in a group of 3+. | — | "Jake voted · waiting on you and Demo". |
| V8 | P2 | Android | Synthetic horizontal swipe on cards didn't register in swipe mode. This may be an Appetize input limitation, but please verify the gesture threshold and velocity on a real device. | — | Verify on a real device; lower the threshold. |

### 3.2 No-consensus & counter-propose
| # | Sev | Platform | Issue | Fix |
|---|---|---|---|---|
| C1 | **P0** | Web | "Counter-propose" just navigates to the group page. Nothing is created. | Implement it. The copy says it "keeps this option and lets you swap in new ones. Votes reset." |
| C2 | **P0** | iOS | "Counter-propose" opens a **blank** New Proposal (it doesn't keep any option); the result has `parentId: null`, so it's unlinked, and the original stays OPEN. | Prefill the kept options, set `parentId`, and mark the parent `SUPERSEDED` (or close it). |
| C3 | **P0** | All | The no-consensus banner says "Lock in a Maybe, counter-propose, or start over", but **only Counter-propose exists**. | Add "Lock in [best option]" (auto-pick: most Yes plus Maybe, no No) and "Start over". |
| C4 | P1 | All | `voteDeadline` is always null, so plans never close. The web shows "Reminder: Fri 8 PM if not everyone's voted", but nothing resolves after that. | Default deadline (e.g., 24 h before the event); at the deadline, auto-pick the best option or notify the creator to decide. |
| C5 | P1 | Android | No "no consensus" banner after all votes were in (iOS showed one). | Parity with iOS. |

### 3.3 Dates & times (highest-impact UX bug class)
| # | Sev | Issue | Evidence | Fix |
|---|---|---|---|---|
| D1 | **P0** | **"Tonight near me" returns past events.** On Sun Nov 15 it listed Fri Nov 13 events (WBB, Eyes of the Nile, WAR). | iOS Discover | Filter `start >= now` in the user's timezone; query today's local date range. |
| D2 | **P0** | **Past-dated events can be added, sent and locked in.** R3 decided on a game from 2 days earlier; the web immediately asks "How was WBB? Rate your date". | R3 | Block or warn on past options; hide past events in Discover. |
| D3 | **P0** | **Proposal date disagrees with what the user picked and with the options.** | R2: Android "When?" showed Mon Nov 16 7:00 PM → saved `2026-11-24T17:00Z` (Tue Nov 24, 12:00 PM ET); the header chip says "Tue, Nov 24" and the web sidebar says "Next Tuesday at 12:00 PM". R3: titled "Date night · Friday" (events Fri Nov 13) but saved Mon Nov 16 7 PM, and the web says "Tomorrow at 7:00 PM". R1 (earlier): finalize said Sun Nov 15, while the options showed Sat Nov 14. | One source of truth: if every option has a start time, derive the plan date from the chosen option; otherwise use the explicit picker. Store UTC and render in the viewer's timezone. Generate the auto-title from the same date. |
| D4 | P1 | The default "When?" was 12:00 noon (already past) on web; Android defaulted to Mon 7 PM. | — | Default to the next sensible evening slot; never default into the past. |
| D5 | P1 | Venue/restaurant options have no date at all, while event options do. The plan header date then means different things. | R2 | Show "Plan date" once at the top; options inherit it unless they have a fixed time. |

### 3.4 Calendar
| # | Sev | Issue | Fix |
|---|---|---|---|
| K1 | **P0** | **"Add to calendar" fails on iOS and Android** ("Could not add to calendar. Please try adding the event manually."). No permission prompt appears. | iOS 17 needs `NSCalendarsWriteOnlyAccessUsageDescription` (or `NSCalendarsFullAccessUsageDescription`) in Info.plist plus `requestWriteOnlyAccessToEvents`. Android needs `WRITE_CALENDAR`/`READ_CALENDAR`, or better, launch an `Intent.ACTION_INSERT` to the Calendar app (no permission needed). Expo: `expo-calendar` with the plugin permissions set in app.json. As a fallback, offer an `.ics` download/share. |

### 3.5 Invites, joining, new members (the focus of this round)
| # | Sev | Platform | Issue | Fix |
|---|---|---|---|---|
| I1 | **P0** | Web | The invite client sends a lowercase `method` (`"link"`), so **every invite type returns 400**. It works only with `LINK/EMAIL/USERNAME` uppercase. | Uppercase in the client, or make the API case-insensitive. |
| I2 | **P0** | Web | The USERNAME tab has no input field. | Add input + search/autocomplete of friends. |
| I3 | **P0** | All | EMAIL and USERNAME invites never surface for the invitee: no inbox item, no push, no email, and there's no "pending invites" endpoint or UI. | Add a `GET /api/invitations/pending` + "Invites" section with Accept/Decline; send email via transactional mail; push to existing users. |
| I4 | P1 | All | The invite **link is single-use** (a second person gets 404). That's a poor fit for a group link. | Multi-use group link with optional expiry/max uses; single-use only for email/username. |
| I5 | P1 | iOS/Android | The invite link opens in the device **browser**, not the app, and requires signing in again. | Universal Links (apple-app-site-association on datemeup.app) + Android App Links (assetlinks.json); deferred deep link through install. |
| I6 | P1 | Web | "Generate invite" creates duplicate invites on repeat taps. | Reuse the active link. |
| I7 | P2 | Web | The email invite UI says "Invite created", not "Invite sent". | Fix copy once email is actually sent. |
| I8 | P2 | Web | Two clicks are needed to create a group, and the invite options sit below the plan section. | Put "Invite members" first after creating a group. |
| I9 | P2 | All | No "join with code" option. | Short code alternative to links (great for in-person). |

### 3.6 Groups & copy for 3+ people
| # | Sev | Issue | Fix |
|---|---|---|---|
| G1 | P1 | A new group defaults to "Couple · Partner hasn't joined yet" (it later changed to "Group · 3 members"). | Ask type at creation, or infer from member count. |
| G2 | P1 | Two-person copy in group contexts: "You both said yes to this one", "Your partner votes by link", "when you both pick". | Pluralize by member count ("Everyone said yes!"). |
| G3 | P1 | The mobile group header shows 2 avatars for 3 members. | Show up to 4 + "+N". |
| G4 | P2 | The Android group list needed pull-to-refresh to show a newly joined group. | Refresh on focus / push. |
| G5 | P2 | A new account's avatar shows "H" (from the email) while the name is "G R"; vote chips show "G:". | Use displayName initials consistently; chips show first name. |
| G6 | P2 | The Demo account has 3 leftover "E2E Test Group…" groups from automation. | Clean the review/demo account before submission. |

### 3.7 Friends
| # | Sev | Issue | Fix |
|---|---|---|---|
| F1 | P1 | Web has no friends UI; G R has a pending friend request from Jake that can't be seen or accepted on web, and there's no notification. | Friends page on web; notify on request. |
| F2 | P2 | The Android "Add Friend" button doesn't change state after sending (a second tap shows "already sent"). | Switch to "Requested" state. |

### 3.8 Notifications
| # | Sev | Issue | Fix |
|---|---|---|---|
| N1 | **P1** | Only "It's a match!" notifications exist. There are none for: a new plan in your group, someone voted, a new comment, a friend request, a group invite, or a plan that's about to expire. | Add these as in-app plus push (Expo push / APNs / FCM), with per-type toggles in Settings. |
| N2 | P1 | "Let them know" (iOS) opens the OS share sheet with plain text and **no link**. The other members are already in the group, so it should be an in-app nudge/push. | Change it to "Nudge group" (push); keep share for non-members, with the link. |

### 3.9 Invite cards
| # | Sev | Platform | Issue |
|---|---|---|---|
| IC1 | P1 | Android | The picker shows plain colored tiles with no preview, an uneven layout and low-contrast "Movie marquee" text. The "Customise your card" preview is a blank teal block with no plan data. |
| IC2 | P1 | Web | Wrong sample date "Sun, Sep 27 · 2:00 PM" on Ticket Stub, Playbill/Gig Poster and Newspaper. |
| IC3 | P2 | Web | Sample names remain: Receipt ("Blue Room"), 8-bit Arcade, Departures Board, Wanted Poster ("JAKE & SARAH"). Terminal still says "togetherplans". |

### 3.10 Match screen & navigation
| # | Sev | Issue |
|---|---|---|
| M1 | P1 | The iOS/Android match modal reappears every time you open a decided plan. The iOS modal has no close button and tapping outside doesn't dismiss it. |
| M2 | P2 | The iOS rating prompt repeats. |
| M3 | P2 | Android: after "Sent to group", pressing Back returns into Discover and then an empty New Proposal (stale back stack). Reset the stack to Group → Plan. |
| M4 | P2 | The web decided view shows the winner twice (in "The plan" and again in the options list). |

### 3.11 Discover data quality
| # | Sev | Issue |
|---|---|---|
| DQ1 | P1 | The "Comedy" category returns restaurants and conference halls (National Conference Center Dining, Ethiopian Buffet, Running Dish), all tagged "Comedy". The category filter isn't constraining the source query or the tag mapping. |
| DQ2 | P2 | Discover on Android had partial Spanish earlier; this session the proposal form was English. Check that locale persists. |

### 3.12 Accounts & persistence
| # | Sev | Issue |
|---|---|---|
| A1 | P1 | Onboarding runs after every sign-in. `tp_onboarded` and `tp.favCategories` are stored on the device only, so a new device or reinstall repeats onboarding and loses favorites. Store them on the user profile. |
| A2 | P1 | Both apps still report **v1.5.0**. Bump the version and build number for each store upload. |
| A3 | P1 | The Google sign-up fix still needs a retest (see the earlier DateMeUp-google-signin-fix.md). |
| A4 | P2 | The Appetize sessions signed out repeatedly while idle. That may be Appetize, but confirm token refresh (the access token should silently refresh and stay valid for days). |

---

## 4. Fix plan (suggested order)

**Sprint A — data integrity (P0):** V1, V2, D1, D2, D3, K1, I1.

**Sprint B — group mechanics:**
- I2, I3, I4, I5 (invites)
- C1–C4 (counter-propose and deadline)
- V3, V5 (votes)
- G1–G3 (groups)
- N1, N2 (notifications)

**Sprint C — polish:** IC1–IC3, M1–M4, DQ1, A1, F1–F2, and the remaining P2s.

Add to CI an **automated API test** that runs the 3-user scenario above (create group → link join ×2 → propose → votes → note → change vote → decided; no-consensus → counter-propose → parent superseded). Most of the P0s here would have been caught by it.

---

## 5. Retest checklist (I'll run this after the fixes)
- [ ] Save a note on Yes, Maybe and No (web/iOS/Android): the vote persists and the note shows in the breakdown.
- [ ] "Tonight near me" shows only today's future events in local time.
- [ ] Past options are blocked or warned when added and when sending.
- [ ] The plan date equals the picked date or the option's start time everywhere (header chip, sidebar, title, group card, invite card, calendar).
- [ ] Add to calendar works on iOS and Android (with a permission prompt) and offers an .ics download on web.
- [ ] LINK, EMAIL and USERNAME invites from web work; the invitee sees them in-app and by email or push; the link opens the app.
- [ ] Multi-use group link: two people can join from the same link.
- [ ] Counter-propose on web and iOS: kept option prefilled, `parentId` set, parent closed.
- [ ] No-consensus: "Lock in best" and "Start over" both work; the deadline auto-resolves.
- [ ] Copy is correct for 3+ members; counters are right; all avatars show.
- [ ] Push notifications for: new plan, vote, comment, invite, friend request, match.

---

## 6. Store submission: everything needed

### 6.1 Both stores
- [ ] **Version/build:** bump `version` (e.g., 1.6.0) plus iOS `buildNumber` and Android `versionCode` (monotonic) in app.json/app.config. Rebuild with EAS (`eas build -p ios --profile production`, `eas build -p android --profile production`).
- [ ] **Bundle IDs:** iOS currently runs as `app.togetherplans.datenight`, while Android is `datemeup.app`. Decide on the final iOS bundle ID **before** first submission, because it can't be changed after the App Store listing exists. If keeping the old ID, the display name and everything user-visible must still say DateMeUp.
- [ ] **Remove leftover "togetherplans" strings** (Terminal invite card, bundle ID if renamed, any URLs/emails).
- [ ] **Privacy policy URL** (https://datemeup.app/privacy) and **Terms** (https://datemeup.app/terms) live and linked in-app (Settings → Legal).
- [ ] **Support URL** and a contact email on @datemeup.app.
- [ ] **In-app account deletion** that actually deletes server data, plus a **web deletion URL** (required by Google Play; Apple requires in-app deletion).
- [ ] **UGC safeguards** (comments, notes, photos and group names are user content):
  - report content
  - block user
  - remove a member from a group
  - a published moderation contact
  - a statement in the EULA/Terms that objectionable content isn't tolerated (Apple guideline 1.2)
- [ ] **Demo/review account** on @datemeup.app with clean data. Remove the "E2E Test Group…" leftovers and pre-populate one group with a decided plan and one open plan, so reviewers can see voting without a second device. Put the credentials in the review notes. Make sure the account doesn't hit onboarding loops.
- [ ] **Age rating:** answer honestly. "After Dark" content (bars and nightlife, alcohol references) likely means **Apple 17+** if it's mature or suggestive, or at minimum alcohol references; Google uses an IARC questionnaire, typically "Mature 17+"/"Teen". If After Dark can be disabled, consider gating it behind age confirmation.
- [ ] **Location:** clear permission strings. iOS: `NSLocationWhenInUseUsageDescription` ("…to suggest activities near you"). Android: request only coarse location if fine isn't needed.
- [ ] **Calendar permission strings** (see K1).
- [ ] **Photos permission** (invite card "Add a photo"): iOS `NSPhotoLibraryUsageDescription` / use PHPicker; Android photo picker (no storage permission).
- [ ] **Push notification entitlement and FCM config** (needed for N1).
- [ ] **Deep links:** apple-app-site-association at `https://datemeup.app/.well-known/apple-app-site-association` (and `www`); Android `assetlinks.json` at `/.well-known/assetlinks.json` with the release SHA-256 (plus the Play App Signing key's SHA-256).
- [ ] **Crash reporting/analytics** (e.g., Sentry). If any SDK collects data, it must be reflected in the privacy labels and Data safety form.
- [ ] **Screenshots:**
  - iOS: 6.9" (1320×2868) required, 6.5" optional, plus iPad screenshots if iPad is supported (or set `supportsTablet: false`).
  - Android: phone screenshots, a 1024×500 feature graphic and a 512×512 icon.
  - Suggested scenes: Discover, building a plan, group voting, the "It's a Match!" screen, invite cards, the After Dark teaser.
- [ ] **App preview video** (optional, 15–30 s). The landing-hero footage can be reused.

### 6.2 Apple App Store
- [ ] **Sign in with Apple is mandatory** because the app offers Google sign-in (guideline 4.8). Add it on iOS (expo-apple-authentication) and on the backend.
- [ ] **Google sign-in native** on iOS (iOS client ID + reversed client ID URL scheme), not a web redirect.
- [ ] **App Privacy "nutrition labels"** in App Store Connect:
  - contact info (email, name)
  - location (coarse/precise, for app functionality)
  - user content (comments, photos)
  - identifiers (user ID)
  - usage data (if analytics)
  - mark "linked to user"; no tracking unless ad SDKs are added
- [ ] **Privacy manifest** (`PrivacyInfo.xcprivacy`) declaring required-reason APIs (UserDefaults, file timestamp, etc.); Expo SDK 50+ supports this through app.json `ios.privacyManifests`.
- [ ] **Export compliance:** `ITSAppUsesNonExemptEncryption: false` (HTTPS only).
- [ ] **TestFlight:** internal testing first, then external testing (needs Beta App Review).
- [ ] **Review notes:**
  - how to test group voting with one device: use the demo account, which already has members, or the web app as the second participant
  - what After Dark is
  - demo credentials

### 6.3 Google Play
- [ ] **New personal developer account rule:** a closed test with **at least 12 testers opted in for 14 consecutive days** before production access. Start this immediately; it's the longest lead-time item.
- [ ] **Target API level:** API 35 (Android 15) is required for new apps and updates. Confirm `targetSdkVersion` in the Expo build properties.
- [ ] **App bundle (.aab)**, signed with Play App Signing.
- [ ] **Data safety form** (mirror of the Apple labels), including the account-deletion URL.
- [ ] **Content rating questionnaire (IARC)**, target audience (18+ recommended given dating/nightlife), and ads declaration (none).
- [ ] **Permissions declarations:** location (foreground only); declare calendar if it's used. Avoid `READ_MEDIA_*` by using the photo picker.
- [ ] **Store listing:** short description (≤80 chars), full description, category (Lifestyle or Social), contact email, privacy policy.

### 6.4 Google Cloud / OAuth housekeeping (from earlier work)
Already done:
- origins `https://datemeup.app` and `https://www.datemeup.app` added to Web client 1
- project renamed "DateMeUp"
- branding set to DateMeUp, with datemeup.app home, privacy and terms links
- OAuth app published "In production"

Held, to do **after** Google sign-in passes a retest and the final callback URL is confirmed:
- [ ] Remove togetherplans origins and redirect URIs.
- [ ] Remove togetherplans.pages.dev after the Cloudflare rename.
- [ ] Remove togetherplans.app from authorized domains.

Also:
- [ ] Add **API-key application restrictions** to the Maps/Places keys:
  - HTTP referrers for the web key
  - iOS bundle ID and Android package + SHA-1 for the mobile keys
- [ ] Create iOS and Android OAuth client IDs if native Google sign-in is used.

### 6.5 Release gate (go/no-go)
- All P0s in §3 fixed and retested (§5).
- Sign in with Apple live; Google sign-in retested.
- Account deletion (in-app and web), report/block live.
- Demo account clean; review notes written.
- Play closed test at 12+ testers × 14 days complete.
- Privacy labels, Data safety, age rating and screenshots done.

---

## 7. Reference IDs
- Group: `655e798f-5338-413d-9ebb-dddc51609c06` (Trio Date Club)
- Proposals: R1 `f1a9d322-af20-4e6a-8041-d07bdf311873` (decided), R2 `cd37c626-9794-46a8-a0c5-f769c843b06d` (open, no consensus), R3 `5ed9b1bd-8d9c-4582-93e0-e30153288663` (decided, past event)
- Endpoints used:
  - `POST /api/invitations {groupId, method:'LINK'|'EMAIL'|'USERNAME', target}`
  - `GET /api/groups/{id}`
  - `GET /api/proposals/{id}`
  - `GET /api/friends`
  - `GET /api/friends/requests`
- Related docs: DateMeUp-full-test-v1.5.0-2026-11-15.md, DateMeUp-google-signin-fix.md, DateMeUp-signup-displayname-fix.md
