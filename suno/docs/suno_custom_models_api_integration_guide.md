# Suno Custom Models API Integration Guide

The exclusive music model can learn consistent musical features from 6 to 24 authorized audio tracks and be used for subsequent song creation. Creation is an asynchronous operation; it is recommended to use 24 stylistically consistent and high-quality audio tracks for more stable results.

> Only submit audio that you have legal rights to use or have obtained authorization for model creation and subsequent generation. Please do not upload unauthorized music or sound materials.

Call one endpoint with action-based operations:

```text
POST https://api.acedata.cloud/suno/custom-models
```

## Create Model

Send a stable `Idempotency-Key` header and reuse it if the request must be retried.

```bash
curl -X POST 'https://api.acedata.cloud/suno/custom-models' \
  -H 'Authorization: ******' \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: album-sound-v1' \
  -d '{
    "action": "create",
    "name": "My Indie Model",
    "audio_urls": [
      "https://cdn.example.com/song-01.mp3",
      "https://cdn.example.com/song-02.mp3",
      "https://cdn.example.com/song-03.mp3",
      "https://cdn.example.com/song-04.mp3",
      "https://cdn.example.com/song-05.mp3",
      "https://cdn.example.com/song-06.mp3"
    ],
    "callback_url": "https://example.com/webhooks/suno"
  }'
```

The request returns immediately with a platform model `id`, task ID, and `queued` status. After creation completes, model `status` changes to `ready`. Only successful model creation is charged **10 Credits**; failed creation incurs no charges.

## Query Model

```bash
curl -X POST 'https://api.acedata.cloud/suno/custom-models' \
  -H 'Authorization: ******' \
  -H 'Content-Type: application/json' \
  -d '{"action":"retrieve","id":"fa518f27-3fac-45cc-9b95-ae7ae0865b5e"}'
```

A model can be used only when its status is `ready`. Models are scoped to the Suno application that created them; rotating an API credential does not change ownership.

List models with pagination:

```json
{
  "action": "retrieve_batch",
  "limit": 20,
  "offset": 0,
  "status": "ready"
}
```

## Use Model to Generate Songs

```json
{
  "action": "generate",
  "id": "fa518f27-3fac-45cc-9b95-ae7ae0865b5e",
  "title": "Neon Rain",
  "lyric": "[Verse]\nCity lights are falling through the rain",
  "style": "indie rock, warm analog synth"
}
```

The `id` must be the exclusive music model under the current application with a status of `ready`. Requests will fail if the model is unavailable and will not automatically switch to another model. Successful song generation consumes **0.90 Credits**; failed generation does not incur charges. Querying and archiving models are free.

## Archive Model

```json
{
  "action": "delete",
  "id": "fa518f27-3fac-45cc-9b95-ae7ae0865b5e"
}
```

The current Beta version will archive the model and prohibit further use, with `capacity_released=false` in the response indicating that archiving does not guarantee the release of model capacity. The archiving operation can be called repeatedly without incurring additional charges.
