# Veo Objects API Integration Guide

This guide describes how to integrate the Veo Objects API. This endpoint is used to **insert or remove objects** in an already-generated Veo video (mask-based local inpainting).

## Application Process

To use the API, you first need to apply for the corresponding service on the Veo service page. If you are not logged in or registered, you will be automatically redirected to the login page.

## Basic Usage

This endpoint requires the following parameters:

- `video_id` (required): The task ID of the source video. **Cannot** be the output of `/veo/extend`.
- `action` (required): The operation type — `insert` or `remove`.
- `prompt`:
  - When `action=insert`: **Required**. Describes the object to be added.
  - When `action=remove`: Optional. Describes the content to be removed (primarily for logging; the actual area to erase is determined by `image_mask`).
- `image_mask`:
  - When `action=insert`: Optional. If not provided, the AI automatically decides where to place the inserted object. If provided, the object is inserted in the white-pixel region of the mask.
  - When `action=remove`: **Required**. The white-pixel region indicates the object to be erased.

`image_mask` accepts two formats:
1. A **publicly accessible HTTP(S) image URL** (recommended).
2. A **base64-encoded JPEG string**, with or without the `data:image/jpeg;base64,` prefix.

### Request Example — Insert an Object (without mask, AI auto-placement)

```shell
curl -X POST 'https://api.acedata.cloud/veo/objects' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "video_id": "dd01fc69-e1f7-4b68-aa8c-463f6b748d11",
    "action": "insert",
    "prompt": "add a flying pig with black wings"
  }'
```

### Request Example — Remove an Object Using a Mask

```shell
curl -X POST 'https://api.acedata.cloud/veo/objects' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "video_id": "dd01fc69-e1f7-4b68-aa8c-463f6b748d11",
    "action": "remove",
    "image_mask": "https://example.com/mask.jpg",
    "prompt": "remove the white cloud"
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

- `action=insert` or `action=remove`: 1.50 Credit / request

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

Through this document, you have learned how to use the Veo Objects API to insert or remove objects in a generated video. If you have any questions, please feel free to contact our technical support team.
