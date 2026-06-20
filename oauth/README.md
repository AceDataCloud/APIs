# OAuth — Sign in with Ace Data Cloud

OAuth 2.0 Authorization Code + PKCE integration for "Sign in with Ace Data Cloud".

![Platform](https://img.shields.io/badge/platform-Ace%20Data%20Cloud-0f766e?style=flat-square) ![API](https://img.shields.io/badge/type-OAuth%202.0-2563eb?style=flat-square) ![Docs](https://img.shields.io/badge/docs-online-16a34a?style=flat-square)

Authorization server: [auth.acedata.cloud](https://auth.acedata.cloud)

Keywords: oauth, oauth2, sign-in-with-ace-data-cloud, authorization-code, pkce, openid-connect, sso, developer-tools, Ace Data Cloud

## Why Use "Sign in with Ace Data Cloud"

- Let users log in to your app with their existing Ace Data Cloud account — no separate registration needed.
- Access Ace Data Cloud resources (API tokens, subscriptions, usage, orders) on behalf of the user after they grant consent.
- Standard OAuth 2.0 Authorization Code + PKCE flow — works with any existing OAuth client library (same as "Sign in with GitHub / Google").
- Suitable for web apps, CLIs, desktop apps, mobile apps, MCP clients, and AI Agents.

## Overview

Ace Data Cloud provides a standard OAuth 2.0 Authorization Server at `https://auth.acedata.cloud`. You register an OAuth application, redirect users to the authorization page, exchange the authorization code for an access token, and then call Ace Data Cloud APIs on the user's behalf.

The authorization server supports:

- `response_type=code` (Authorization Code flow)
- `grant_types`: `authorization_code`, `refresh_token`
- `code_challenge_methods`: `S256`, `plain` (PKCE)
- Client authentication: `client_secret_post` (confidential clients) / `none` (public PKCE clients)

Discovery endpoint:

```bash
curl https://auth.acedata.cloud/.well-known/oauth-authorization-server
```

## Quick Start

Register an OAuth application at [auth.acedata.cloud/user/oauth-apps](https://auth.acedata.cloud/user/oauth-apps), then redirect users to:

```
https://auth.acedata.cloud/oauth2/authorize
  ?response_type=code
  &client_id=<your_client_id>
  &redirect_uri=<your_redirect_uri>
  &scope=openid%20profile
  &state=<random_csrf_token>
```

After the user approves, exchange the `code` for an access token:

```bash
curl -X POST https://auth.acedata.cloud/oauth2/token \
  -d grant_type=authorization_code \
  -d code=<code> \
  -d client_id=<your_client_id> \
  -d client_secret=<your_client_secret> \
  -d redirect_uri=<your_redirect_uri>
```

## Guides

| Guide | Description |
| ----- | ----------- |
| [OAuth Integration Guide](docs/oauth_integration_guide.md) | Complete step-by-step guide to integrating "Sign in with Ace Data Cloud" |
