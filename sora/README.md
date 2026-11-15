# Sora API — retired

The Sora integration is retired and is no longer available in the Ace Data Cloud public API catalog. This repository retains historical documentation only; its previous endpoints, model names and prices are not a supported integration contract.

Do not build new integrations against `/sora/videos` or install Sora-specific tools for new video generation. Existing documentation remains in Git history for reference.

## Migrate an existing workflow

Choose a currently available video service from the [Ace Data Cloud service catalog](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=sora_api_retirement). Review its current API contract and pricing before updating your application:

- [Seedance API](https://github.com/AceDataCloud/SeedanceAPI)
- [Kling API](https://github.com/AceDataCloud/KlingAPI)
- [Veo API](https://github.com/AceDataCloud/VeoAPI)

These services have their own request fields, limits and prices. Switching is an explicit application change; there is no automatic model substitution.

If you need help with a historical task, retain its task ID and trace ID and contact Ace Data Cloud support.
