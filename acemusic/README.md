# ACE Music API

从灵感、歌词或参考音频创作歌曲，可导入参考、翻唱一首已有作品或融合两首参考，试听并下载结果。

本目录由 AceDataCloud/APIs 维护；接口与指南源在 PlatformBackend，文档通过发布流程同步。

- [歌曲生成](audios.md)
- [歌词生成](lyrics.md)
- [任务与历史](tasks.md)
- [OpenAPI](openapi.json)
- [开发者控制台](https://platform.acedata.cloud/console/applications?utm_source=github)
- [Studio](https://studio.acedata.cloud/acemusic?utm_source=github)
- [在线文档](https://docs.acedata.cloud/zh-Hans/guides/acemusic/acemusic_audios?utm_source=github)

基础生成模型：`acemusic-v1.1`（默认）、`acemusic-v1`；翻唱与融合使用 `acemusic-v1.1`。同一 `/acemusic/audios` 接口支持 `generate`、`upload`、`cover` 和 `mashup`。参考使用个人平台音轨 ID，融合要求恰好两首不同且兼容的参考。默认异步，提交后保存平台任务 ID，使用免费任务 API 查询原任务。完整双曲组收一次费用，成功上传一首参考另收上传费；最终失败或部分失败组不收生成费，上传失败不收费。歌词 API 独立收费。

## 开发者与 Agent 入口

[ACE Music 完整生态导航](https://github.com/AceDataCloud/AceMusicMCP)汇集各客户端、工作流宿主和开发工具的安装入口。

| 用途 | 入口 |
| --- | --- |
| 在扣子中接入 | [CozeAPI 导入目录与双语教程](https://github.com/AceDataCloud/CozeAPI) |
| 调用 API | [API 参考与示例](https://docs.acedata.cloud/zh-Hans/guides/acemusic/acemusic_audios.md) · [OpenAPI](openapi.json) |
| 在 Agent 中创作和查询 | [ACE Music MCP](https://github.com/AceDataCloud/AceMusicMCP) · [连接指南](https://platform.acedata.cloud/documents/mcp-acemusic) · [VS Code 扩展](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-acemusic) |
| 给 Agent 安装操作指南 | [ACE Music Skill](https://skills.sh/acedatacloud/skills/ace-music) · [SKILL.md](https://github.com/AceDataCloud/Skills/blob/main/skills/ace-music/SKILL.md) |
| 在脚本或业务代码中使用 | [命令行客户端](https://pypi.org/project/acemusic-cli/) · [Python、TypeScript 和 Go SDK](https://github.com/AceDataCloud/SDK) |
| 在 n8n 中编排 | [社区节点与工作流示例](https://github.com/AceDataCloud/ACEMusicN8N) |

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply. The read-only user flag `has_recharged` records this eligibility; it is not a request parameter.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage. Realtime connection authentication does not occupy this ordinary-request slot and retains its existing per-turn billing.
