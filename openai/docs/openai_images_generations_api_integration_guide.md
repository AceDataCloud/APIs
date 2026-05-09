# OpenAI Images Generations API Application and Usage

The OpenAI Images Generations API currently supports multiple image generation models, including the classic `dall-e-3`, the text-rendering powerhouse `gpt-image-1`, the latest generation **`gpt-image-2`**, as well as the **`nano-banana` / `nano-banana-2` / `nano-banana-pro`** series models. All of them can generate high-quality images from text descriptions.

This document mainly introduces the usage process of the OpenAI Images Generations API, which allows us to easily utilize the image generation capabilities of the OpenAI series.

## Application Process

To use the OpenAI Images Generations API, you can first visit the [OpenAI Images Generations API](https://platform.acedata.cloud/documents/fd932485-90c7-45d6-8394-1e14b6f07b2b) page and click the "Acquire" button to obtain the credentials needed for the request:

![](https://cdn.acedata.cloud/nyq0xz.png)

If you are not logged in or registered, you will be automatically redirected to the login page inviting you to register and log in. After logging in or registering, you will be automatically returned to the current page.

Upon your first application, there will be a free quota provided, allowing you to use the API for free.

## GPT-Image-2 Model

`gpt-image-2` is the latest generation image generation model from OpenAI. Compared to `dall-e-3` and `gpt-image-1`, it has significant improvements in the following areas:

- **Stronger instruction following**: Accurately understands complex compositional, counting, and positional relationship instructions.
- **Clearer text rendering**: English and numbers in posters, menus, infographics, and logos are almost never garbled.
- **Richer style expression**: Natively supports cinematic portraits, retro posters, children's illustrations, product photography, infographics, and more.
- **Native multi-aspect-ratio + high-resolution support**: Covers 5 aspect ratios (1:1, 4:3, 3:4, 16:9, 9:16) across 3 resolution tiers (1K / 2K / 4K).

The calling method is identical to other models — simply set the `model` field to `gpt-image-2`. The `url` in the returned result is a permanently hosted image link on `platform.cdn.acedata.cloud` that can be opened directly in a browser or embedded in a webpage.

### Supported `size` Values and Billing Tiers

`gpt-image-2` only checks the format of `size` — as long as it is not `auto` or an empty string, it must match `WIDTHxHEIGHT` format (e.g., `1024x1024`, `2048x1152`, `800x600`); any other form will return a 400 error. Billing is split into two tiers:

- **1K standard rate**: Any of the 1K recommended sizes in the table below, or the common upstream 1K output aliases (`1254x1254`, `1672x941`, `941x1672` — these are the actual sizes returned by the upstream at the 1K tier; passing them back will not trigger a higher billing tier).
- **Other tier (1.5×)**: Any size not in the above 1K set, including the 2K / 4K presets recommended in the table below, as well as any custom `WIDTHxHEIGHT` you pass in.

Upstream hard constraints for custom sizes: width and height must each be multiples of 16, the long side must be ≤ 3840, and total pixel count must be ≤ 8,294,400. Requests outside this range will be rejected by the upstream with a 4xx response.

| Aspect Ratio | 1K (standard) | 2K (×1.5) | 4K (×1.5) |
| --- | --- | --- | --- |
| 1:1 | `1024x1024` | `2048x2048` | `2880x2880` |
| 4:3 | `1536x1024` | `2048x1536` | `3264x2448` |
| 3:4 | `1024x1536` | `1536x2048` | `2448x3264` |
| 16:9 | `1792x1024` | `2048x1152` | `3840x2160` |
| 9:16 | `1024x1792` | `1152x2048` | `2160x3840` |

> You can also pass `size: "auto"` or **omit the `size` field** entirely, in which case the model will choose a default size and bill at the 1K rate.
>
> At the 1K tier, upstream output is not guaranteed to be pixel-perfect — passing `1024x1024` may yield `1254x1254`, but the aspect ratio remains consistent. If you pass that result back as `size`, it still bills at the 1K rate.
>
> A 4K single call typically takes 4–8 minutes — it is recommended to use the `callback_url` async callback described later in this document.

> **About the `n` parameter**
>
> `gpt-image-2` currently **does not support `n > 1`**: this parameter will be silently ignored. Whether you pass `n=1` or `n=10`, only one image will be returned per request and charged as one image. If you need multiple candidate images at once, please **concurrently send multiple requests** (it is recommended to pass different `prompt` or `seed` values simultaneously; otherwise, the images may be very similar). This restriction also applies to `gpt-image-1` / `gpt-image-1.5` and the `nano-banana` / `nano-banana-2` / `nano-banana-pro` series. `dall-e-2` is currently the only model that natively supports `n > 1`; `dall-e-3` only supports `n = 1`.

Below are several real-world examples to showcase the capabilities of `gpt-image-2`.

### Scenario 1: Cinematic Portrait

You can use cinematic terminology (35mm film, shallow depth of field, neon lighting, etc.) in the prompt to precisely control the atmosphere and texture.

Python sample call code:

```python
import requests

url = "https://api.acedata.cloud/openai/images/generations"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "gpt-image-2",
    "prompt": "A cinematic portrait of a young woman standing in a convenience store at night, illuminated by soft pink and cyan neon signs through the window. Shot on 35mm film, shallow depth of field, slight grain, melancholic mood.",
    "size": "1024x1536"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

The returned result is as follows:

```json
{
  "success": true,
  "task_id": "ab58a5df-6f46-4874-bff6-93169e2849a3",
  "created": 1777048800,
  "data": [
    {
      "revised_prompt": "A cinematic portrait of a young woman standing in a convenience store at night, illuminated by soft pink and cyan neon signs through the window. Shot on 35mm film, shallow depth of field, slight grain, melancholic mood.",
      "url": "https://platform.cdn.acedata.cloud/gpt-image/ab58a5df-6f46-4874-bff6-93169e2849a3_0.png"
    }
  ]
}
```

The generated image is shown below:

<p><img src="https://platform.cdn.acedata.cloud/gpt-image/ab58a5df-6f46-4874-bff6-93169e2849a3_0.png" width="500" class="m-auto"></p>

### Scenario 2: Retro Travel Poster (with Text Rendering)

`gpt-image-2` is stable in typography and font rendering, making it ideal for generating posters, menus, greeting cards, and other text-heavy designs.

```python
payload = {
    "model": "gpt-image-2",
    "prompt": "A vintage travel poster of the Amalfi Coast, Italy. Stylized art-deco illustration of cliffside lemon-yellow houses cascading down to a turquoise sea, with a small white sailboat in the harbor. Bold typography at the top reads AMALFI and at the bottom ITALIA 1958. Limited color palette: cream, sea-blue, lemon yellow, terracotta. Slight paper-grain texture.",
    "size": "1024x1536"
}
```

The image corresponding to the `url` field in the returned result:

<p><img src="https://platform.cdn.acedata.cloud/gpt-image/c6061f92-3fae-498e-af8e-688e7f415ba3_0.png" width="500" class="m-auto"></p>

As you can see, the model accurately reproduces the Art Deco poster visual style, and the title text `AMALFI` and `ITALIA 1958` are clearly and correctly rendered.

### Scenario 3: Complex Composition and Counting

The following prompt tests the model's ability to follow structural instructions regarding "quantity" and "position".

```python
payload = {
    "model": "gpt-image-2",
    "prompt": "A wooden bookshelf consisting of three shelves: On the top shelf, there should be one book. On the second shelf, there should be three books. On the bottom shelf, there should be seven books. Soft warm lighting, photorealistic, cozy library atmosphere.",
    "size": "1024x1024"
}
```

The generated image is shown below:

<p><img src="https://platform.cdn.acedata.cloud/gpt-image/64a3b932-a082-4cad-9f85-9d30474b104d_0.png" width="500" class="m-auto"></p>

As you can see, the number of books on the three shelves (1 / 3 / 7) perfectly matches the prompt — something that was very difficult to do consistently in the `dall-e-3` era.

### Scenario 4: Illustration Style (Landscape)

By specifying art medium and mood keywords, you can guide the model to produce stylized illustrations.

```python
payload = {
    "model": "gpt-image-2",
    "prompt": "A soft, poetic children's book illustration of a small fox reading a book under a glowing mushroom in a moonlit forest. Watercolor and pencil texture, gentle pastel colors, dreamy atmosphere, hand-drawn feel.",
    "size": "1536x1024"
}
```

The generated landscape illustration is shown below:

![](https://platform.cdn.acedata.cloud/gpt-image/6cd57e69-d237-4cc1-a666-759a93964a08_0.png)

### Async and Callback

A single `gpt-image-2` call typically takes 60–90 seconds. If you prefer not to hold a long connection, you can use the `callback_url` async callback mechanism described later in this document. The calling process is identical to other models.

## Nano Banana Series Models

The `nano-banana` series are Gemini-based image generation models accessible through the same `/openai/images/generations` endpoint — no endpoint switching required. Simply set `model` to any value from the table below.

| Model | Billing (Credits / call) | Use Case |
| --- | --- | --- |
| `nano-banana` | 0.14 | Standard image generation, fastest speed and lowest cost |
| `nano-banana-2` | 0.28 | Noticeably improved quality and detail |
| `nano-banana-pro` | 0.35 | Flagship of the series, best composition, detail, and text |

> **Important: Supported Parameters**
>
> Nano Banana connects to the OpenAI protocol via an adapter layer. Compared with `gpt-image-*`, only the following parameters are supported: `model`, `prompt`, `size`.
>
> - `size` is mapped to an internal `aspect_ratio` as follows; unsupported sizes fall back to `1:1`:
>   - `1024x1024` / `512x512` / `256x256` → `1:1`
>   - `1792x1024` → `16:9`
>   - `1024x1792` → `9:16`
> - Parameters such as `n`, `quality`, `style`, `response_format`, `background`, and `output_format` are not supported and will be silently ignored.
> - The response follows the OpenAI format (`data[].url`), but `created` is always `0`, `b64_json` is never returned, and `revised_prompt` is always equal to the original `prompt`.

### Basic Call

```python
import requests

url = "https://api.acedata.cloud/openai/images/generations"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "nano-banana",
    "prompt": "a small red apple on a white table, photoreal",
    "size": "1024x1024"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

The returned result is as follows:

```json
{
  "created": 0,
  "data": [
    {
      "url": "https://platform.cdn.acedata.cloud/nanobanana/6870b330-65c4-436c-bb80-819fdae7a7a4.png",
      "revised_prompt": "a small red apple on a white table, photoreal"
    }
  ]
}
```

The generated image can be accessed directly via the returned `url` field:

<p><img src="https://platform.cdn.acedata.cloud/nanobanana/6870b330-65c4-436c-bb80-819fdae7a7a4.png" width="500" class="m-auto"></p>

### Upgrading to the Flagship Model `nano-banana-pro`

Simply change `model` to `nano-banana-pro`; all other parameters remain the same:

```python
payload = {
    "model": "nano-banana-pro",
    "prompt": "abstract painting",
    "size": "1024x1024"
}
```

Response example:

```json
{
  "created": 0,
  "data": [
    {
      "url": "https://platform.cdn.acedata.cloud/nanobanana/6227fcc9-3442-4aa3-a76c-4a4441a99649.png",
      "revised_prompt": "abstract painting"
    }
  ]
}
```

<p><img src="https://platform.cdn.acedata.cloud/nanobanana/6227fcc9-3442-4aa3-a76c-4a4441a99649.png" width="500" class="m-auto"></p>

### Asynchronous Callback

The `callback_url` async callback mechanism works identically for nano-banana. The calling process is the same as for other models — see the [Asynchronous Callback](#asynchronous-callback) section below for details.

## Basic Usage

Next, you can fill in the corresponding content on the interface, as shown in the figure:

<p><img src="https://cdn.acedata.cloud/zv58ug.png" width="500" class="m-auto"></p>

When using the interface for the first time, you need to fill in at least three pieces of information: one is `authorization`, which can be selected directly from the dropdown list. The other parameter is `model`, which is the category of the OpenAI DALL-E model we choose to use; here we mainly have one model, and details can be found in the models we provide. The last parameter is `prompt`, which is the input for the image generation prompt.

You can also notice that there is corresponding code generation on the right side; you can copy the code to run directly or click the "Try" button for testing.

<p><img src="https://cdn.acedata.cloud/pbss4f.png" width="500" class="m-auto"></p>

Python sample call code:

```python
import requests

url = "https://api.acedata.cloud/openai/images/generations"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

After the call, we find the returned result as follows:

```json
{
  "created": 1721626477,
  "data": [
    {
      "revised_prompt": "A delightful image showcasing a young sea otter, who is born brown, with wide charming eyes. It is delightfully lying on its back, paddling in the calm sea waters. Its dense, velvety fur appears wet and shimmering, capturing the essence of its habitat. The small creature curiously plays with a sea shell with its small paws, looking absolutely innocent and charming in its natural environment.",
      "url": "https://dalleprodsec.blob.core.windows.net/private/images/5d98aa7c-80c6-4523-b571-fc606ad455b9/generated_00.png?se=2024-07-23T05%3A34%3A48Z&sig=GAz%2Bi3%2BkHOQwAMhxcv22tBM%2FaexrxPgT9V0DbNrL4ik%3D&ske=2024-07-23T08%3A41%3A10Z&skoid=e52d5ed7-0657-4f62-bc12-7e5dbb260a96&sks=b&skt=2024-07-16T08%3A41%3A10Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02"
    }
  ]
}
```

The returned result contains multiple fields, described as follows:

- `created`, the ID generated for this image generation, used to uniquely identify this task.
- `data`, which contains the result information of the image generation.

Among them, `data` includes the specific information of the model-generated image, and the `url` inside it is the detailed link to the generated image, as shown in the figure.

<p><img src="https://cdn.acedata.cloud/dz7u0x.png" width="500" class="m-auto"></p>

## Image Quality Parameter `quality`

Next, we will introduce how to set some detailed parameters for the image generation results, among which the image quality parameter `quality` includes two types: the first `standard` indicates generating standard images, and the other `hd` indicates that the created image has finer details and greater consistency.

Below, we set the image quality parameter to `standard`, with specific settings as shown in the figure:

<p><img src="https://cdn.acedata.cloud/1q303w.png" width="500" class="m-auto"></p>

You can also notice that there is corresponding code generation on the right side; you can copy the code to run directly or click the "Try" button for testing.

<p><img src="https://cdn.acedata.cloud/c0ps6i.png" width="500" class="m-auto"></p>

Python sample call code:

```python
import requests

url = "https://api.acedata.cloud/openai/images/generations"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter",
    "quality": "standard"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

After the call, we find the returned result as follows:

```json
{
  "created": 1721636023,
  "data": [
    {
      "revised_prompt": "A cute baby sea otter is lying playfully on its back in the water, with its fur looking glossy and soft. One of its tiny paws is reaching out curiously, and it has an expression of pure joy and warmth on its face as it looks up to the sky. Its body is surrounded by bubbles from its playful twirling in the water. A gentle breeze is playing with its fur making it look more charming. The scene portrays the tranquility and charm of marine life.",
      "url": "https://dalleprodsec.blob.core.windows.net/private/images/a93ee5e7-3abd-4923-8d79-dc9ef126da46/generated_00.png?se=2024-07-23T08%3A13%3A55Z&sig=wTXGYvUOwUIkaB2CxjK9ww%2FHjS8OwYUWcYInXYKwcAM%3D&ske=2024-07-23T11%3A32%3A05Z&skoid=e52d5ed7-0657-4f62-bc12-7e5dbb260a96&sks=b&skt=2024-07-16T11%3A32%3A05Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02"
    }
  ]
}
```

The returned result is consistent with the basic usage content, and you can see the generated image with the image quality parameter set to `standard` as shown in the figure:

<p><img src="https://cdn.acedata.cloud/j5v15b.png" width="500" class="m-auto"></p>

With the same operation as above, simply setting the image quality parameter to `hd` can yield the image shown in the figure below:

<p><img src="https://cdn.acedata.cloud/vjpbqr.png" width="500" class="m-auto"></p>

It can be seen that the images generated with `hd` have finer details and greater consistency compared to those generated with `standard`.

## Image Size Parameter `size`
We can also set the size of the generated images, and we can make the following settings.

The size of the image is set to `1024 * 1024`, and the specific settings are shown in the figure below:

<p><img src="https://cdn.acedata.cloud/dx5rwh.png" width="500" class="m-auto"></p>

At the same time, you can notice that there is corresponding code generation on the right side, which you can copy and run directly, or you can click the "Try" button for testing.

<p><img src="https://cdn.acedata.cloud/0sbybl.png" width="500" class="m-auto"></p>

Python sample call code:

```python
import requests

url = "https://api.acedata.cloud/openai/images/generations"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter",
    "size": "1024x1024"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

After the call, we found that the returned result is as follows:

```json
{
  "created": 1721636652,
  "data": [
    {
      "revised_prompt": "A delightful depiction of a baby sea otter. The small mammal is captured in its natural habitat in the ocean, floating on its back. It has thick brown fur that is sleek and wet from the sea water. Its eyes are closed as if it is enjoying a moment of deep relaxation. The water around it is calm, reflecting the peacefulness of the scene. The background should hint at a diverse marine ecosystem, with visible strands of kelp floating on the surface, suggesting the baby otter's preferred environment.",
      "url": "https://dalleprodsec.blob.core.windows.net/private/images/9d625ac6-fd2b-42a9-84a6-8c99eb357ccf/generated_00.png?se=2024-07-23T08%3A24%3A24Z&sig=AXtYXowEakGxfRp8LhC2DwqL%2F07LhEDW40oCP%2BdTO8s%3D&ske=2024-07-23T18%3A00%3A45Z&skoid=e52d5ed7-0657-4f62-bc12-7e5dbb260a96&sks=b&skt=2024-07-16T18%3A00%3A45Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02"
    }
  ]
}
```

The returned result is consistent with the basic usage content, and we can see that the size of the generated image is `1024 * 1024`, as shown in the figure below:

<p><img src="https://cdn.acedata.cloud/o4pvvx.png" width="500" class="m-auto"></p>

With the same operation as above, simply changing the image size to `1792 * 1024`, we can obtain the image shown below:

![](https://cdn.acedata.cloud/4pilae.png)

It can be seen that the image sizes are obviously different. Additionally, more sizes can be set; for detailed information, please refer to our official documentation.

## Image Style Parameter `style`

The image style parameter `style` includes two parameters. The first one, `vivid`, indicates that the generated image is more vivid, while the second one, `natural`, indicates that the generated image is more natural.

The image style parameter is set to `vivid`, and the specific settings are shown in the figure below:

<p><img src="https://cdn.acedata.cloud/609l9i.png" width="500" class="m-auto"></p>

At the same time, you can notice that there is corresponding code generation on the right side, which you can copy and run directly, or you can click the "Try" button for testing.

<p><img src="https://cdn.acedata.cloud/ee3u9o.png" width="500" class="m-auto"></p>

Python sample call code:

```python
import requests

url = "https://api.acedata.cloud/openai/images/generations"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter",
    "style": "vivid"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

After the call, we found that the returned result is as follows:

```json
{
  "created": 1721637086,
  "data": [
    {
      "revised_prompt": "A baby sea otter with soft, shiny fur and sparkling eyes floating playfully on calm ocean waters. This adorable creature is trippingly frolicking amidst small, gentle waves under a bright, clear, sunny sky. The tranquility of the sea contrasts subtly with the delightful energy of this young otter. The critter gamely clings to a tiny piece of driftwood, its small paws adorably enveloping the floating object.",
      "url": "https://dalleprodsec.blob.core.windows.net/private/images/6e48f701-7fd3-4356-839e-a2f6f0fe82d9/generated_00.png?se=2024-07-23T08%3A31%3A37Z&sig=4percxqTbUR1j3BQmkhvj%2FAhHzInKI%2FqiTo1MP69coI%3D&ske=2024-07-27T10%3A39%3A55Z&skoid=e52d5ed7-0657-4f62-bc12-7e5dbb260a96&sks=b&skt=2024-07-20T10%3A39%3A55Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02"
    }
  ]
}
```

The returned result is consistent with the basic usage content, and we can see that the generated image with the style parameter set to `vivid` is shown in the figure below:

<p><img src="https://cdn.acedata.cloud/e0rpc3.png" width="500" class="m-auto"></p>

With the same operation as above, simply changing the image style parameter to `natural`, we can obtain the image shown below:

<p><img src="https://cdn.acedata.cloud/q9tqwu.png" width="500" class="m-auto"></p>

It can be seen that the image generated with `vivid` is more vivid and realistic than that with `natural`.

## Image Link Format Parameter `response_format`

The last image link format parameter `response_format` also has two types. The first type, `b64_json`, encodes the image link in Base64, while the second type, `url`, is a regular image link that can be viewed directly.

The image link format parameter is set to `url`, and the specific settings are shown in the figure below:

<p><img src="https://cdn.acedata.cloud/2zbgrg.png" width="500" class="m-auto"></p>

At the same time, you can notice that there is corresponding code generation on the right side, which you can copy and run directly, or you can click the "Try" button for testing.

<p><img src="https://cdn.acedata.cloud/a9exmp.png" width="500" class="m-auto"></p>

Python sample call code:

```python
import requests

url = "https://api.acedata.cloud/openai/images/generations"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter",
    "response_format": "url"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

After the call, we found that the returned result is as follows:
```json
{
  "created": 1721637575,
  "data": [
    {
      "revised_prompt": "A charming depiction of a baby sea otter. The otter is seen resting serenely on its back amidst the gentle, blue ocean waves. The baby otter's fur is an endearing mix of soft greyish brown shades, glinting subtly in the muted sunlight. Its small paws are touching, lifted slightly towards the sky as if playing with an unseen object. Its round, expressive eyes are wide in curiosity, sparking with life and innocence. Use a realistic style to evoke the otter's natural habitat and its adorably fluffy exterior.",
      "url": "https://dalleprodsec.blob.core.windows.net/private/images/87792c5f-8b6d-412e-81dd-f1a1baa19bd2/generated_00.png?se=2024-07-23T08%3A39%3A47Z&sig=zzRAn30TqIKHdLVqZPUUuSJdjCYpoJdaGU6BeoA76Jo%3D&ske=2024-07-23T13%3A32%3A13Z&skoid=e52d5ed7-0657-4f62-bc12-7e5dbb260a96&sks=b&skt=2024-07-16T13%3A32%3A13Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02"
    }
  ]
}
```

The returned result is consistent with the basic usage content, and the image link format parameter for the `url` of the generated image is [Image URL](https://dalleprodsec.blob.core.windows.net/private/images/87792c5f-8b6d-412e-81dd-f1a1baa19bd2/generated_00.png?se=2024-07-23T08%3A39%3A47Z&sig=zzRAn30TqIKHdLVqZPUUuSJdjCYpoJdaGU6BeoA76Jo%3D&ske=2024-07-23T13%3A32%3A13Z&skoid=e52d5ed7-0657-4f62-bc12-7e5dbb260a96&sks=b&skt=2024-07-16T13%3A32%3A13Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02) which can be accessed directly, and the image content is shown below:

<p><img src="https://cdn.acedata.cloud/33hs4z.png" width="500" class="m-auto"></p>

By performing the same operation as above, simply changing the image link format parameter to `b64_json`, you can obtain the Base64 encoded image link, with the specific result shown below:

```json
{
  "created": 1721638071,
  "data": [
    {
      "b64_json": "iVBORw0..............v//AQEAAP4AAAD+AAADAQAAAwEEA/4D//8Q/Pbw64mKbVTFoQAAAABJRU5ErkJggg==",
      "revised_prompt": "A charming image of a young baby sea otter. The otter is gently floating on a calm blue sea, basking in the warm, golden rays of sunlight streaming down from a clear sky above. The otter's fur is a rich chocolate brown, and it looks incredibly soft and fluffy. The otter's eyes are bright and expressive, filled with childlike curiosity and joy. It has small, pricked ears and a button-like nose which adds to its overall cuteness. In the sea around it, twinkling droplets of water can be seen, pepped up by the sunlight, the sight is certainly a delightful one."
    }
  ]
}
```

## Asynchronous Callback

Due to the potentially long time taken by the OpenAI Images Generations API to generate images, if the API does not respond for a long time, the HTTP request will keep the connection open, leading to additional system resource consumption. Therefore, this API also provides support for asynchronous callbacks.

The overall process is: when the client initiates a request, an additional `callback_url` field is specified. After the client initiates the API request, the API will immediately return a result containing a `task_id` field, representing the current task ID. When the task is completed, the generated image result will be sent to the client-specified `callback_url` in POST JSON format, which also includes the `task_id` field, allowing the task result to be associated by ID.

Let’s understand how to operate specifically through an example.

First, the Webhook callback is a service that can receive HTTP requests, and developers should replace it with the URL of their own HTTP server. For demonstration purposes, a public Webhook sample site https://webhook.site/ is used, and opening this site will provide a Webhook URL, as shown in the image:

![](https://cdn.acedata.cloud/cjjfly.png)

Copy this URL, and it can be used as a Webhook. The sample here is `https://webhook.site/3d32690d-6780-4187-a65c-870061e8c8ab`.

Next, we can set the `callback_url` field to the above Webhook URL, while filling in the corresponding parameters, as shown in the following code:

```python
import requests

url = "https://api.acedata.cloud/openai/images/generations"

headers = {
    "accept": "application/json",
    "authorization": "Bearer {token}",
    "content-type": "application/json"
}

payload = {
    "model": "dall-e-3",
    "prompt": "A cute baby sea otter",
    "callback_url": "https://webhook.site/3d32690d-6780-4187-a65c-870061e8c8ab"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)
```

Clicking run, you can find that an immediate result is obtained, as follows:

```json
{
  "task_id": "6a97bf49-df50-4129-9e46-119aa9fca73c"
}
```

After a moment, we can observe the generated image result at the Webhook URL, with the content as follows:

```json
{
  "success": true,
  "task_id": "6a97bf49-df50-4129-9e46-119aa9fca73c",
  "trace_id": "9b4b1ff3-90f2-470f-b082-1061ec2948cc",
  "data": {
    "created": 1721626477,
    "data": [
      {
        "revised_prompt": "A delightful image showcasing a young sea otter...",
        "url": "https://dalleprodsec.blob.core.windows.net/private/images/..."
      }
    ]
  }
}
```

You can see that the result contains a `task_id` field, and the `data` field includes the same image generation result as the synchronous call, allowing the task to be associated through the `task_id` field.

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
Through this document, you have learned how to easily use the image generation capabilities of the OpenAI Images Generations API, including `dall-e-3`, `gpt-image-1`, `gpt-image-2`, and the `nano-banana` series. We hope this document helps you better integrate and use the API. If you have any questions, please feel free to contact our technical support team.
