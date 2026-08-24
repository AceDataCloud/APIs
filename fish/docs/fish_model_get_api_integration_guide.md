# Fish Model Get API Integration Guide

Use `GET https://api.acedata.cloud/fish/model/{id}` to retrieve the complete details of a cloned voice. The `id` path parameter is the voice `_id`, a 32-character hexadecimal identifier returned when creating a voice or listed by the Fish Model Query API.

```bash
curl 'https://api.acedata.cloud/fish/model/8d2c17a9b26d4d83888ea67a1ee565b2' \
  -H 'Authorization: ******'
```

The response contains the model metadata, including `_id`, `title`, `description`, `state`, `tags`, `samples`, `languages`, `visibility`, and `author`. Use the returned `_id` as `reference_id` in `/fish/tts`.

The endpoint is free. Invalid or unavailable IDs return an appropriate `400` or `404` response; invalid tokens return `401`.
