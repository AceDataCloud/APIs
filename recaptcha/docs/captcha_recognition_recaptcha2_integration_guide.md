# Recaptcha2 Image Recognition API Integration Instructions

This article will introduce a Recaptcha2 image recognition API integration, which can identify the content entered by the user and the Recaptcha2 verification image, and finally return the coordinates of the small images that need to be clicked to complete the verification.

## Application Process

To use the Recaptcha2 image recognition API, first go to the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) to obtain your API Token for future use.

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in, and after completion, you will be automatically returned to the current page.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application will grant a free quota for a trial experience; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> Complete Documentation: [Recaptcha2 Image Recognition API](https://platform.acedata.cloud/documents/captcha-recognition-recaptcha2)

## Basic Usage

First, let's understand the basic usage. We need to capture the Recaptcha2 verification image from the website. The URL of the example website is: `https://www.google.com/recaptcha/api2/demo`. We need to click the checkbox of the verification code to display the verification image. We need to simply pass a field called `image`, which is the specific Recaptcha2 verification image. The image must be scaled to standard sizes (100x100, 300x300, 450x450) so that the service can determine the image type. You need to compress the image yourself; this article recommends using [Photopea](https://www.photopea.com/) where you can resize and compress the image.

You also need to input the recognition content parameter related to the verification image, `question`. We only provide the following content table for reference:

### Chinese Content Table

```json
{
  "/m/0pg52": "出租车",
  "/m/01bjv": "巴士",
  "/m/02yvhj": "校车",
  "/m/04_sv": "摩托车",
  "/m/013xlm": "拖拉机",
  "/m/01jk_4": "烟囱",
  "/m/014xcs": "人行横道",
  "/m/015qff": "红绿灯",
  "/m/0199g": "自行车",
  "/m/015qbp": "停车计价表",
  "/m/0k4j": "汽车",
  "/m/015kr": "桥",
  "/m/019jd": "船",
  "/m/0cdl1": "棕榈树",
  "/m/09d_r": "山",
  "/m/01pns0": "消防栓",
  "/m/01lynh": "楼梯"
}
```

### English Content Table

```json
{
  "/m/0pg52": "taxis",
  "/m/01bjv": "bus",
  "/m/02yvhj": "school bus",
  "/m/04_sv": "motorcycles",
  "/m/013xlm": "tractors",
  "/m/01jk_4": "chimneys",
  "/m/014xcs": "crosswalks",
  "/m/015qff": "traffic lights",
  "/m/0199g": "bicycles",
  "/m/015qbp": "parking meters",
  "/m/0k4j": "cars",
  "/m/015kr": "bridges",
  "/m/019jd": "boats",
  "/m/0cdl1": "palm trees",
  "/m/09d_r": "mountains or hills",
  "/m/01pns0": "fire hydrant",
  "/m/01lynh": "stairs"
}
```

The Request Headers include:

- `accept`: the format of the response result you want to receive, here filled in as `application/json`, which is JSON format.
- `authorization`: the key to call the API, which can be selected directly after application.

The Request Body includes:

- `image`: the Base64 encoded verification image.
- `question`: the question ID, please refer to the table, starting with `/m/`.

### Request Example

```shell
curl -X POST 'https://api.acedata.cloud/captcha/recognition/recaptcha2' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "question": "/m/01pns0",
  "image": "iVBORw0KGgoAAAANSUhEUgAAASoAAAEsCAIAAAD7AWllAAAAAX..."
}'
```

The Python integration code is as follows:

```python
import requests

url = "https://api.acedata.cloud/captcha/recognition/recaptcha2"

headers = {
    "accept": "application/json",
    "authorization": "******",
    "content-type": "application/json"
}

payload = {
    "question": "/m/01pns0",
    "image": "iVBORw0KGgoAAAANSUhEUgAAASoAAAEsCAIAAAD7AWllAAAAAX..."
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "solution": {
    "size": 300,
    "label": "/m/01pns0",
    "confidences": [
      0,
      0.0007,
      1,
      0.0003,
      0.0046,
      1,
      0,
      1,
      0
    ],
    "objects": [
      2,
      5,
      7
    ],
    "type": "multi"
  }
}
```

The returned result contains multiple fields, described as follows:

- `solution`, the verification result after processing the Recaptcha2 verification image task.
    - `size`, the size of the Recaptcha2 verification image.
    - `label`, the content recognized from the Recaptcha2 verification image.
    - `confidences`, the confidence levels of the recognized areas in the Recaptcha2 verification image, with areas starting from 0.
    - `objects`, the areas that meet the recognized content in the Recaptcha2 verification image, with areas starting from 0.
    - `type`, the type of the Recaptcha2 verification image task, which is `multi` when there are multiple areas.

We can see that we have obtained the verification result for processing the Recaptcha2 verification image. We first divide the verification image into areas. The areas start from 0, and from the result in `objects`, we obtained 2, 5, and 7. We only need to simulate clicking on these three areas of the verification code to pass the verification.

## Asynchronous Mode (async)

By default, the API is synchronous and blocking: a request will wait until the recognition result is processed before returning. If you are doing multi-solver rotation and want to "immediately get the task_id after submitting the task, schedule other solvers, and come back later for the result," you can pass `async: true` in the request body.

After passing `async: true`, the interface will immediately return a `task_id` without blocking:

```shell
curl -X POST 'https://api.acedata.cloud/captcha/recognition/recaptcha2' \
-H 'accept: application/json' \
-H 'authorization: ******' \
-H 'content-type: application/json' \
-d '{
  "question": "/m/01pns0",
  "image": "iVBORw0KGgoAAAANSUhEUgAAASoAAAEsCAIAAAD7AWllAAAAAX...",
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

When processing is complete, it will return `status: ready` and the recognition result `solution` (the field structure is completely consistent with the synchronous mode):

```json
{
  "success": true,
  "task_id": "61138bb6-19aa-11ec-a9c8-0242ac110002",
  "status": "ready",
  "solution": {
    "size": 300,
    "label": "/m/01pns0",
    "objects": [2, 5, 7],
    "type": "multi"
  }
}
```

Billing Note: In asynchronous mode, creating tasks and polling "processing" do not incur charges; **only when successfully obtaining the recognition result is there a charge (consistent with the price of synchronous mode)**. Therefore, canceling unfinished tasks during rotation will not incur costs. `/captcha/tasks` is applicable to all captcha interfaces (token and recognition series), and you can poll with the same `task_id`.

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
