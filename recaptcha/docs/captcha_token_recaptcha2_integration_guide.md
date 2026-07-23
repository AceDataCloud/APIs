# Recaptcha2 Protocol Recognition API Integration Instructions

This article will introduce a Recaptcha2 protocol recognition API integration instruction, which allows users to bypass the recognition and clicking of Recaptcha2 verification images, achieving automatic decoding in the background by simply submitting the Website Key.

## Application Process

To use the Recaptcha2 protocol recognition API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token for future use.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in, and after completion, you will be automatically returned to the current page.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application will grant a free quota for a trial experience; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete Documentation: [Recaptcha2 Protocol Recognition API](https://platform.acedata.cloud/documents/captcha-token-recaptcha2)

## Basic Usage

First, understand the basic usage method, which is to input the URL of the website needing to process the verification code to obtain the processed result. You first need to simply pass a `website_url` field. Our example website is: `https://www.google.com/recaptcha/api2/demo`, and we need to obtain the `website_key` from the `website_url` page. First, open this webpage, press F12 to enter the console, and then perform a global search for `recaptcha-demo` in the Element page. The string corresponding to `data-sitekey` is the value of the `website_key`.

The Request Headers include:

- `accept`: the format of the response result you want to receive, filled in as `application/json`, which is in JSON format.
- `authorization`: the key for calling the API, which can be directly selected after application.

The Request Body includes:

- `website_url`: the URL of the website needing to process the verification code.
- `website_key`: the website key identifier in Recaptcha2.

### Request Example

```shell
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha2' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
  "website_url": "https://www.google.com/recaptcha/api2/demo"
}'
```

The Python integration code is as follows:

```python
import requests

url = "https://api.acedata.cloud/captcha/token/recaptcha2"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "website_url": "https://www.google.com/recaptcha/api2/demo"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "token": "03AFcWeA5kjJyDQ9S1a9UYimR6nuxnpEnAs5x2Pixao0dXZhMB......"
}
```

The return result has multiple fields, described as follows:

- `token`, the verification result after processing the Recaptcha2 captcha task.

We can see that we have obtained the verification result for processing the Recaptcha2 captcha, which we can use for POST or simulate submission to the target website, for one-time use, valid for 120 seconds, and it is recommended to use it within 60 seconds.

To submit the processed token to the target website, we need to find how the website sends the POST request. Open F12 console and manually complete the verification. Once done, check the POST request in the network tab. For the demo site `https://www.google.com/recaptcha/api2/demo`, the CURL code for submitting the token is as follows:

```shell
curl 'https://www.google.com/recaptcha/api2/demo' \
  --data-raw 'g-recaptcha-response={token}'
```

The corresponding Python code is as follows:

```python
import requests

token = '{token}'

data = {
    'g-recaptcha-response': token,
}

response = requests.post('https://www.google.com/recaptcha/api2/demo', data=data)

if response.status_code:
    print(response.text)
```

## Asynchronous Mode (async)

By default, the API is synchronous and blocking: a request will wait until the token processing is complete before returning. If you are doing multi-solver rotation and want to "immediately get the task_id after submitting the task, schedule other solvers, and come back later to get the result," you can pass `async: true` in the request body.

After passing `async: true`, the interface will immediately return a `task_id` without blocking:

```shell
curl -X POST 'https://api.acedata.cloud/captcha/token/recaptcha2' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "website_key": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
  "website_url": "https://www.google.com/recaptcha/api2/demo",
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
  "token": "03AFcWeA5kjJyDQ9S1a9UYimR6nuxnpEnAs5x2Pixao0dXZhMB......"
}
```

Billing explanation: In asynchronous mode, creating tasks and polling "processing" do not incur charges; **only when successfully obtaining results is there a one-time charge** (consistent with the price of synchronous mode). Therefore, canceling unfinished tasks during rotation will not incur costs. `/captcha/tasks` is universal for all captcha interfaces (token and recognition series), and you can poll with the same `task_id`.

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
