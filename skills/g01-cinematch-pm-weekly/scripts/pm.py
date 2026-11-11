import sys
from pathlib import Path

# The skill lives in a vault that syncs itself to GitHub, so no __pycache__ may land next to the code.
sys.dont_write_bytecode = True
# Added explicitly so the package still imports under `python -I`, which drops the script's own folder from the path.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pm_weekly.commands import main  # noqa: E402

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
