# Short URL API Integration Instructions

This article introduces the Short URL API integration instructions, which generates a compact short link for a given long URL.

## Application Process

To use the Short URL API, apply for the corresponding service on the [Short URL API](https://platform.acedata.cloud/documents/d57df7ea-e1ba-4873-905c-d4c072e40450) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free. **One API key can call every service on the platform — you do not need to apply separately for each service.**

## Basic Usage

The most basic usage is to send the original URL in `content`. The result is the short link. The request body fields are described below:

- `content`: the long URL to shorten (required).

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/shorturl' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "content": "https://platform.acedata.cloud/service/shorturl"
  }'
```

### Response Example

```json
{
  "data": { "url": "https://suro.id/abc123" },
  "success": true
}
```

The shortened link is returned in `data.url`.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
