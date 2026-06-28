#!/usr/bin/env python3
"""Install gaokao-guide into a writable Codex skills directory.

`/mnt/skills` is commonly mounted read-only by hosted runtimes, so this
installer defaults to `${CODEX_HOME:-~/.codex}/skills` instead.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


SKILL_NAME = "gaokao-guide"


def default_skills_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def can_write_dir(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".gaokao-guide-write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return True
    except OSError:
        return False


def copy_skill(source: Path, destination: Path, force: bool) -> None:
    if destination.exists() and force:
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Install gaokao-guide into a writable Codex skills directory.")
    parser.add_argument("--target", type=Path, default=None, help="Target skills directory. Defaults to ${CODEX_HOME:-~/.codex}/skills.")
    parser.add_argument("--force", action="store_true", help="Remove an existing gaokao-guide install before copying.")
    parser.add_argument("--dry-run", action="store_true", help="Print the resolved install location without copying files.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    source = repo_root / SKILL_NAME
    if not (source / "SKILL.md").exists():
        print(f"ERROR: {source}/SKILL.md not found. Run this installer from the repository root.", file=sys.stderr)
        return 2

    requested_target = args.target.expanduser() if args.target else default_skills_dir()
    target = requested_target

    if str(target).startswith("/mnt/skills") and not can_write_dir(target):
        fallback = default_skills_dir()
        print(f"WARNING: {target} is not writable; /mnt/skills is usually a read-only system mount.")
        print(f"Using writable user skills directory instead: {fallback}")
        target = fallback

    if not can_write_dir(target):
        print(f"ERROR: target skills directory is not writable: {target}", file=sys.stderr)
        print("Try: python3 install.py --target ~/.codex/skills", file=sys.stderr)
        return 1

    destination = target / SKILL_NAME
    if args.dry_run:
        print(f"source={source}")
        print(f"target={target}")
        print(f"destination={destination}")
        return 0

    copy_skill(source, destination, args.force)
    print(f"Installed {SKILL_NAME} to {destination}")
    print("Restart Codex or reload skills if the skill does not appear immediately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
