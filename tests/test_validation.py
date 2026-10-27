"""Regression fixtures for portable skills, packages, and client integrations."""

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("package_check", ROOT / "scripts/check-package.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
validator = check.skills


class SkillTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.skill = self.base / "sample-skill"
        self.skill.mkdir()
        self.entry = self.skill / "SKILL.md"
        self.write("Use the supplied notes.")

    def write(self, body, header="name: sample-skill\ndescription: Summarize supplied notes"):
        self.entry.write_text(f"---\n{header}\n---\n{body}\n", encoding="utf-8")

    def symlink(self, path, target, directory=False):
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlinks unavailable: {exc}")

    def test_minimal_skill(self):
        self.assertEqual(validator.validate(self.skill), [])

    def test_jinja_and_markdown_examples_are_literal(self):
        examples = [
            "Render {{ username }}.",
            "```markdown\n[Report](report.md)\n```",
            "~~~~markdown\n```\n[Report](report.md)\n```\n~~~~",
            "`[Report](report.md)`",
            "``Use `code` and [Report](report.md)``",
            "    [Report](report.md)\n    [Missing][undefined]",
            ">     [Report](report.md)",
        ]
        for example in examples:
            with self.subTest(example=example):
                self.write(example)
                self.assertEqual(validator.validate(self.skill), [])

    def test_real_link_after_fence_is_checked(self):
        self.write("```\n[Example](missing.md)\n```\n[Real](required.md)")
        errors = validator.validate(self.skill)
        self.assertEqual(len(errors), 1)
        self.assertIn("required.md", errors[0])

    def test_real_relative_link_and_packaged_target(self):
        self.write("[Reference](references/guide.md)")
        self.assertTrue(validator.validate(self.skill))
        (self.skill / "references").mkdir()
        (self.skill / "references/guide.md").write_text("Guide", encoding="utf-8")
        self.assertEqual(validator.validate(self.skill), [])

    def test_reference_documents_are_checked(self):
        (self.skill / "references").mkdir()
        (self.skill / "references/guide.md").write_text("[Missing](missing.md)", encoding="utf-8")
        self.assertTrue(validator.validate(self.skill))

    def test_reference_links_check_the_packaged_destination(self):
        for syntax in ("[Read][guide]", "[guide][]", "[guide]", "![Diagram][guide]"):
            with self.subTest(syntax=syntax):
                self.write(syntax + '\n\n[guide]: <guide (v2).md> "Guide"')
                self.assertTrue(any("missing link target" in error for error in validator.validate(self.skill)))
                target = self.skill / "guide (v2).md"
                target.write_text("Guide", encoding="utf-8")
                self.assertEqual(validator.validate(self.skill), [])
                target.unlink()

    def test_undefined_explicit_reference_links_are_rejected(self):
        for syntax in ("[Read][missing]", "[missing][]", "![Diagram][missing]"):
            with self.subTest(syntax=syntax):
                self.write(syntax)
                self.assertTrue(any("undefined link reference" in error for error in validator.validate(self.skill)))
        self.write("Ordinary [bracketed text] and \\[literal][missing].")
        self.assertEqual(validator.validate(self.skill), [])

    def test_parentheses_titles_and_escaped_destinations(self):
        target = self.skill / "report(v2).md"
        target.write_text("Report", encoding="utf-8")
        for link in ('[Report](report(v2).md "Title")', r"[Report](report\(v2\).md)"):
            with self.subTest(link=link):
                self.write(link)
                self.assertEqual(validator.validate(self.skill), [])
        target.unlink()
        self.assertTrue(any("missing link target" in error for error in validator.validate(self.skill)))

    def test_own_scaffold_markers_are_rejected(self):
        self.write("@@ADD_SKILL_WORKFLOW@@")
        self.assertTrue(validator.validate(self.skill))

    def test_invalid_names_produce_one_actionable_error(self):
        for name in ("null", "42", "[]", "Bad_Name", "''"):
            with self.subTest(name=name):
                self.write("Instructions", f"name: {name}\ndescription: Test")
                errors = validator.validate(self.skill)
                self.assertEqual(len(errors), 1)
                self.assertIn("name must be", errors[0])
        self.write("Instructions", "name: other\ndescription: Test")
        self.assertEqual(len(validator.validate(self.skill)), 1)
        self.assertIn("directory name", validator.validate(self.skill)[0])

    def test_helper_scaffold_markers_are_rejected_without_checking_example_links(self):
        helper = self.skill / "scripts/helper.py"
        helper.parent.mkdir()
        helper.write_text('# @@ADD_SKILL_WORKFLOW@@\n# [Example](output.md)\n', encoding="utf-8")
        errors = validator.validate(self.skill)
        self.assertEqual(len(errors), 1)
        self.assertIn(str(Path("scripts/helper.py")), errors[0])
        self.assertIn("scaffold marker", errors[0])
        helper.write_text('# [Example](output.md)\n', encoding="utf-8")
        self.assertEqual(validator.validate(self.skill), [])

    def test_binary_resources_are_not_scanned_for_scaffold_markers(self):
        for data in (b"\xff@@ADD_SKILL_NAME@@", b"\x00@@ADD_SKILL_NAME@@"):
            with self.subTest(data=data):
                (self.skill / "resource.bin").write_bytes(data)
                self.assertEqual(validator.validate(self.skill), [])

    def test_template_assets_can_keep_markers(self):
        (self.skill / "assets").mkdir()
        (self.skill / "assets/template.md").write_text("@@ADD_SKILL_NAME@@\n[Output](output.md)", encoding="utf-8")
        self.assertEqual(validator.validate(self.skill), [])

    def test_external_resource_symlinks_are_rejected(self):
        outside = self.base / "outside.txt"
        outside.write_text("external", encoding="utf-8")
        for folder in ("scripts", "assets", "references"):
            with self.subTest(folder=folder):
                link = self.skill / folder / "linked.txt"
                self.symlink(link, Path("../../outside.txt"))
                self.assertTrue(validator.validate(self.skill))
                link.unlink()

    def test_external_directory_symlink_is_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.symlink(self.skill / "scripts", Path("../outside"), directory=True)
        self.assertTrue(validator.validate(self.skill))

    def test_external_entrypoint_symlink_is_rejected(self):
        outside = self.base / "external.md"
        outside.write_text(self.entry.read_text(), encoding="utf-8")
        self.entry.unlink()
        self.symlink(self.entry, outside)
        self.assertTrue(validator.validate(self.skill))

    def test_relative_internal_symlinks_survive_relocation(self):
        (self.skill / "assets").mkdir()
        target = self.skill / "assets/data.txt"
        target.write_text("data", encoding="utf-8")
        self.symlink(self.skill / "scripts/data.txt", Path("../assets/data.txt"))
        self.symlink(self.skill / "shared-assets", Path("assets"), directory=True)
        self.assertEqual(validator.validate(self.skill), [])
        relocated = self.base / "relocated/sample-skill"
        shutil.copytree(self.skill, relocated, symlinks=True)
        shutil.rmtree(self.skill)
        self.assertEqual(validator.validate(relocated), [])
        self.assertEqual((relocated / "scripts/data.txt").read_text(), "data")
        self.assertEqual((relocated / "shared-assets/data.txt").read_text(), "data")

    def test_absolute_internal_symlinks_are_rejected(self):
        target = self.skill / "data.txt"
        target.write_text("data", encoding="utf-8")
        self.symlink(self.skill / "linked.txt", target)
        self.assertTrue(any("must be relative" in error for error in validator.validate(self.skill)))

    def test_broken_symlink_is_rejected(self):
        self.symlink(self.skill / "broken.txt", self.skill / "absent.txt")
        self.assertTrue(validator.validate(self.skill))

    def test_file_uris_and_windows_paths_are_rejected(self):
        for link in ("file:///outside/config.yaml", "file:config.yaml", "C:/outside/config.yaml"):
            with self.subTest(link=link):
                self.write(f"[Config]({link})")
                self.assertTrue(validator.validate(self.skill))

    def test_remote_links_and_anchors_are_allowed(self):
        self.write("[Docs](https://example.com/docs)\n[Section](#workflow)")
        self.assertEqual(validator.validate(self.skill), [])

    def test_traversal_link_is_rejected(self):
        self.write("[Outside](../outside.md)")
        self.assertTrue(validator.validate(self.skill))

    def test_deep_and_oversized_yaml_return_errors(self):
        for extra in ("nested: " + "[" * 600 + "0" + "]" * 600,
                      "extra: " + "x" * (validator.MAX_FRONTMATTER_BYTES + 1)):
            with self.subTest(extra_size=len(extra)):
                self.write("Instructions", "name: sample-skill\ndescription: Test\n" + extra)
                self.assertTrue(validator.validate(self.skill))

    def test_yaml_aliases_are_rejected_before_construction(self):
        header = "name: sample-skill\ndescription: Test\na: &a {value: 1}\n"
        previous = "a"
        for index in range(6):
            name = f"b{index}"
            header += f"{name}: &{name} {{<<: [" + ", ".join([f"*{previous}"] * 8) + "]}\n"
            previous = name
        for extra in (header, "name: &name sample-skill\ndescription: *name"):
            with self.subTest(header=extra), patch.object(validator.yaml, "safe_load") as load:
                self.write("Instructions", extra)
                self.assertTrue(any("aliases are not supported" in error for error in validator.validate(self.skill)))
                load.assert_not_called()

    def test_oversized_document_returns_error(self):
        self.write("x" * validator.MAX_DOCUMENT_BYTES)
        self.assertTrue(validator.validate(self.skill))

    def test_malformed_yaml_and_wrong_name_return_errors(self):
        for header in ("name: [", "name: other\ndescription: Test"):
            with self.subTest(header=header):
                self.write("Instructions", header)
                self.assertTrue(validator.validate(self.skill))


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.catalog = {
            "name": "test-skills",
            "interface": {"displayName": "Test Skills"},
            "plugins": [{
                "name": "test-plugin", "source": {"source": "local", "path": "./"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Developer Tools",
            }],
        }
        self.catalog_path = self.root / ".agents/plugins/marketplace.json"
        self.catalog_path.parent.mkdir(parents=True)
        self.plugin = {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
                       "name": "test-plugin", "version": "0.1.0", "description": "Test skills", "license": "Apache-2.0"}
        self.save_catalog()
        (self.root / "plugin.json").write_text(json.dumps(self.plugin), encoding="utf-8")
        skill = self.root / "skills/sample-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: sample-skill\ndescription: Test\n---\nInstructions\n", encoding="utf-8")

    def save_catalog(self):
        self.catalog_path.write_text(json.dumps(self.catalog), encoding="utf-8")

    def add_adapters(self):
        adapter = {key: self.plugin[key] for key in ("name", "version", "description")}
        claude = self.root / ".claude-plugin"
        claude.mkdir()
        (claude / "plugin.json").write_text(json.dumps(adapter), encoding="utf-8")
        (claude / "marketplace.json").write_text(json.dumps({
            "name": self.catalog["name"], "owner": {"name": "Test"},
            "plugins": [{"name": self.plugin["name"], "source": "./"}],
        }), encoding="utf-8")
        (self.root / "gemini-extension.json").write_text(json.dumps(adapter), encoding="utf-8")
        (self.root / "bob-extension.json").write_text(json.dumps({
            **adapter, "contextFileName": "BOB.md",
        }), encoding="utf-8")
        (self.root / "BOB.md").write_text("Read [sample-skill](skills/sample-skill/SKILL.md).", encoding="utf-8")

    def symlink(self, path, target, directory=False):
        try:
            path.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlinks unavailable: {exc}")

    def test_complete_package_passes_without_duplicate_root_catalog(self):
        self.assertFalse((self.root / "marketplace.json").exists())
        self.assertEqual(check.check_package(self.root), [])

    def test_portable_package_needs_no_client_catalogs(self):
        shutil.rmtree(self.root / ".agents")
        self.assertEqual(check.check_package(self.root), [])
        (self.root / "skills/sample-skill/SKILL.md").write_text("Invalid", encoding="utf-8")
        self.assertTrue(any("sample-skill" in error for error in check.check_package(self.root)))

    def test_all_client_adapters_pass_and_are_read_only(self):
        self.add_adapters()
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(check.check_package(self.root), [])
        self.assertEqual(before, {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()})

    def test_client_metadata_drift_is_rejected(self):
        self.add_adapters()
        for relative in (".claude-plugin/plugin.json", "gemini-extension.json", "bob-extension.json"):
            path = self.root / relative
            original = path.read_text()
            for key in ("name", "version", "description"):
                with self.subTest(path=relative, key=key):
                    adapter = json.loads(original)
                    adapter[key] = "changed"
                    path.write_text(json.dumps(adapter), encoding="utf-8")
                    self.assertTrue(any(f"{key} must match" in error for error in check.check_package(self.root)))
                    path.write_text(original, encoding="utf-8")

    def test_client_catalogs_must_agree(self):
        self.add_adapters()
        path = self.root / ".claude-plugin/marketplace.json"
        catalog = json.loads(path.read_text())
        catalog["name"] = "different-marketplace"
        path.write_text(json.dumps(catalog), encoding="utf-8")
        self.assertTrue(any("catalogs must name the same" in error for error in check.check_package(self.root)))

    def test_extension_context_must_exist_and_stay_packaged(self):
        self.add_adapters()
        path = self.root / "bob-extension.json"
        original = path.read_text()
        outside = self.base / "outside.md"
        outside.write_text("Outside", encoding="utf-8")
        for target in ("missing.md", "../outside.md", str(outside)):
            with self.subTest(target=target):
                adapter = json.loads(original)
                adapter["contextFileName"] = target
                path.write_text(json.dumps(adapter), encoding="utf-8")
                self.assertTrue(check.check_package(self.root))
        path.write_text(original, encoding="utf-8")
        (self.root / "BOB.md").write_text("Read [missing](missing.md).", encoding="utf-8")
        self.assertTrue(any("missing link target" in error for error in check.check_package(self.root)))

    def test_malformed_or_external_client_adapters_are_rejected(self):
        self.add_adapters()
        for relative in (".claude-plugin/plugin.json", "gemini-extension.json", "bob-extension.json"):
            with self.subTest(path=relative):
                path = self.root / relative
                original = path.read_text()
                path.write_text("[]", encoding="utf-8")
                self.assertTrue(check.check_package(self.root))
                path.unlink()
                outside = self.base / "outside.json"
                outside.write_text(original, encoding="utf-8")
                self.symlink(path, outside)
                self.assertTrue(any("outside" in error for error in check.check_package(self.root)))
                path.unlink()
                path.write_text(original, encoding="utf-8")

    def test_package_check_never_changes_files(self):
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(check.check_package(self.root), [])
        after = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_invalid_json_types_and_missing_catalog_return_errors(self):
        cases = ["{ invalid json", "[]", json.dumps({"name": 123, "plugins": []}),
                 json.dumps({"name": "test-skills", "plugins": "invalid"})]
        for content in cases:
            with self.subTest(content=content):
                self.catalog_path.write_text(content, encoding="utf-8")
                self.assertTrue(check.check_package(self.root))
        self.catalog_path.unlink()
        self.assertTrue(check.check_package(self.root))

    def test_missing_or_non_directory_plugin_source_is_rejected(self):
        for source in ("./absent", "./plugin.json"):
            with self.subTest(source=source):
                self.catalog["plugins"][0]["source"]["path"] = source
                self.save_catalog()
                self.assertTrue(check.check_package(self.root))

    def test_source_escape_is_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.symlink(self.root / "external", outside, directory=True)
        for source in ("./../outside", "./external"):
            with self.subTest(source=source):
                self.catalog["plugins"][0]["source"]["path"] = source
                self.save_catalog()
                self.assertTrue(check.check_package(self.root))

    def test_catalog_directory_and_file_symlinks_cannot_escape(self):
        outside = self.base / "outside"
        (outside / "plugins").mkdir(parents=True)
        target = outside / "plugins/marketplace.json"
        target.write_text(json.dumps(self.catalog), encoding="utf-8")
        self.catalog_path.unlink()
        self.catalog_path.parent.rmdir()
        (self.root / ".agents").rmdir()
        self.symlink(self.root / ".agents", outside, directory=True)
        self.assertTrue(any("outside" in error for error in check.check_package(self.root)))
        (self.root / ".agents").unlink()
        self.catalog_path.parent.mkdir(parents=True)
        self.symlink(self.catalog_path, target)
        self.assertTrue(any("outside" in error for error in check.check_package(self.root)))
        self.assertEqual(json.loads(target.read_text()), self.catalog)

    def test_package_checker_checks_every_skill(self):
        second = self.root / "skills/second-skill"
        second.mkdir()
        (second / "SKILL.md").write_text("invalid skill", encoding="utf-8")
        errors = check.check_package(self.root)
        self.assertTrue(any("second-skill" in error for error in errors))

    def test_plugin_and_catalog_schemas_are_checked(self):
        self.plugin["author"] = 123
        (self.root / "plugin.json").write_text(json.dumps(self.plugin), encoding="utf-8")
        self.assertTrue(any("author" in error for error in check.check_package(self.root)))
        del self.plugin["author"]
        (self.root / "plugin.json").write_text(json.dumps(self.plugin), encoding="utf-8")
        self.catalog["plugins"][0]["policy"]["installation"] = "UNKNOWN"
        self.save_catalog()
        self.assertTrue(any("installation" in error for error in check.check_package(self.root)))

    def test_duplicate_plugin_names_are_rejected(self):
        self.catalog["plugins"].append(dict(self.catalog["plugins"][0]))
        self.save_catalog()
        self.assertTrue(any("duplicate" in error for error in check.check_package(self.root)))

    def test_catalog_and_plugin_names_must_match(self):
        self.catalog["plugins"][0]["name"] = "different-plugin"
        self.save_catalog()
        self.assertTrue(any("does not match" in error for error in check.check_package(self.root)))

    def test_manifest_must_stay_inside_its_plugin(self):
        package = self.root / "nested-plugin"
        package.mkdir()
        self.symlink(package / "plugin.json", self.root / "plugin.json")
        self.catalog["plugins"][0]["source"]["path"] = "./nested-plugin"
        self.save_catalog()
        self.assertTrue(any("outside" in error for error in check.check_package(self.root)))


if __name__ == "__main__":
    unittest.main()
