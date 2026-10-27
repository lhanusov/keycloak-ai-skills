"""Validate portable plugin metadata, client integrations, and collection skills."""

import importlib.util
import json
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit("Python 3.10+ is required")

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("Install development dependencies with: python -m pip install -r requirements-dev.txt")

ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


skills = load_module("validate_skill", ROOT / "skills/add-skill/scripts/validate_skill.py")
TEXT = {"type": "string"}
NAME = {"type": "string", "minLength": 1, "maxLength": 64, "pattern": r"^[a-z0-9]+(?:-[a-z0-9]+)*$"}
# Agent Plugins 1.0.0 manifest contract:
# https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
PLUGIN_SCHEMA = {
    "type": "object", "required": ["$schema", "name"], "additionalProperties": False,
    "properties": {
        "$schema": {"const": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"},
        "name": {"type": "string", "minLength": 1, "maxLength": 64,
                 "pattern": r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$"},
        **{key: TEXT for key in ("version", "description", "homepage", "repository", "license")},
        "author": {"type": "object", "additionalProperties": False,
                   "properties": {key: TEXT for key in ("name", "email", "url")}},
        "keywords": {"type": "array", "items": TEXT},
        "extensions": {"type": "object", "additionalProperties": {"type": "object"}},
    },
}
# This schema describes this project's local-source Codex catalog, not every
# possible Codex source type.
CODEX_SCHEMA = {
    "type": "object", "required": ["name", "interface", "plugins"], "additionalProperties": False,
    "properties": {
        "name": NAME,
        "interface": {"type": "object", "required": ["displayName"], "additionalProperties": False,
                      "properties": {"displayName": {"type": "string", "minLength": 1}}},
        "plugins": {"type": "array", "minItems": 1, "items": {
            "type": "object", "required": ["name", "source", "policy", "category"], "additionalProperties": False,
            "properties": {
                "name": NAME, "category": {"type": "string", "minLength": 1},
                "source": {"type": "object", "required": ["source", "path"], "additionalProperties": False,
                           "properties": {"source": {"const": "local"}, "path": {"type": "string", "pattern": r"^\./"}}},
                "policy": {"type": "object", "required": ["installation", "authentication"], "additionalProperties": False,
                           "properties": {"installation": {"const": "AVAILABLE"},
                                          "authentication": {"const": "ON_INSTALL"}}},
            },
        }},
    },
}
MARKETPLACE_SCHEMA = {
    "type": "object", "required": ["name", "owner", "plugins"], "additionalProperties": False,
    "properties": {
        "name": NAME,
        "owner": {"type": "object", "required": ["name"], "additionalProperties": False,
                  "properties": {"name": {"type": "string", "minLength": 1}}},
        "plugins": {"type": "array", "minItems": 1, "items": {
            "type": "object", "required": ["name", "source"], "additionalProperties": False,
            "properties": {"name": NAME, "source": {"type": "string", "pattern": r"^\./"}},
        }},
    },
}
# Supported compatibility manifests intentionally expose no tools or hooks.
ADAPTER_SCHEMA = {
    "type": "object", "required": ["name", "version", "description"], "additionalProperties": False,
    "properties": {"name": NAME, **{key: {"type": "string", "minLength": 1}
                                   for key in ("version", "description", "license")}},
}
BOB_SCHEMA = {
    **ADAPTER_SCHEMA,
    "required": ADAPTER_SCHEMA["required"] + ["contextFileName"],
    "properties": {**ADAPTER_SCHEMA["properties"], "contextFileName": {"type": "string", "minLength": 1}},
}


def read_json(root: Path, relative: Path, schema: dict, errors: list[str]):
    path = root / relative
    try:
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("manifest resolves outside the repository")
        content = json.loads(skills.read_document(path))
        failures = list(Draft202012Validator(schema).iter_errors(content))
        for failure in failures:
            location = ".".join(str(part) for part in failure.absolute_path) or "root"
            errors.append(f"{relative} ({location}): {failure.message}")
        return None if failures else content
    except (OSError, ValueError, RuntimeError) as exc:
        errors.append(f"{relative}: {exc}")
        return None


def check_skills(package: Path, errors: list[str]) -> None:
    skill_parent = package / "skills"
    if not skill_parent.resolve().is_relative_to(package):
        raise ValueError("skills directory resolves outside its plugin")
    folders = sorted(path for path in skill_parent.iterdir() if path.is_dir()) if skill_parent.is_dir() else []
    if not folders:
        errors.append(f"{package.name}: no skill directories found")
    for folder in folders:
        if not folder.resolve().is_relative_to(package):
            errors.append(f"{folder.name}: skill directory resolves outside its plugin")
        else:
            errors.extend(f"{folder.name}: {error}" for error in skills.validate(folder))


def check_catalog(root: Path, root_manifest: dict, catalog: dict, errors: list[str], checked: set[Path]) -> None:
    names = set()
    for entry in catalog["plugins"]:
        if entry["name"] in names:
            errors.append(f"duplicate catalog plugin name: {entry['name']}")
            continue
        names.add(entry["name"])
        try:
            source = entry["source"]["path"] if isinstance(entry["source"], dict) else entry["source"]
            package = (root / source).resolve(strict=True)
            if not package.is_relative_to(root):
                raise ValueError(f"plugin source leaves the repository: {source}")
            if not package.is_dir():
                raise ValueError(f"plugin source must be a directory: {source}")
            if ".." in Path(source).parts:
                raise ValueError(f"plugin source must not contain parent traversal: {source}")
            manifest = root_manifest if package == root else read_json(package, Path("plugin.json"), PLUGIN_SCHEMA, errors)
            if manifest and manifest["name"] != entry["name"]:
                errors.append(f"plugin name {manifest['name']!r} does not match catalog entry {entry['name']!r}")
            if package not in checked:
                check_skills(package, errors)
                checked.add(package)
        except (OSError, ValueError, RuntimeError) as exc:
            errors.append(f"{entry['name']}: {exc}")


def catalog_sources(catalog: dict) -> set[tuple[str, str]]:
    return {(entry["name"], entry["source"]["path"] if isinstance(entry["source"], dict)
             else entry["source"]) for entry in catalog["plugins"]}


def check_package(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    manifest = read_json(root, Path("plugin.json"), PLUGIN_SCHEMA, errors)
    if manifest is None:
        return errors
    try:
        check_skills(root, errors)
    except (OSError, ValueError, RuntimeError) as exc:
        errors.append(str(exc))
    checked = {root}
    catalogs = []
    for relative, schema in ((Path(".agents/plugins/marketplace.json"), CODEX_SCHEMA),
                             (Path(".claude-plugin/marketplace.json"), MARKETPLACE_SCHEMA)):
        # A portable package needs no client catalog. When a catalog directory is
        # present, require its manifest rather than silently overlooking damage.
        if not (root / relative.parent).exists():
            continue
        catalog = read_json(root, relative, schema, errors)
        if catalog is not None:
            catalogs.append(catalog)
            check_catalog(root, manifest, catalog, errors, checked)
    if len(catalogs) == 2:
        if catalogs[1]["name"] != catalogs[0]["name"] or catalog_sources(catalogs[1]) != catalog_sources(catalogs[0]):
            errors.append("client catalogs must name the same marketplace and plugin sources")

    adapters = ((Path(".claude-plugin/plugin.json"), ADAPTER_SCHEMA),
                (Path("gemini-extension.json"), ADAPTER_SCHEMA), (Path("bob-extension.json"), BOB_SCHEMA))
    for relative, schema in adapters:
        path = root / relative
        if not path.exists() and not path.is_symlink() and relative.parent == Path("."):
            continue
        if not path.parent.exists():
            continue
        adapter = read_json(root, relative, schema, errors)
        if adapter is None:
            continue
        for key in ("name", "version", "description", "license"):
            if key in adapter and adapter[key] != manifest.get(key):
                errors.append(f"{relative}: {key} must match plugin.json")
        if "contextFileName" in adapter:
            try:
                context = (root / adapter["contextFileName"]).resolve(strict=True)
                if Path(adapter["contextFileName"]).is_absolute() or not context.is_relative_to(root):
                    raise ValueError("context file must be packaged inside the repository")
                errors.extend(skills.check_links(context, skills.read_document(context), root))
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append(f"{relative}: {exc}")
    return errors


def main() -> int:
    try:
        errors = check_package(ROOT)
    except (OSError, ValueError, RuntimeError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"FAIL {error}", file=sys.stderr)
    if not errors:
        print("PASS: portable plugin, client integrations, and every collection skill")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
