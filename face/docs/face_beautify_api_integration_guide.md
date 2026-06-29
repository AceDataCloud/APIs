# Face Beautify API Integration Instructions

This article introduces the Face Beautify API integration instructions, which enhances a portrait with adjustable smoothing, whitening, face-lifting, and eye-enlarging controls.

## Application Process

To use the Face Beautify API, apply for the corresponding service on the [Face Beautify API](https://platform.acedata.cloud/documents/7d536eb6-8fea-48d5-a050-43aa57a23f7e) page. After entering the page, click the "Acquire" button.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

There is a free quota available for first-time applicants, allowing you to use this API for free. **One API key can call every service on the platform — you do not need to apply separately for each service.**

## Basic Usage

The most basic usage is to provide an `image_url`. The result is the beautified image. The request body fields are described below:

- `image_url`: the portrait to beautify (required).
- `smoothing`: skin smoothing strength.
- `whitening`: skin whitening strength.
- `face_lifting`: face slimming strength.
- `eye_enlarging`: eye enlargement strength.

### Request Example

```bash
curl -X POST 'https://api.acedata.cloud/face/beautify' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "image_url": "https://example.com/portrait.jpg",
    "smoothing": 5,
    "whitening": 5
  }'
```

### Response Example

```json
{
  "image_url": "https://faceeffect-1254418846.cos.ap-guangzhou.myqcloud.com/fmu/BeautifyPic/1256437459/4027c868-60e9-40e0-b929-0fdb69dcf3c1"
}
```

Download the beautified image from the `image_url` field.

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
