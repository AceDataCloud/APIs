# hCaptcha Protocol Recognition API Integration Instructions

This article will introduce a method for integrating the hCaptcha Protocol Recognition API, which allows users to bypass the identification and clicking of hCaptcha verification images, and instead achieve automatic decoding in the background by simply submitting the Website Key.

## Application Process

To use hCaptcha Protocol Recognition API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back to this page automatically.

**A single API Token works across every service on the platform — no need to subscribe per service.** New accounts receive free starter credit; when it runs low you can top up your shared balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Full documentation: [hCaptcha Protocol Recognition API →](https://platform.acedata.cloud/documents/captcha-token-hcaptcha)

## Basic Usage

The basic usage is to input the URL of the website that needs to process the hCaptcha verification code and the website key to obtain a token.

To get the `website_key` from a target page, open the page in a browser, press F12 to enter the console, and perform a global search for `data-sitekey` in the Elements panel. The string value of `data-sitekey` is the `website_key`.

**Request Headers** include:

- `accept`: the format of the response result you want to receive, set to `application/json`.
- `authorization`: the key for calling the API.

**Request Body** includes:

- `website_url`: the URL of the website that needs to process the verification code.
- `website_key`: the website key identifier in hCaptcha.

### Code Example

```shell
curl -X POST 'https://api.acedata.cloud/captcha/token/hcaptcha' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
  "website_url": "https://accounts.hcaptcha.com/demo"
}'
```

The Python integration code is as follows:

```python
import requests

url = "https://api.acedata.cloud/captcha/token/hcaptcha"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
    "website_url": "https://accounts.hcaptcha.com/demo"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

The returned `token` is valid for one-time use with a validity period of 120 seconds. It is recommended to use it within 60 seconds.

## Using the Token

Once you have the token, you can submit it to the target website. First, understand how the website sends its POST request by using the browser's developer tools to inspect the network requests during verification.

For example, for `https://accounts.hcaptcha.com/demo`, the CURL code for calling the token verification is:

```shell
curl 'https://accounts.hcaptcha.com/demo' \
  --data-raw 'email=&g-recaptcha-response={token}&h-captcha-response={token}'
```

The corresponding Python code is:

```python
import requests

token = '{token}'

data = {
    'email': '',
    'g-recaptcha-response': token,
    'h-captcha-response': token
}

response = requests.post('https://accounts.hcaptcha.com/demo', data=data)

if response.status_code == 200:
    print(response.text)
```

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
