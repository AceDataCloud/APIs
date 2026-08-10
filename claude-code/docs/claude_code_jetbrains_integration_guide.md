# Using Claude Code in JetBrains IDEs

Claude Code integrates with IntelliJ IDEA, PyCharm, Android Studio, WebStorm, PhpStorm, GoLand, and other IDEs through the official JetBrains plugin. The plugin does not bundle the Claude Code CLI: it runs the local `claude` command in the IDE's integrated terminal, so install the CLI first.

The plugin installation, shortcuts, `/ide`, Claude command, Remote Development, and WSL behavior are verified against the [official JetBrains documentation](https://code.claude.com/docs/en/jetbrains). The Ace Data Cloud configuration below only covers API credentials and endpoint settings.

## Get an Ace Data Cloud Token

Open the Coding Application in the [Ace Data Cloud console](https://platform.acedata.cloud/console/applications) to create or copy an API token. Do not put the token in screenshots, chat messages, or a Git repository.

## Install the Claude Code CLI

On macOS, Linux, or WSL:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

On Windows PowerShell:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Reopen your terminal and verify the installation:

```bash
claude --version
```

## Install the Official JetBrains Plugin

Choose either supported installation method.

### Marketplace

1. Open **Settings / Preferences → Plugins → Marketplace**.
2. Search for and install the **Claude Code** plugin.
3. Restart the IDE completely.

![Claude Code Plugin in JetBrains Marketplace](https://cdn.acedata.cloud/de78fd305b.png)

### Install from Claude Code

In a terminal at the IDE project directory, run:

```bash
claude
```

Then run:

```text
/ide
```

If Claude Code detects a running JetBrains IDE without the plugin, `/ide` installs the plugin and asks you to restart the IDE.

If the plugin cannot find `claude`, enter the full executable path in the plugin's **Claude command** setting. Find it with:

```bash
which claude
```

## Configure Ace Data Cloud

The `env` field in Claude Code settings accepts literal environment-variable values; do not assume it expands `${NAME}`. Prefer setting credentials in the local environment that starts the IDE.

On macOS, Linux, or WSL:

```bash
export ANTHROPIC_BASE_URL="https://api.acedata.cloud"
export ANTHROPIC_AUTH_TOKEN="your Ace Data Cloud API token"
```

On Windows PowerShell:

```powershell
$env:ANTHROPIC_BASE_URL="https://api.acedata.cloud"
$env:ANTHROPIC_AUTH_TOKEN="your Ace Data Cloud API token"
```

Start JetBrains from that configured environment, or add these variables to the local user environment that launches the IDE. Restart the IDE after configuration.

If you instead use Claude Code settings, only write the token to the private `~/.claude/settings.json` or a Git-ignored `.claude/settings.local.json` file:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.acedata.cloud",
    "ANTHROPIC_AUTH_TOKEN": "replace locally with your API token"
  }
}
```

Do not commit a token to a shared `.claude/settings.json`. If an older `ANTHROPIC_API_KEY` is set in the same startup environment, remove it first:

```bash
unset ANTHROPIC_API_KEY
```

## Use and Verify

Running `claude` from the IDE terminal automatically enables IDE integration. You can also start Claude Code from an external terminal in the project root, then connect it to the running IDE:

```bash
cd /path/to/project
claude
```

```text
/ide
```

After a successful connection, Claude Code displays a message such as `Connected to IntelliJ IDEA`.

First verify the connection with a minimal command:

```bash
claude -p "Reply only OK"
```

Then use a read-only task in the IDE:

```text
Explain this project's directory structure without modifying files.
```

The official plugin supports the IDE diff viewer, current selection and tab context, file-line references, and diagnostics sharing. Useful shortcuts include:

- macOS: `Cmd+Esc` opens Claude Code; `Cmd+Option+K` inserts a file reference.
- Windows/Linux: `Ctrl+Esc` opens Claude Code; `Alt+Ctrl+K` inserts a file reference.

## Remote Development and WSL

- For JetBrains Remote Development, install the plugin on the remote host through **Settings → Plugin (Host)**.
- Configure the Claude Code CLI, API environment variables, and project path on the remote host, not only on the local UI machine.
- On WSL2, IDE detection relies on Windows/WSL network connectivity. If `/ide` cannot detect the IDE, review the [official WSL troubleshooting guidance](https://code.claude.com/docs/en/jetbrains#wsl-configuration) for firewall and mirrored-networking settings.

## Troubleshooting

### Cannot launch Claude Code or `command not found`

The plugin does not include the CLI. Confirm that `claude --version` succeeds. If the IDE has a different `PATH`, set **Claude command** to the full path returned by `which claude`, then restart the IDE.

### IDE not detected

Confirm that the official plugin is enabled, start Claude Code from the same project root, and run `/ide` again. With Remote Development, confirm that the plugin is installed on the host.

### 401 response

Confirm the token belongs to an available Coding Application, the IDE process inherited `ANTHROPIC_AUTH_TOKEN`, and no old `ANTHROPIC_API_KEY` remains set.

### Model unavailable

The model catalog changes over time. Use the exact model ID and verification status shown in the Coding configuration selector and live model catalog rather than a static guide.

## Official References

- [Claude Code for JetBrains IDEs](https://code.claude.com/docs/en/jetbrains)
- [Claude Code Settings](https://code.claude.com/docs/en/settings)
- [Claude Code Setup](https://code.claude.com/docs/en/setup)
