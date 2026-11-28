# Short URL API Integration Instructions

This article introduces the Short URL API integration instructions, which generates a compact short link for a given long URL.

## Application Process

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. Initialize it on your first visit if prompted, then copy the key shown in **API KEY**. Keep the copied key on your server and use it in place of `{token}` below.

![General Application API KEY field and copy button](https://cdn.acedata.cloud/dvc3cg.jpg)

[Short URL API](https://platform.acedata.cloud/documents/d57df7ea-e1ba-4873-905c-d4c072e40450)

There is a free quota available for first-time applicants, allowing you to use this API for free.

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

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [platform documentation](https://platform.acedata.cloud/documents?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)
