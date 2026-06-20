# OAuth Integration Guide — Sign in with Ace Data Cloud

Add "Sign in with Ace Data Cloud" to your product and, after the user grants consent, **act on behalf of the user** to read and write their Ace Data Cloud resources (profile, API tokens, subscriptions, usage, orders, etc.). The underlying protocol is standard **OAuth 2.0 Authorization Code + PKCE**, identical to "Sign in with GitHub / Google" — any OAuth client library you already have will work.

> **Ideal use cases**: Third-party apps, Agents, MCP clients, and automation workflows that want users to log in with their Ace Data Cloud account and access their platform resources without manually copying and pasting an API key.

## Endpoints Quick Reference

All endpoints are under `https://auth.acedata.cloud`. Retrieve the latest addresses at any time from the discovery endpoint:

```bash
curl https://auth.acedata.cloud/.well-known/oauth-authorization-server
```

| Purpose | Endpoint |
|---------|----------|
| Discovery document | `GET /.well-known/oauth-authorization-server` |
| Authorization page (browser redirect) | `GET https://auth.acedata.cloud/oauth2/authorize` |
| Token endpoint (exchange / refresh token) | `POST https://auth.acedata.cloud/oauth2/token` |
| Revoke token | `POST https://auth.acedata.cloud/oauth2/revoke` |
| User info (UserInfo) | `GET https://auth.acedata.cloud/api/v1/users/me` |
| OAuth app management (self-service) | `https://auth.acedata.cloud/user/oauth-apps` |

Supported capabilities: `response_type=code`, `grant_types=authorization_code, refresh_token`, `code_challenge_methods=S256, plain`, client authentication via `client_secret_post` (confidential clients) / `none` (PKCE public clients).

## Permission Scopes

Request the minimum scopes you need. Users will see each requested permission on the consent page.

**Identity (OIDC-compatible)**

| Scope | Meaning | Fields returned by `/users/me` |
|-------|---------|-------------------------------|
| `openid` | Unique user identifier | `id` |
| `profile` | Basic profile | `username`, `nickname`, `avatar`, `is_verified`, `date_joined` |
| `email` | Email address | `email` |
| `phone` | Phone number (sensitive) | `phone`, `region` |

**Platform resources**

| Scope | Meaning |
|-------|---------|
| `applications:read` / `applications:write` | Read / modify user's service subscriptions and quotas |
| `credentials:read` / `credentials:write` | Read / create / revoke user's API tokens |
| `usage:read` | Read user's call history |
| `orders:read` / `orders:write` | Read orders / place orders and initiate payment |

**Aggregate scopes (automatically expanded)**

| Scope | Expands to |
|-------|-----------|
| `platform:read` | `applications:read` + `credentials:read` + `usage:read` + `orders:read` |
| `platform:write` | `applications:write` + `credentials:write` + `orders:write` |
| `platform` | `platform:read` + `platform:write` |

**Special**

| Scope | Meaning |
|-------|---------|
| `offline_access` | Issues a **Refresh Token** (omitting this scope issues only an Access Token; re-authorization is required once it expires) |

> Typical combinations: Third-party "one-click login" = `openid profile`; MCP / IDE client that needs to auto-configure an API key = `openid profile credentials:read credentials:write`; full management console = `openid profile email platform offline_access`.

## Step 1: Register an OAuth Application

Open [auth.acedata.cloud/user/oauth-apps](https://auth.acedata.cloud/user/oauth-apps) → "Create Application" and fill in:

1. **Application name / description / logo**: Displayed on the user consent page.
2. **Client type**:
   - **Confidential** — You have a backend that can securely store `client_secret` (web service, backend service).
   - **Public** — Pure frontend / desktop / CLI / mobile, **cannot** store a secret; **must** use **PKCE**.
3. **Redirect URIs**: The URL users are redirected to after authorization. **Must exactly match the `redirect_uri` you send in the authorization request.** Multiple values are allowed.
4. **Scopes**: Check the scopes you need from the section above.

After saving you receive a **`client_id`**; confidential clients also get a **one-time-display** **`client_secret`** — save it immediately, it cannot be viewed again (you can rotate it from the app detail page with "Rotate Secret", which immediately invalidates the old secret).

> Each account can create a maximum of **20** OAuth applications.

## Step 2: Redirect the User to the Authorization Page

In your application, redirect the user's browser to the authorization page with query parameters:

```
https://auth.acedata.cloud/oauth2/authorize
  ?response_type=code
  &client_id=<your_client_id>
  &redirect_uri=<your_registered_redirect_uri>
  &scope=openid%20profile%20credentials:read
  &state=<random_csrf_string>
  &code_challenge=<PKCE_challenge>          # required for public clients
  &code_challenge_method=S256              # required for public clients
```

- `state`: A random string you generate. Returned unchanged in the callback. **Always verify it** to prevent CSRF.
- **PKCE (mandatory for public clients, also recommended for confidential clients)**: Generate a random `code_verifier`, then compute
  `code_challenge = BASE64URL( SHA256( code_verifier ) )`, include `code_challenge` in the authorization URL, and keep `code_verifier` for Step 3.

After the user logs in and clicks "Allow", the browser is redirected to:

```
<redirect_uri>?code=<authorization_code>&state=<original_state_value>
```

If the user denies: `<redirect_uri>?error=access_denied&error_description=...&state=...`

> Authorization codes are valid for **10 minutes** and are **single-use**.

## Step 3: Exchange the Authorization Code for Tokens

Use the `code` from Step 2 to call the token endpoint from your **backend** (confidential client) or client (PKCE public client).

**Confidential client (with client_secret):**

```bash
curl -X POST https://auth.acedata.cloud/oauth2/token \
  -d grant_type=authorization_code \
  -d code=<code_from_previous_step> \
  -d client_id=<your_client_id> \
  -d client_secret=<your_client_secret> \
  -d redirect_uri=<exact_same_redirect_uri_as_step_2>
```

**Public client (PKCE, no client_secret):**

```bash
curl -X POST https://auth.acedata.cloud/oauth2/token \
  -d grant_type=authorization_code \
  -d code=<code> \
  -d client_id=<your_client_id> \
  -d code_verifier=<code_verifier_from_step_2> \
  -d redirect_uri=<redirect_uri>
```

Successful response (`refresh_token` only appears when `offline_access` was requested):

```json
{
  "access_token": "<JWT>",
  "token_type": "Bearer",
  "expires_in": 1296000,
  "scope": "openid profile credentials:read",
  "refresh_token": "<JWT, only when offline_access was requested>"
}
```

The `access_token` is a JWT containing a `scope` claim. Validity: **15 days** (`expires_in` seconds). Refresh Token validity: **30 days**.

## Step 4: Call APIs with the Access Token

Place the token in the `Authorization: Bearer` header.

**Read user info (UserInfo — fields filtered to authorized scopes):**

```bash
curl https://auth.acedata.cloud/api/v1/users/me \
  -H "Authorization: ******"
```

**Call platform resource APIs** (`api.acedata.cloud`, authorized by scope). Example with `credentials:read`:

```bash
curl https://api.acedata.cloud/api/v1/credentials/ \
  -H "Authorization: ******"
```

The platform backend verifies the `scope` claim inside the JWT — the token can only access resources the user has authorized. Accessing an unauthorized resource returns `403`.

## Refreshing Tokens

When the Access Token expires, use the Refresh Token to obtain a new token pair (requires `offline_access` to have been requested):

```bash
curl -X POST https://auth.acedata.cloud/oauth2/token \
  -d grant_type=refresh_token \
  -d refresh_token=<your_refresh_token>
```

The response structure is the same as Step 3. The scope is **preserved** from the original authorization. After refreshing, the old Refresh Token is invalidated (rotation) — save the new one.

## Revoking Tokens

```bash
curl -X POST https://auth.acedata.cloud/oauth2/revoke \
  -d token=<access_token_or_refresh_token>
```

## Real-World Example: Ace Data Cloud's Own MCP Servers

Ace Data Cloud's 15+ MCP servers (NanoBanana, Midjourney, Suno, Seedance, Kling, …) use this exact flow for the "Sign in with Ace Data Cloud" connection in Claude Desktop / Cursor. They are all registered as **public (PKCE)** OAuth applications, request `credentials`-related scopes, and after the user authorizes, the MCP server can call `api.acedata.cloud` on their behalf — no manual API key copying required. Your integration works the same way.

## Common Errors

Error responses are uniformly structured as `{ "error": "<code>", "error_description": "<human-readable message>" }`:

| error | Meaning / Troubleshooting |
|-------|--------------------------|
| `invalid_request` | Missing or invalid parameter (e.g., missing `code` or `client_id`) |
| `invalid_client` | `client_id` does not exist, app is disabled, or `client_secret` is wrong |
| `invalid_grant` | Authorization code not found / expired (>10 minutes) / already used / PKCE verification failed / `redirect_uri` does not match the one used during authorization |
| `access_denied` | User clicked "Deny" on the consent page |
| `unsupported_grant_type` | `grant_type` is not `authorization_code` or `refresh_token` |

## Limits Quick Reference

| Item | Value |
|------|-------|
| Max OAuth apps per account | 20 |
| Authorization code validity | 10 minutes, single-use |
| Access Token validity | 15 days |
| Refresh Token validity | 30 days (rotated on refresh) |
| `redirect_uri` | Must exactly match the registered value |
| `client_secret` | Shown only once at creation / rotation; stored as SHA-256 hash on the server |
