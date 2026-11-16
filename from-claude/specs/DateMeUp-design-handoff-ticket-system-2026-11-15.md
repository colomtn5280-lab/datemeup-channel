# DateMeUp design handoff: the ticket system, every screen
**For:** Hermes  **Date:** 2026-11-15  **Design canvas:** https://claude.ai/artifact/Y8rmhnuoAp9WxJnvoW3b6T  (pages: "All screens", "Landing hero options")

This replaces the look of the app on iOS, Android and web. It does **not** change what the app does.

---

## 0. Read this first: the three rules

1. **Same features, new look.** Every control and piece of information on today's screens must still exist after the redesign. Each screen below has a **parity checklist** that maps every element of today's screen to where it lives in the new design. Build against the checklist, not just the picture.
2. **If something on today's screen isn't in a checklist, it stays.** Restyle it and ask. Never drop it because the mockup didn't show it.
3. **Your current fix queue is unchanged.** Everything in `DateMeUp-3-participant-test-and-store-readiness-2026-11-15.md` (V, D, K, I, C, G, F, N, IC, M, DQ, A series) is still yours, and logic fixes come first. Where a screen depends on one of those fixes, its checklist names the fix ID. This handoff is presentation only.

Items marked **NEW** add something that didn't exist before (Forgot password, notifications inbox on mobile, After Dark on mobile, data export on mobile, guest voting with "Text me the result"). Items marked **removed** are duplicates or placeholders, each with its reason.

---

## 1. What changed since the craft spec (`DateMeUp-craft-polish-implementation-spec-2026-11-15.md`)

| Craft spec section | Status |
|---|---|
| §1 Design tokens | **Superseded** by §2 below (new palette, ticket system). Fonts unchanged: Bricolage Grotesque (headings) + Inter (everything else). |
| §1.6 Icons, no emoji | **Applies.** Phosphor (MIT, free) line icons, regular weight, recolored to ink. |
| §2 Haptics, press physics | **Applies.** |
| §3 Feedback layer (vote bar, notes, sheets, toasts) | **Applies**, restyled as tickets (see the voting screen). |
| §4 Signature moments | **Applies.** The match moment is now the "IT'S A PLAN" stamp landing on a ticket; see the match board. |
| §5 Illustration commission + Rive | **Dropped.** No budget; no illustrations. Rive's free plan adds a splash screen to exported files, so animations are coded (Reanimated / CSS). The ticket and stamp *are* the visual identity. |
| §6 Invite card renderer + link previews | **Applies.** Host card images on **Cloudflare R2**, resize photos with **Cloudflare Image Transformations** (free tier: 5,000 unique transformations/month). Keep photo sizes to 2 widths. Skip the GCP load balancer. |
| §7 Onboarding + permission primers | **Applies**, content is now on the onboarding and location boards. |
| §8 Backend craft (fairness, taste, weather, notifications) | **Applies.** |
| §9 Platform polish (Live Activity, widgets, edge-to-edge, web) | **Applies.** Widgets stay hidden from Profile until they ship. |
| §10 Copy + string catalog | **Applies.** Vote labels: I'm in / Maybe / Not for me. Decided: "It's a plan." |
| §11 Performance | **Applies.** |
| §12 Google Cloud | **Applies** except the card bucket/CDN (moved to Cloudflare). |
| NEW: "Text me the result" on the invite page | Approved by the owner. Needs an SMS provider (e.g., Twilio; per-message cost + US carrier registration), explicit opt-in checkbox, STOP handling, one text per plan, delete the number after sending. Offer "Email me instead" too. |

---

## 2. The ticket system

### 2.1 Idea
Every plan is a ticket. Ideas are tickets you vote on at the stub, decisions get **stamped**, counts live on the stub. Night (ink) backgrounds are only for big moments: Tonight, It's a plan, After Dark, the landing hero.

### 2.2 Color tokens (replaces the earlier palette)
```css
:root{
  --ink:#1E1A38;          /* text, outlines, night surfaces */
  --dusk:#2B2552;         /* night cards, skyline */
  --page:#F5F6FA;         /* app page background (cool near-white; no beige) */
  --ticket:#FFFFFF;       /* tickets, cards, fields, sheets */
  --muted:#4A4562;        /* secondary text */
  --hairline:#C9CCD6;     /* dashed row dividers */
  --teal:#0E8A86;         /* primary action, "I'm in" */
  --teal-bright:#12A39E;  /* stub: votes */
  --amber:#F5A524;        /* stub: add / keep */
  --maybe:#B5740A;        /* "Maybe" (text-safe) */
  --coral:#FF6B57;        /* stamps, stub: admit / plan, landing CTA */
  --lilac:#B9A7F5;        /* stub: everything else */
  --moon:#FFE7B0;         /* night accents: moon, windows, small caps on night */
  --danger:#B3261E;       /* delete, block */
}
```
**Stub colors are meaning, not decoration:** teal = vote counts, amber = Add/Added/Keep, coral = Admit/plan/Review, lilac = anything else. Text on any stub is ink.

### 2.3 Type
- Bricolage Grotesque 800: screen titles 32 (mobile) / clamp(30–44) (web), ticket titles 17–22, landing headline up to 92.
- Inter 400/500/600: body 15–16, meta 13, buttons 15 (600).
- Labels: Inter 600, 11px, letter-spacing .14em, UPPERCASE ("IDEA 01", "ADMIT 3", "OPEN · VOTE BY THU 6 PM"). Labels only, never sentences.

### 2.4 Components (all on the "Ticket system · reference" board)
- **Ticket:** white, 2px ink outline, radius 18, notches 22px half-circles at the perforation, perforation 2px ink dashed 3/4. Top/left = what it is; stub = what you do or the count.
- **Stamp:** 3px border + 1.5px inner outline (offset −7px), radius 8, Bricolage 800 caps, rotated −8° to −14°. Colors: coral "IT'S A PLAN", teal "I'M IN", maybe-amber "MAYBE"/"SO CLOSE", ink "NOT FOR ME". Lands with a 260 ms scale 1.6 → 1 and a medium haptic. One stamp per ticket.
- **Buttons:** pill, min-height 48 (44 for icon buttons), 2px ink border. Primary teal/white text; secondary white; disabled = dashed border + reason text below; danger = red outline.
- **Vote control:** three pills (I'm in / Maybe / Not for me) with line icons; selected fills (teal / maybe-amber / ink). Fixed height; nothing moves when you vote.
- **Chips, segmented controls, fields, toggles, bottom sheets, tab bar:** see any board; all share the 2px ink outline and white fill.
- **Icons:** one line set, 2–2.4 stroke, round caps. **No emoji anywhere in the interface** (fine inside what people type).

### 2.5 Motion & haptics
Press: scale 0.95 in 90 ms. Select: fill in 160 ms. Stamp: 260 ms. Respect reduced motion (no stamp scale, no confetti). Haptics per craft spec §2.1.

---

## 3. Decisions made

- **Landing:** Option A, "city at night" (navy sky, moon, skyline with lit windows, white tickets, coral stamp, coral "how it works" band).
  - The **30-second preview video auto-plays at the top** inside a phone frame: muted, looping, playsinline, with a poster image until it loads and a sound button on the video. "Watch with sound" opens it full screen with audio. Reduced motion or data saver shows the poster plus a play button. Add a caption for screen readers.
  - **The video must be re-shot** after this redesign ships, since the current one shows the old design. Use the old one as a placeholder until then. Shot list: chat chaos → adding ideas → voting with counts ticking → stamp → calendar + invite card → logo. Captured from the real new build with the demo account.
- **Illustrations:** none. The ticket/stamp system replaces them.
- **Hosting for card images and photo resizing:** Cloudflare (R2 + Image Transformations).
- **Font:** Bricolage Grotesque.
- **Text me the result:** yes (see §1).
- **Open product question (not designed):** the member menu has only Block / Report. Should owners get "Remove from group" and everyone get "Leave group"? Owner to decide.

---

## 4. Bugs found while capturing every screen (add to your queue; not design work)

- Welcome and Log in show **two different logos and taglines**. Use one: the ticket logo, "DateMeUp", "Plan together. Go together."
- **No "Forgot password?"** anywhere on mobile.
- Sign up offers Google + Facebook but **no Apple** (required on iOS when other social logins exist).
- Onboarding says **"Tap a heart"** (voting has no hearts) and **"What are you two into?"** (assumes a couple).
- A **decided plan shows "Almost there! You haven't matched yet"** with New proposal / Give it time and "1 of 2 voted".
- **Share the plan names a different winner** than the match pop-up and shows the time as **12:00 AM**.
- Profile email shows **@togetherplans.app**. The avatar's **pencil badge does nothing**. **Home area doesn't respond** on Android.
- **Widget preview** is a "coming soon" page with fake plans ("The Tin Pan"). Hide it until widgets ship; store reviewers flag placeholder screens.
- Plans tab: the floating **New group button is half hidden under the tab bar** and duplicates "+ New".
- Invite People: **double header**; the Friends tab offers **Invite for people already in the group**.
- Member menu is a **system alert**.
- Web Settings: **Display name field is blank** even though the name is set.
- Web Discover has **3 categories mobile lacks** (Couples Events, After Dark, Fun Ideas) and a different date filter. The redesign unifies them; the data must match too.
- Mobile has **no notifications inbox, no After Dark, no data export** (web has all three). The redesign adds them.

---

## 5. Placeholders in the mockups (don't ship these strings)
Grey "Photo / Event photo / Video frame" blocks are image slots. These were invented for the mockups: "Late show improv", "Sam M.", the After Dark level tags (use web's real ones), the notification times, "Cakes & Coffee"-style sample ideas, the "Saturday night out" sample title, and "DateMeUp 1.6.0". Always render real data.

**Three screens were drawn without a capture of today's version:** mobile Preview, web Log in and web Sign up. List today's elements first, then build.

---

## 6. Build order (suggested)
1. Tokens + components (§2) in a shared package for mobile and web; lint rules (no emoji in UI strings, no system alerts).
2. Voting, match, new plan, Discover (the core loop), with parity checklists ticked.
3. Groups, invites, Profile, Friends, notifications, After Dark.
4. Auth, onboarding, permission primer, error sheets.
5. Web pages, then the landing (Option A) with the video slot.
6. QA: walk every checklist below on iOS, Android and web; compare side by side with the "today" captures on the canvas.
7. Re-shoot the landing video from the finished build.

---

## 7. Per-screen parity checklists
Tick every box on each platform the screen exists on. Board names match the canvas.

### Mobile (iOS + Android)


#### Voting · proposed  
*Board:* `VoteProposed.dc.html`

**PARITY · Voting (look changes only, no features removed)**
- [ ] Back button → kept (outlined)
- [ ] OPEN status → kept ("Open · vote by…" label)
- [ ] Title, date → kept (date on each ticket)
- [ ] "0 / 3 voted" → "2/3 VOTED" stub, now with who voted
- [ ] Invite someone to vote → kept, same label
- [ ] Copy link (clipboard) → kept, link icon
- [ ] "A member voted · waiting on you" → "Waiting on you / G R and Jake have voted"
- [ ] Swipe to vote → List / Swipe toggle
- [ ] Category tag, title, address, date, vote count → kept on ticket
- [ ] Yes / Maybe / No → I'm in / Maybe / Not for me (same 3 values)
- [ ] Add a note → kept (always visible)
- [ ] Next option card → kept below


#### Match · proposed  
*Board:* `MatchProposed.dc.html`

**PARITY · Match**
- [ ] LOCKED IN → kept ("Locked in · plan name")
- [ ] Headline → "It's a plan." (copy change only)
- [ ] Winning option: name, category, address → kept on ticket, plus date
- [ ] Add to calendar → kept, same label
- [ ] Pick an invite card → kept, same label
- [ ] View all votes → kept, same label
- [ ] How everyone voted (every option × every person) → kept inline
- [ ] NEW: Close button (fix M1)


#### New plan, empty · proposed  
*Board:* `EmptyProposed.dc.html`

**PARITY · New plan (checked against mobile + web)**
- [ ] Back → close button (same action)
- [ ] "Your Plan" / Activities (0 / 5) → "New plan" / "IDEAS · 0 OF 5"
- [ ] Empty message → "Start with a few ideas"
- [ ] + Add another activity → Browse ideas (opens Discover) + Tonight
- [ ] Title → NAME
- [ ] When? date & time → WHEN
- [ ] Vote deadline (web only today) → VOTE BY, now on mobile too
- [ ] Personal message (web only today) → MESSAGE, now on mobile too
- [ ] Send to (group) → shown in header "for Trio Date Club"
- [ ] "Votes by link, no account needed" → kept under Send
- [ ] Preview → kept
- [ ] Send to group → kept; disabled until 2 ideas, with reason shown


#### Plans tab · proposed  
*Board:* `PlansHome.dc.html`

**PARITY · Plans tab (checked against the live app)**
- [ ] Greeting "Good afternoon, Demo" → kept
- [ ] + New (opens New group) → "New group", same action
- [ ] Floating button (also New group, hidden under the tab bar) → removed as a duplicate; same action stays in "New group"
- [ ] Groups list: avatars, name, "x open · y decided" → kept
- [ ] Past plans (9) with Decided → kept
- [ ] NEW, from the same data: "Waiting on you" and "Coming up" shown first
- [ ] Tab bar Plans / Discover / Profile → kept
- [ ] NEW: bell → Notifications inbox (M26)


#### Group page · proposed  
*Board:* `GroupPage.dc.html`

**PARITY · Group page**
- [ ] Back → kept
- [ ] Invite members → kept, same label
- [ ] Group name, member avatars, member count → kept (all avatars, fix G3)
- [ ] New proposal → "New plan"
- [ ] + Add more activities → "Add ideas"
- [ ] Active: status, title, progress, x/3 voted → kept on each ticket stub
- [ ] Past: Decided + title → kept, with stamp + the pick
- [ ] Members list + ⋯ menu → kept; menu options unchanged
- [ ] Web only: Delete group → kept


#### Discover · proposed  
*Board:* `Discover.dc.html`

**PARITY · Discover**
- [ ] Back, location chip, Done → kept
- [ ] Tonight near me → kept ("Tonight near you")
- [ ] Pick date + helper → kept
- [ ] Search area: Nearby 10 / 25 / 60 / Day trip 150 → kept, same values
- [ ] Search another area → kept
- [ ] Browse by category + All → kept
- [ ] ALL 14 categories stay: Comedy, Concerts, Family Activities, Sports & Active, Hiking Trails, Hotel Stays, Local Experiences, Movies, Streaming Night, Performing Arts, Restaurants & Dining, Volunteering, Wellness & Spa, Bars & Nightlife (screen shows the first 8; rest scroll)


#### Discover results + plan tray · proposed  
*Board:* `DiscoverResults.dc.html`

**PARITY · Results + tray**
- [ ] Result card: photo, category, title, date/time, address, distance → kept
- [ ] + Add to Date → "Add to plan"; Added state → kept ("Added" + check)
- [ ] "N options added · tap to review" banner → plan tray (same tap target)
- [ ] Review sheet (list, remove ×, Finalize Plan, Keep browsing) → unchanged in content, restyled as a ticket; "Finalize Plan" → "Review plan"
- [ ] 5-idea limit → kept (tray shows the count and "up to 5")
- [ ] Try it: tap Add / Added in Play


#### Invite card picker · proposed  
*Board:* `CardPicker.dc.html`

**PARITY · Invite card picker**
- [ ] All 32 designs → kept (screen shows 6; rest scroll)
- [ ] Tiles now show real previews with the plan's own title and date (fixes IC1)
- [ ] Selected state → kept
- [ ] Skip this step → kept
- [ ] Next → kept


#### Customize invite card · proposed  
*Board:* `CardCustomize.dc.html`

**PARITY · Customize card**
- [ ] Back → kept
- [ ] Card preview → now shows real plan data (fixes IC1)
- [ ] Personal note (optional, 140 chars, counter) → kept
- [ ] Add a photo → kept
- [ ] Use this card → kept, same label


#### Error sheet (calendar) · proposed  
*Board:* `ErrorSheet.dc.html`

**PARITY · Error sheet**
Replaces every system alert. Calendar example:
- [ ] Title "Could not add to calendar" → "Couldn't reach your calendar"
- [ ] Body "Please try adding the event manually" → explains the .ics fallback
- [ ] OK → "Not now" (same dismiss)
- [ ] NEW: "Get the invite file" (.ics, from Hermes's K1 fix)


#### Welcome · proposed  
*Board:* `M01_Welcome.dc.html`

**PARITY · Welcome**
- [ ] Logo + "datemeup" + "Date night, decided." → one brand: ticket logo, "DateMeUp", "Plan together. Go together." (same on log in, web)
- [ ] Continue with Google → kept
- [ ] Sign up with email → kept
- [ ] Already have an account? Log in → kept
- [ ] NEW: Continue with Apple (iOS requirement, already in Hermes's store list; hide on Android/web if wanted)
- [ ] NEW: Terms + Privacy line


#### Sign up · proposed  
*Board:* `M02_SignUp.dc.html`

**PARITY · Sign up**
- [ ] Back → kept
- [ ] "Create your account" + FREE tag → kept
- [ ] Email / Phone toggle → kept
- [ ] Display name, Email (or Phone number), Password 8+ → kept
- [ ] Create account → kept
- [ ] Google, Facebook → kept
- [ ] NEW: Apple (iOS requirement)
- [ ] Already have an account? Log in → kept


#### Log in · proposed  
*Board:* `M03_LogIn.dc.html`

**PARITY · Log in**
- [ ] Calendar logo + "DateMeUp!" + "Plan together, decide together" → unified ticket logo, "Welcome back"
- [ ] Email / Phone toggle → kept
- [ ] Email, Password → kept
- [ ] Log in → kept
- [ ] Continue with Google, Sign in with Facebook → kept
- [ ] No account? Create account → kept
- [ ] NEW: Forgot password? (missing today)
- [ ] NEW: Apple (iOS requirement)


#### Forgot password · NEW  
*Board:* `M04_ForgotPassword.dc.html`

**PARITY · Forgot password**
NEW screen (missing today on mobile). Hermes: needs a reset-email endpoint + a set-new-password page on the web (W13).
- [ ] Email field, Send reset link
- [ ] Confirmation ticket (shown after sending; never reveals whether the account exists)
- [ ] Phone accounts: reset by text


#### Onboarding 1 · proposed  
*Board:* `M05_Onboarding1.dc.html`

**PARITY · Onboarding 1**
- [ ] Skip → kept
- [ ] "47 MESSAGES LATER" + two chat bubbles → kept (+1 bubble)
- [ ] "Sound familiar?" + sub → kept
- [ ] Next + 4 dots → kept, plus "1 of 4"


#### Onboarding 2 · proposed  
*Board:* `M06_Onboarding2.dc.html`

**PARITY · Onboarding 2**
- [ ] Three example ideas + "LOCKED IN" tag → kept as three ticket ideas, one stamped "IT'S A PLAN"
- [ ] Headline "Tap a heart. Match, and it's a plan." → rewritten: voting has no hearts
- [ ] Sub → rewritten to name the three real vote choices
- [ ] Next + dots → kept


#### Onboarding 3 · proposed  
*Board:* `M07_Onboarding3.dc.html`

**PARITY · Onboarding 3**
- [ ] "What are you two into?" → "What are you into?" (works for groups)
- [ ] Pick up to 5 + sub → kept
- [ ] Category chips → kept, emoji removed; list now matches Discover exactly (adds Couples Events, Fun Ideas, which web has)
- [ ] "Skip for now" → button reads "Skip for now" with 0 picked, "Continue · N picked" after picking
- [ ] Skip (top) → kept


#### Onboarding 4 · proposed  
*Board:* `M08_Onboarding4.dc.html`

**PARITY · Onboarding 4**
- [ ] "Who do you plan with most?" → kept
- [ ] Couple (Most popular) / Friends / Family → kept
- [ ] Name it field → kept
- [ ] Create group & Invite them → kept
- [ ] Skip → kept


#### Location primer · NEW  
*Board:* `M09_LocationPrimer.dc.html`

**PARITY · Location primer**
NEW. Shown once, right before the system location prompt (today the system prompt appears with no explanation).
- [ ] Use my location → triggers the system prompt
- [ ] Choose a city instead → opens Home area (M28); everything works without location


#### New group · proposed  
*Board:* `M10_NewGroup.dc.html`

**PARITY · New group**
- [ ] Create (top right) → "Create group" at the bottom; disabled until a name, with reason
- [ ] Cancel (under the title) → close button, top left
- [ ] Group type Couple / Friends / Family → kept
- [ ] Group name * → kept ("required")
- [ ] Description (optional) → kept
- [ ] Opened by Plans "New group" (was + New and the hidden floating button)


#### Invite people · proposed  
*Board:* `M11_InvitePeople.dc.html`

**PARITY · Invite people**
- [ ] Double header ("Invite People" bar + back) → one header
- [ ] "Link expires in 72 h" → kept
- [ ] Title "Invite members Trio Date Club" → "Invite to Trio Date Club"
- [ ] Tabs Friends / Link / Email / Share / Username → all kept (Link shown)
- [ ] Link: ONE USE tag, explainer, link + Copy, Share link → kept
- [ ] Email: email field + Send invite → kept (not shown)
- [ ] Share: Share invite link → kept (not shown)
- [ ] Username: @username field → kept (not shown)
- [ ] Friends: list + Invite → kept; people already in the group show "Already in group" instead of Invite


#### Member menu · proposed  
*Board:* `M12_MemberMenu.dc.html`

**PARITY · Member menu**
- [ ] System alert "G R / Choose an action" → branded bottom sheet with name and role
- [ ] BLOCK USER → kept ("Block G R"), confirm sheet next
- [ ] REPORT USER → kept ("Report G R"), reason sheet next
- [ ] CANCEL → kept
Product gap (not added here): no "Remove from group" (owner) or "Leave group". Decide with Hermes.


#### Tonight near you · proposed  
*Board:* `M13_Tonight.dc.html`

**PARITY · Tonight near you**
- [ ] "Tonight near me" banner → night ticket header with today's date
- [ ] Results list + Add to Date → kept as result tickets with Add / Added on the stub
- [ ] NEW: only events that haven't started (fix D1 in Hermes's queue); subtitle says so
- [ ] Search area chip → kept in header


#### When & where sheet · proposed  
*Board:* `M14_WhenWhere.dc.html`

**PARITY · When & where**
- [ ] Mobile: Pick date + "Choose a specific date" → "Pick a date" chip
- [ ] Web: Tonight / This weekend / This week / Anytime → same chips on mobile too
- [ ] Search area 10 / 25 / 60 / Day trip 150 → kept
- [ ] Search another area / Change location → "Area · Change"
- [ ] Results update → "Show N ideas"


#### Plan review sheet · proposed  
*Board:* `M15_PlanReview.dc.html`

**PARITY · Plan review sheet**
- [ ] "Your Plan  3 / 5" → kept
- [ ] Each idea: photo, title, address, remove × → kept (icon instead of photo thumbnail is optional; keep photo if preferred)
- [ ] Finalize Plan -> → kept
- [ ] Keep browsing → kept


#### Preview · proposed  
*Board:* `M16_Preview.dc.html`

**PARITY · Preview**
I couldn't capture today's Preview screen; Hermes, list its elements and keep each.
- [ ] Shows the plan exactly as members will see it (title, date, deadline, message, ideas with vote buttons)
- [ ] Edit → back to New plan
- [ ] Send to group → kept


#### Swipe mode · proposed  
*Board:* `M17_Swipe.dc.html`

**PARITY · Swipe mode**
- [ ] "Swipe to vote" / "List view" toggle → List / Swipe segmented control
- [ ] Card with photo, category, title, address, date → kept as a ticket; stamp previews while dragging
- [ ] "← No · Swipe to vote · Yes →  ↑ Maybe" hint → kept, new labels
- [ ] No / Maybe / Yes buttons → kept as round buttons
- [ ] "All options voted!" end state → kept (not shown)


#### Notes & discussion · proposed  
*Board:* `M18_Discussion.dc.html`

**PARITY · Notes & discussion**
- [ ] Per-idea notes (Add a note / Save note) → kept on each ticket; all notes also listed here with who, vote and idea (depends on Hermes's V1/V2 note fixes)
- [ ] Discussion list (initial, time, text) → kept with names, not single letters
- [ ] "Say something…" + Send → kept


#### So close (no consensus) · proposed  
*Board:* `M19_SoClose.dc.html`

**PARITY · So close**
- [ ] iOS banner "So close! No unanimous choice yet. Lock in a Maybe, counter-propose, or start over." → full state with the closest idea and every idea's tally
- [ ] Counter-propose → kept
- [ ] Lock in / Start over → the buttons the banner promised (Hermes's C3 fix builds the logic)
- [ ] Android + web: same state (missing there today)


#### Counter-propose · proposed  
*Board:* `M20_CounterPropose.dc.html`

**PARITY · Counter-propose**
- [ ] Web "Counter-propose keeps this option and lets you swap in new ones. Votes reset." → this screen does exactly that
- [ ] iOS opened a blank New Proposal → now pre-fills the kept idea (Hermes C1/C2 fix links it to the original)
- [ ] Send to group → kept


#### Decided plan page · proposed  
*Board:* `M21_DecidedPlan.dc.html`

**PARITY · Decided plan page**
- [ ] Back, Share → kept
- [ ] Title, date chip, "x of y voted" → title + the pick ticket (date, time, address)
- [ ] "Almost there! You haven't matched yet" + New proposal / Give it time → removed on decided plans (it contradicts the match; bug)
- [ ] Option cards with votes → "How everyone voted" with every person's vote
- [ ] Add to calendar, Pick an invite card → kept (shortened "Invite card")
- [ ] Discussion → kept


#### Share the plan · proposed  
*Board:* `M22_SharePlan.dc.html`

**PARITY · Share the plan**
- [ ] DECIDED card with title, group, date, time, address → kept as a night ticket with the stamp (uses the same winner + time as everywhere else; fixes the mismatch)
- [ ] "How the group voted" bars → kept
- [ ] Share with friends → kept


#### Rate your date · proposed  
*Board:* `M23_RateDate.dc.html`

**PARITY · Rate your date**
- [ ] "How was {pick}? Rate your date" + stars (web + iOS) → kept
- [ ] Shows once per person per plan (today it repeats on iOS)
- [ ] NEW: optional note, Not now


#### Profile · proposed (full scroll)  
*Board:* `M24_Profile.dc.html`

**PARITY · Profile (whole page)**
- [ ] Avatar + edit badge → "Change photo" (the badge does nothing today) + "Edit name"
- [ ] Name, email → kept (email must show the account's real address, not @togetherplans.app)
- [ ] "9 PLANS DECIDED" → kept on the stub
- [ ] Connections › My Friends → kept
- [ ] Notifications: New proposals / When everyone votes / Reminders → kept ("New plans")
- [ ] Language: 9 options → kept
- [ ] Home area → kept (opens M28; unresponsive today)
- [ ] Favorite categories → kept
- [ ] Widget preview (coming soon) → hidden until widgets ship (placeholder page with fake plans)
- [ ] Appearance System / Light / Dark → kept
- [ ] Sign out, Delete account → kept
- [ ] NEW on mobile (web has them): Notifications inbox, After Dark, Your data / export


#### Friends · proposed  
*Board:* `M25_Friends.dc.html`

**PARITY · Friends (Connections)**
- [ ] Friends / Requests / Find People tabs → kept (shown together here for review; build stays as tabs)
- [ ] Friend row: avatar, name, Plan date, ⋯ → kept ("Plan a date")
- [ ] Requests empty state "No pending requests…" → kept (empty state uses the ticket style)
- [ ] Find People: exact username or email search → kept
- [ ] NEW: Accept / Ignore on requests (web has no requests view today; same component there)


#### Notifications inbox · NEW on mobile  
*Board:* `M26_Notifications.dc.html`

**PARITY · Notifications inbox**
NEW on mobile; mirrors the web Notifications page (today web shows only "It's a match!" items).
- [ ] Entry point: Profile › Notifications, and a bell on the Plans tab header
- [ ] Types follow Hermes's N1 list (match, new plan, comment, friend request, …) with names first
- [ ] Mark all read


#### After Dark · NEW on mobile  
*Board:* `M27_AfterDark.dc.html`

**PARITY · After Dark (mobile)**
NEW on mobile; mirrors web /after-dark.
- [ ] Header + tagline → kept
- [ ] Notice line under the header → kept (shown as intro text)
- [ ] Create your own → kept
- [ ] Idea cards with level tag + Add to Date → kept as night tickets with ADD on the stub (keep web's real tag names; mine are placeholders)
- [ ] 18+ gate: confirm age once before first view (store age rating)


#### Home area · proposed  
*Board:* `M28_HomeArea.dc.html`

**PARITY · Home area**
- [ ] Profile row "Home area · Not set" → opens this screen (does nothing on Android today)
- [ ] Web: Settings › Home city "Used to find activities near you" → same control, same wording


#### Your data & delete account · proposed  
*Board:* `M29_YourData.dc.html`

**PARITY · Your data**
- [ ] Mobile Profile › Delete account → kept here, with what happens explained
- [ ] Web "Your data rights": Export my data → now on mobile too
- [ ] Web "Danger zone": Delete my account, 30-day grace → same wording on both
- [ ] Confirmation step (type DELETE or confirm sheet) → keep whatever exists today


### Web


#### Web · Dashboard  
*Board:* `W02_Dashboard.dc.html`

**PARITY · Web dashboard**
- [ ] Greeting + "All your groups' plans in one place." → kept (count of plans waiting)
- [ ] "What are we doing this weekend?" + Start a new plan → kept as a night panel
- [ ] Ideas near you + See all + Add to Date → kept ("Add to plan")
- [ ] Past plans (2) + Decided → kept ("It's a plan")
- [ ] Sidebar: Your groups + Manage + New group → kept
- [ ] Profile card: Settings, Sign out → kept
- [ ] NEW: "Waiting on you" plans first
- [ ] Top nav: Home, Groups, Discover, Friends, After Dark, New Date Plan, dark mode, bell, avatar → all kept ("New plan")


#### Web · Groups  
*Board:* `W03_Groups.dc.html`

**PARITY · Web groups**
- [ ] "Your groups" + sub → kept
- [ ] + New group → kept
- [ ] Filters All / Couples / Friends & family with counts → kept
- [ ] Group card: avatars, Active, name, members, open plan link → kept
- [ ] New group tile → kept


#### Web · Group page  
*Board:* `W04_GroupPage.dc.html`

**PARITY · Web group page**
- [ ] Back to groups, avatars, name, "Group · 3 members", New Date Plan → kept
- [ ] Proposals list (title, date, ideas, OPEN) → kept with vote counts on the stub
- [ ] Past plans + Decided → kept
- [ ] Invite members: LINK / EMAIL / SMS / USERNAME + Generate invite → kept (USERNAME gets its input; Hermes I2)
- [ ] Members (3) + ⋯ → kept
- [ ] Delete group → kept


#### Web · Plan voting page  
*Board:* `W05_PlanPage.dc.html`

**PARITY · Web plan page**
- [ ] Back link, OPEN tag, title, date · N options → kept
- [ ] Each option: photo, category, title, address, date, "You've voted on this one", I'm in / Maybe / Don't think so, note + Save note → kept ("Not for me")
- [ ] "You've voted on N options" + Let them know → kept (Let them know becomes the nudge from Hermes N2)
- [ ] Discussion + Send → kept
- [ ] Who's voted → kept as stub ticket
- [ ] Not feeling it? Counter-propose, Cancel proposal → kept
- [ ] Date, Reminder → kept
- [ ] Invite someone to vote → kept
- [ ] NEW: keyboard voting hint


#### Web · Discover  
*Board:* `W06_Discover.dc.html`

**PARITY · Web Discover**
- [ ] Getting location / Change location → kept
- [ ] Tonight near me → kept
- [ ] 17 categories + All → kept (mobile gets the same list)
- [ ] When: Tonight / This weekend / This week / Anytime → kept, + Pick a date (from mobile)
- [ ] Distance: Nearby 10 / 25 / 60 / Day trip 150 → kept
- [ ] Result cards: photo, category, title, place, distance, Add to Date → kept ("Add to plan")
- [ ] NEW on web: plan tray (mobile has it)


#### Web · New plan  
*Board:* `W07_NewPlan.dc.html`

**PARITY · Web new plan ("Finalize Your Plan")**
- [ ] "BUILD YOUR PLAN" + title → kept ("New plan")
- [ ] Activities (0 / 5) empty + Browse Discover → kept, + Tonight
- [ ] Plan title, When?, Vote deadline (optional), Send to, Personal message (optional) → all kept
- [ ] Send to group → kept, disabled with reason until 2 ideas
- [ ] "No ads. Your group votes by link — no account needed." → kept


#### Web · Join & guest vote (invite link)  
*Board:* `W08_JoinVote.dc.html`

**PARITY · Join / guest vote**
- [ ] /join/{token} today → asks to log in, then joins. Kept for members.
- [ ] Guest votes (the API already counts guestVotes) → vote with first name only, no account
- [ ] Invite card hero with real plan data
- [ ] NEW: "Text me the result" (you approved; needs an SMS provider, explicit opt-in, STOP) + "Email me instead"
- [ ] App Store / Google Play → kept


#### Web · Friends  
*Board:* `W09_Friends.dc.html`

**PARITY · Web friends**
- [ ] "Your friends" (empty: "No friends yet…") → kept
- [ ] Find people + Search → kept
- [ ] NEW: Requests (Jake's request is invisible on web today; Hermes F1)
- [ ] NEW: Plan a date (mobile has it)


#### Web · Notifications  
*Board:* `W10_Notifications.dc.html`

**PARITY · Web notifications**
- [ ] Page title + list of "It's a match! 🎉" items with time → kept ("It's a plan", no emoji)
- [ ] Header bell dropdown → kept
- [ ] NEW: Mark all read; more types from Hermes N1


#### Web · Settings  
*Board:* `W11_Settings.dc.html`

**PARITY · Web settings**
- [ ] Profile: Display name (blank today; must show the saved name), Home city + "Used to find activities near you", Save profile → kept
- [ ] Account: email, Sign out → kept
- [ ] Favorite categories + Edit → kept
- [ ] Quick links (Back to groups, Notifications, Browse activities) → removed: same links are in the top nav
- [ ] Language: 9 options → kept
- [ ] Your data rights: Export my data → kept (moved into Account)
- [ ] Danger zone: Delete my account, 30-day grace → kept
- [ ] NEW on web (mobile has them): notification toggles, Appearance (replaces the header moon toggle's hidden setting)


#### Web · After Dark  
*Board:* `W12_AfterDark.dc.html`

**PARITY · Web After Dark**
- [ ] Moon + "After Dark" + tagline + notice → kept (emoji moon → icon)
- [ ] Create your own → kept
- [ ] Idea cards: icon, level tag, title, description, Add to Date → kept (emoji icons removed; keep the real level names)


#### Web · Log in / sign up / reset  
*Board:* `W13_Auth.dc.html`

**PARITY · Web auth**
I couldn't view web log in / sign up while signed in; Hermes, list today's fields and keep each.
- [ ] Log in + Create account on one page (tabs)
- [ ] Email, password, Forgot password? → link to reset (+ "set new password" page for the emailed link)
- [ ] Google (+ Facebook if web has it today) → kept; Apple added for parity with iOS


#### Web · 404  
*Board:* `W14_NotFound.dc.html`

**PARITY · 404**
- [ ] Big "404" + "Page not found" + explainer → kept, ticket styled
- [ ] Go to my plans → kept


#### Web · Privacy / Terms template  
*Board:* `W15_Legal.dc.html`

**PARITY · Privacy / Terms**
- [ ] Existing pages and text → kept word for word; only the layout uses the system (72-character line length, Bricolage headings)


### Landing page


#### Landing hero · Option A: city at night (chosen)  
*Board:* `W16a_LandingTickets.dc.html`

**LANDING · Option A: city at night (CHOSEN)**
Navy night sky, moon, stars, skyline with lit windows. Headline left; on the right the existing 30-second preview video auto-plays inside a phone frame, framed by two tickets, one stamped "IT'S A PLAN".
VIDEO (keep today's behavior, top of page):
- [ ] autoplay, muted, loop, playsinline; poster image shown until it loads
- [ ] sound button on the video; "Watch with sound" opens it full screen with sound
- [ ] prefers-reduced-motion or data saver: show the poster with a play button instead of autoplay
- [ ] caption/transcript available for screen readers
- [ ] compressed MP4 (H.264) + WebM, under ~3 MB; lazy-load anything below the fold, not this
Below: solid coral "Three taps to a plan" band with white ticket cards and colored stubs.
Keeps today's content: nav, tag, headline, sub, Open app, tour, store badges, feature cards.
