# Veo Extend API Integration Guide

This guide describes how to integrate the Veo Extend API. This endpoint is used to **extend the duration** of an already-generated Veo video — the AI automatically generates the continuation of the scene.

## Application Process

To use the API, you first need to apply for the corresponding service on the Veo service page. If you are not logged in or registered, you will be automatically redirected to the login page.

## Basic Usage

This endpoint requires the following parameters:

- `video_id` (required): The task ID of the source video (from `/veo/videos` or from a previous call to this endpoint itself).
- `model` (required): The model used for extension. **Only `veo31-fast` and `veo31` are supported** — other models are not supported upstream.
- `prompt` (optional): A text prompt to guide the continuation of the scene.

### Request Example

```shell
curl -X POST 'https://api.acedata.cloud/veo/extend' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "video_id": "dd01fc69-e1f7-4b68-aa8c-463f6b748d11",
    "model": "veo31-fast",
    "prompt": "the camera slowly zooms out to reveal more of the landscape"
  }'
```

### Response Example

The response follows the same structure as `/veo/videos`:

```json
{
  "success": true,
  "task_id": "5fa2d9a6-7e54-481b-a4b0-3dc6f25dd2ab",
  "data": [
    {
      "id": "9b6f3b6b9c45419fbf2e3fe2f10b2b3a",
      "video_url": "https://platform.cdn.acedata.cloud/veo/5fa2d9a6.mp4",
      "created_at": "2025-07-25 16:07:43",
      "complete_at": "2025-07-25 16:10:28",
      "state": "succeeded"
    }
  ]
}
```

## Important Limitations

The extended video output from `/veo/extend` **can be used as input for another `/veo/extend` call** (i.e., you can chain extensions), but it **cannot** be processed by the following endpoints:

- `/veo/reshoot` — camera motion cannot be changed on an extended video
- `/veo/objects` — objects cannot be added or removed from an extended video

If you pass a `video_id` that is the result of `/veo/extend`, those endpoints will return a 400 error. Use the original source video instead.

## Pricing

- `model=veo31-fast`: 1.20 Credit / request
- `model=veo31`: 7.64 Credit / request

## Asynchronous Callback

This endpoint supports asynchronous mode. Pass a `callback_url` to receive the result via a POST request once the task is complete.

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

## Conclusion

Through this document, you have learned how to use the Veo Extend API to extend the duration of a generated video. If you have any questions, please feel free to contact our technical support team.
