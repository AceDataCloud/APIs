# AI Chat Conversations API Integration Guide

The AI Chat Conversations API provided by Ace Data Cloud simplifies integration compared to raw chat completion APIs (such as OpenAI's Chat Completions API). You do not need to manage the `messages` array or handle token-limit issues yourself — the API handles context internally. It also supports multi-turn stateful conversations, conversation querying, and modification, making integration straightforward.

## Application Process

To use the API, visit the [AI Chat API](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a) page and click the "Acquire" button.

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not yet logged in or registered, you will be redirected to the login page. After logging in, you will be returned to this page automatically.

First-time applicants receive a free usage quota.

## Basic Usage

The recommended endpoint is `https://api.acedata.cloud/aichat2/conversations` (the legacy compatibility endpoint is `https://api.acedata.cloud/aichat/conversations`).

The simplest usage is to send a question and receive an answer by providing `model` and `question`.

For example, asking "What's your name?":

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "question": "What'\''s your name?"
}'
```

Python equivalent:

```python
import requests

url = "https://api.acedata.cloud/aichat2/conversations"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "gpt-4o",
    "question": "What's your name?"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

The response looks like:

```json
{
  "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44",
  "answer": "I am an AI language model developed by OpenAI and I don't have a personal name. However, you can call me GPT or simply Chatbot. How can I assist you today?"
}
```

The `answer` field contains the model's reply, and `id` is the conversation ID.

### Request Headers

| Header | Description |
| --- | --- |
| `accept` | Response format: `application/json` (default), `application/x-ndjson`, or `text/event-stream` |
| `authorization` | Bearer token obtained from your Ace Data Cloud account |

### Request Body

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `model` | string | ✅ | The model to use (see supported models below) |
| `question` | string | ❌ | Prompt text for chat mode |
| `action` | string | ❌ | Action type: `chat`, `retrieve`, `retrieve_batch`, `update`, `delete` |
| `message` | string / array | ❌ | Multimodal input (text/image/file blocks) |
| `id` | string | ❌ | Conversation ID (required for retrieval/update/delete and multi-turn continuation) |
| `stateful` | boolean | ❌ | Enable stateful (multi-turn) conversation mode; default is `true` |
| `preset` | string | ❌ | System-level preset (equivalent to `system_prompt`) |
| `references` | array of strings | ❌ | Image URLs for vision/image-recognition requests |
| `max_turns` | integer | ❌ | Maximum retained turns in stateful conversations |
| `async` | boolean | ❌ | Enable asynchronous processing |
| `callback_url` | string | ❌ | Callback URL for async results |

### Supported Models

The following models are currently supported as values for the `model` field:

`gpt-4`, `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `gpt-4o`, `gpt-4o-2024-05-13`, `gpt-4o-all`, `gpt-4o-image`, `gpt-4o-mini`, `gpt-5-all`, `gpt-5.1-all`, `gpt-5.2-pro`, `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-image-1`, `claude-3-5-haiku-20241022`, `claude-3-5-sonnet-20240620`, `claude-3-5-sonnet-20241022`, `claude-3-7-sonnet-20250219`, `claude-3-haiku-20240307`, `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-haiku-4-5-20251001`, `claude-opus-4-1-20250805`, `claude-opus-4-20250514`, `claude-opus-4-5-20251101`, `claude-opus-4-6`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-4-20250514`, `claude-sonnet-4-5-20250929`, `claude-sonnet-4-6`, `gemini-2.0-flash-lite`, `gemini-2.5-flash-lite`, `gemini-3-pro-preview`, `gemini-3.1-flash-image-preview`, `gemini-3.1-flash-lite-preview`, `gemini-3.1-pro`, `gemini-3.1-pro-preview`, `grok-3`, `grok-3-fast`, `grok-4`, `grok-4-0709`, `deepseek-chat`, `deepseek-r1`, `deepseek-r1-0528`, `deepseek-reasoner`, `deepseek-v3`, `deepseek-v3-250324`, `deepseek-v3.2-exp`, `deepseek-v4-flash`, `kimi-k2-0711-preview`, `kimi-k2-0905-preview`, `kimi-k2-instruct-0905`, `kimi-k2-thinking`, `kimi-k2-thinking-turbo`, `kimi-k2-turbo-preview`, `kimi-k2.5`, `glm-3-turbo`, `glm-4.5`, `glm-4.5v`, `glm-4.6`, `glm-4.7`, `glm-5`, `glm-5-turbo`, `glm-5.2`, `glm-5.1`, `o1`, `o1-mini`, `o1-pro`, `o3`, `o3-mini`, `o3-pro`, `o4-mini`

## Multi-Turn Conversations

To enable multi-turn (stateful) conversations, pass the `stateful: true` parameter. The API will return an `id` field representing the conversation ID. Pass that `id` in all subsequent requests to continue the conversation.

**First request:**

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "question": "What'\''s your name?",
  "stateful": true
}'
```

Response:

```json
{
  "answer": "I am an AI language model created by OpenAI and I don't have a personal name. You can simply call me OpenAI or ChatGPT. How can I assist you today?",
  "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"
}
```

**Second request** (pass the `id` from the previous response):

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "stateful": true,
  "id": "7cdb293b-2267-4979-a1ec-48d9ad149916",
  "question": "What did I ask you just now?"
}'
```

Response:

```json
{
  "answer": "You asked me what my name is. As an AI language model, I do not possess a personal identity, so I don't have a specific name. However, you can refer to me as OpenAI or ChatGPT. Is there anything else I can help you with?",
  "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"
}
```

The API automatically maintains context across turns.

## Streaming Responses

The API supports streaming responses, which is useful for web applications that want a word-by-word display effect. To enable streaming, set the `accept` header to `application/x-ndjson`.

**Python example:**

```python
import requests

url = "https://api.acedata.cloud/aichat2/conversations"

headers = {
    "accept": "application/x-ndjson",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "gpt-4o",
    "stateful": True,
    "id": "7cdb293b-2267-4979-a1ec-48d9ad149916",
    "question": "Hello"
}

response = requests.post(url, json=payload, headers=headers, stream=True)
for line in response.iter_lines():
    print(line.decode())
```

Each streamed line is a JSON object (NDJSON chunk), for example:

```json
{"type": "text_delta", "content": " today", "delta_answer": " today", "answer": "Hello! How can I assist you today", "id": "f2f4b3e8-0c0a-4d3a-aaa2-7ff80c0a1c44"}
```

- `type`: Stream chunk type (for example `text_delta`).
- `content`: Token content for this chunk.
- `answer`: The full answer accumulated so far.
- `delta_answer`: The newly added token(s) in this chunk.

**Node.js example:**

```javascript
const axios = require("axios");

const url = "https://api.acedata.cloud/aichat2/conversations";
const headers = {
  "Content-Type": "application/json",
  Accept: "application/x-ndjson",
  Authorization: "Bearer {token}",
};
const body = {
  question: "Hello",
  model: "gpt-4o",
  stateful: true,
};

axios
  .post(url, body, { headers: headers, responseType: "stream" })
  .then((response) => {
    console.log(response.status);
    response.data.on("data", (chunk) => {
      console.log(chunk.toString());
    });
  })
  .catch((error) => {
    console.error(error);
  });
```

**Java example:**

```java
String url = "https://api.acedata.cloud/aichat2/conversations";
OkHttpClient client = new OkHttpClient();
MediaType mediaType = MediaType.parse("application/json");
RequestBody body = RequestBody.create(mediaType, "{\"question\": \"Hello\", \"stateful\": true, \"model\": \"gpt-4o\"}");
Request request = new Request.Builder()
        .url(url)
        .post(body)
        .addHeader("Content-Type", "application/json")
        .addHeader("Accept", "application/x-ndjson")
        .addHeader("Authorization", "Bearer {token}")
        .build();

client.newCall(request).enqueue(new Callback() {
    @Override
    public void onFailure(Call call, IOException e) {
        e.printStackTrace();
    }

    @Override
    public void onResponse(Call call, Response response) throws IOException {
        if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(response.body().byteStream(), "UTF-8"))) {
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                System.out.println(responseLine);
            }
        }
    }
});
```

## Model Preset

The `preset` field sets a system-level prompt for the model (equivalent to `system_prompt` in OpenAI's API). For example, to make the model act as a professional artist:

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "stateful": true,
  "question": "What can you help me?",
  "preset": "You are a professional artist"
}'
```

Response:

```json
{
  "answer": "As a professional artist, I can offer a range of services and assistance depending on your specific needs. Here are a few ways I can help you:\n\n1. Custom Artwork: If you have a specific vision or idea, I can create custom artwork for you.\n2. Commissioned Pieces: I can create commissioned art pieces tailored to your preferences.\n3. Art Consultation: I can provide professional advice on art selection and display."
}
```

## Image Recognition

Vision-capable models can analyze images passed via the `references` field. Provide image URLs in the array, and select a vision-capable model such as `gpt-4-vision-preview` or `gpt-4o`.

```shell
curl -X POST 'https://api.acedata.cloud/aichat2/conversations' \
-H 'accept: application/json' \
-H 'authorization: Bearer {token}' \
-H 'content-type: application/json' \
-d '{
  "model": "gpt-4o",
  "question": "How many apples are in the picture?",
  "references": ["https://cdn.acedata.cloud/ht05g0.png"]
}'
```

Response:

```json
{
  "answer": "There are 5 apples in the picture."
}
```

## Response Schema

### Success (200)

| Field | Type | Description |
| --- | --- | --- |
| `answer` | string | The model's reply to the question |
| `id` | string | Conversation ID |
| `type` | string | Stream chunk type (`application/x-ndjson` / `text/event-stream`) |
| `content` | string | Stream chunk content (`application/x-ndjson` / `text/event-stream`) |
| `delta_answer` | string | Newly added text in the current stream chunk |

### Error (400 / 401 / 404 / 429 / 500)

| Field | Type | Description |
| --- | --- | --- |
| `error.code` | string | Error code (e.g. `bad_request`, `token_mismatched`, `invalid_token`, `not_found`, `too_many_requests`, `chat_error`) |
| `error.message` | string | Human-readable error description |
| `trace_id` | string | Trace ID for debugging |
