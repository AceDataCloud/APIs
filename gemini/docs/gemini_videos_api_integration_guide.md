---
title: "Gemini Videos Generation API Integration Instructions"
description: "Gemini AI integration guide - Ace Data Cloud"
---

Generate videos from a text prompt, with optional image and video references.

## Request

Send `POST https://api.acedata.cloud/gemini/videos` with an `Authorization` bearer token and `Content-Type: application/json`.

```bash
curl -X POST 'https://api.acedata.cloud/gemini/videos' \
  -H 'Authorization: ******' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "A cinematic shot of a kitten chasing a butterfly in a sunlit garden",
    "model": "omni-flash",
    "aspect_ratio": "16:9",
    "resolution": "720p"
  }'
```

`prompt` is required. `model` defaults to `omni-flash`; `aspect_ratio` is `16:9` or `9:16`; and `resolution` is `720p` or `1080p`. `image_urls` accepts reference images. `video_urls` accepts at most one reference video and requires at least one `image_urls` item. Set `async: true` or provide `callback_url` to receive a task ID immediately.

## Response

A completed request returns `success`, `task_id`, `trace_id`, and `data`. Each data item has an `id`, `video_url`, `state` (`pending`, `succeeded`, or `failed`), `aspect_ratio`, and `prompt`. Asynchronous requests return a `task_id`; query it through the Gemini Tasks API.

