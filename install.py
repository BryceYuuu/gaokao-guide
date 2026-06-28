#!/usr/bin/env python3
"""Install gaokao-guide into a writable local skills directory.

`/mnt/skills` is commonly mounted read-only by hosted runtimes, so this
installer defaults to user-writable Codex or Claude skills directories.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


SKILL_NAME = "gaokao-guide"


def expand_path(path: Path) -> Path:
    return Path(os.path.expandvars(str(path))).expanduser()


def default_codex_skills_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return expand_path(Path(codex_home)) / "skills"
    return Path.home() / ".codex" / "skills"


def default_claude_skills_dir(scope: str, repo_root: Path) -> Path:
    if scope == "project":
        return repo_root / ".claude" / "skills"
    claude_home = os.environ.get("CLAUDE_HOME")
    if claude_home:
        return expand_path(Path(claude_home)) / "skills"
    return Path.home() / ".claude" / "skills"


def default_skills_dir(platform: str, scope: str, repo_root: Path) -> Path:
    if platform == "claude":
        return default_claude_skills_dir(scope, repo_root)
    return default_codex_skills_dir()


def is_read_only_system_mount(path: Path) -> bool:
    return str(path).startswith("/mnt/skills")


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
    parser = argparse.ArgumentParser(description="Install gaokao-guide into a writable local skills directory.")
    parser.add_argument("--platform", choices=("codex", "claude"), default="codex", help="Target runtime. Defaults to codex.")
    parser.add_argument("--scope", choices=("global", "project"), default="global", help="Claude install scope. Codex ignores this option.")
    parser.add_argument("--target", type=Path, default=None, help="Target skills directory. Overrides --platform and --scope defaults.")
    parser.add_argument("--force", action="store_true", help="Remove an existing gaokao-guide install before copying.")
    parser.add_argument("--dry-run", action="store_true", help="Print the resolved install location without copying files.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent
    source = repo_root / SKILL_NAME
    if not (source / "SKILL.md").exists():
        print(f"ERROR: {source}/SKILL.md not found. Run this installer from the repository root.", file=sys.stderr)
        return 2

    requested_target = expand_path(args.target) if args.target else default_skills_dir(args.platform, args.scope, repo_root)
    target = requested_target

    if is_read_only_system_mount(target):
        fallback = default_skills_dir(args.platform, args.scope, repo_root)
        print(f"WARNING: {target} points to /mnt/skills, which is usually a read-only system mount.")
        print(f"Using writable local skills directory instead: {fallback}")
        target = fallback

    destination = target / SKILL_NAME
    if args.dry_run:
        print(f"platform={args.platform}")
        print(f"scope={args.scope}")
        print(f"source={source}")
        print(f"target={target}")
        print(f"destination={destination}")
        return 0

    if not can_write_dir(target):
        print(f"ERROR: target skills directory is not writable: {target}", file=sys.stderr)
        if args.platform == "claude":
            print("Try: python3 install.py --platform claude --target ~/.claude/skills", file=sys.stderr)
        else:
            print("Try: python3 install.py --target ~/.codex/skills", file=sys.stderr)
        return 1

    copy_skill(source, destination, args.force)
    print(f"Installed {SKILL_NAME} to {destination}")
    if args.platform == "claude":
        print("Restart Claude and run /skills if the skill does not appear immediately.")
    else:
        print("Restart Codex or reload skills if the skill does not appear immediately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
