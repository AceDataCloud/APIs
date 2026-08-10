---
title: "Kimi Chat Completion API Application and Usage"
description: "Kimi integration guide - Ace Data Cloud"
---

Kimi is a very powerful AI dialogue system that can generate smooth and natural replies in just a few seconds by inputting prompt words. Kimi provides amazing intelligent assistance, greatly enhancing human work efficiency and creativity.

This document mainly introduces the usage process of the Kimi Chat Completion API, allowing us to easily utilize the official Kimi dialogue features.

The recommended model is `kimi-k3`, which supports reasoning, vision, tool calling, a 1,048,576-token context window, and up to 16,384 output tokens. Kimi K2 models remain available for compatibility.

## Application Process

To use Kimi Chat Completion API, first obtain your API Token from the [Ace Data Cloud Console](https://platform.acedata.cloud/console/applications).

![](https://cdn.acedata.cloud/5hmkdg.jpg)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will automatically return to the current page.

**One API Token can call all services on the platform without applying separately for each service.** The first application grants a free trial quota; recharge the general balance in the [console](https://platform.acedata.cloud/console/coin) when it is insufficient.

> 📘 Complete Documentation: [Kimi Chat Completion API →](https://platform.acedata.cloud/documents/kimi-chat-completions)

## Basic Usage

Next, you can fill in the corresponding content on the interface, as shown in the figure:

<p><img src="https://cdn.acedata.cloud/ej5ozg.png" width="400" class="m-auto"></p>

When using this interface for the first time, fill in `authorization`, `model`, and `messages`. Use `kimi-k3` for the current flagship or a compatible K2 model. Each message contains `role` and `content`; `role` supports `user`, `assistant`, `system`, `developer`, and `tool`. Message content can be a string or an array of text, image, and file parts.

You can also notice that there is corresponding code generation on the right side; you can copy the code to run directly or click the "Try" button for testing.

<p><img src="https://cdn.acedata.cloud/six7e3.png" width="400" class="m-auto"></p>

The following response snapshot was captured from a K2.5 request and is retained to illustrate the response structure. When you use the K3 examples below, the response `model` field will be `kimi-k3` and the generated content will reflect K3:

```json
{
  "id": "chatcmpl-b5d9e1b799c137e3",
  "object": "chat.completion",
  "created": 1770991864,
  "model": "kimi-k2.5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": " Hello! How can I help you today?",
        "refusal": null,
        "tool_calls": []
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 184,
    "total_tokens": 193,
    "prompt_tokens_details": {
      "cached_tokens_details": {}
    },
    "completion_tokens_details": {}
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

## Streaming Response

This interface also supports streaming responses, which is very useful for web integration, allowing the webpage to achieve a word-by-word display effect.

If you want to return responses in a streaming manner, you can change the `stream` parameter in the request header to `true`.

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
    "model": "kimi-k3",
    "messages": [{"role":"user","content":"Hello"}],
    "reasoning_effort": "max",
    "stream": True
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

JavaScript is also supported, for example, the streaming call code for Node.js is as follows:

```javascript
const options = {
  method: "post",
  headers: {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
  },
  body: JSON.stringify({
    "model": "kimi-k3",
    "messages": [{"role":"user","content":"Hello"}],
    "stream": true
  })
};

fetch("https://api.acedata.cloud/kimi/chat/completions", options)
  .then(response => response.json())
  .then(response => console.log(response))
  .catch(err => console.error(err));
```

Java sample code:

```java
JSONObject jsonObject = new JSONObject();
jsonObject.put("model", "kimi-k3");
jsonObject.put("messages", [{"role":"user","content":"Hello"}]);
jsonObject.put("stream", true);
MediaType mediaType = "application/json; charset=utf-8".toMediaType();
RequestBody body = jsonObject.toString().toRequestBody(mediaType);
Request request = new Request.Builder()
  .url("https://api.acedata.cloud/kimi/chat/completions")
  .post(body)
  .addHeader("accept", "application/json")
  .addHeader("authorization", "Bearer {token}")
  .addHeader("content-type", "application/json")
  .build();

OkHttpClient client = new OkHttpClient();
Response response = client.newCall(request).execute();
System.out.print(response.body!!.string())
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
    "model": "kimi-k3",
    "messages": [{"role":"assistant","content":"Hello! How can I help you today?"},{"role":"user","content":"What model are you?"}],
    "reasoning_effort": "max"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

By uploading multiple query words, you can easily achieve multi-turn dialogue. The following retained K2.5 snapshot illustrates the response structure; a K3 request returns `model: kimi-k3` and K3-generated content:

```json
{
  "id": "chatcmpl-81e5f161ea077f5e",
  "object": "chat.completion",
  "created": 1770992310,
  "model": "kimi-k2.5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": " I'm Kimi, an AI assistant made by Moonshot AI. I'm from the **K2.5** series.",
        "refusal": null,
        "tool_calls": []
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 28,
    "completion_tokens": 235,
    "total_tokens": 263,
    "prompt_tokens_details": {
      "cached_tokens_details": {}
    },
    "completion_tokens_details": {}
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
