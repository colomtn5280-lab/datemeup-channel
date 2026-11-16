# DateMeUp — full 3-account test, build c96ed33 (2026-11-16)

Builds: iOS and Android latest on Appetize (c96ed33, uploaded 5:21 PM; the header still says **v1.6.3**), and web. Accounts: review account, then Jake on iOS; Demo on Android; G R on web. Flow: Demo created "Comedy Night" in Trio Date Club (Tue Nov 17 7 PM, 2 options); Demo, then G, then Jake voted "I'm in" on Tysons Comedy Cellar.

**Fixed ✅ — core flow passes on all three platforms**
- **F2 vote counter:** the header updates live on iOS, Android and web (1, then 2, then 3 of 3) and matches the group card.
- **F7 match sheet:** iOS and Android now have an X that closes it. The iOS voter chips fit on one line.
- **F3 date:** the plan kept Tue Nov 17 after the match on all platforms.
- **F1 onboarding:** not shown after sign-in (iOS: review and Jake; Android: Demo).
- **F6 review account:** sign-in works. Alex Reviewer, OWNER badge, 3 members (Sam, Jordan). Weekend plans is open with 2 of 3 voted, and header and card agree. Friday night out is decided. Left untouched.
- **F4 Remove (owner):** "Remove from group" appears in the iOS member menu for the owner. Not executed.
- The match fires live on Android while another user casts the last vote.

**Still open ❌**
1. **iOS Delete-account sheet can't be closed (P0 for review).** Profile → Delete account opens a sheet whose Cancel and Delete buttons are below the screen edge. Swipe-down and tapping outside do nothing, so you have to kill the app. Apple tests this flow. Fix: make it a scrollable sheet with a visible Cancel, and support swipe-down.
2. **Leave group is missing on iOS and Android** (as a non-owner, and as owner on iOS). Web has it.
3. **The member menu is still the system alert**, not the branded sheet (spec: decisions addendum §1).
4. **Web groups list:** the Trio Date Club card says "No plan yet" while R2 is open.
5. **Web plan page after a match:** the winner card says "You both said yes" for 3 people.
6. **Android Plans "+ New"** opens New group, not New plan. Either relabel it or route it to the new-plan flow.
7. **Android New Proposal** shows two stacked headers, each with its own back button.
8. **Discover → Comedy** includes Red Panda Buffet and Umi Hotpot Sushi & Seafood Buffet (restaurants). Check the category mapping.
9. **Profile avatar initials are clipped** at the top on iOS ("AR").
10. **Location:** both iOS and Android ask for Precise. Privacy answers say approximate (iOS: `NSLocationDefaultAccuracyReduced`; Android: request only `ACCESS_COARSE_LOCATION`).
11. **Version name** is still 1.6.3. Bump it before store builds.

**Landing tour video: new files ready** in `from-claude/landing-tour/`:
- `tour-16x9.mp4` (1920×1080, 30 s)
- `tour-9x16.mp4` (1080×1920, 30 s)
- `tour-poster-16x9.jpg`, `tour-poster-9x16.jpg`

Drop them into the web `public/` folder with the same names; the landing page already loads `/tour-16x9.mp4` and `/tour-9x16.mp4`. Bump the cache-busting query or file hash so CDNs pick up the new versions. The new video uses the ticket design and today's app copy (I'm in / Maybe / Not for me, "2 of 3 voted", IT'S A PLAN stamp, "Everyone said yes.", Admit Three invite, ticket logo end card). The source is `tour-source.html`.

**Next for Hermes (priority):** 1, 2, then 4 and 5, then 6 to 11. After that, the remaining screens on the ticket design: group page, Discover, new plan, "Sent to" confirmation (no emoji).
