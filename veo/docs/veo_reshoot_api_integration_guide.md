# Veo Reshoot API Integration Guide

This guide describes how to integrate the Veo Reshoot API. This endpoint is used to **regenerate a Veo video with a new camera motion style** — the scene content stays the same, but the camera position and movement are re-interpreted according to the `motion_type`.

## Application Process

To use the API, you first need to apply for the corresponding service on the Veo service page. If you are not logged in or registered, you will be automatically redirected to the login page.

## Basic Usage

This endpoint requires the following parameters:

- `video_id` (required): The task ID of the source video. **Cannot** be the output of `/veo/extend`.
- `motion_type` (required): The new camera motion style, specified using uppercase underscore-separated aliases.

### `motion_type` Supported Values

| Alias | Description |
|---|---|
| `STATIONARY` | Camera stays fixed |
| `STATIONARY_UP` | Camera fixed, tilts upward |
| `STATIONARY_DOWN` | Camera fixed, tilts downward |
| `STATIONARY_LEFT` | Camera fixed, pans left |
| `STATIONARY_RIGHT` | Camera fixed, pans right |
| `STATIONARY_DOLLY_IN_ZOOM_OUT` | Camera fixed, dolly in + zoom out |
| `STATIONARY_DOLLY_OUT_ZOOM_IN` | Camera fixed, dolly out + zoom in |
| `UP` | Camera moves upward |
| `DOWN` | Camera moves downward |
| `LEFT_TO_RIGHT` | Camera pans from left to right |
| `RIGHT_TO_LEFT` | Camera pans from right to left |
| `FORWARD` | Camera moves forward |
| `BACKWARD` | Camera moves backward |
| `DOLLY_IN_ZOOM_OUT` | Moving dolly in + zoom out |
| `DOLLY_OUT_ZOOM_IN` | Moving dolly out + zoom in |

### Request Example

```shell
curl -X POST 'https://api.acedata.cloud/veo/reshoot' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "video_id": "dd01fc69-e1f7-4b68-aa8c-463f6b748d11",
    "motion_type": "LEFT_TO_RIGHT"
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

## Pricing

- Single reshoot: 1.20 Credit

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

Through this document, you have learned how to use the Veo Reshoot API to regenerate a video with new camera motion while preserving the scene content. If you have any questions, please feel free to contact our technical support team.
