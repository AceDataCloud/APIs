# Fish Model Get API Integration Guide

`GET https://api.acedata.cloud/fish/model/{id}`

Retrieve one voice model. `id` is required and is the model's `_id`.

```bash
curl 'https://api.acedata.cloud/fish/model/d7900c21663f485ab63ebdb7e5905036' \
  --header 'Authorization: ******'
```

The model entity includes `_id`, title and metadata, `samples`, ISO 8601 `created_at` and `updated_at`, `languages`, `visibility`, engagement fields, and `author`. Use `_id` as `reference_id` in `POST /fish/tts`.
