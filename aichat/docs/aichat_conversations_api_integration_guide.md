# AI Chat Conversations API Integration Guide

Many Q&A APIs on the market are relatively difficult to integrate. For example, the OpenAI Chat Completions API requires a `messages` field — to support continuous multi-turn dialogue you must pass the entire conversation history every time, and you need to handle token limit overflows yourself.

The AceDataCloud AI Chat API addresses these pain points. It preserves full answer quality while wrapping multi-turn dialogue management internally — you no longer need to pass message history, and you never need to worry about token limits (handled automatically). The API also provides conversation querying and modification features, making integration significantly simpler.

## Application Process

To use the API, first visit the [AI Chat API](https://platform.acedata.cloud/documents/59fb1199-6694-4afb-a222-3554d7f7d05a) page and click the **Acquire** button:

![](https://cdn.acedata.cloud/q6ytrc.png)

If you are not yet logged in or registered, you will be redirected to the login page. After logging in or registering you will be returned to this page automatically.

First-time applicants receive a free quota so you can start using the API at no cost.

## Basic Usage

The simplest use case is sending a question and receiving an answer. Just pass a `question` field and the desired `model`.

For example, to ask "What's your name?", fill in the interface as shown:

![](https://cdn.acedata.cloud/xqxda4.png)

**Request Headers:**

- `accept`: Response format — set to `application/json` for JSON.
- `authorization`: Your API token, selected from the dropdown after applying.

**Request Body:**

- `model`: The model to use (e.g., `gpt-4o`, `gpt-5`, etc.).
- `question`: The question to ask — any plain text.

The right-hand panel shows generated code you can copy and run:

<p><img src="https://cdn.acedata.cloud/dvkps6.png" width="500" class="m-auto"></p>

Click **Try** to test. The response looks like:

```json
{
  "answer": "I am an AI language model developed by OpenAI and I don't have a personal name. However, you can call me GPT or simply Chatbot. How can I assist you today?"
}
```

The `answer` field contains the model's reply. You can ask any question and receive a corresponding answer.

If you do not need multi-turn conversation support, this API makes integration extremely straightforward.

**cURL example:**

```shell
curl -X POST 'https://api.acedata.cloud/aichat/conversations' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "model": "gpt-4o",
    "question": "What'\''s your name?"
  }'
```

**Python example:**

```python
import requests

url = "https://api.acedata.cloud/aichat/conversations"

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

## Multi-turn Conversation

To use multi-turn (stateful) dialogue, pass the additional parameter `stateful: true` in every request. When `stateful` is set, the API returns an `id` field representing the conversation ID. Pass that `id` in subsequent requests to continue the same conversation.

**First request** — set `stateful: true` along with `model` and `question`:

![](https://cdn.acedata.cloud/fn4bi9.png)

```shell
curl -X POST 'https://api.acedata.cloud/aichat/conversations' \
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

**Second request** — pass the `id` from the first response and keep `stateful: true`:

![](https://cdn.acedata.cloud/46a6kd.png)

```shell
curl -X POST 'https://api.acedata.cloud/aichat/conversations' \
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
  "answer": "You asked me what my name is. As an AI language model, I do not possess a personal identity, so I don't have a specific name. However, you can refer to me as OpenAI or ChatGPT, the names used for this AI model. Is there anything else I can help you with?",
  "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"
}
```

The model correctly references the previous question, demonstrating full context-aware conversation.

## Streaming Responses

The API supports streaming responses, which is especially useful for web applications that display text token-by-token.

To enable streaming, change the `accept` header to `application/x-ndjson`:

![](https://cdn.acedata.cloud/axt1aa.png)

With streaming enabled, the API returns one JSON object per line as tokens are generated.

**Python streaming example:**

```python
import requests

url = "https://api.acedata.cloud/aichat/conversations"

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

Sample output:

```json
{"answer": "Hello", "delta_answer": "Hello", "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"}
{"answer": "Hello!", "delta_answer": "!", "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"}
{"answer": "Hello! How", "delta_answer": " How", "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"}
{"answer": "Hello! How can", "delta_answer": " can", "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"}
{"answer": "Hello! How can I", "delta_answer": " I", "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"}
{"answer": "Hello! How can I assist", "delta_answer": " assist", "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"}
{"answer": "Hello! How can I assist you", "delta_answer": " you", "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"}
{"answer": "Hello! How can I assist you today", "delta_answer": " today", "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"}
{"answer": "Hello! How can I assist you today?", "delta_answer": "?", "id": "7cdb293b-2267-4979-a1ec-48d9ad149916"}
```

Each line contains `answer` (the full answer so far) and `delta_answer` (the newly appended token). Use these fields to update your UI incrementally.

**Node.js streaming example:**

```javascript
const axios = require("axios");

const url = "https://api.acedata.cloud/aichat/conversations";
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

**Java streaming example:**

```java
String url = "https://api.acedata.cloud/aichat/conversations";
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

The same pattern applies to any other language — open a streaming HTTP connection and read the response line by line.

## Model Presets

OpenAI-style APIs support a `system_prompt` to set a persona or context for the model. This API exposes the same capability via the `preset` parameter.

For example, to make the model act as a professional artist, pass `preset: "You are a professional artist"`:

![](https://cdn.acedata.cloud/ird6i9.png)

```shell
curl -X POST 'https://api.acedata.cloud/aichat/conversations' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "model": "gpt-4o",
    "stateful": true,
    "question": "What can you help me with?",
    "preset": "You are a professional artist"
  }'
```

Response:

```json
{
  "answer": "As a professional artist, I can offer a range of services and assistance depending on your specific needs. Here are a few ways I can help you:\n\n1. Custom Artwork: If you have a specific vision or idea, I can create custom artwork for you. This can include paintings, drawings, digital art, or any other medium you prefer.\n\n2. Commissioned Pieces: If you have a specific subject or concept in mind, I can create commissioned art pieces tailored to your preferences.\n\n3. Art Consultation: If you need guidance on art selection, interior design, or how to showcase and display art in your space, I can provide professional advice to help enhance your aesthetic sense and create a cohesive look."
}
```

## Image Recognition

The API supports image understanding by passing one or more image URLs via the `references` field. Use a vision-capable model such as `gpt-4-vision-preview` or `gpt-4o`.

For example, given an apple image at `https://cdn.acedata.cloud/ht05g0.png`:

![](https://cdn.acedata.cloud/ht05g0.png)

![](https://cdn.acedata.cloud/cstrbq.png)

```shell
curl -X POST 'https://api.acedata.cloud/aichat/conversations' \
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

## Web Browsing

The API includes models that can search the internet in real time and summarise the results. Select a browsing-enabled model such as `gpt-4o-search-preview` to use this feature:

![](https://cdn.acedata.cloud/x5i8np.png)

```shell
curl -X POST 'https://api.acedata.cloud/aichat/conversations' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer {token}' \
  -H 'content-type: application/json' \
  -d '{
    "model": "gpt-4o-search-preview",
    "question": "What'\''s the weather in New York today?"
  }'
```

Response:

```json
{
  "answer": "The weather in New York today is as follows:\n- Current Temperature: 16°C (60°F)\n- High: 16°C (60°F)\n- Low: 10°C (50°F)\n- Humidity: 47%\n- UV Index: 6 of 11\n- Sunrise: 5:42 am\n- Sunset: 8:02 pm\n\nIt's overcast with a chance of occasional showers overnight, and the chance of rain is 50%.\nFor more details, you can visit [The Weather Channel](https://weather.com).\n\nIs there anything else you'd like to know?"
}
```

The model automatically fetches live data from the web and returns a summarised, up-to-date answer.

## Request Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `model` | string | ✅ | The model to use for generating the answer. |
| `question` | string | ✅ | The prompt or question to answer. |
| `id` | string | ❌ | Conversation ID for continuing a stateful conversation. |
| `stateful` | boolean | ❌ | Set to `true` to enable stateful multi-turn conversation. |
| `preset` | string | ❌ | System prompt / persona preset for the model. |
| `references` | string[] | ❌ | Array of image URLs for vision-capable models. |

## Response Fields

| Field | Type | Description |
|---|---|---|
| `answer` | string | The model's generated answer. |
| `id` | string | Conversation ID (returned when `stateful: true`). |
| `delta_answer` | string | Incremental token added in this chunk (streaming only). |
