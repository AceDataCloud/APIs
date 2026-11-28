# Face Swap API Integration Instructions

This article introduces the Face Swap API integration instructions, which replaces the face in a target image with the face from a source image.

## Get an API key

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Click the copy button beside **API KEY**, marked **1** in the screenshot. Keep the key on your server and use it in place of `{token}` in the examples.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

API reference: [Face Swap API](https://platform.acedata.cloud/documents/6be9e2dd-e3ca-4e8f-b38c-d5057e92354e).

## Basic Usage

The most basic usage is to provide `source_image_url` and `target_image_url`. The result is the merged image. The request body fields are described below:

- `source_image_url`: the photo whose face is taken (required).
- `target_image_url`: the photo whose face is replaced (required).
- `timeout`: optional processing timeout in seconds.
- `callback_url`: an asynchronous callback URL.
- `async`: optional. When `true`, the API returns immediately with a `task_id`.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/face/swap' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "source_image_url": "https://example.com/source.jpg",
    "target_image_url": "https://example.com/target.jpg"
  }'
```

### Response Example

```json
{
  "image_url": "https://platform.cdn.acedata.cloud/face/swap-result.jpg"
}
```

Download the swapped image from the `image_url` field.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [platform documentation](https://platform.acedata.cloud/documents?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)
