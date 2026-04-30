# OpenAI Images Edits API Application and Usage

OpenAI image editing service allows you to input any number of images and instructions, outputting modified images. The API currently supports `dall-e-2`, `gpt-image-1`, the enhanced **`gpt-image-1.5`**, the latest **`gpt-image-2`**, as well as the **`nano-banana` / `nano-banana-2` / `nano-banana-pro`** series models.

This document mainly describes the usage process of the OpenAI Images Edits API, enabling us to easily utilize the official OpenAI image editing features.

## Application Process

To use the OpenAI Images Edits API, you can first visit the [OpenAI Images Edits API](https://platform.acedata.cloud/documents/251f1efa-aaa6-462e-8af4-66854b1bc94d) page and click the "Acquire" button to obtain the credentials needed for the request:

![](https://cdn.acedata.cloud/nyq0xz.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

Upon the first application, there will be a free quota provided, allowing you to use the API for free.

## GPT-Image-2 Model

`gpt-image-2` shows significant improvements over `gpt-image-1` in image editing scenarios:

- **More stable structure preservation**: When changing colors, backgrounds, or styles, the original layout and composition are almost never disrupted.
- **More accurate text retention**: Text in infographics, posters, menus, and other text-heavy images remains clear and readable after editing.
- **Supports URL input**: In addition to the traditional `multipart/form-data` file upload, `gpt-image-2` also **supports passing image URLs via JSON**, eliminating the need to download images locally first — ideal for server-side pipeline integration.

Below are two real-world examples to showcase the editing capabilities of `gpt-image-2`.

### Method 1: JSON + Image URL (Recommended)

Send a request directly using `application/json`, with the `image` field set to a URL of an image. The model will fetch the image and edit it according to the `prompt`.

For example, this original image is an infographic generated with `gpt-image-2`:

<p><img src="https://platform.cdn.acedata.cloud/gpt-image/5c9fa635-8794-4c6d-88f8-584d7f4716c6_0.png" width="500" class="m-auto"></p>

We want to convert it to a "dark mode" color scheme. Here's how to call it:

```shell
curl -X POST "https://api.acedata.cloud/openai/images/edits" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-2",
    "image": "https://platform.cdn.acedata.cloud/gpt-image/5c9fa635-8794-4c6d-88f8-584d7f4716c6_0.png",
    "prompt": "Convert this infographic to dark mode: dark navy background, light cream text, deep gray rounded module cards with soft shadows. Keep all layout, structure, and module arrangement identical — only invert the color scheme.",
    "size": "1024x1536"
  }'
```

Or using Python:

```python
import requests

url = "https://api.acedata.cloud/openai/images/edits"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "gpt-image-2",
    "image": "https://platform.cdn.acedata.cloud/gpt-image/5c9fa635-8794-4c6d-88f8-584d7f4716c6_0.png",
    "prompt": "Convert this infographic to dark mode: dark navy background, light cream text, deep gray rounded module cards with soft shadows. Keep all layout, structure, and module arrangement identical — only invert the color scheme.",
    "size": "1024x1536"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

The returned result is as follows:

```json
{
  "success": true,
  "task_id": "cb104e35-af1f-45be-9fac-b62e2b256753",
  "trace_id": "3e5c77c6-6c2e-4bba-a42d-98ea049b58a8",
  "created": 1777048863,
  "data": [
    {
      "revised_prompt": "Convert this infographic to dark mode: dark navy background, light cream text, deep gray rounded module cards with soft shadows. Keep all layout, structure, and module arrangement identical — only invert the color scheme.",
      "url": "https://platform.cdn.acedata.cloud/gpt-image/cb104e35-af1f-45be-9fac-b62e2b256753_0.png"
    }
  ],
  "elapsed": 83.859
}
```

The edited image is shown below:

<p><img src="https://platform.cdn.acedata.cloud/gpt-image/cb104e35-af1f-45be-9fac-b62e2b256753_0.png" width="500" class="m-auto"></p>

As you can see, the module structure, information layout, and typography are all strictly preserved — only the color scheme is inverted to a dark theme.

> **Tip**: The `image` field also supports passing an array, e.g., `"image": ["url1", "url2", "url3"]`. You can pass up to 16 reference images simultaneously, allowing the model to reference multiple images during editing.

### Method 2: JSON + Multiple Reference Images

`gpt-image-2` supports referencing multiple images simultaneously to generate the final result, for example combining multiple product photos into a gift basket:

```python
payload = {
    "model": "gpt-image-2",
    "image": [
        "https://example.com/item1.png",
        "https://example.com/item2.png",
        "https://example.com/item3.png"
    ],
    "prompt": "Combine all the items above into a single 'Relax & Unwind' gift basket on a clean white background, photorealistic, soft natural lighting.",
    "size": "1024x1024"
}
```

### Example Scenario: Style Change + Structure Preservation

Here is another example that replaces a wooden bookshelf with a modern floating shelf while strictly preserving the number and arrangement of books on each shelf.

Original image (wooden bookshelf generated with `gpt-image-2`):

<p><img src="https://platform.cdn.acedata.cloud/gpt-image/141970f0-65fb-4ec8-ab7d-9be173641350_0.png" width="500" class="m-auto"></p>

Call:

```python
payload = {
    "model": "gpt-image-2",
    "image": "https://platform.cdn.acedata.cloud/gpt-image/141970f0-65fb-4ec8-ab7d-9be173641350_0.png",
    "prompt": "Replace the wooden bookshelf with a sleek modern white floating shelf mounted on a pastel blue wall. Keep the exact same arrangement of books (1 book on top, 3 in middle, 7 on bottom). Add a small potted succulent on the top shelf next to the book. Bright airy daylight from the left.",
    "size": "1024x1024"
}
```

Edited result (`task_id`: `e9544dba-727e-44a2-81e1-223d49869380`):

<p><img src="https://platform.cdn.acedata.cloud/gpt-image/e9544dba-727e-44a2-81e1-223d49869380_0.png" width="500" class="m-auto"></p>

As you can see, the style and environment are fully replaced according to the prompt, but the number of books on each shelf (1 / 3 / 7) is strictly preserved, and a succulent was added as requested.

### Method 3: multipart/form-data (OpenAI SDK Compatible)

If you are already using the official OpenAI Python SDK, the existing `multipart/form-data` upload method is also supported — just change the `model` to `gpt-image-2`:

```python
import base64
from openai import OpenAI
client = OpenAI()

result = client.images.edit(
    model="gpt-image-2",
    image=[open("test.png", "rb")],
    prompt="Convert this image to dark mode while keeping the layout intact."
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)
with open("edited.png", "wb") as f:
    f.write(image_bytes)
```

When using the SDK, set two environment variables: `OPENAI_BASE_URL` to `https://api.acedata.cloud/openai` and `OPENAI_API_KEY` to the token you obtained:

```shell
export OPENAI_BASE_URL=https://api.acedata.cloud/openai
export OPENAI_API_KEY={token}
```

## Nano Banana Series Models

The `nano-banana` series is also accessible through the same `/openai/images/edits` endpoint. Simply change `model` to any of the values in the table below.

| Model | Billing (Credits / call) | Use Case |
| --- | --- | --- |
| `nano-banana` | 0.14 | Standard image editing, fastest speed and lowest cost |
| `nano-banana-2` | 0.28 | Noticeably improved quality and detail |
| `nano-banana-pro` | 0.35 | Flagship of the series, best structure, text, and style preservation |

> **Important: Supported Parameters**
>
> Nano Banana connects to the OpenAI protocol via an adapter layer. Only the following parameters are supported: `model`, `prompt`, `image`.
>
> - `image` can be supplied either as a file upload via `multipart/form-data` (the worker will convert it internally to `data:<mime>;base64,...`) or as an image URL string passed as a form field.
> - Parameters such as `mask`, `n`, `size`, and `response_format` are not supported and will be silently ignored.
> - The response follows the OpenAI format (`data[].url`), but `created` is always `0`, `b64_json` is never returned, and `revised_prompt` is always equal to the original `prompt`.

### Calling with a Form Field + Image URL

```shell
curl -X POST "https://api.acedata.cloud/openai/images/edits" \
  -H "Authorization: Bearer {token}" \
  -F "model=nano-banana" \
  -F "prompt=add a green leaf on top of the apple" \
  -F "image=https://platform.cdn.acedata.cloud/nanobanana/6870b330-65c4-436c-bb80-819fdae7a7a4.png"
```

The returned result is as follows:

```json
{
  "created": 0,
  "data": [
    {
      "url": "https://platform.cdn.acedata.cloud/nanobanana/311e95b6-5eb1-4c4a-8ee6-0cb03ee44f61.jpeg",
      "revised_prompt": "add a green leaf on top of the apple"
    }
  ]
}
```

The edited image:

<p><img src="https://platform.cdn.acedata.cloud/nanobanana/311e95b6-5eb1-4c4a-8ee6-0cb03ee44f61.jpeg" width="500" class="m-auto"></p>

### Calling with a Form Field + Local File

```python
import requests

url = "https://api.acedata.cloud/openai/images/edits"

headers = {
    "authorization": "Bearer {token}"
}

files = {
    "image": open("apple.png", "rb"),
}
data = {
    "model": "nano-banana-pro",
    "prompt": "add a green leaf on top of the apple"
}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.text)
```

### Asynchronous Callback

The `callback_url` async callback mechanism works identically for nano-banana. The calling process is the same as for other models — see the [Asynchronous Callback](#asynchronous-callback) section below for details.

## Basic Usage

Next, you can use code to make calls; below is an example using CURL:

```curl
curl -s -D >(grep -i x-request-id >&2) \
  -o >(jq -r '.data[0].b64_json' | base64 --decode > gift-basket.png) \
  -X POST "https://api.acedata.cloud/v1/images/edits" \
  -H "Authorization: Bearer {token}" \
  -F "model=gpt-image-1" \
  -F "image[]=@test.png" \
  -F 'prompt=Create a lovely gift basket with these items in it'
```

When using this interface for the first time, we need to fill in at least four pieces of information: one is `authorization`, which can be selected directly from the dropdown list. The other parameter is `model`, which is the category of the OpenAI official model we choose to use; here we mainly have one model, details can be found in the models we provide. Another parameter is `prompt`, which is the input prompt for generating the image. The last parameter is `image`, which requires the path of the image to be edited, as shown in the image below:

<p><img src="https://cdn.acedata.cloud/jw9iwu.png" width="500" class="m-auto"></p>

A Python example with the same calling effect:

```python
import base64
from openai import OpenAI
client = OpenAI()

prompt = """
Generate a photorealistic image of a gift basket on a white background 
labeled 'Relax & Unwind' with a ribbon and handwriting-like font, 
containing all the items in the reference pictures.
"""

result = client.images.edit(
    model="gpt-image-1",
    image=[
        open("test.png", "rb")
    ],
    prompt=prompt
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("gift-basket.png", "wb") as f:
    f.write(image_bytes)
```

When using Python, we need to import two environment variables: one `OPENAI_BASE_URL`, which can be set to `https://api.acedata.cloud/openai`, and another variable for the credential `OPENAI_API_KEY`, which is the value obtained from `authorization`. On Mac OS, you can set the environment variables with the following commands:

```shell
export OPENAI_BASE_URL=https://api.acedata.cloud/openai
export OPENAI_API_KEY={token} 
```

After the call, we find that an image `gift-basket.png` will be generated in the current directory, with the specific result as follows:

<p><img src="https://cdn.acedata.cloud/574s8h.png" width="500" class="m-auto"></p>

Thus, we have completed the image editing operation. Currently, the Edits API supports `dall-e-2`, `gpt-image-1`, `gpt-image-1.5`, `gpt-image-2`, and the `nano-banana` / `nano-banana-2` / `nano-banana-pro` series. Among them, `gpt-image-2` is the recommended model — see the [GPT-Image-2 Model](#gpt-image-2-model) section above for details.

## Asynchronous Callback

Since the OpenAI Images Edits API may take a relatively long time to edit images, if the API does not respond for a long time, the HTTP request will keep the connection open, leading to additional system resource consumption. Therefore, this API also provides support for asynchronous callbacks.

The overall process is: when the client initiates a request, an additional `callback_url` field is specified. After the client initiates the API request, the API will immediately return a result containing a `task_id` field, representing the current task ID. When the task is completed, the result of the edited image will be sent to the client-specified `callback_url` in POST JSON format, which also includes the `task_id` field, allowing the task result to be associated by ID.

Let's understand how to operate specifically through an example.

First, the Webhook callback is a service that can receive HTTP requests, and developers should replace it with the URL of their own HTTP server. For convenience, we use a public Webhook sample site https://webhook.site/; opening this site will give you a Webhook URL, as shown in the image:

![](https://cdn.acedata.cloud/cjjfly.png)

Copy this URL, and it can be used as a Webhook; the sample here is `https://webhook.site/3d32690d-6780-4187-a65c-870061e8c8ab`.

Next, we can set the `callback_url` field to the above Webhook URL and fill in the corresponding parameters, as shown in the following code:

```shell
curl -X POST "https://api.acedata.cloud/v1/images/edits" \
  -H "Authorization: Bearer {token}" \
  -F "model=gpt-image-1" \
  -F "image[]=@test.png" \
  -F "prompt=Create a lovely gift basket with these items in it" \
  -F "callback_url=https://webhook.site/3d32690d-6780-4187-a65c-870061e8c8ab"
```

After the call, you will immediately receive a result, as follows:

```json
{
  "task_id": "6a97bf49-df50-4129-9e46-119aa9fca73c"
}
```

After a moment, we can observe the result of the edited image at the Webhook URL, with the content as follows:

```json
{
  "success": true,
  "task_id": "6a97bf49-df50-4129-9e46-119aa9fca73c",
  "trace_id": "9b4b1ff3-90f2-470f-b082-1061ec2948cc",
  "data": {
    "created": 1721626477,
    "data": [
      {
        "b64_json": "iVBORw0KGgo..."
      }
    ]
  }
}
```

You can see that the result contains a `task_id` field, and the `data` field includes the same image editing result as the synchronous call, allowing the task to be associated through the `task_id` field.

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
Through this document, you have learned how to easily use the official OpenAI image editing features with the OpenAI Images Edits API. We hope this document helps you better integrate and use the API. If you have any questions, please feel free to contact our technical support team.