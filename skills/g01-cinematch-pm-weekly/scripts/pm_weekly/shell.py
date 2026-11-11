import subprocess
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class CommandOutput:
    stdout: str
    stderr: str


class CommandFailed(Exception):
    def __init__(self, arguments: list[str], stderr: str):
        super().__init__(f"`{' '.join(arguments)}` failed:\n{stderr.strip()}")


CommandRunner = Callable[[list[str]], CommandOutput]


def run_command(arguments: list[str]) -> CommandOutput:
    completed = subprocess.run(arguments, capture_output=True, text=True, encoding="utf-8")
    if completed.returncode != 0:
        raise CommandFailed(arguments, completed.stderr)
    return CommandOutput(stdout=completed.stdout, stderr=completed.stderr)
