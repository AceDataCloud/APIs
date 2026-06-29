# Face Swap API Integration Instructions

This article introduces the Face Swap API integration instructions, which replaces the face in a target image with the face from a source image.

## Application Process

To use the Face Swap API, apply for the corresponding service on the [Face Swap API](https://platform.acedata.cloud/documents/6be9e2dd-e3ca-4e8f-b38c-d5057e92354e) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free. **One API key can call every service on the platform — you do not need to apply separately for each service.**

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

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
