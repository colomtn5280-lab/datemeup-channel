# DateMeUp — decisions addendum (2026-11-15, owner-approved)

This adds to `DateMeUp-design-handoff-ticket-system-2026-11-15.md` and the logo package. If they conflict, this file wins. None of it repeats the fix queue from the 3-participant test.

---

## 1. Member actions: Remove from group, Leave group (NEW)

Design: canvas board **M12b · Member menu, remove & leave**. It shows the mobile sheets 1–4 and the web group page.

**Who sees what**

| Viewer taps… | Actions |
|---|---|
| Another member, viewer is **owner** | Remove from group · Report · Block |
| Another member, viewer is a member | Report · Block (unchanged) |
| Their own row (anyone) | Leave group. Sole owner also sees "Make someone else owner". |
| Group settings (web and mobile) | "Leave group" row at the bottom, for everyone |

**Rules**
- Both actions ask for confirmation in a second sheet (a centred dialog on web). The destructive button is red. Cancel is always there, and focus starts on Cancel on web. Copy is exactly as on the board.
- **Sole owner leaves:** prompt them to pick a new owner first. If they leave without picking, ownership passes to the longest-standing member. **Last member leaves:** archive the group (soft delete; keep data for the export and retention policy already in place).
- **After a remove or leave:**
  - The person's past votes still count.
  - They lose access to the group's plans, discussion, notifications and widgets.
  - Pending invites they sent stay valid.
  - They can be re-invited.
- **No push to the removed person.** Add a group activity line: "G R removed Sam" / "Sam left".
- **Live Activity / widget:** if the group's plan is showing for that person, end it when they're removed or leave.

**Backend**
```
POST /groups/{groupId}/members/{userId}/remove   (owner only; 403 otherwise; 409 if userId == caller)
POST /groups/{groupId}/leave                      (any member; body: { newOwnerId?: string })
```
- Enforce the rules on the server, not only in the UI. Use a transaction:
  - membership `status = 'removed' | 'left'`, `endedAt`
  - owner transfer
  - archive if no members remain
- Security rules: a member whose status isn't `active` can't read group or plan documents. Revoke their FCM topic subscription for the group.
- Analytics events: `member_removed`, `member_left`, `owner_transferred`, `group_archived`.

**Tests:**
- An owner removes a member, and that member's open app loses the group without crashing.
- A sole owner leaves → ownership transfers.
- The last member leaves → the group is archived.
- A non-owner calling remove gets 403.
- Votes are unchanged after a remove.

## 2. Sign in with Apple (iOS)

Required because iOS offers Google sign-in. Put the official Apple button above Google on M02 Sign up and M03 Log in, following Apple's HIG (black on light, white on dark; label "Sign in with Apple" / "Continue with Apple").
- Use Firebase Auth's Apple provider. Handle the hidden relay email ("Hide My Email"). Store the name on the first sign-in only, because Apple sends it once.
- Account deletion (already in Your data) must also revoke the Apple token (`/auth/revoke`), per App Review 5.1.1(v).
- Android and web: optional, not required. Skip for now.

## 3. One category and filter list

Mobile uses **web's** category and filter list, so both platforms have the same set, labels and order.
- Move the list into a single shared source: a config doc or a shared constants module read by both apps. Don't hardcode it in each app.
- Map any old mobile-only category values to their web equivalent when reading saved filters.

## 4. Sample content does not ship

These are placeholders in the boards: "Late show improv", "Sam M.", the After Dark tags, notification times, and the sample ideas. Use the real data the app already has. Where an empty state needs words, use the empty-state copy from the handoff, not invented sample items. If any placeholder string turns up in a build, that's a bug.

## 5. Loading spinner: the ticket (NEW)

Keep the loading spinner, but replace it with the animated logo ticket. Files are in `DateMeUp-logo/spinner/`:
- `TicketSpinner.tsx` for React Native (react-native-svg + Reanimated), with a `useDelayedSpinner` hook
- `spinner-web.html` for web (CSS keyframes, drop-in)
- `spinner-on-light.svg` / `spinner-on-dark.svg`, self-animating, which also work in `<img>`
- `spinner-preview.gif`, a reference for timing

**Motion** (1.4 s loop):
- the perforation on the stub runs downward
- the teal head, then the coral head (0.2 s later), hop 5 units
- the two "admit" bars blink in turn

**Reduce Motion / prefers-reduced-motion:** no movement, only a slow fade.

**Where to use it:** full-screen and page loads, section loads (a list or card area while it fetches), and pull-to-refresh content. Sizes: 64 px for full screen, 40 px in sections.

**Where not to use it:**
- **Inside buttons, and anything under 32 px.** The ticket is unreadable that small. Keep a simple ring spinner in the button's text colour, and keep the button's label ("Saving…").
- **Instead of skeletons.** Where the handoff specifies skeleton cards (plans list, discover results), keep the skeletons.

**Timing:** show only after 300 ms of loading; once shown, keep it at least 500 ms. Pair it with a short line where it helps ("Finding plans near you…"). On web, use `role="status"`; on mobile, the accessibility label is "Loading".

The splash screen stays static (see the logo README). The spinner takes over if loading is still going after the splash.
