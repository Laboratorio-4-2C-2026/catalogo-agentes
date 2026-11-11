# Setup

Once per person. `pm.py doctor` says which of these are missing.

## Python

Python 3.10 or newer, plus two packages:

```
pip install openpyxl tzdata
```

`openpyxl` reads the exported spreadsheets. `tzdata` gives Python the Argentina timezone on Windows, which ships without one; on macOS and Linux it is usually already there.

## rclone

The Drive app mounts real files (.xlsx, .pptx) as a disk, but Google-native files (the Tablero, the cátedra's EVM) appear there as stubs that cannot be read. rclone exports them as .xlsx.

**Install**, then check with `rclone version`:

| System | Command |
|---|---|
| Windows | `winget install Rclone.Rclone`, then open a new terminal so it is on the path |
| macOS | `brew install rclone` |
| Linux | the distribution's package (`sudo apt install rclone`), or the installer from rclone.org |

**Configure** with `rclone config`, in your own terminal because it asks questions. A *remote* is a saved connection to one account, used as `name:` in commands.

| Prompt | Answer |
|---|---|
| `n/s/q>` | `n`, new remote. Skip `s`: a config password makes every command ask for it |
| `name>` | anything; `gdrive` is the usual. `pm.py` finds it by type, not by name |
| `Storage>` | `drive`, typed as a word: the number changes between versions |
| `client_id>`, `client_secret>` | Enter both, unless you made your own client (below) |
| `scope>` | `drive.readonly`. The skill never writes to Drive, and this makes sure it cannot |
| `service_account_file>` | Enter |
| `Edit advanced config?` | `n` |
| `Use web browser to automatically authenticate?` | `y`, then sign in with the Google account that has access to the team's Drive folder |
| `Configure this as a Shared Drive (Team Drive)?` | `n`: the team folder is shared with you, not a Shared Drive. Answering `y` by mistake is harmless if none is found |
| `Keep this remote?` | `y`, then `q` |

Check it with `pm.py doctor`, then `pm.py fetch <scratch folder>`.

### Own client ID

rclone warns that its shared Google client is being retired during 2026. When `fetch` starts failing on authentication, create your own OAuth client following https://rclone.org/drive/#making-your-own-client-id and give it to the remote with `rclone config` (edit the remote, paste `client_id` and `client_secret`). Nothing else changes.

## GitHub

The `gh` CLI, logged in with `gh auth login`, with read access to the app repository and to the KPI platform repository (both in [project.json](../project.json)). The skill only runs `gh pr list` and read requests to `gh api`.

## Project values

Every value in `<angle brackets>` in [project.json](../project.json) belongs to the team and is left out of this skill: the app repository, the Linear team key, the Drive file names and their sheet names, and the team's tab in the Tablero. Fill them in once, from the team's own Drive and repositories, before the first `fetch`.

## Environment variables

Two project identifiers stay out of the repository and are read from the environment:

| Variable | What it is | Needed by |
|---|---|---|
| `CINEMATCH_DRIVE_FOLDER_ID` | The id of the team's Drive folder, the last part of its URL | `fetch` |
| `CINEMATCH_KPI_PROJECT_ID` | The team's project id on the KPI platform | `kpis` |

The values belong to the team, not to this skill: ask the team's PM for them. Set them once in your user environment (on Windows, `setx CINEMATCH_DRIVE_FOLDER_ID <value>` and the same for the other, then open a new terminal; on macOS and Linux, an `export` line in your shell profile). `pm.py doctor` says whether each one is set, without printing it.

## Linear

The official Linear MCP, added once to Claude Code:

```
claude mcp add --transport http --scope user linear https://mcp.linear.app/mcp
```

Restart Claude Code, run `/mcp` and authorize in the browser. If the MCP later shows only `authenticate`, the authorization expired: run `/mcp` again.
