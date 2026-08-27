from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env", override=False)


def main() -> None:
    root = os.environ.get("PARQUET_ROOT_PATH", "").strip()
    print(f"PARQUET_ROOT_PATH={root or '<unset>'}")
    assert root, "PARQUET_ROOT_PATH is not set"
    assert Path(root).exists(), f"PARQUET_ROOT_PATH does not exist: {root}"


if __name__ == "__main__":
    main()
