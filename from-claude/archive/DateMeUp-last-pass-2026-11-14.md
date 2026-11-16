# DateMeUp: Last Full Pass, Web, iOS & Android

**Date:** Sat 14 Nov 2026, 9:00–9:10 PM ET

**Builds tested:**
- Web: datemeup.app
- iOS: iPhone 14 Pro / iOS 17.2, signed in as Jake
- Android: new upload `b_xwlfig…` on Pixel 7 / Android 13, signed in as Demo

Both apps still report **v1.3.0** in Appetize, but both are clearly new builds. **Bump the version and build numbers** before submitting, or the stores will reject the upload as a duplicate.

## Two-account test

- Demo proposed from the web and voted Yes ×3 on **Android**.
- Jake voted on **iOS**:

| Option (Discover date: Sun, Nov 15) | Demo | Jake |
|---|---|---|
| Madama Butterfly | Yes | No |
| Daniel Sloss: BITTER | Yes | Maybe |
| **Gilla Band** | Yes | **Yes** |

**Result: Gilla Band on all three platforms** ✅
- iOS match screen: "You both said yes to this one 👍".
- Android updated live with the same match.
- Web: "🏆 Winner · Gilla Band · ✓ You both said yes". The other options read "You've voted on this one · 2/2" instead of falsely claiming agreement.

---

## ✅ Fixed since the last pass

**Mobile**
- **Bottom tab bar works** on iOS and Android: Discover and Profile open.
- **The winner is correct in the apps,** matching the server.
- **Profile is reachable** and shows "4 plans decided" (correct).
- Profile has new sections: Home area, Favorite categories, a widget preview, Appearance (System / Light / Dark), and **Delete account** (Apple requires one).
- **Single back button** on the group and proposal screens.
- **Muted category colors** in mobile Discover.
- **Event dates** now show on each proposal option.
- **App Store rating prompt** appears at the match moment (see #6 for its timing).
- "How was it? Rate it" follow-up added.
- Live sync: Android showed the decision as soon as Jake voted on iOS.

**Web**
- The teal band's "Open app →" is readable (`#086B6B` on white).
- The video's play/pause button now switches label and icon correctly.
- After Dark now uses the muted `#A24A66`.
- Result labels: only the true all-Yes option says "You both said yes".
- **Vote deadline (optional)** field added to Finalize.
- The default title follows the plan date.

---

## 🔴 Must fix before submission

### 1. Event dates are still one day early (all platforms)
- Discover lists Madama Butterfly, Daniel Sloss and Gilla Band on **Sun, Nov 15**. Finalize, the proposal (web, iOS, Android) and the result all show **Sat, Nov 14 · 7:00 PM**, and the web result says "Tonight at 7:00 PM".
- "When?" defaults to `2026-11-14T19:00`, two hours in the past, below the field's own minimum (`2026-11-14T21:03`).
- **The plan still sends with a past date.**
- Because of the wrong date, "How was it? Rate your date" appears for a date that hasn't happened.
- **Fix:**
  - Store event times with their time zone and format them in the event's time zone.
  - Block sending when the date is in the past.
  - Show "How was it?" only after the event's real end time.

### 2. Version numbers
Both builds say v1.3.0. Bump the marketing version (e.g. 1.4.0) and the build number on both platforms.

### 3. Onboarding still shows on every sign-in (iOS and Android)
It showed again for both accounts on the new builds.

### 3a. Five invite card templates are empty placeholders (web; check the apps)
- On "Pick an invite card" (heading says "36 designs"), the last five tiles show only an internal ID on a pale-teal block:
  - **4a Fortune cookie**
  - **4b Matchbook**
  - **4c Crossword**
  - **4d Recipe card**
  - **4e Library card**
- They can still be picked. Choosing Fortune cookie opens "Customise your card" with a **blank "4a" preview** and an active **"Use this card ✓"** button, so a person could send their date an empty invite.
- **Fortune cookie is the card shown in the landing page phone loop, the "See it in action" video and the App Store promo video.** People will look for it, and it's the one that's broken.
- **Fix:**
  - Build Fortune cookie first, to match the promo (red card, cookie halves, the fortune slip with the date, "IT'S WRITTEN", the plan name and the date block).
  - Hide 4b–4e behind a feature flag until each is finished, and update the count ("31 designs").
  - Never show internal IDs like "4a" to users.
  - Disable "Use this card" for any template without a finished design.

---

## 🟠 High priority

### 4. Discover data quality (web, and the apps that use the same feed)
"All categories" mixes in places that aren't date ideas, and miscategorizes others:
- **Tagged "Dining":**
  - offices and government buildings: Booz Allen Hamilton, Micron Technology, Northrop Grumman, the US Census Bureau, the State Department
  - other non-restaurants: Wheaton High School, Amtrak Ivy City Yard, Barcroft Sport and Fitness Center
  - landmarks: Lincoln Memorial, Washington Monument, WWII Memorial, Thomas Jefferson Memorial
- **Tagged "Comedy":** Rock Creek Park and Shenandoah National Park.
- **Wrong location:** Grant's Bar (Pittsburgh, PA) listed as 26.6 mi away; "Washington, D.C. 60024" has a Chicago ZIP.
- **Already over:** events that started at 7 PM still appear under "Anytime" at 9 PM.
- **Fix:**
  - Whitelist place types per category.
  - Drop results without a matching type.
  - Re-check the distance against the parsed coordinates.
  - Hide events that have started.

### 5. Counters and avatars (mobile)
- The group card says **"0 / 2 voted"** while the proposal says "1 of 2 voted" and "Demo Reviewer voted · waiting on you".
- On iOS, the group header shows **"DR" twice**. Android shows DR · JY correctly.
- "Us Two · 1 open · 0 decided" on iOS, with no open plan.
- **Vote counts show before you vote:** "1 vote" appeared on each option before Jake voted. The web says "Hearts stay hidden until everyone has voted"; the apps should match.

### 6. The rating prompt covers the result (iOS)
"Enjoying DateMeUp?" appears on top of "It's a Match!" before the winner can be read. Show it after the match card is dismissed, or after a few seconds, and only once.

### 7. "View all votes" still shows only totals (iOS/Android)
Daniel Sloss (Yes + Maybe) and Gilla Band (Yes + Yes) both read "2 votes", so nobody can tell why Gilla won. After a decision, show each person's vote per option.

### 8. Spanish is partly translated (iOS)
- **Translated:** Perfil, Planes, Descubrir.
- **Still in English:**
  - Preferences, Home area, Not set
  - Favorite categories, None yet
  - Widget preview (coming soon)
  - Appearance, System / Light / Dark
  - Account

---

## 🟡 Medium

### 9. Android content scrolls under the status bar
On the proposal screen, the "Daniel Sloss: BITTER" title overlaps the camera cutout and status icons. Add a fixed header or a status-bar safe-area inset.

### 10. Android match screen is double-dimmed
The scrim behind "It's a Match!" darkens the whole screen, including the system navigation bar, as if two overlays are stacked.

### 11. Discover category colors (web): three left
- Bars & Nightlife uses `#A24A66` (After Dark) instead of `#9C5F38` (Eat & drink).
- All categories, when selected, is `#111418` instead of `#2B3532`.
- After Dark and Fun Ideas have no `aria-pressed`.

### 12. Mobile Discover icons
The colors match the web now, but the apps still use emoji inside the circles instead of the web's line icons.

### 13. Landing page (web)
- **Hero App Store / Google Play badges:** `#084C4A` text on `#111418`, effectively unreadable. The badges lower on the page are fine (white on black).
- **Wrong "Tonight" label:** the listings panel calls "Rishab Rikhiram Sharma | Sitar For Mental Health" "Tonight", but it's Tue, Nov 17.
- **Headline length:** it still wraps to 4 lines on desktop.

### 14. Web group page
It still shows "No plans yet. Start one." next to "Past plans (4)".

### 15. Location-denied wording (mobile)
After denying location, Discover still shows "Tonight near me" and "back to my location ×".

---

## Fix order
1. **The date shift** and past-date blocking (#1). This is the last bug that can send people on the wrong day.
2. **Version bump** (#2) and the **onboarding flag** (#3).
3. **Discover data cleanup** (#4).
4. **Counters, hidden counts, rating-prompt timing and per-person votes** (#5–#7).
5. **Spanish strings** (#8), Android safe area and scrim (#9, #10), then the remaining polish.
