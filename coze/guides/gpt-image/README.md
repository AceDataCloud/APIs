# GPT Image by Ace Data Cloud for Coze

Use GPT Image through an independent Coze plugin maintained by **Ace Data Cloud**. This integration calls Ace Data Cloud APIs; it does not claim to be the model brand's official plugin or a Coze default model provider.

[简体中文](README_zh-CN.md) · [Current pricing](https://platform.acedata.cloud/models?utm_source=coze&utm_medium=referral&utm_campaign=evergreen&utm_content=coze_gpt-image_pricing)

## 1. Find and install the correct plugin

Open [GPT Image in Coze Plugin Store](https://www.coze.com/store/plugin/7695652131059187765). Confirm the publisher is **AceDataCloud**. The latest recorded submission was under review on **2026-10-12**; approval and search/install availability have not been authenticated again. If Install/Add is absent or the version is under review, stop at that gate; do not treat this source guide as a released store package.

Search terms: **gpt image, GPT Image by Ace Data Cloud**. These are relevant service names, not a guarantee of ranking. The prepared display title is **GPT Image by Ace Data Cloud**; existing approved titles may differ until a reviewed update is published.

After the listing is approved and available, add its tools to your Agent or Workflow. In the international editor, open the Agent's plugins/tools area, select this listing and add **generateImage** and **getTaskResults**. Retain the existing plugin ID when updating; do not create a duplicate listing.

Coze China low-code uses **Skills → Plugins → +** for an Agent and **Add node → Plugin** for a Workflow. It is a separate store and the newer extension center uses a different package format. The official reference below illustrates the low-code controls; it shows another plugin, not Ace installed or the international editor.

![Official Coze China Agent plugin area](../../_assets/tutorial/coze-official-agent-tools.webp)

![Official Coze China Workflow plugin node picker](../../_assets/tutorial/coze-official-workflow-tools.webp)

Source: [Coze official guide](https://docs.coze.cn/guides_use_plugin), retrieved **2026-10-18**, unmodified. Actual international install/credential screenshots remain queued for authenticated verification.

## 2. Register and get your API Token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=coze&utm_medium=referral&utm_campaign=evergreen&utm_content=coze_gpt-image_api_key); register or sign in.
2. Find **General application**. If absent, choose **Initialize General Application**. A general key can use the services your account is entitled to use; a service-specific application's key is limited to its service. Check **GPT Image**, current model price and balance.
3. Copy the existing API Key, or open **Manage Keys → Create** to create a separately named key such as `Coze GPT Image`. Review expiration, usage limit and Allowed APIs. For this first flow, allow `/openai/images/generations` and `/openai/tasks`; also allow the editing operation only if you intend to use it.

![Copy a redacted API Key or open Manage Keys](../../_assets/tutorial/get-api-key-en.png)

![Create an optional separate credential](../../_assets/tutorial/create-api-key-en.png)

These are existing Ace account screenshots reused from the [SunoDify guide](https://github.com/AceDataCloud/SunoDify/blob/8d3d03570e73324220f111f7fe343da0792a8071/README.md). They were reviewed on **2026-10-18** and contain redacted values. `Dify tutorial` is the example name in the original image; use `Coze GPT Image` instead. No new key was created for this guide.

Copy only the token string. A `platform-...` account-management token cannot replace an API Token for the service. Any trial allowance is what your account currently displays; the plugin listing does not make generation free.

## 3. Bind the credential privately in Coze

In each tool's **Authorization** parameter, select **Reference → adc_auth**, a private String variable containing `Bearer <your API Token>`. Keep shared/default values empty and exclude the variable from prompts. In preview/debug, set the current session's private value, then read back the saved Reference binding. A fixed Input default can be replaced by a model placeholder; never send the token in chat, examples, screenshots or exported workflows.

Only the Authorization header gets the literal `Bearer ` prefix; a token-only field expects the raw token. Each user uses their own key and balance. First authentication, cancellation, expiration and reconnect still require ordinary-user verification after review.

## 4. First use and the same task's result

For an authorized first generation, select **generateImage** and use the exact documented model rather than asking the Agent to substitute one. Check current pricing and intended spend before running. This example is a request template, **not a new executed test**:

```json
{
  "model": "gpt-image-2",
  "prompt": "A blue ceramic teapot on a neutral studio background.",
  "n": 1,
  "async": true
}
```

The image task tool queries an existing task. It must not be replaced with another generation while the first task is pending.

Retain the returned **task_id**. In **getTaskResults** on `/openai/tasks`, select **Reference** to the generation tool's task ID (or use an already-owned completed task):

```json
{
  "id": "YOUR_EXISTING_TASK_ID",
  "action": "retrieve"
}
```

If pending or the response is empty, query the **same ID** again. Never rerun the generation to poll. A task ID, HTTP 200 or an intermediate preview is not completion. Inspect terminal success and the real media field **response.data[].url**; stop on an explicit terminal error. Open only the URL returned by the actual task. Placeholders in this guide are not result evidence.

## Troubleshooting

| Symptom | Check |
|---|---|
| Listing missing / Under Review | Confirm region, publisher, approved version and workspace permissions; wait for review rather than creating a duplicate. |
| 401 / 403 | Full token, application/service permissions, expiry, usage limits, balance, and private Reference binding. |
| 400 | Copy the exact model/action and expected input shape; optional fields vary by model. |
| Pending / empty media | Keep the original task ID and query again; do not generate another task. |
| 429 | Respect rate limits and reduce concurrency; no automatic paid retry. |
| 5xx / failed | Preserve the task/trace ID and inspect the original request; never expose the key. |

[API access and current pricing](https://platform.acedata.cloud/models?utm_source=coze&utm_medium=referral&utm_campaign=evergreen&utm_content=coze_gpt-image_pricing) · [Account and keys](https://platform.acedata.cloud/console/applications?utm_source=coze&utm_medium=referral&utm_campaign=evergreen&utm_content=coze_gpt-image_api_key) · [Source](../../plugins/gpt-image.yaml)

## Publisher checklist

Use the existing store item where one exists; read back search, approved version, installed tools, private authorization and tagged setup link separately. Prepared files: [Coze import](../../imports/gpt-image.json) and [full API contract](../../plugins/gpt-image.json). Import compatibility and real runtime evidence are separate gates. Do not publish a personal token as a shared default. Full tool parity, store approval, default-provider inclusion and real growth are not inferred from source tests.
