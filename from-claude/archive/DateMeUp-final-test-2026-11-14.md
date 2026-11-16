# DateMeUp Final Test: Web, iOS & Android

**Date:** Sat 14 Nov 2026, 7:05–7:15 PM ET

**Builds tested:**
- Web: datemeup.app
- iOS: v1.3.0 on iPhone 14 Pro / iOS 17.2 (Appetize), signed in as Jake
- Android: v1.3.0 on Pixel 7 / Android 13 (Appetize), signed in as Demo Reviewer

> ⚠️ **The phones are still running v1.3.0, the same build tested earlier today.** Hermes's mobile fixes haven't been uploaded to Appetize, so every app-side bug below is unchanged. Upload the new iOS and Android builds to Appetize (or TestFlight / internal testing) and run this test again. Server-side changes (winner logic, counts, dates) did show up, and are reported below.

## Two-account test

- Demo proposed from the **web** and voted Yes on all three options.
- Jake voted from **iOS**:

| Option | Demo | Jake | Should win? |
|---|---|---|---|
| Ford's Fish Shack South Riding | Yes | **No** | No |
| Mamma Mia! (Sat, Nov 14, 7 PM) | Yes | **Maybe** | No |
| Trey Anastasio Band (Sat, Nov 14, 7 PM) | Yes | **Yes** | **Yes** |

| Where | Winner shown | Correct? |
|---|---|---|
| Server / web result page | **Trey Anastasio Band**, "✓ You both said yes" | ✅ **Fixed** |
| iOS app (v1.3.0) match screen | **Ford's Fish Shack**, "You both loved Ford's Fish Shack and Mamma Mia!" | ❌ Picked an option Jake voted **No** on |

The server now picks the right winner. The v1.3.0 app works out its own winner on the phone, using the old logic, and shows that instead.
- **Fix:** the apps must show the server's decided winner and never work it out on the device.
- **Before release:** confirm the new mobile builds do this.

---

## 🔴 Blockers

### 1. Mobile builds haven't been updated (iOS and Android)
Every app-side fix from the last report is missing because v1.3.0 is still installed:
- The bottom tab bar still doesn't respond. Discover and Profile do nothing on either phone.
- Onboarding still shows on every sign-in, on both phones.
- The iOS match screen still picks the wrong winner on the phone (see the table above).

Upload the new builds before any store submission.

### 2. Event dates are shifted one day earlier (web, and every app that uses the data)
- Discover lists Mamma Mia! and Trey Anastasio Band as **Sat, Nov 14**. The finalize screen, proposal and result all show **Fri, Nov 13 · 7:00 PM**.
- The "When?" field is now filled in from the activities (good), but with `2026-11-13T19:00`, which is earlier than the field's own minimum (`2026-11-14T19:11`).
- The plan sent anyway, so nothing checks for a past date.
- The pre-filled title "Date Night · Friday" is also wrong on a Saturday.
- This is almost certainly a time-zone problem: a local event time is stored or converted as UTC and then read back as a date.
- **Fix:**
  - Store each event's date and time with its time zone (or as a local date plus a time zone).
  - Format it in the event's own time zone.
  - Base the default title on the same date.
  - Block sending a plan whose date is in the past.
- **Acceptance:** a Sat, Nov 14, 7 PM ET event shows as Sat, Nov 14 · 7:00 PM in Discover, the proposal, the result, the calendar file and the group's past-plans list.

### 3. The result page says everyone agreed on options they didn't (web)
- The winner box is correct. But the full list labels **every** option "✓ Everyone picked this": Ford's (Jake said No) and Mamma Mia! (Maybe) included.
- **Fix:** show each person's actual vote per option ("Demo: Yes · Jake: No"). Use "Everyone picked this" only when every vote is Yes.

---

## 🟠 High priority

### 4. "Open app →" in the teal band is invisible (web landing page, new)
In the "Friday's sorted by Tuesday." band, the button is **white text on a white background**, so it looks like an empty white pill. Its text should be `#084C4A`, as in the spec.

### 5. The video button never changes (web landing page, new)
The "See it in action" video works well:
- It autoplays muted and looped once it scrolls into view.
- The source is right, `preload="none"` is set, and it's about 0.5 MB.

But the button stays on **"Play the video"** with a ▶ icon the whole time. Clicking it does pause and resume the video; only the label and icon never change.
- **Fix:** listen for the video's `play` and `pause` events and update the icon and `aria-label` from them, not from the click.

### 6. Counters still disagree
- In the iOS app, the group card showed "0 / 2 voted" after Demo had voted on all three. The proposal screen itself correctly said "1 of 2 voted" (**fixed** there).
- On iOS, the group header shows **"DR" twice**. Android shows "DR · JY" correctly.
- On the web, the group page still shows "No plans yet. Start one." next to "Past plans (3)".
- Android's Plans list didn't refresh after the decision: "3 decided" and no "Final test vote" until the group was opened.

### 7. Vote counts show before you vote (iOS, regression)
Jake saw "1 vote" on each option before voting. Last test, nothing showed until you voted. The web text says "Hearts stay hidden until everyone has voted", so the apps should hide counts until then too.

---

## 🟡 Medium priority

### 8. Discover category colors (web): mostly done, four mismatches with spec v4
| Category | Spec | Live |
|---|---|---|
| After Dark | `#A24A66` | `#C2255C` (still the old bright pink, the loudest pill on the page) |
| Bars & Nightlife | `#9C5F38` (Eat & drink) | `#A24A66` (After Dark's color) |
| All categories | `#2B3532` | `#111418` |
| After Dark, Fun Ideas | `aria-pressed` | missing |

The other 14 categories match exactly, and the selected state uses the new same-color offset ring.

### 9. Couples Events has no group in the spec
It's showing Stay in violet `#6A5AA8`, which works. Add it to that list in the spec so it doesn't drift.

### 10. Past plans don't open (Android)
Tapping "Final test vote" under Past in the group did nothing.

### 11. A stale draft follows you around (web)
"Plan (1)" (Ford's Fish Shack, left over from an earlier session) showed on the landing page and the group page. Offer to clear or resume it once, then stop showing it on marketing pages.

### 12. The landing listings show stale or generic items (web)
- The hero panel shows "Eyes of the Nile: Iron Maiden Tribute · Tonight". Earlier today the app dated the same event **Fri, Nov 13**, so it may be the same date bug as #2.
- Arts & Culture and Sports still use a generic ★ icon.

### 13. Still open from earlier
- The hero headline wraps to 4 lines on desktop.
- Store badges are dark-on-dark.
- The couple recipient label shows the group name ("Send to Jake Testing Group") instead of the partner's.
- All mobile-only items from the previous report (#7–#17) are untested because the build is unchanged.

---

## ✅ Verified fixed in this pass
- **Winner logic on the server:** the all-Yes option wins over Yes+No and Yes+Maybe.
- **"See it in action" section,** built to spec:
  - placed below How it works
  - autoplays in view, muted, looped, inline
  - `preload="none"`, 1280×720 desktop file, poster set
  - hidden text description for screen readers
  - App Store / Google Play buttons
- The hero button says "Watch the 30-second tour" and jumps to the video.
- Discover uses the muted solid colors for 14 of 18 categories, with the same-color offset-ring selected state.
- The "When?" field is filled in from the activities (logic present; see #2 for the date error).
- The proposal screen's voter count ("1 of 2 voted") is now correct.
- Notes on options have a **Save note** button on the web.
- No "Hmm, two hearts" banner after a No vote.
- The FAQ and the business-portal link are present on the landing page.

---

## Fix order
1. **Upload the new iOS and Android builds**, then rerun this test (tab bar, onboarding, winner shown from the server).
2. **The one-day date shift** (#2), plus blocking past dates.
3. **Honest per-option result labels** (#3).
4. **Landing page quick fixes:** the invisible teal-band button (#4) and the video button state (#5).
5. **Counters, avatars, hidden counts and Android refresh** (#6, #7).
6. **The four color mismatches** (#8) and the remaining medium items.
