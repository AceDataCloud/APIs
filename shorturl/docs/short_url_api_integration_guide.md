# Short URL API Integration Instructions

This article introduces the Short URL API integration instructions, which generates a compact short link for a given long URL.

## Get an API key

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Click the copy button beside **API KEY**, marked **1** in the screenshot. Keep the key on your server and use it in place of `{token}` in the examples.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

API reference: [Short URL API](https://platform.acedata.cloud/documents/d57df7ea-e1ba-4873-905c-d4c072e40450).

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
