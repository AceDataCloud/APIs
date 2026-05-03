# Veo Upsample API Integration Guide

This guide describes how to integrate the Veo Upsample API. This endpoint is used to upsample an already-generated Veo video or export it as an animated GIF preview.

## Application Process

To use the API, you first need to apply for the corresponding service on the Veo service page. If you are not logged in or registered, you will be automatically redirected to the login page.

## Basic Usage

This endpoint requires two parameters:

- `video_id`: The task ID of the source video. Can be a video ID from `/veo/videos`, `/veo/extend`, `/veo/reshoot`, or `/veo/objects`.
- `action`: The upsample action. Supported values:
  - `1080p`: Upsample the video to 1080p resolution.
  - `4k`: Upsample the video to 4K resolution.
  - `gif`: Convert the video to an animated GIF preview.

### Request Example

```shell
curl -X POST 'https://api.acedata.cloud/veo/upsample' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "video_id": "dd01fc69-e1f7-4b68-aa8c-463f6b748d11",
    "action": "4k"
  }'
```

### Response Example

The response follows the same structure as `/veo/videos`. It is an asynchronous task and you can query the task status via `/veo/tasks` using the `task_id`:

```json
{
  "success": true,
  "task_id": "8f5a90ae-3f86-4c4f-86f7-7126f5e92c76",
  "trace_id": "0f3e09c2-4c2e-46ea-9cdc-a31ec48b7c12",
  "data": [
    {
      "id": "253eedc47f1c4eb2a370ed2312168f4b",
      "video_url": "https://platform.cdn.acedata.cloud/veo/8f5a90ae.mp4",
      "created_at": "2025-07-25 16:07:43",
      "complete_at": "2025-07-25 16:10:28",
      "state": "succeeded"
    }
  ]
}
```

The response fields are:

- `success`: Whether the upsample task was submitted successfully.
- `task_id`: The ID of this upsample task.
- `data`: The upsampled video result.
  - `video_url`: The URL of the upsampled video.

## Pricing

- `action=1080p`: 0.16 Credit / request
- `action=4k`: 0.50 Credit / request
- `action=gif`: 0.13 Credit / request

If an unsupported `action` value is provided, it will be charged at 0.50 Credit by default. It is recommended to always specify a supported value explicitly.

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

Through this document, you have learned how to use the Veo Upsample API to upsample generated videos to higher resolutions or convert them to GIF previews. If you have any questions, please feel free to contact our technical support team.
