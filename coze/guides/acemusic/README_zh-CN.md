# 在扣子中使用 ACE Music

将三个 HTTP 工具导入自己的扣子工作空间，即可创作歌曲、写歌词和查询原任务。支持远程 MCP 的客户端也可以使用专门的 MCP 工具。

## 导入插件

1. 下载 [扣子专用 YAML](../../imports/acemusic.yaml) 或 [JSON](../../imports/acemusic.json)，在工作空间创建 API 插件并导入文件。服务地址是 `https://api.acedata.cloud`。
2. 登录[应用列表](https://platform.acedata.cloud/console/applications)，打开**通用应用**，复制 **API KEY** 栏中的密钥。

   ![通用应用中的 API KEY 栏和复制按钮](https://cdn.acedata.cloud/dvc3cg.jpg)

   新建私有变量 `adc_auth`，值为 `Bearer YOUR_API_TOKEN`，把每个工具的 `Authorization` 请求头绑定到变量。确认凭据允许使用相应接口，并核对[价格和余额](https://platform.acedata.cloud/services/acemusic)。共享默认值、对话和导出文件中不要填写真实凭据。
3. 先添加 `getTaskResults`。填 `action=retrieve` 和已有任务的 `id`，即可免费验证查询链路。成功音轨的播放地址在 `response.data[].audio_url`，以后翻唱需要的音轨 ID 在 `response.data[].id`；歌词任务返回 `response.data[].text`。

| 工具 | 用法 |
| --- | --- |
| `generateMusic` | `action=generate` 支持灵感描述，或 `custom=true` 加标题 `title`、歌词 `lyric`、风格 `style`。可选 `acemusic-v1.1` 或 `acemusic-v1`；完整成功时返回两首候选。 |
| `generateLyrics` | 输入主题 `prompt` 和可选风格 `style`，获得标题与可编辑歌词，按独立操作计费。 |
| `getTaskResults` | `retrieve` 查一个 `id`，`retrieve_batch` 批量查 `ids`，`list` 浏览自己的历史。查询免费并需要授权。 |

## 使用参考音频和恢复任务

上传参考时，在 `generateMusic` 选择 `action=upload`，传有权使用的公开 HTTPS MP3 地址 `audio_url`。上传单独计费，成功时返回一首参考音轨。翻唱用 `action=cover` 和一个自有 `audio_id`；融合用 `action=mashup` 和两个不同且兼容的自有 `mashup_audio_ids`。二者均使用 `acemusic-v1.1`，并需提供 `lyric` 和 `style`。表单中其他动作的参数留空。

创作只提交一次，保存返回的 `task_id`，之后用 `getTaskResults` 查询同一 ID。`partial_failed` 时展示已完成且有播放地址的候选并停止轮询。遇到 `submission_unknown`，保留任务和追踪信息，先查历史。[歌曲与参考音频指南](https://platform.acedata.cloud/documents/acemusic-audios-integration?lang=zh-cn&utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## 远程 MCP

使用 [ACE Music MCP 配置](../../mcp-plugins/acemusic.json) 和自己的私有凭据连接 `https://acemusic.mcp.acedata.cloud/mcp`。HTTP 插件对应三个 API；托管 MCP 列出 11 个工具，包括模型查询、参考导入、翻唱和融合。连接后可先列出工具并运行 `acemusic_list_models`。[公开工具清单](https://acemusic.mcp.acedata.cloud/.well-known/mcp/server-card.json)

[English](README.md) · [Coze Studio 导入验证](../../validation/studio_import/README.md)
