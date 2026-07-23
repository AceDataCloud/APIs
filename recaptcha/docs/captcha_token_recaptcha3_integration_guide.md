# Recaptcha3 Protocol Recognition API Integration Instructions

This article will introduce a Recaptcha3 protocol recognition API integration instruction, which allows users to complete verification without recognizing and clicking on Recaptcha3 captcha images, simply by submitting the Website Key for automatic decoding in the background.

## Application Process

To use the Recaptcha3 protocol recognition API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token for future use.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in, and after completion, you will be automatically returned to the current page.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application will grant a free quota for a trial experience; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete documentation: [Recaptcha3 Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-recaptcha3)

## Basic Usage

First, understand the basic usage method. Compared to Recaptcha2, we need to pass an additional parameter `page_action`, which needs to be obtained from the code. The demo URL for this presentation is: `https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php`.

### Quick Method to Obtain Parameters

Open F12, then search for `.execute(` in the Elements page. In the result, we can see the `action` parameter, and there is also a string following execute, which is the `website_key`.

Next, you need to input the URL of the website that requires captcha processing to obtain the processed result. First, you need to simply pass a `website_url` field, and finally, you need to input the parameter `website_key`.

The Request Headers include:

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which is JSON format.
- `authorization`: the key for calling the API, which can be directly selected after application.

The Request Body includes:

- `page_action`: needs to be obtained from the website code where the captcha is located.
- `website_url`: the URL of the website that requires captcha processing.
- `website_key`: the website key identifier in Recaptcha3.

### Request Example

```shell
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha3' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_url": "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
  "website_key": "6LdKlZEpAAAAAAOQjzC2v_d36tWxCl6dWsozdSy9",
  "page_action": "examples/v3scores"
}'
```

The Python integration code is as follows:

```python
import requests

url = "https://api.acedata.cloud/captcha/token/recaptcha3"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "website_url": "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
    "website_key": "6LdKlZEpAAAAAAOQjzC2v_d36tWxCl6dWsozdSy9",
    "page_action": "examples/v3scores"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "token": "03AFcWeA5mfdNlQD0RGX9PTWPs0l65QukjwbYObCue5hygRuA6......"
}
```

The return result contains multiple fields, described as follows:

- `token`, the verification result after processing the Recaptcha3 captcha task.

We can see that we have obtained the verification result for processing the Recaptcha3 captcha, which we can use for POST or GET to simulate submission to the target website, valid for 120 seconds, and it is recommended to use it within 60 seconds.

To verify the token against the target website:

```python
import requests

url = "https://recaptcha-demo.appspot.com/recaptcha-v3-verify.php?action=examples/v3scores&token='{token}'"

r = requests.get(url)
if r.status_code == 200:
    print(r.text)
```

The result will be:

```json
{
  "success": true,
  "hostname": "recaptcha-demo.appspot.com",
  "challenge_ts": "2024-09-14T08:52:26Z",
  "apk_package_name": null,
  "score": 0.9,
  "action": "examples/v3scores",
  "error-codes": []
}
```

The `success` field indicates the processing result of this verification, confirming that we have successfully passed the Recaptcha3 captcha verification.

## Asynchronous Mode (async)

By default, the API is synchronous and blocking: a request will wait until the token processing is complete before returning. If you are doing multi-solver rotation and want to "get the task_id immediately after submitting the task, schedule other solvers, and come back later for the result," you can pass `async: true` in the request body.

After passing `async: true`, the interface will immediately return a `task_id` without blocking:

```shell
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha3' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_url": "https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php",
  "website_key": "6LdKlZEpAAAAAAOQjzC2v_d36tWxCl6dWsozdSy9",
  "page_action": "examples/v3scores",
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
  "token": "03AFcWeA5mfdNlQD0RGX9PTWPs0l65QukjwbYObCue5hygRuA6......"
}
```

Billing Explanation: In asynchronous mode, creating tasks and polling "processing" are not charged; **only when successfully obtaining results is it charged once** (at the same price as synchronous mode). Therefore, canceling unfinished tasks during rotation will not incur costs. `/captcha/tasks` is applicable to all captcha interfaces (token and recognition series), and you can poll with the same `task_id`.

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
