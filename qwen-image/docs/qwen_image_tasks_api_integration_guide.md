# Qwen Image Tasks API Integration and Usage

The Qwen Image Tasks API queries the execution status and results of tasks created by the Qwen Image Images API.

## Application Process

To use the Qwen Image Tasks API, first open the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications) and copy your API Token.

If you are not logged in, you will be redirected to sign in and brought back automatically.

**One API Token can call all services on the platform without needing to apply separately for each service.** The first application will grant a free quota for a trial experience; when the quota is insufficient, you can recharge the general balance in the [console](https://platform.acedata.cloud/console/coin).

> 📘 Complete Documentation: [Qwen Image Tasks API →](https://platform.acedata.cloud/documents/qwen-image-tasks)

## Request Example

Use a task ID returned by the Qwen Image Images API to retrieve one task, or use multiple task IDs to retrieve tasks in a batch.

### Setting Request Headers and Request Body

**Request Headers** include:

- `accept`: Specifies that the response should be in JSON format, set to `application/json`.
- `authorization`: your Ace Data Cloud API Token.
- `content-type`: `application/json`.

**Request Body** includes:

- `id`: task ID for a single-task query.
- `ids`: task ID array for a batch query.
- `action`: operation method, `retrieve` or `retrieve_batch`. The default is `retrieve`.

### Retrieve One Task

```bash
curl -X POST 'https://api.acedata.cloud/qwen-image/tasks' \
-H 'accept: application/json' \
-H 'authorization: YOUR_API_TOKEN' \
-H 'content-type: application/json' \
-d '{
  "id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "action": "retrieve"
}'
```

### Python Example

```python
import requests

url = "https://api.acedata.cloud/qwen-image/tasks"

headers = {
    "accept": "application/json",
    "authorization": "YOUR_API_TOKEN",
    "content-type": "application/json"
}

payload = {
    "id": "ec22ae22-0140-4033-8c86-a48b536da595",
    "action": "retrieve"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

### Response Example

```json
{
  "id": "ec22ae22-0140-4033-8c86-a48b536da595",
  "type": "images",
  "trace_id": "1cc87db0-8ee5-4436-969b-35cc571a9fd5",
  "created_at": 1769262721.763,
  "started_at": 1769262721.823,
  "finished_at": 1769262731.094,
  "elapsed": 9.271,
  "request": {
    "model": "qwen-image-3.0",
    "prompt": "a serene mountain lake at sunrise, photorealistic",
    "size": "1024*1024"
  },
  "response": {
    "success": true,
    "task_id": "ec22ae22-0140-4033-8c86-a48b536da595",
    "data": [
      {
        "image_url": "https://cdn.acedata.cloud/qwen-image/example.png"
      }
    ]
  }
}
```

The returned result contains multiple fields, with the `request` field being the request body when the task was initiated and the `response` field being the response body returned after the task is completed.

- `id`: task identifier.
- `type`: task type.
- `trace_id`: request trace identifier.
- `request`: original request information.
- `response`: task result information.
- `created_at`: task creation time, Unix timestamp in seconds.
- `started_at`: task start time, Unix timestamp in seconds.
- `finished_at`: task completion time, Unix timestamp in seconds. This field is not returned if the task is not completed.
- `elapsed`: task execution time in seconds. This field is not returned if the task is not completed.

## Batch Query Operation

For querying multiple task IDs, set `action` to `retrieve_batch` and pass `ids`.

```bash
curl -X POST 'https://api.acedata.cloud/qwen-image/tasks' \
-H 'accept: application/json' \
-H 'authorization: YOUR_API_TOKEN' \
-H 'content-type: application/json' \
-d '{
  "ids": ["ec22ae22-0140-4033-8c86-a48b536da595", "ec22ae22-0140-4033-8c86-a48b536da596"],
  "action": "retrieve_batch"
}'
```

### Batch Response Example

```json
{
  "items": [
    {
      "id": "ec22ae22-0140-4033-8c86-a48b536da595",
      "type": "images",
      "trace_id": "1cc87db0-8ee5-4436-969b-35cc571a9fd5",
      "created_at": 1769262721.763,
      "request": {
        "model": "qwen-image-3.0",
        "prompt": "a serene mountain lake at sunrise, photorealistic"
      },
      "response": {
        "success": true,
        "data": [
          {
            "image_url": "https://cdn.acedata.cloud/qwen-image/example.png"
          }
        ]
      }
    }
  ],
  "count": 1
}
```

- `items`: array of matching task records.
- `count`: number of tasks returned in this batch query.

If the requested task does not exist, the API may return an empty object.

## Error Handling

When calling the API, if an error occurs, the API will return the corresponding error code and message. For example:

- `400 token_mismatched`: Bad request, the token is not matched with this API.
- `400 api_not_implemented`: Bad request, the API is not implemented.
- `401 invalid_token`: Unauthorized, invalid or missing authorization token.
- `429 too_many_requests`: Too many requests, you have exceeded the rate limit.
- `500 api_error`: Internal server error, something went wrong on the server.

### Error Response Example

```json
{
  "error": {
    "code": "api_error",
    "message": "Internal server error."
  },
  "trace_id": "2efa9340-b21b-4e26-9e14-4aac95f343ab"
}
```

## Conclusion

Through this document, you have learned how to use the Qwen Image Tasks API to query single or batch image tasks. If you have any questions, please contact our technical support team.
