# DateMeUp — final 3-account test (2026-11-15, 8:10 PM ET)

**Builds tested:**
- iOS **v1.6.3** (Appetize, Jake)
- Android **v1.5.0** (Appetize, Demo Reviewer)
- Web: datemeup.app (G R)

**Test plan:** "Final 3-way test" in Trio Date Club (proposal `4cf38a96-6b93-4556-b191-7dccb19e396b`), created on web. All three accounts voted "in" on the George Washington basketball idea.

## Files Hermes needs (this report is one of six)

| File | What it's for | If they conflict |
|---|---|---|
| `DateMeUp-3-participant-test-and-store-readiness-2026-11-15.md` | Earlier fix queue + store checklist | — |
| `DateMeUp-craft-polish-implementation-spec-2026-11-15.md` | Tokens, haptics, card renderer, backend pieces | Superseded where the handoff says so |
| `DateMeUp-design-handoff-ticket-system-2026-11-15.md` | **The design to build**: 54 per-screen parity checklists | Wins over the craft spec |
| `DateMeUp-decisions-addendum-2026-11-15.md` | Remove/leave group, Sign in with Apple, one category list, no sample content, ticket spinner | Wins over both above |
| `DateMeUp-design-boards-source-2026-11-15.zip` | Board HTML for every screen (latest: includes M12b member actions + spinner board) | — |
| `DateMeUp-logo-package-2026-11-15.zip` | Admit two icons for iOS/Android/web, lockups, OG image, spinner code, README | — |
| **This file** | What's still wrong in the current builds | Newest; fix these first |

### Build/config items decided tonight (not in the files above)

- **Bundle IDs:** iOS `app.togetherplans.datenight`, Android `datemeup.app`. Don't use `app.datemeup`. Change display names only.
- **Apple App ID:** Associated Domains is now enabled (Sign In with Apple + Push were already on). The old provisioning profiles are invalid, so regenerate them with `eas credentials` / `--clear-credentials-cache`.
- **Android versionCode must be ≥ 5** (Play internal track already has 4). A draft internal release with notes is waiting in Play Console.
- **Ads: keep AdMob.** See "Next build checklist" item 4 below. Store privacy forms were filled in on that basis.
- **Review demo account:** clean the Demo Reviewer account (F9), or create a dedicated one, and seed one open plan and one decided plan. Its credentials get entered by the owner in Play "Sign in details" and in App Store Connect App Review.
- **Store copy:** the App Store listing is now named "DateMeUp" with new description/keywords; the Play listing draft is "DateMeUp: Plan Date Night". The in-app display name must match: "DateMeUp".

## Retest — 9:45 PM (iOS 1.6.3 new build, Android 1.6.3, web)

**Fixed ✓**
- Landing: "Plan together." now white; the hero phone autoplays `tour-9x16.mp4` (muted, looping); the "Video frame" placeholder is gone.
- Web nav logo is now Admit two.
- Android is now on 1.6.3, the same build line as iOS.
- Welcome screens on iOS + Android: "DateMeUp" lockup with the Admit two mark, no blobs, no heart badge. Sign in with Apple is on iOS.
- Android vote buttons: I'm in / Maybe / Not for me.
- Android group page: the new ticket layout, all 3 avatars, DECIDED stamps, member ⋯.
- Android Profile: Delete account present.

**Correction to B5:** the coral-arrow favicon I reported was Claude in Chrome's tab indicator, not the site. The site's real `/favicon.svg` is wrong in a different way: it's an **old purple calendar icon** (`#aa3bff`). Replace it with `web/favicon.svg` from the logo package; `favicon.ico` probably needs the same fix.

**Still open**
- **F1 onboarding loop:** still shows after every sign-in (Android, retested).
- **F2/F3 vote counter:** Android plan header "2 of 3 voted" vs the group stub "3/3 VOTED" on the same plan.
- **F4 dates, now worse:** when "Final 3-way test" locked, the plan date silently changed from **Fri Nov 20 7:30 PM → "Sun Nov 15 · Tonight at 7:00 PM"** (the winning idea's date, already past). Ideas must keep the event's real date, and the plan's own date must not be overwritten on lock (or ask first). This also triggers "Rate your date" early (F6).
- **F7 member menu:**
  - Mobile is still the system alert "Choose an action: Block user / Report user / Cancel", not the branded sheet.
  - No **Remove from group** on any platform.
  - **No Leave group on mobile** (your own row isn't listed; no Leave in the group page).
- **F9 test data is back:** 3 new "E2E Test Group 17947…" groups were created on demo@togetherplans.app **after** tonight's cleanup (timestamps ≈ 9:15–9:35 PM). The E2E suite is writing to production with the demo account. Point it at a test DB or a dedicated `e2e@` account, then re-run the cleanup.
- **F10:** "You both said yes 🎉" for 3 people (web + mobile).
- **New: review account seed (review@datemeup.app) isn't usable:**
  1. Review Crew has **only the reviewer** as a member.
  2. **"Weekend plans" (open) doesn't appear**: the group page shows the "First proposal" empty state, yet the Plans list says "1 open · 1 decided".
  3. "Friday night out" is "LOCKED IN / You both said yes" but both options say **"No votes yet"**.
  4. The display name is **"App"**.

  The review notes in both stores tell reviewers to vote on "Weekend plans", so this must be fixed before submitting.
- **New: Android match sheet can't be closed:** neither back nor tapping outside dismisses "It's a Match!"; the user is stuck.
- **Android Profile:**
  - "10 PLANS DECIDED" stamp clipped off the left edge
  - "Widget preview (coming soon)" still listed
  - emoji icons (📍 💚 📱 and flags)
  - Notifications, After Dark and Your data/export screens still missing on mobile
- **Copy/emoji (all platforms):** unchanged from the list below. "New proposal", "IT'S A MATCH", "Hearts stay hidden", "DONE" stubs, and emoji on the plan and match screens are all still there.
- **Web app screens:** dashboard, Discover, new-plan and invite-card picker are unchanged (old design).
- **Landing:** still not full-bleed at wide widths (hero 1077px inside a 2560px viewport).
- **iOS (retested, 1.6.3 new build):** same results as Android for F1 (onboarding loop), F7 (system alert Block/Report only, no Remove, no Leave), the "New proposal" label and the Profile issues. iOS-only:
  - the log-in screen has a **third tagline**, "Plan night together." (the welcome screen says "Date night, decided."; web says "Plan together. Go together."). Use one tagline everywhere.
  - **"Sign in with Facebook" appeared on iOS only.** If it stays: add it to Android/web, add Facebook Login to the privacy policy and both stores' privacy answers, and get the Meta app reviewed. Otherwise remove it.
  - emoji on the Email/Phone tabs (✉️ 📱)
  - **Profile avatar initials are clipped** (only the top of "J" shows)
  - overlapping group avatars still clip "JY"
- **Landing video:** don't re-record yet. Most screens in the shot list (plan/vote, match, Discover, invite card) are still the old design. Re-shoot once they're on the ticket system.
- **iOS welcome mark:** shown as a hard-edged navy square. Use the bare mark or a rounded tile (same on Android).

## Verdict

**The core flow works.** Create plan → send to group → 3 votes on 3 platforms → plan locks, and every platform updated in real time.

**Not ready to submit.** The ticket-system design handoff is mostly not implemented. The release gate also fails on: the onboarding loop, the vote counter, wrong idea dates, the review-account clutter, and a missing "Remove from group".

Android is **v1.5.0** while iOS is **v1.6.3**. Is the Android Appetize upload an older build? Please confirm, and upload the current one.

---

## P0 — fix before submission

| # | Platform | Bug | Repro / evidence |
|---|---|---|---|
| F1 | iOS + Android | **Onboarding shows after every sign-in** | Sign in → "Sound familiar?" onboarding every time (seen twice on each platform) |
| F2 | iOS + Android | **"0 of 3 voted" header never updates** | Group list shows 2/3 and the card shows "2 votes", but the plan header still says "0 of 3 voted". Android's banner says "A member voted · waiting on you" next to "0 of 3 voted" |
| F3 | Android | **Group list counts are stale** | Plans list said Trio Date Club "1 open" after the new plan existed (iOS correctly said "2 open") |
| F4 | All | **Idea dates are wrong** | Plan is for Fri Nov 20, 7:30 PM. Both ideas show "Sun, Nov 15 · 07:00 PM" (today). Discover listed the basketball game for a different day. The date isn't carried over from Discover, or it's overwritten |
| F5 | Web | **Reminder after the event** | "Reminder: Fri 8 PM, if not everyone's voted" for a 7:30 PM plan |
| F6 | Web | **"Rate your date" shown immediately** on a decided plan that's 5 days away | Should only appear after the plan's date/time |
| F7 | Web | **No "Remove from group" for the owner** | G R (owner, sees Delete group) → member ⋯ menu shows only Block user / Report user. See decisions addendum §1. Leave group is present ✓ |
| F8 | Web | **"Lock in …" button text spills out** of the button, over "Save note" and into the sidebar, after voting "I'm in" | Plan page, first idea |
| F9 | Android | **Demo Reviewer account is cluttered** with ~10 "E2E Test Group 1794…" groups | Must be clean before App Review / Play review |
| F10 | Mobile | Match screen says **"You both said yes"** in a 3-person group | iOS and Android |

## P1 — branding and landing

| # | Where | Issue | Fix |
|---|---|---|---|
| B1 | Web landing | **"Plan together." is invisible**: h1 first line is #1E1A38 on navy | Make it white |
| B2 | Web landing | **Hero phone shows a "Video frame" placeholder.** The only video (`/tour-16x9.mp4`) is at the bottom and `autoplay=false` | Put the tour video in the hero phone: autoplay, muted, loop, playsinline, poster. Keep "Watch with sound". Remove the placeholder |
| B3 | Web landing | Hero isn't full width (1077px box with grey bands at 2560px) | Make the night background full-bleed |
| B4 | Web | **Nav mark is the ticket-with-check (option 2)**, not Admit two | Use `lockups/lockup-on-light.svg` |
| B5 | Web | **Favicon is an unrelated coral arrow** (inline data-URI SVG) | Use `web/favicon.svg` + `favicon.ico` from the logo package |
| B6 | iOS + Android | Welcome screen shows **"datemeup" lowercase** + old tagline "Date night, decided." with blobs. iOS shows the ticket tilted in a teal circle with a heart badge; Android shows the old two-figure logo | Use the lockup "DateMeUp". No badge or circle |
| B7 | Android | Log-in screen: old calendar logo, **"DateMeUp!"**, "Plan together, decide together" | Same lockup |
| B8 | Android | App icon still the old two-figure mark (Appetize listing icon) | Logo package `android/` |
| B9 | iOS | Onboarding "47 MESSAGES LATER" chip is **white on white** | Ink chip |
| ✓ | Web | og-image and apple-touch-icon are the new Admit two assets | — |
| ✓ | iOS | Sign in with Apple present on welcome | — |
| ✓ | Web | Display name now shows "G R" | — |

## P1 — copy still old

- "Hearts stay hidden until everyone has voted" (web plan page, Who's voted). There are no hearts now: "Votes stay hidden until everyone has voted."
- "It's a Match! 🎉" / "IT'S A MATCH" / "LOCKED IN" → **"It's a plan."** (the iOS match screen has both the new stamp and the old headline)
- Vote chips on the match screen say "✓ Yes" → "I'm in"
- Android vote buttons are still **"Yes 👍 / Maybe 🤔 / No 🙅"** → I'm in / Maybe / Not for me (web and iOS are correct ✓)
- "New proposal" (iOS + Android group page) → "New plan"
- "Add to Date" (web Discover, dashboard) → "Add to plan"
- Past plans: iOS stub says "DONE", web says "Decided" → **"It's a plan"** (stamp)
- Old "Finalize Your Plan." page title on web new-plan
- Android vote chips truncate G R to "G:"

## P1 — emoji still in UI (handoff rule: no emoji; Phosphor icons)

- **Web:**
  - new-plan "Send to Trio Date Club ♥" and the heart in the message placeholder
  - plate emoji placeholders on dashboard cards
  - the mobile-width nav (⌂ 📋 🧭 👥 ⚙️)
  - plan page 📤 🏆 📅 ⭐
  - support / footer 🍎 ▶
- **iOS + Android plan page:** 🗳 📋 🕐 📍 📅 👆
- **Match screen:** 🎉 👍 📅 💌 and the party-popper illustration
- **Discover:** 🌙 "Tonight near me"

## Design handoff status (screen by screen)

Implemented means it matches the ticket-system boards. Partial means some tokens are in (font, colours, outlines) but the old layout remains.

| Screen | iOS 1.6.3 | Android 1.5.0 | Web |
|---|---|---|---|
| Welcome / Sign up / Log in | Old (Apple button added) | Old | — |
| Onboarding 1–4 | Old copy, new button style | Old | — |
| Plans home | **Partial**: ticket stubs on past plans; floating tab bar overlaps the list | Old | **Partial** (dashboard: old teal hero, old cards) |
| Group page | **Partial**: ticket stubs, DECIDED stamps, member ⋯; avatars overlap/clip "JY" | Old; shows 2 of 3 avatars | Old layout + Leave/Delete group |
| Plan / vote | Partial: new vote labels, old layout + emoji | Old | Partial: new vote labels |
| Match / decided | Mixed (stamp + old match) | Old | Old |
| Discover / Results | — not reached | — | Old (multicolour category tiles) |
| New plan | — | — | Old |
| Invite card picker | — | — | Old (32 designs) |
| Landing | — | — | **New**, with bugs B1–B3 |

Not re-checked this pass: Profile, Friends, Notifications, After Dark, Home area, Your data, Settings, Legal, 404, spinner. They're blocked on the design implementation; I'll re-run the full per-screen parity checklists when the next builds include the handoff.

## Works ✓

- Creating a plan from Discover on web and sending it to a group
- Real-time sync: web, iOS and Android all showed the lock within seconds
- Three-platform vote → lock on the matching option
- Leave group present on web
- The earlier Android sign-out was Appetize's session expiring, not an app crash. Opening the group again worked fine.

## Next build checklist

1. Fix F1–F10.
2. Implement the design handoff on mobile (Android especially), starting with the screens in the table.
3. Branding B1–B9 from `DateMeUp-logo-package-2026-11-15.zip`.
4. Ads (decided: keep): add the ATT prompt + `NSUserTrackingUsageDescription`, the UMP consent form (EEA/UK), SKAdNetwork IDs, live AdMob app ID, `app-ads.txt` on datemeup.app, and a `/delete-account` web page. Change the homepage "Free, no ads" → "Free".
5. Upload the matching Android build to Appetize (and the AAB to Play internal testing, versionCode ≥ 5).
