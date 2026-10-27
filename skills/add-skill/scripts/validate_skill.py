"""Check skill structure and resource containment; requires Python 3.10+."""

import argparse
import os
import re
import sys
from pathlib import Path, PureWindowsPath
from urllib.parse import unquote, urlsplit

if sys.version_info < (3, 10):
    sys.exit("Python 3.10+ is required")

try:
    import yaml
    from markdown_it import MarkdownIt
    from markdown_it.common.utils import normalizeReference
except ImportError:
    sys.exit("Install the dependencies in requirements.txt next to this script.")

MAX_DOCUMENT_BYTES = 1024 * 1024
MAX_FRONTMATTER_BYTES = 16 * 1024
MAX_YAML_DEPTH = 32
MAX_YAML_EVENTS = 4096
SCAFFOLD_MARKER = re.compile(r"@@ADD_SKILL_[A-Z_]+@@")


def read_document(path: Path) -> str:
    with path.open("rb") as stream:
        content = stream.read(MAX_DOCUMENT_BYTES + 1)
    if len(content) > MAX_DOCUMENT_BYTES:
        raise ValueError(f"document exceeds {MAX_DOCUMENT_BYTES} bytes")
    return content.decode("utf-8")


def packaged_files(directory: Path, errors: list[str]) -> list[Path]:
    """Inspect every resource without following directory symlinks."""
    files = []

    def walk_error(error: OSError) -> None:
        errors.append(f"cannot inspect packaged resources: {error}")

    for parent, folders, names in os.walk(directory, followlinks=False, onerror=walk_error):
        for name in folders + names:
            path = Path(parent) / name
            label = path.relative_to(directory)
            try:
                if path.is_symlink() and Path(os.readlink(path)).is_absolute():
                    errors.append(f"{label}: symlink target must be relative for relocation")
                    continue
                resolved = path.resolve(strict=True)
                if not resolved.is_relative_to(directory):
                    errors.append(f"{label}: resolves outside the skill directory")
                elif path.is_file():
                    files.append(path)
            except (OSError, RuntimeError) as exc:
                errors.append(f"{label}: cannot resolve resource: {exc}")
    return files


def parse_frontmatter(source: str) -> tuple[dict, str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", source, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter delimited by ---")
    header = match.group(1)
    if len(header.encode("utf-8")) > MAX_FRONTMATTER_BYTES:
        raise ValueError(f"YAML frontmatter exceeds {MAX_FRONTMATTER_BYTES} bytes")
    depth = 0
    for count, event in enumerate(yaml.parse(header), start=1):
        if count > MAX_YAML_EVENTS:
            raise ValueError("YAML frontmatter contains too many elements")
        # Parsing limits alone do not bound merge expansion during construction.
        if isinstance(event, yaml.AliasEvent):
            raise ValueError("YAML aliases are not supported in skill frontmatter")
        if isinstance(event, (yaml.MappingStartEvent, yaml.SequenceStartEvent)):
            depth += 1
            if depth > MAX_YAML_DEPTH:
                raise ValueError(f"YAML frontmatter nesting exceeds {MAX_YAML_DEPTH} levels")
        elif isinstance(event, (yaml.MappingEndEvent, yaml.SequenceEndEvent)):
            depth -= 1
    metadata = yaml.safe_load(header)
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a mapping")
    return metadata, source[match.end():]


def undefined_reference(state, silent: bool) -> bool:
    """Report explicit [text][label] and [label][] without a definition.

    CommonMark treats these as plain text. Run after its link rule and reuse its
    label parser so escapes, nesting, and code spans retain Markdown semantics.
    Bare [text] remains valid prose, since it need not be a shortcut link.
    """
    if silent or state.src[state.pos] != "[":
        return False
    end = state.md.helpers.parseLinkLabel(state, state.pos, True)
    if end < 0 or end + 1 >= state.posMax or state.src[end + 1] != "[":
        return False
    reference_end = state.md.helpers.parseLinkLabel(state, end + 1)
    if reference_end < 0:
        return False
    label = state.src[end + 2:reference_end] or state.src[state.pos + 1:end]
    if normalizeReference(label) in state.env.get("references", {}):
        return False
    state.env.setdefault("undefined_references", []).append(label)
    state.push("text", "", 0).content = state.src[state.pos:reference_end + 1]
    state.pos = reference_end + 1
    return True


def link_targets(tokens):
    for token in tokens:
        if token.type in ("link_open", "image"):
            yield token.attrGet("href" if token.type == "link_open" else "src")
        if token.children:
            yield from link_targets(token.children)


def check_links(document: Path, content: str, directory: Path) -> list[str]:
    errors = []
    label = document.relative_to(directory)
    markdown = MarkdownIt("commonmark")
    # Inspect all URI schemes, including file:, which renderers normally suppress.
    # This validator never renders HTML or opens a destination.
    markdown.validateLink = lambda target: True
    markdown.inline.ruler.after("link", "undefined_reference", undefined_reference)
    environment = {}
    tokens = markdown.parse(content, environment)
    for reference in environment.get("undefined_references", []):
        errors.append(f"{label}: undefined link reference: {reference}")
    for target in link_targets(tokens):
        if not target:
            continue
        try:
            parsed = urlsplit(target)
            if parsed.scheme.lower() == "file" or PureWindowsPath(unquote(target)).drive:
                errors.append(f"{label}: machine-local link must use a packaged relative path: {target}")
                continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (document.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(directory):
                errors.append(f"{label}: link leaves the skill directory: {target}")
            elif not resolved.exists():
                errors.append(f"{label}: missing link target: {target}")
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(f"{label}: invalid link {target}: {exc}")
    return errors


def validate(directory: Path) -> list[str]:
    """Read packaged resources without executing helpers or fetching links."""
    directory = directory.resolve()
    if not directory.is_dir():
        return ["missing skill directory"]
    errors = []
    files = packaged_files(directory, errors)
    entrypoint = directory / "SKILL.md"
    if entrypoint not in files:
        return errors or ["missing SKILL.md"]
    try:
        source = read_document(entrypoint)
        metadata, body = parse_frontmatter(source)
    except (OSError, ValueError, yaml.YAMLError, RecursionError) as exc:
        return errors + [f"invalid SKILL.md: {exc}"]

    name = metadata.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append("name must be 1–64 lowercase letters/digits with single internal hyphens")
    elif name != directory.name:
        errors.append(f"name {name!r} must match directory name {directory.name!r}")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append("description must be a nonempty string of at most 1024 characters")
    if not body.strip():
        errors.append("SKILL.md must contain instructions after the frontmatter")

    # Assets may intentionally contain scaffold markers and Markdown templates.
    for document in files:
        relative = document.relative_to(directory)
        if relative.parts[0] == "assets":
            continue
        prose = document == entrypoint or (document.suffix == ".md" and relative.parts[0] == "references")
        try:
            content = source if document == entrypoint else read_document(document)
        except UnicodeDecodeError as exc:
            if prose:
                errors.append(f"{relative}: cannot read: {exc}")
            continue  # Binary resources do not contain skill scaffold text.
        except (OSError, ValueError) as exc:
            errors.append(f"{relative}: cannot read: {exc}")
            continue
        if not prose and "\x00" in content:
            continue
        if SCAFFOLD_MARKER.search(content):
            errors.append(f"{relative}: unfinished add-skill scaffold marker")
        if prose:
            errors.extend(check_links(document, body if document == entrypoint else content, directory))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directories", nargs="+", type=Path, help="skill directories to check")
    args = parser.parse_args()
    failed = False
    for directory in args.directories:
        try:
            errors = validate(directory)
        except (OSError, ValueError, RuntimeError) as exc:
            errors = [str(exc)]
        if errors:
            failed = True
            for error in errors:
                print(f"FAIL {directory}: {error}", file=sys.stderr)
        else:
            print(f"PASS {directory}")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
