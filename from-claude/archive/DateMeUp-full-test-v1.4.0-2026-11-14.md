# DateMeUp: Full Test, v1.4.0 (Web, iOS & Android)

**Date:** Sat 14 Nov 2026, 11:15 PM–11:35 PM ET

**Builds tested:**
- iOS v1.4.0 on iPhone 14 Pro / iOS 17.2 (Appetize)
- Android v1.4.0 on Pixel 7 / Android 13 (Appetize)
- datemeup.app

**Accounts:** Demo Reviewer and Jake (Yahoo). Both were used on the phones and on the web.

**What I exercised:**
- Onboarding
- Plans, groups and the tab bar
- Profile: friends (search, request, accept), notifications, language (Español), appearance, account
- Discover: location allowed and denied, ZIP search, categories, add to plan, plan tray, Done
- Proposing from Android to a group
- Swipe-to-vote and list voting
- Notes and the Android keyboard
- Two-account vote and match
- Per-person vote breakdown
- Invite card gallery and customise
- Web: landing, notifications, settings, After Dark, 404 page

**This round's vote test:** Jake proposed from Android; Jake voted Yes ×3 on Android; Demo voted on the web.

| Option | Jake | Demo |
|---|---|---|
| Running Dish | Yes | No |
| Ethiopian Buffet | Yes | Maybe |
| **Kylie Morgan** (Thu, Nov 19, 7 PM) | Yes | **Yes** |

**Result: Kylie Morgan, correct on Android and the web.** ✅ The Android match screen now shows **"How everyone voted"** with each person's vote per option.

---

## ✅ Fixed since the last pass
- **Version bumped to v1.4.0** on both apps.
- **Bottom tab bar works** on iOS and Android.
- **Winner logic is correct** across platforms. The web result labels only the real all-Yes option "You both said yes".
- **Per-person vote breakdown** on the Android match screen (Jake ✓ Yes / Demo ✗ No / Demo ~ Maybe).
- **"+ Add to Date" adds directly** on mobile, with a "2 options added · tap to review" banner.
- **Mobile "Your Plan" tray** (3/5, remove ×, Finalize, Keep browsing) matches the web.
- **The Discover sheet has a Done button.**
- **Android keyboard** now scrolls the focused note field above it.
- **Single back button** on group and proposal screens.
- **Friends system:**
  - Find People → Add Friend → "Requested ✓"
  - Requests (1) shows on the other device → Accept
  - A "Plan date" shortcut on each friend
- **Location allowed** shows "Near Ashburn · 25 mi"; **location denied** shows a working City/ZIP prompt.
- **Swipe-to-vote mode** exists ("← No · Yes →, ↑ Maybe"), with a List view toggle.
- **Optional vote deadline** on mobile and web.
- **Web group page** lists the open proposal under Proposals; the "No plans yet" contradiction is gone.
- **Fortune Cookie invite design** now exists.
- **Web extras:**
  - a good 404 page ("Lost? Page not found · Go to my plans")
  - GDPR/CCPA data export and deletion in Settings
  - After Dark loads with a dark theme

---

## 🔴 Must fix before submission

### 1. Invite cards: wrong data, broken saving, unfinished templates (web; check the apps)
- **Previews show sample data, not the plan.**
  - Ticket Stub shows "JAKE & SARAH PRESENTS · Saturday Night Out · Jazz at Blue Room · Sun, Sep 27 · 2051 Welton St, Denver CO".
  - Fortune Cookie shows "Saturday Night Out · Sat, Nov 15 · 7 PM · Sam & Riley".
  - The plan was actually Kylie Morgan, Thu Nov 19, Leesburg VA, Demo & Jake.
- **Raw template code is visible:** Ticket Stub shows the literal text `{{ p.i }}`.
- **Old brand:** Ticket Stub prints **"TOGETHERPLANS.APP"**. Search every template for `togetherplans`.
- **"Use this card ✓" fails** with "Something went wrong. Please try again." I tried twice on a decided plan, with a note.
  - The browser's pre-check (`OPTIONS https://api.datemeup.app/api/invite-cards/{id}`) returned 204, but the actual save request was never logged.
  - That points to CORS: the API's preflight probably doesn't allow the method or headers the save uses.
  - Or the save is rejected because the plan is already decided.
- **Four empty placeholders remain:** 4b Matchbook, 4c Crossword, 4d Recipe card, 4e Library card, still counted in "36 designs".
- **Fortune Cookie layout:** all the content sits in the top third of the card; the bottom two-thirds is empty red.
- **Android:** "Pick an invite card" on the match screen did nothing when tapped.
- **Fix:**
  - Fill every template with the plan's real data (title, winner, venue, date and time, both names).
  - Remove leftover `{{ }}` text and the TogetherPlans branding.
  - Fix the save request.
  - Hide 4b–4e and show the correct count.
  - Lay out Fortune Cookie as in the promo video.
  - Make the Android button open the gallery.

### 2. Dates are still wrong in several places
- The plan title says **"Date night · Thursday"**, but the date chip and the web say **Fri, Nov 20, 12:00 PM**. Its only dated event is **Thu, Nov 19 · 7 PM**.
- The web result's date panel says **"This Friday at 12:00 PM"**. That's both the wrong day and an odd noon default.
- **Reminders go out on the wrong day:** the notification "Tomorrow: Re-review vote test 🎉" was sent Sat 14 Nov at 5 PM for a plan whose event is **Tue, Nov 17**.
- The previous pass's one-day shift (Sunday events shown as Saturday) is still there in older plans.
- **Fix:**
  - Default the plan date to the earliest dated activity, in the event's time zone.
  - Make the title match the date.
  - Schedule reminders from the winning event's real start time.
  - Block plans whose date is in the past.

### 3. Discover results are still miscategorized
- Comedy, near Ashburn with location allowed, still returns **Ethiopian Buffet** and **Running Dish**. Both are restaurants, tagged COMEDY.
- The other data-quality problems from the last report are unchanged: offices and memorials tagged Dining, parks tagged Comedy, a Pittsburgh bar shown as 27 mi away.

### 4. Onboarding still shows on every launch (iOS and Android)
It appeared on both phones at the start of this session, and again on iOS after the app restarted.

### 5. The iOS app restarted and switched accounts
- After about six minutes in the background, the iOS app restarted to onboarding.
- After skipping, it was signed in as **Jake**. It had been **Demo** a few minutes earlier, with "Good evening, Demo".
- This may be Appetize restoring an older session, but it needs checking. Confirm sign-in tokens are stored per account and that a cold start restores the last signed-in user.

---

## 🟠 High priority

### 6. Spanish is only partly translated (iOS and Android)
With Español selected, these parts are translated:
- Perfil, Planes, Descubrir
- Nueva propuesta, Tu Plan, Título
- Invitar a votar, Ver Plan, Volver a Grupos

These are still English:
- Connections, Friends, Requests, Find People, "No connections yet"
- New Proposal (header), "Add another activity", When?, Date & Time, Vote deadline, Plan with
- "Send to Jake Testing Group"
- **Every category name** (Comedy, Concerts, Family Activities…)
- "Discover Activities", "+ Add to Date", "Done"
- "Swipe to vote", "List view", "Send via DateMeUp", "Let them know"
- Preferences, Appearance, Account
- **Mixed phrases:** "Sent to Jake Testing Group ❤️" sits above a Spanish line.

The language setting also **carried over to the next account on the same device**: Jake's Android was in Spanish because Demo had picked it earlier. Store language per user, or per device on purpose.

### 7. Counters and avatars
- iOS still shows **"DR" twice** in the Jake Testing Group header.
- "Us Two · 1 open · 0 decided" still shows an open plan that doesn't exist.
- **Vote counts show before you vote** ("1 vote" visible to the second voter). The web says hearts stay hidden.

### 8. Notifications (web)
- "Everyone's waiting on you 👀" stays unread after the plan is decided. Clear or resolve vote reminders once a plan locks in.
- There's no "Mark all read".
- Timestamps use the raw `11/14/2026, 11:22:07 PM` format. Use relative times ("5 min ago").

### 9. Notes on options still have no Save button (iOS and Android)
The web has "Save note"; the apps don't, and Enter doesn't submit. It's unclear whether mobile notes save or who can see them.

### 10. Swipe-to-vote doesn't move to the next card
A right swipe registered Yes, but the card stayed put. It should animate off and show the next option, with a "1 of 3" progress indicator.

### 11. Proposal form layout (Android)
The "3 options added · tap to review" banner and the Send button cover the Title / When? section. You have to scroll from a precise spot to reach the date. The banner is redundant on the form screen; hide it there.

---

## 🟡 Medium

12. **Privacy of Find People.** Searching "Jake" returned four accounts (Jake, Jake, Jake Agent, Jake (Yahoo)) with names and initials. For a dating and couples app, let people opt out of being searchable, or search by exact username, email or phone only.
13. **Group members aren't connections.** Demo and Jake share a group but showed "No connections yet". Suggest group members as friends automatically.
14. **After Dark:**
    - Every card is tagged "🔥 Spicy", including "Make a couples playlist" and "Cook a 3-course meal", so the tag means nothing. Use real levels or drop it.
    - There's no age confirmation before entering. Add an 18+ gate (App Store age-rating and Play content-rating consistency).
15. **Web Settings vs. app Profile.**
    - The web Settings page has no notification toggles or appearance option; the apps have both.
    - "Email: demo@togetherplans.app" exposes the old domain on the demo account. That's fine for testing, but the App Review demo account should use @datemeup.app.
16. **The web past-plans list isn't in date order:** Feb 19, Nov 15, Nov 14, Nov 13, Oct 25. Sort by plan date, newest first.
17. **The 404 page title** is the generic homepage title. Use "Page not found · DateMeUp".
18. **Location prompt timing (Android).** Location is now asked the first time you tap the Discover tab. That's good, but on Android the system dialog appears with no lead-in screen. Add a one-line explanation before the system prompt, as iOS has.
19. **Carried over from the last report, not rechecked this round:**
    - the hero App Store / Google Play badge contrast
    - three web category colors (Bars & Nightlife, All categories, `aria-pressed`)
    - Android content scrolling under the status bar
    - the rating prompt covering the match card
    - mobile Discover using emoji icons

---

## 💡 Recommendations
1. **Invite cards:** make every template a data-bound component, with one renderer shared by the preview and the sent card. Add a test that renders each template with a fixture plan and fails on `{{`, "togetherplans" or sample names (Jake & Sarah, Sam & Riley, Blue Room).
2. **One date source:** the plan date, title, reminders, calendar file and "How was it?" prompt should all come from the winning activity's time-zoned start time.
3. **Translations:** move every UI string to translation files, then run a "pseudo-locale" build (all text shown as e.g. `[!!Ĉőmédý!!]`) to spot anything hard-coded. Six languages besides Spanish are offered and probably have the same gaps.
4. **Discover filtering:** whitelist place types per category, drop anything that doesn't match, and hide events that have started.
5. **Automated end-to-end test:** two accounts; propose, vote No/Maybe/Yes, decide; pick an invite card and send it; check the reminder time. Run it on every build. This pass would have caught #1, #2 and #10.
6. **Before submission:** create clean App Review accounts on @datemeup.app with a pre-made group and one open plan, so the reviewer sees a populated app.

---

## Fix order
1. Invite card data, saving and placeholders (#1)
2. Dates and reminders (#2)
3. The account switch on restart (#5) and the onboarding flag (#4)
4. Discover categories (#3)
5. Spanish strings and per-user language (#6)
6. Counters, hidden counts, notifications, notes, swipe-to-vote (#7–#11)
7. Medium items
