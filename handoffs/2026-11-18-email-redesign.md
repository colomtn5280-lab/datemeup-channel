# Handoff: email redesign (all 12 emails), Claude → Jarvis
Date: 2026-11-18, ~11 PM ET. Jake approved the design and asked for every template to be replaced.

- **PR:** colomtn5280-lab/togetherplans, branch `feat/email-redesign`, PR #9 (link below)
- **Commit:** 7b238ea
- **Design reference (Jake has it):** "DateMeUp email redesign" canvas. Ticket style: dark ink hero, champagne labels, perforated stub, wine buttons on cream.
- **Rendered previews:** `from-claude/email-previews/` in this channel repo. Open any `.html` in a browser; `preview-sheet.png` shows invite / reminder / it's-a-plan / verify. Logos appear broken there only because the sandbox can't reach datemeup.app.

## What changed and where

All paths are relative to the togetherplans repo root.

| File | What |
|---|---|
| `backend/src/services/emailLayout.ts` | **NEW.** Shared building blocks: `layout()` (head, logo header, footer with Richmond address), `ticket()`, `stubField()`, `avatars()`, `button()`, `buttons()`, `card()`, `optionsCard()`, `eyebrow()`, `h1()`, `para()`, `note()`, `link()`, `divider()`. Helpers: `esc()`, `formatDay()`, `firstName()`, `nameList()`, `googleCalendarUrl()`. All colors and fonts live here. Change a look once and every email follows. |
| `backend/src/services/email.ts` | **REWRITTEN.** Each email now has a pure `buildXxxEmail(...)` that returns `{ subject, html }`, plus the existing `sendXxxEmail(...)`, which builds and sends via Resend. Deliverability headers and the plain-text fallback are kept. The template loading (`loadTemplate`, `getTemplates`, `renderTemplate`) is gone. |
| `backend/src/emails/*.html` | **DELETED** (all 12). HTML now comes from TypeScript, so there are no template files to copy at deploy. |
| `backend/Dockerfile` | Removed `&& cp -r src/emails dist/emails` from the build RUN line. **Required.** The folder no longer exists, so the old `cp` would fail the image build. |
| `backend/src/routes/invitations.ts` | Invite email now passes group member names and `invitation.expiresAt`. |
| `backend/src/routes/proposals.ts` | Nudge (`POST /:id/nudge`): proposal query now includes `creator.displayName`; the reminder gets options, votes-in count, member count, proposer and date. Counter (`POST /:id/counter`): loads the group name and passes the new options + date to the take-2 email. |
| `backend/src/routes/internal.ts` | 24h reminder job: same additions as nudge (adds `creator` to the include). |
| `backend/src/services/consensus.ts` | Match members now select `displayName`. Loads the group name (wrapped in try/catch so it can never block DECIDED). Passes winner name/address/eventDate plus group name and "going" names. |
| `backend/src/__tests__/email-templates.test.ts` | **NEW.** 17 tests: every email renders, with no `{{`, `undefined`, `null`, `NaN` or `<svg>`, and no fake sample text. Checks escaping, link routes, real data, and that output degrades cleanly when optional data is missing. |
| `web/src/pages/VerifyEmailPage.tsx` | If the URL has `?token=` (from the email link), it verifies automatically. The page used to need the token typed in, and the old email linked to `/verify/<token>`, which was a 404. |

## Function signatures (all backward compatible: new params are optional and go last)

```
sendVerifyEmail(to, name, email, token)
sendWelcomeEmail(to, email)
sendPasswordResetEmail(to, email, token)
sendGroupInviteEmail(to, inviter, groupName, token, { members?: string[], expiresAt? })
sendNewProposalEmail(to, proposer, title, proposalId, PlanExtra?)          // not called anywhere yet
sendStatusUpdateEmail(to, voterName, proposalId, PlanExtra & { title? }?)  // not called anywhere yet
sendVoteReminderEmail(to, email, proposalId, title, groupName?, PlanExtra?)
sendItsAMatchEmail(to, email, proposalId, title, WinnerInfo?, { groupName?, going?: string[] }?)
sendTake2Email(to, email, proposalId, title, proposerName, PlanExtra?)
sendPlanChangedEmail(to, email, proposalId, title, { change?, winner?, groupName? }?)  // not called yet
sendShareCardEmail(to, email, proposalId, cardId, senderName, { title?, note? }?)     // not called yet
sendAccountDeletedEmail(to, email)

PlanExtra  = { email?, groupName?, proposer?, options?: {name, category?, address?, eventDate?}[],
               votedCount?, memberCount?, dateTime? }
WinnerInfo = { name?, address?, eventDate? }
```

## Data mapping: where each field on screen comes from

| Email | On screen | Source |
|---|---|---|
| 04 Invite | "Join {group}" | `group.name` |
| | Inviter first name | `inviter.displayName` (first word) |
| | WHO'S IN avatars + "Maya, Theo, Ana + 1" | `group.members[].user.displayName`, ordered by `joinedAt` |
| | INVITE EXPIRES | `invitation.expiresAt` (72h TTL). The old copy wrongly said 7 days. |
| | Join button | `/join/{invitation.token}` |
| 07 Reminder | Headline | `proposal.title` |
| | "VOTE NEEDED · {group}" | `proposal.group.name` |
| | VOTES IN "3 of 4" | distinct voters (`votedUserIds.size`) / `group.members.length` |
| | SUGGESTED BY | `proposal.creator.displayName` |
| | WHEN | `proposal.dateTime` |
| | Options list (max 5) | `proposal.options[]`: `name`, `eventDate`, `address` |
| | Vote button | `/proposals/{id}` |
| 08 It's a plan | Headline | `winner.name` (falls back to `proposal.title`) |
| | DATE / WHERE | `winner.eventDate` (UTC calendar day) / `winner.address` |
| | GOING | all group members' `displayName` |
| | Add to calendar | Google Calendar all-day link built from winner name/date/address. Hidden if there's no date. |
| | See the plan / Choose a card | `/proposals/{id}`, `/proposals/{id}/invite-card` |
| 09 Take 2 | Options, date, group | `counter.options`, `counter.dateTime`, group name |
| 01 Verify | Button | `/verify-email?email=…&token=…` (JWT, 24h) |
| 03 Reset | Button | `/reset-password?token=…` (JWT, 1h). The old link `/reset/<token>` was a 404. |
| Footer (all) | Manage notifications | `/settings`. The old `/settings/notifications` was a 404, and so was the `List-Unsubscribe` header URL; both are fixed. |
| Header (all) | Logo | `https://datemeup.app/icon-192.png` (hosted PNG; email clients strip inline SVG) |

No schema changes and no migrations. Everything uses existing columns.

## What Jarvis needs to do

1. **Review and merge PR #9** into main. If main moved, rebase. Conflicts can only touch the files above.
2. **Check CI is green before walking away.** Last time a lint failure silently blocked the deploy. Locally: `npm run typecheck`, `npm run lint` (0 warnings) and `npm test` (73/73) all pass in `backend/`.
3. **Deploy the backend AND the web app.** The backend has the new emails and the Dockerfile change. The web app has the VerifyEmailPage auto-verify.
4. **Confirm `https://datemeup.app/icon-192.png`** returns the new wine icon in production.
5. **Live test.** Send a test to Jake for each of these and check them in Gmail (web + phone):
   - group invite (`POST /api/invitations`, method EMAIL)
   - vote reminder (`POST /api/proposals/:id/nudge`)
   - it's a plan (get a 2-person test group to unanimous approval)
   - verify (register a new test account; the button should land on /verify-email and verify automatically)
   - password reset (the button should open /reset-password with the token)
6. **Post back in CHANNEL.md** with the deploy commit and test results. Note anything that looks off; screenshots help.

## Not in scope / follow-ups

- 05 new proposal, 06 someone voted, 10 plan changed and 11 invite card received are designed and built, but **nothing calls them yet**. Wire them only when Jake wants those notifications, and pass the extras listed above.
- The headline font (Bricolage Grotesque via Google Fonts) shows in Apple Mail and iOS Mail. Gmail and Outlook fall back to Helvetica/Arial. This is expected.
- Outlook desktop squares off rounded corners. That's expected and harmless.

## Rules (unchanged)
No secrets in this channel (it's public). Production and account changes need Jake's OK; he has approved this redesign.
