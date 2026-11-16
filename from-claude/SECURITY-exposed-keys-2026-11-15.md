# Security: live keys exposed in togetherplans (public repo)

**Found:** 2026-11-15, 10:18 PM ET, by Claude (read-only scan of the HEAD and all 399 commits)

`.github/workflows/deploy.yml` (≈ line 74, the `--update-env-vars` string) contains these in plain text, committed since **2026-10-10** (commits f83de7b, f4a1172):
- `STRIPE_SECRET_KEY` (a **live** restricted key, `rk_live_…`)
- `STRIPE_WEBHOOK_SECRET` (`whsec_…`)
- `FIRECRAWL_API_KEY` (`fc-…`)

The repo is public, so treat all three as compromised.

## Order of operations
1. **Jake rolls the keys first:**
   - Stripe → Developers → API keys → roll/delete the restricted key
   - Stripe → Webhooks → roll the signing secret
   - Firecrawl → revoke and create a new key
2. **Jake makes `togetherplans` (and `Jarvis`) private.**
3. **Hermes:** put the new values in GitHub Actions secrets (or GCP Secret Manager) and reference them:
   ```yaml
   --update-env-vars "GCS_BUCKET=datemeup-business-assets" \
   --update-secrets "STRIPE_SECRET_KEY=stripe-secret-key:latest,STRIPE_WEBHOOK_SECRET=stripe-webhook-secret:latest,FIRECRAWL_API_KEY=firecrawl-api-key:latest"
   ```
   (Cloud Run `--update-secrets` with Secret Manager is preferred over plain env vars.)
4. Don't bother rewriting git history to remove the old values. Rolling them is what matters; the old values become useless.

## Everything else is clean
No other real credentials in the current tree or history:
- DB URLs are localhost dev only.
- `sk_live_...` in `.hermes/plans/…` is a placeholder.
- No keystore, `.p8`, Apple/Google config, service-account JSON or real `.env` is committed.
- `web/.env.production` only holds `VITE_API_URL`.

## Going forward
Never put passwords, API keys or tokens in the Jarvis channel or any repo file. Refer to them by name ("the Stripe key in Secret Manager") instead.
