import re
from pathlib import Path

from .shell import CommandOutput, CommandRunner, run_command

DRIVE_BACKEND = "drive"
GLOB_SPECIAL_CHARACTER = re.compile(r"([*?\[\]{}\\])")


def drive_remotes(run: CommandRunner = run_command) -> list[str]:
    """Remote names are chosen by each person in `rclone config`, so they are discovered, never assumed."""
    output = run(["rclone", "listremotes", "--long"])
    remotes = []
    for line in output.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[-1] == DRIVE_BACKEND:
            remotes.append(parts[0].rstrip(":"))
    return remotes


def export_from_folder(
    *,
    remote: str,
    folder_id: str,
    file_names: list[str],
    destination: Path,
    run: CommandRunner = run_command,
) -> CommandOutput:
    """Google-native files come out as .xlsx/.pptx; rclone lists them under those export names."""
    arguments = [
        "rclone", "copy", f"{remote}:", str(destination),
        "--drive-root-folder-id", folder_id,
        "--max-depth", "1",
    ]
    for file_name in file_names:
        arguments += ["--include", _literal_glob(file_name)]
    return run(arguments)


def _literal_glob(file_name: str) -> str:
    return GLOB_SPECIAL_CHARACTER.sub(r"\\\1", file_name)
