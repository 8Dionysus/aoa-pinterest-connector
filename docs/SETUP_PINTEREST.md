# Connect a Pinterest account

This is the fast owner-account path for Pinterest API v5.

## What Pinterest requires

- A Pinterest business account with verified email.
- Accepted Pinterest Developer Terms.
- A submitted app request approved for Trial access.
- A test access token with `user_accounts:read`, `boards:read`, and `pins:read`.

Pinterest reviews Trial applications. Once approved, the **My apps** page exposes
the app ID/secret and can generate a product-limited test token. Current test
tokens expire after 24 hours, so this path is for bootstrap validation, not an
unattended runtime.

## Fast bootstrap

1. Open <https://developers.pinterest.com/apps/> and sign in with the business account.
2. Accept the developer terms, choose **Connect app**, complete the request, and submit it.
3. After Trial approval, generate a test token with the three read scopes above.
4. On the connector host create the owner-local file:

   ```bash
   PYTHONPATH=src python -m aoa_pinterest_connector setup --json
   ```

5. Edit `~/.config/aoa-pinterest-connector/credentials.env` locally and paste the
   token after `AOA_PINTEREST_ACCESS_TOKEN=`. Never paste it into chat.
6. Validate locally, then perform the bounded reads:

   ```bash
   PYTHONPATH=src python -m aoa_pinterest_connector config-check --json
   PYTHONPATH=src python -m aoa_pinterest_connector auth-check --json
   PYTHONPATH=src python -m aoa_pinterest_connector pins-list --page-size 10 --json
   ```

## Safety posture

- The token is sent in the Authorization header, never in the URL.
- The credential file must be regular, current-user-owned, non-symlink, and mode `0600`.
- Responses are size-bounded and output never contains the token.
- These commands read only. Publication remains disabled.
- Full Authorization Code OAuth and continuous refresh are deferred until needed.

Official sources:

- https://developers.pinterest.com/docs/getting-started/connect-app/
- https://developers.pinterest.com/docs/getting-started/set-up-authentication-and-authorization/
- https://developers.pinterest.com/docs/getting-started/make-an-api-call/
- https://developers.pinterest.com/docs/key-concepts/access-tiers/
