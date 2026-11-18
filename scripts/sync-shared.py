"""Check or refresh generated skill references and agent guidance (Python 3.10+)."""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONSUMERS = {
    "github-cli.md": ("triage-bug", "triage-cve", "review-pr", "fix-issue", "backport-pr", "implement-feature", "diagnose-ci", "address-review", "add-skill", "update-skill"),
    "evidence.md": ("triage-bug", "triage-cve", "review-pr", "fix-issue", "backport-pr", "implement-feature", "diagnose-ci", "address-review"),
    "security-handling.md": ("triage-bug", "triage-cve", "review-pr", "fix-issue", "backport-pr", "implement-feature", "diagnose-ci", "address-review"),
    "duplicate-search.md": ("triage-bug", "triage-cve"),
    "ripwire.md": ("triage-bug", "triage-cve", "review-pr", "fix-issue", "implement-feature", "diagnose-ci", "address-review"),
}


def sync(root: Path, write: bool = False) -> list[str]:
    root = root.resolve()
    errors = []
    copies = {
        Path("shared") / name: [Path("skills") / skill / "references" / name for skill in consumers]
        for name, consumers in CONSUMERS.items()
    }
    copies[Path("AGENTS.md")] = [Path(".github/copilot-instructions.md")]
    for relative, targets in copies.items():
        source = root / relative
        try:
            if not source.resolve().is_relative_to(root):
                raise ValueError("source resolves outside the repository")
            content = source.read_bytes()
        except (OSError, ValueError, RuntimeError) as exc:
            errors.append(f"{source.relative_to(root)}: {exc}")
            continue
        expected = (f"<!-- Generated from {relative.as_posix()}; edit the source and run "
                    "python scripts/sync-shared.py --write. -->\n\n").encode() + content
        for target_path in targets:
            target = root / target_path
            try:
                if not target.resolve().is_relative_to(root):
                    raise ValueError("generated copy resolves outside the repository")
                # Generated files must carry their own portable content.
                if target.is_symlink() or target.parent.is_symlink():
                    raise ValueError("generated copy must not be a symlink")
                if write:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(expected)
                elif not target.is_file() or target.read_bytes() != expected:
                    errors.append(f"{target.relative_to(root)}: missing or stale; "
                                  "run python scripts/sync-shared.py --write")
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append(f"{target.relative_to(root)}: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="refresh checked-in copies")
    args = parser.parse_args()
    errors = sync(ROOT, write=args.write)
    for error in errors:
        print(f"FAIL: {error}")
    if not errors:
        print("PASS: generated guidance " + ("synchronized" if args.write else "matches sources"))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
