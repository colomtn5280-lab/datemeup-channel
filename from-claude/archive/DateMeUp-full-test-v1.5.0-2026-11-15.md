# DateMeUp: Full Test, v1.5.0 (Web, iOS & Android)

**Date:** Sun 15 Nov 2026, 12:00–12:15 PM ET

**Builds tested:**
- iOS v1.5.0 on iPhone 14 Pro / iOS 17.2 (Appetize), signed in as Jake
- Android v1.5.0 on Pixel 7 / Android 13 (Appetize), signed in as Demo
- datemeup.app, signed in as Demo

**What I exercised:**
- **Web:**
  - landing (badges, hero listings, headline, video, branding, testimonials)
  - Discover (colors, data quality, dates)
  - adding to the plan, Finalize, the default date and past-date check
  - the invite card gallery (all 36 tiles) and customise and save
  - voting
  - notifications, settings, After Dark, 404
- **iOS:**
  - onboarding, Plans and group counts
  - swipe-to-vote (left, up, right)
  - the match screen and per-person votes
  - the rating prompt, Pick an invite card, Add to calendar
  - Profile, Español, Connections and the friend menu
- **Android:**
  - plan sync after the match
  - Profile (Appearance, Home area, Favorite categories), language state

**Vote test:** Demo proposed on the web and voted Yes ×3. Jake voted on iOS using swipe-to-vote.

| Option (Discover: Sun, Nov 15) | Demo | Jake |
|---|---|---|
| Madama Butterfly | Yes | No (left swipe) |
| Daniel Sloss: BITTER | Yes | Maybe (button; the up-swipe scrolled the page instead) |
| **Gilla Band** | Yes | **Yes** (right swipe) |

**Result: Gilla Band ✅.** The iOS match screen shows "How everyone voted" (Demo ✓ Yes / Jake ✗ No / ~ Maybe / ✓ Yes). Android picked up the decision.

---

## ✅ Fixed since v1.4.0
- **Hero store badges are readable** (white on `#111418`).
- **Discover colors match the spec:** Bars & Nightlife `#9C5F38`, All categories `#2B3532`.
- **Past events no longer show** in Discover; the earliest listing is today.
- **Vote counts stay hidden** until you vote (iOS showed no "1 vote" before Jake voted).
- **Swipe-to-vote moves to the next card** after a left or right swipe.
- **Per-person vote breakdown on iOS** (it was Android only).
- **iOS group avatars are correct** (JY · DR).
- **The rating prompt waits a few seconds** before appearing.
- **Saving an invite card works** on an open plan ("Use this card ✓" returns to the proposal). It failed on a decided plan in v1.4.0.
- **Web notifications** have "Mark all read" and relative times ("12h ago").
- The Fortune Cookie design exists.
- No TogetherPlans references or invented testimonials remain on the landing page.

---

## 🔴 Must fix before submission

### 1. Invite cards never show the real plan (web; affects anything sent)
I audited all 36 tiles on the gallery for "v1.5 full test":

| Check | Result |
|---|---|
| Show this plan's details (Gilla Band, Madama Butterfly, etc.) | **0 of 32** |
| Show sample couples / venues ("Jake & Sarah", "Sam & Riley", "Jazz at Blue Room", "2051 Welton St, Denver") | **32 of 32** |
| Contain raw template code `{{ p.i }}` | **15** (Bold Poster, Ticket Stub, Collage/Sticker, Map Pin, Neon Sign, Swiss Grid, Comic Panel, Newspaper, Confetti Invite, Badge/Seal, Trading Card, Sticky Notes, Bingo Card, Tarot Card, Wanted Poster) |
| Say "TOGETHERPLANS.APP" | **3** (Ticket Stub, Playbill/Gig Poster, Terminal) |
| Empty placeholders (4b–4e) | **4** (still counted in "36 designs") |

- The customise preview also uses the sample data: Fortune Cookie shows "Saturday Night Out · Sat, Nov 15 · 7 PM · Sam & Riley".
- Unless the card that's actually sent is rendered differently, **every invite card a user sends will show a stranger's date.**
- **iOS:** "Pick an invite card" now opens an **in-app browser at the website's login page**, so a signed-in user has to sign in again. Open the picker inside the app, or pass the session.
- **Fix:**
  - Use one data-bound renderer for both the preview and the sent card.
  - Remove the `{{ }}` leftovers and the TogetherPlans branding.
  - Hide 4b–4e and show the real count (31).
  - Add a test that renders every template with a sample plan and fails on `{{`, `togetherplans`, "Jake & Sarah", "Sam & Riley" or "Blue Room".

### 2. Event dates are still shifted one day earlier
- **Reproduced again today:** Madama Butterfly, Daniel Sloss and Gilla Band are **Sun, Nov 15** in Discover, but **Sat, Nov 14 · 7:00 PM** on Finalize, the proposal (web and iOS) and the result.
- "When?" defaults to **2026-11-14 19:00**, yesterday, below the field's own minimum (`2026-11-15T12:06`). The default title says "Date Night · **Saturday**".
- **The plan still sends with a past date.** The tonight date has become a yesterday plan.
- **Notifications:** last night's "Tomorrow: Re-review vote test" reminder went out for an event on Tue, Nov 17.
- **Landing hero listings** label everything "Tonight", including the Sitar concert (Nov 17) and Kylie Morgan (Nov 19).
- **Fix:**
  - Store each event's start time with its time zone and format it in that zone.
  - Default the plan date to the earliest dated activity.
  - Block past dates.
  - Schedule reminders from the real start time.
  - Compute the hero's "Tonight / Tomorrow / Tue" label from the date.

### 3. Discover data is unchanged
- Still listed under the wrong categories:
  - Dining: Booz Allen Hamilton, the US Census Bureau, the State Department, Micron, Northrop Grumman, Wheaton High School, Amtrak Ivy City Yard, the Lincoln, Jefferson, MLK and WWII memorials, the Washington Monument, the National Mall
  - Comedy: Rock Creek Park, Shenandoah National Park
  - Grant's Bar (Pittsburgh, PA) shown as 26.6 mi away; a Chicago ZIP on West Potomac Park
- Comedy in the apps returned restaurants (Ethiopian Buffet, Running Dish) in v1.4.0.

### 4. Screens don't refresh after a match (iOS and Android)
- **iOS:** right after the match, the group page still listed "v1.5 full test" as **OPEN · 0 / 2 voted**.
- **Android:** Plans showed "1 open · 6 decided" until I changed tabs a couple of times.
- **The group card's vote count is still wrong:** "0 / 2 voted" while the proposal said "1 of 2 voted · Demo Reviewer voted".
- **Fix:** refresh plan, group and count data on decision events (push or socket) and when returning to a screen.

### 5. Match notifications (web)
- Demo received **no notification** for today's match on "v1.5 full test".
- "Everyone's waiting on you 👀 · Date night · Thursday" is still unread **12 hours after that plan was decided**.

---

## 🟠 High priority

### 6. Android Profile settings don't respond
- **Appearance → Dark** did nothing (two tries); Light stayed selected.
- **Home area** did nothing when tapped.
- **Favorite categories** opens, but shows "None yet", while the web Settings for the same Demo account lists **Comedy**. Favorites aren't synced between web and app.

### 7. Spanish still partly English (iOS)
- With Español selected:
  - Perfil, Planes and Descubrir are translated
  - **CONNECTIONS, My Friends, NOTIFICATIONS, New proposals, When everyone votes, Reminders** and the whole **Connections** screen (Friends, Requests, Find People, Plan date) are English
- Category names, the proposal form, "Swipe to vote", "Send via DateMeUp" and others were English in v1.4.0 and aren't confirmed fixed.

### 8. Swipe up for Maybe scrolls the page
On iOS, an upward swipe on the card scrolls the page instead of voting Maybe. Lock vertical scrolling while a card is being dragged, or use a long-press for Maybe.

### 9. Add to calendar gives no feedback (iOS)
Tapping it closed the match card with no calendar sheet, permission prompt or confirmation. It may be an Appetize limitation; check on a real device. If it saves silently, show "Added to Calendar ✓".

### 10. Onboarding
- It showed at the start of every Appetize session. That could be correct if Appetize installs the app fresh each time, so confirm on a real device.
- The real bug is last night's case: the app restarted mid-session and showed onboarding again.
- Store "seen onboarding" on the server per user, so signing in on a new device also skips it.

---

## 🟡 Medium
11. **The friend "⋯" menu** only offers "Remove". Add Block and Report there too, matching the group member menu (Apple 1.2).
12. **"Us Two · 1 open · 0 decided"** still shows an open plan that doesn't exist (iOS).
13. **The rating prompt still lands on the match card** (now after a few seconds). Show it after the card is closed, and at most once per version.
14. **iOS proposal header:** the "Share" button overlaps the status bar on the decided-plan screen.
15. **The hero headline** still wraps to 4 lines on desktop.
16. **Carried over, not rechecked this round:**
    - `aria-pressed` missing on After Dark and Fun Ideas
    - the After Dark "Spicy" tag on every card and no 18+ check
    - Find People privacy
    - Android status-bar overlap
    - mobile Discover still using emoji icons
    - the web past-plans list not sorted by date
    - the 404 page title

---

## 💡 Recommendations
1. **Invite cards first.** This is now the most visible bug: a couple's very first shared moment would show someone else's names and date. One renderer, real data, and an automated check (see #1).
2. **One date and time source:** the winning event's time-zoned start drives the plan date, title, reminders, calendar file, hero labels and the "How was it?" prompt.
3. **Live updates:** send a "plan decided" event to every device and refresh the lists, counts, notifications and the match notification from it.
4. **Settings parity:** one preferences API (favorites, home area, appearance, language, notifications) shared by web, iOS and Android.
5. **Pre-release checklist on a real device:**
   - fresh install → onboarding once → restart → no onboarding
   - propose → swipe-vote → match
   - pick and send an invite card → open it from the recipient's side
   - add to calendar
   - switch to Spanish and check every screen

---

## Fix order
1. Invite card data and branding, plus the iOS in-app picker (#1)
2. Dates and reminders (#2)
3. Refreshing after a match, counts, and match notifications (#4, #5)
4. Discover data (#3)
5. Android Profile settings and favorites sync (#6)
6. Spanish, swipe-up, calendar feedback, onboarding (#7–#10)
7. Medium items
