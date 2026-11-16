# ACE Music API

从一句灵感或自定义歌词创作歌曲，试听并下载两首候选。

本目录由 AceDataCloud/APIs 维护；接口与指南源在 PlatformBackend，文档通过发布流程同步。

- [歌曲生成](audios.md)
- [歌词生成](lyrics.md)
- [任务与历史](tasks.md)
- [OpenAPI](openapi.json)
- [开发者控制台](https://platform.acedata.cloud/console/applications)
- [Studio](https://studio.acedata.cloud/acemusic)
- [在线文档](https://docs.acedata.cloud/zh-Hans/guides/acemusic/acemusic_audios)

模型：`acemusic-v1.1`（默认）、`acemusic-v1`。歌曲生成默认异步，提交后保存平台任务 ID，使用免费任务 API 查询原任务。一次完整双曲组收一次费用；最终失败或部分失败不收生成费。歌词 API 独立收费。

本次新增服务的发布依赖对应 Backend 与 worker PR；源码存在不表示生产已开放。

## Trial account concurrency

Accounts with neither a successful paid top-up nor an administrator's manual credit addition may run **one billable request at a time across the entire account**, shared by all API keys and services. Rewards, redemption cards and transferred credits do not count as paid top-ups. A successful paid top-up or manual credit addition removes this trial restriction; balance and key usage-limit checks still apply. The read-only user flag `has_recharged` records this eligibility; it is not a request parameter.

A new billable request returns `429 too_many_requests` while another is running. Wait for the active request's final result before submitting the next one. Free task polling remains available.

For async APIs, acceptance or a task ID is not completion: keep querying the same task until its final result. A disconnect or proxy timeout does not mean execution stopped. If a task has no terminal result for a long time, contact support with `trace_id`.

This restriction changes neither trial API availability nor pricing; fees are settled after execution based on actual usage. Realtime connection authentication does not occupy this ordinary-request slot and retains its existing per-turn billing.
