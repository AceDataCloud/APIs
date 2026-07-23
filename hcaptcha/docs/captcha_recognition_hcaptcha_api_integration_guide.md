# hCaptcha Image Recognition API Integration Instructions

This article will introduce a method for integrating the hCaptcha image recognition API, which can identify the content entered by the user and the hCaptcha verification image, and finally return the coordinates of the small image that needs to be clicked to complete the verification.

## Application Process

To use hCaptcha Image Recognition API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [hCaptcha Image Recognition API →](https://platform.acedata.cloud/documents/recognition-hcaptcha-integration)

## Basic Usage

The basic usage is to input the hCaptcha verification image that needs to be processed to obtain the processed result. You need to pass a `queries` field containing the hCaptcha verification image as Base64 encoding, and a `question` field with the recognition content.

**Request Headers** include:

- `accept`: the format of the response result you want to receive, set to `application/json`.
- `authorization`: the key for calling the API.

**Request Body** includes:

- `queries`: a list of Base64 encoded verification images.
- `question`: the recognition content parameter related to the verification image, supporting direct input in Chinese and English.

### Code Example

```shell
curl -X POST 'https://api.acedata.cloud/captcha/recognition/hcaptcha' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "question": "Please click on the UNIQUE object among the others.",
  "queries": ["iVBORw0KGgoAAAANSU.....eY+85KVlzKHav28uq/WLVhL2kHUlFMKUcZbL31S8bpd0pEPKxNllXAE2wgu3uEfj+BfAzOGelsQNFAAAAAElFTkSuQmCC"]
}'
```

The Python integration code is as follows:

```python
import requests

url = "https://api.acedata.cloud/captcha/recognition/hcaptcha"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "question": "Please click on the UNIQUE object among the others.",
    "queries": ["iVBORw0KGgoAAAANSU.....eY+85KVlzKHav28uq/WLVhL2kHUlFMKUcZbL31S8bpd0pEPKxNllXAE2wgu3uEfj+BfAzOGelsQNFAAAAAElFTkSuQmCC"]
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "solution": {
    "label": "Please click on the UNIQUE object among the others",
    "box": [
      "360",
      "276"
    ],
    "confidences": 0.6354503631591797
  }
}
```

The returned result contains multiple fields:

- `solution`: the verification result after processing the hCaptcha verification image task.
  - `label`: the content recognized from the hCaptcha verification image.
  - `box`: the location information of the recognition result, composed of coordinate information of the image.
  - `confidences`: the confidence level of the recognition content.

The `box` coordinates define where to click in the verification image. The origin is at the lower left corner of the image, with the first value as the horizontal coordinate and the second as the vertical coordinate. Simulate a click at these coordinates to pass the verification.

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
