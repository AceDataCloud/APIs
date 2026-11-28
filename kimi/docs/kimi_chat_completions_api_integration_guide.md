# Kimi Chat Completion API Application and Usage

Kimi is a very powerful AI dialogue system that can generate smooth and natural replies in just a few seconds by inputting prompt words. Kimi provides amazing intelligent assistance, greatly enhancing human work efficiency and creativity.

This document mainly introduces the usage process of the Kimi Chat Completion API, allowing us to easily utilize the official Kimi dialogue features.

`kimi-k3.1-pro` supports reasoning, visual understanding, and tool calling. Its official context window is up to 1,048,576 tokens, but actual request limits depend on the current API. The other supported model IDs are `kimi-k3`, `kimi-k2.6`, and `kimi-k2.7-code`. K3.1 Pro always uses reasoning; do not set `thinking` to disabled.

## Application Process

Sign in to [Applications](https://platform.acedata.cloud/console/applications) and open **General Application**. Initialize it on your first visit if prompted, then copy the key shown in **API KEY**. Set the server-side `ACEDATACLOUD_API_KEY` environment variable to the copied value.

![General Application API KEY field and copy button](https://cdn.acedata.cloud/dvc3cg.jpg)

[Kimi Chat Completion API](https://platform.acedata.cloud/documents/kimi-chat-completions)

During the first application, there will be a free quota provided, allowing you to use the API for free.

## Basic Usage

Next, you can fill in the corresponding content on the interface, as shown in the figure:

<p><img src="https://cdn.acedata.cloud/ej5ozg.png" width="400" class="m-auto"></p>

When using this interface for the first time, we need to fill in at least three pieces of content: one is `authorization`, which can be selected directly from the dropdown list. The other parameter is `model`; use `kimi-k3.1-pro` for the current flagship or select another supported Kimi model. The last parameter is `messages`, which is an array of our input questions. It is an array that allows multiple questions to be uploaded simultaneously, with each question containing `role` and `content`. The `role` indicates the role of the questioner, and we provide three identities: `user`, `assistant`, and `system`. The other `content` is the specific content of our question.

You can also notice that there is corresponding code generation on the right side; you can copy the code to run directly or click the "Try" button for testing.

<p><img src="https://cdn.acedata.cloud/six7e3.png" width="400" class="m-auto"></p>

This example shows the response structure from a K3 request. The `model` field identifies the requested model.

```json
{
  "id": "msg_2D4Btbg1WgvkNE3tCYkR4xGA",
  "object": "chat.completion",
  "created": 1784466588,
  "model": "kimi-k3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 86,
    "completion_tokens": 206,
    "total_tokens": 292
  }
}
```

The returned result contains multiple fields, described as follows:

- `id`, the ID generated for this dialogue task, used to uniquely identify this dialogue task.
- `model`, the selected Kimi official model.
- `choices`, the response information provided by Kimi for the question.
- `usage`: statistics on the tokens used for this Q&A.

Among them, `choices` contains Kimi's response information, and the `choices` inside it shows the specific information of Kimi's response, as can be seen in the figure.

<p><img src="https://cdn.acedata.cloud/tv9rul.png" width="400" class="m-auto"></p>

As can be seen, the `content` field in `choices` contains the specific content of Kimi's reply.

## Reasoning Effort

For `kimi-k3.1-pro`, set the top-level `reasoning_effort` field to `low`, `high`, or `max`. Reasoning is always enabled; do not send a configuration that disables it. For `kimi-k3`, use `max`. The `thinking` field is for K2.6, not K3.1 Pro or K3.

```bash
curl https://api.acedata.cloud/kimi/chat/completions \
  -H "Authorization: Bearer $ACEDATACLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k3.1-pro",
    "messages": [{"role": "user", "content": "Review this code and suggest a fix."}],
    "reasoning_effort": "low"
  }'
```

Read the reply from `choices[].message.content`. If the response includes `reasoning_content` or `tool_calls`, preserve the complete assistant message and send it back unchanged in subsequent turns, including when returning tool results. Input, output, and cache-hit token usage affect billing; consult the model catalog's Pricing card for current prices.

## Streaming Response

This interface also supports streaming responses, which is very useful for web integration, allowing the webpage to achieve a word-by-word display effect.

If you want to return responses in a streaming manner, you can set the `stream` field in the JSON request body to `true`.

Modify as shown in the figure, but the calling code needs to have corresponding changes to support streaming responses.

<p><img src="https://cdn.acedata.cloud/a3nzpw.png" width="400" class="m-auto"></p>

After changing `stream` to `true`, the API will return the corresponding JSON data line by line, and we need to make corresponding modifications at the code level to obtain the line-by-line results.

Python sample calling code:

```python
import requests

url = "https://api.acedata.cloud/kimi/chat/completions"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "kimi-k3.1-pro",
    "messages": [{"role":"user","content":"Hello"}],
    "stream": True
}

response = requests.post(url, json=payload, headers=headers, stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode("utf-8"))
```

The response uses Server-Sent Events. Each event starts with `data:` and ends with a blank line. The final chunk before `data: [DONE]` may contain a `usage` object summarizing token consumption. Always wait for `data: [DONE]` before treating the response as complete.

```text
data: {"id":"chatcmpl-example","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}],"usage":null}

data: {"id":"chatcmpl-example","object":"chat.completion.chunk","choices":[],"usage":{"prompt_tokens":1,"completion_tokens":1,"total_tokens":2}}

data: [DONE]
```

JavaScript is also supported, for example, the streaming call code for Node.js is as follows:

```javascript
const options = {
  method: "POST",
  headers: {
    accept: "application/json",
    authorization: "Bearer {token}",
    "content-type": "application/json"
  },
  body: JSON.stringify({
    model: "kimi-k3.1-pro",
    messages: [{ role: "user", content: "Hello" }],
    stream: true
  })
};

const response = await fetch("https://api.acedata.cloud/kimi/chat/completions", options);
const reader = response.body.getReader();
const decoder = new TextDecoder("utf-8");
while (true) {
  const { value, done } = await reader.read();
  if (done) break;
  process.stdout.write(decoder.decode(value));
}
```

Java sample code:

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import org.json.JSONArray;
import org.json.JSONObject;

public class Main {
  public static void main(String[] args) throws Exception {
    JSONObject payload = new JSONObject()
      .put("model", "kimi-k3.1-pro")
      .put("messages", new JSONArray().put(new JSONObject().put("role", "user").put("content", "Hello")))
      .put("stream", true);
    RequestBody body = RequestBody.create(payload.toString(), MediaType.parse("application/json; charset=utf-8"));
    Request request = new Request.Builder()
      .url("https://api.acedata.cloud/kimi/chat/completions")
      .post(body)
      .addHeader("accept", "application/json")
      .addHeader("authorization", "Bearer {token}")
      .addHeader("content-type", "application/json")
      .build();

    try (Response response = new OkHttpClient().newCall(request).execute()) {
      if (!response.isSuccessful() || response.body() == null) {
        throw new IllegalStateException("HTTP " + response.code());
      }
      try (BufferedReader reader = new BufferedReader(new InputStreamReader(response.body().byteStream(), StandardCharsets.UTF_8))) {
        for (String line; (line = reader.readLine()) != null; ) {
          if (!line.isEmpty()) {
            System.out.println(line);
          }
        }
      }
    }
  }
}
```

Other languages can be rewritten accordingly; the principle is the same.

## Multi-turn Dialogue

If you want to integrate multi-turn dialogue functionality, you need to upload multiple query words in the `messages` field. The specific examples of multiple query words are shown in the image below:

<p><img src="https://cdn.acedata.cloud/g85v2a.png" width="400" class="m-auto"></p>

Python sample call code:

```python
import requests

url = "https://api.acedata.cloud/kimi/chat/completions"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "kimi-k3.1-pro",
    "messages": [{"role":"assistant","content":"Hello! How can I help you today?"},{"role":"user","content":"What model are you?"}]
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

Send conversation history in `messages` to continue a dialogue. This K3 response shows the structure of the final result.

```json
{
  "id": "msg_Rqp8nPGBDHWwBlL4VpxuafOp",
  "object": "chat.completion",
  "created": 1784466628,
  "model": "kimi-k3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I’m Kimi, an AI assistant developed by Moonshot AI (月之暗面). I don’t have a specific public model version identifier to share from here."
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 134,
    "completion_tokens": 346,
    "total_tokens": 480
  }
}
```

As you can see, the information contained in `choices` is consistent with the basic usage content, which includes the specific content of Kimi's responses to multiple dialogues, allowing you to answer corresponding questions based on multiple dialogue contents.

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

Through this document, you have learned how to easily implement the official Kimi dialogue function using the Kimi Chat Completion API. We hope this document helps you better integrate and use the API. If you have any questions, please feel free to contact our technical support team.
