# Digital English Captcha Recognition API Integration Instructions

This document will introduce a Digital English Captcha Recognition API integration guide, which is based on deep learning technology and can be used to recognize variable-length English numeric captchas. Input the content of the captcha image and output the captcha result.

## Application Process

To use Digital English Captcha Recognition API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> Full documentation: [Digital English Captcha Recognition API](https://platform.acedata.cloud/documents/captcha-recognition-image2text)

## Basic Usage

First, understand the basic usage method, which is to input the variable-length English numeric captcha image that needs to be processed to obtain the processed result. You need to simply pass a `image` field, which is the specific English numeric captcha image.

Convert the captcha image to a Base64 encoded captcha image. It is recommended to use the Google Chrome extension FeHelper for the conversion. The Base64 encoding should not include the prefix `data:image/png;base64`.

The Request Headers include:

- `accept`: the format of the response result you want to receive, here filled in as `application/json`, which is JSON format.
- `authorization`: the key to call the API, which can be directly selected after application.

The Request Body includes:

- `image`: the Base64 encoded captcha image (without the prefix `data:image/png;base64`).

### Request Example

```shell
curl -X POST 'https://api.acedata.cloud/captcha/recognition/image2text' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "image": "iVBORw0KGgoAAAANSUhEUgAAAgUAAAE3CAYAAAA6xjI2AAAAAX..."
}'
```

The Python integration code is as follows:

```python
import requests

url = "https://api.acedata.cloud/captcha/recognition/image2text"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "image": "iVBORw0KGgoAAAANSUhEUgAAAgUAAAE3CAYAAAA6xjI2AAAAAX..."
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "text": "7364"
}
```

The returned result contains multiple fields, described as follows:

- `text`: the text content after processing the variable-length English numeric captcha image task.

We can see that we have obtained the verification result for processing the variable-length English numeric captcha image, and we only need to verify based on the text content in the `text` result.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 token_mismatched`: Bad request, possibly due to missing or invalid parameters.
- `400 api_not_implemented`: Bad request, possibly due to missing or invalid parameters.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "api_error",
    "message": "fetch failed"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

## Support

If you meet any issue, please check [support info](https://platform.acedata.cloud/support) or browse the latest documentation on [docs.acedata.cloud](https://docs.acedata.cloud)
