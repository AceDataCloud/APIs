# Face Beautify API Integration Instructions

This article introduces the Face Beautify API integration instructions, which enhances a portrait with adjustable smoothing, whitening, face-lifting, and eye-enlarging controls.

## Get an API key

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Click the copy button beside **API KEY**, marked **1** in the screenshot. Keep the key on your server and use it in place of `{token}` in the examples.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

API reference: [Face Beautify API](https://platform.acedata.cloud/documents/7d536eb6-8fea-48d5-a050-43aa57a23f7e).

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

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [platform documentation](https://platform.acedata.cloud/documents?lang=en&utm_source=github&utm_medium=referral&utm_campaign=evergreen)
