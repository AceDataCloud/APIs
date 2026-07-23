# hCaptcha Protocol Recognition API Integration Instructions

This article will introduce a method for integrating the hCaptcha protocol recognition API, which allows users to bypass the identification and clicking of hCaptcha verification images, and instead achieve automatic decoding in the background by simply submitting the Website Key.

## Application Process

To use the hCaptcha protocol recognition API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token for future use.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in, after which you will be automatically returned to the current page.

**One API Token can call all services on the platform, without the need to apply separately for each service.** The first application will grant a free quota for a trial experience; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete Documentation: [hCaptcha Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-hcaptcha)

## Basic Usage

First, understand the basic usage method, which is to input the URL of the website that needs to process the hCaptcha verification code to obtain the processed result. You first need to simply pass a `website_url` field. Our example website is: `https://accounts.hcaptcha.com/demo`, and we need to obtain the `website_key` from the `website_url` page. First, open this webpage, press F12 to enter the console, and then perform a global search for `hcaptcha-demo` on the Element page. The string corresponding to `data-sitekey` is the value of the `website_key`.

The Request Headers include:

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which means JSON format.
- `authorization`: the key for calling the API, which can be directly selected after application.

The Request Body includes:

- `website_url`: the URL of the website that needs to process the verification code.
- `website_key`: the website key identifier in hCaptcha.

### Request Example

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
  "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9......"
}
```

We can see that we have obtained the verification result for processing the hCaptcha verification code, which we can use for POST or simulate submission to the target website, for one-time use, valid for 120 seconds, and it is recommended to use it within 60 seconds.

To submit the processed token to the target website to pass the hCaptcha verification, we need to find how the website sends the POST request. We need to open the F12 console and manually go through the verification. Once the verification completes, check the POST request in the network tab. For the demo site `https://accounts.hcaptcha.com/demo`, the CURL code for submitting the token is as follows:

```shell
curl 'https://accounts.hcaptcha.com/demo' \
  --data-raw 'email=&g-recaptcha-response={token}&h-captcha-response={token}'
```

The corresponding Python code is as follows:

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

## Asynchronous Mode (async)

By default, the API is synchronous and blocking: a request will wait until the token processing is complete before returning. If you are doing multi-solver rotation and want to "immediately get the task_id after submitting the task, schedule other solvers, and come back later to get the result," you can pass `async: true` in the request body.

After passing `async: true`, the interface will immediately return a `task_id` without blocking:

```shell
curl -X POST 'https://api.acedata.cloud/captcha/token/hcaptcha' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_key": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",
  "website_url": "https://accounts.hcaptcha.com/demo",
  "async": true
}'
```

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab",
  "status": "processing"
}
```

Then use the `task_id` to poll `POST /captcha/tasks` (recommended every 3-5 seconds) to get the result:

```shell
curl -X POST 'https://api.acedata.cloud/captcha/tasks' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002"
}'
```

During processing, it will return `status: processing`:

```json
{ "success": true, "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002", "status": "processing" }
```

When processing is complete, it will return `status: ready` and the token:

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "ready",
  "token": "P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni......"
}
```

Billing Explanation: In asynchronous mode, creating tasks and polling "processing" do not incur charges; **only when successfully obtaining the token is there a charge once** (consistent with the price of synchronous mode). Therefore, canceling unfinished tasks during rotation will not incur costs. `/captcha/tasks` is applicable to all verification code interfaces (token and recognition series, such as hcaptcha, recaptcha2, recaptcha3, recognition/*, etc.), and the same `task_id` can be used for polling.

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
