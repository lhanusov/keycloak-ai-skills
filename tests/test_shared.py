"""Verify generated guidance maintenance and standalone skill relocation."""

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("sync_shared", ROOT / "scripts/sync-shared.py")
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
spec = importlib.util.spec_from_file_location("validate_skill", ROOT / "skills/add-skill/scripts/validate_skill.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SharedTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "shared", self.root / "shared")
        (self.root / "AGENTS.md").write_text("# Repository guidance\n\nRead README.md.\n", encoding="utf-8")

    def test_check_is_read_only_and_write_repairs_missing_and_stale_copies(self):
        self.assertTrue(shared.sync(self.root))
        self.assertFalse((self.root / "skills").exists())
        self.assertEqual(shared.sync(self.root, write=True), [])
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(shared.sync(self.root), [])
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        source = self.root / "shared/evidence.md"
        source.write_text(source.read_text() + "\nNew guidance.\n", encoding="utf-8")
        self.assertEqual(len(shared.sync(self.root)), len(shared.CONSUMERS["evidence.md"]))
        self.assertEqual(shared.sync(self.root, write=True), [])
        self.assertEqual(shared.sync(self.root), [])

    def test_missing_source_is_reported(self):
        for relative in ("shared/evidence.md", "AGENTS.md"):
            with self.subTest(source=relative):
                (self.root / relative).unlink()
                self.assertTrue(any(str(Path(relative)) in e for e in shared.sync(self.root, write=True)))

    def test_copilot_copy_is_checked_and_refreshed_from_repository_guidance(self):
        source = self.root / "AGENTS.md"
        target = self.root / ".github/copilot-instructions.md"
        errors = shared.sync(self.root)
        self.assertTrue(any(str(target.relative_to(self.root)) in error for error in errors))
        self.assertFalse(target.exists())

        self.assertEqual(shared.sync(self.root, write=True), [])
        original = target.read_bytes()
        self.assertTrue(original.endswith(source.read_bytes()))
        source.write_text("# Updated guidance\n\nRun the documented checks.\n", encoding="utf-8")
        errors = shared.sync(self.root)
        self.assertEqual(len(errors), 1)
        self.assertIn(str(target.relative_to(self.root)), errors[0])
        self.assertEqual(target.read_bytes(), original)

        self.assertEqual(shared.sync(self.root, write=True), [])
        self.assertTrue(target.read_bytes().endswith(source.read_bytes()))
        self.assertEqual(shared.sync(self.root), [])

    def test_collection_has_current_copies(self):
        self.assertEqual(shared.sync(ROOT), [])

    def test_symlinked_ancestors_cannot_read_or_write_outside_the_repository(self):
        for index, relative in enumerate(("shared", "skills", "skills/triage-bug", ".github")):
            with self.subTest(path=relative):
                package = self.root / f"package-{index}"
                outside = self.root / f"outside-{index}"
                shutil.copytree(ROOT / "shared", package / "shared")
                shutil.copyfile(self.root / "AGENTS.md", package / "AGENTS.md")
                outside.mkdir()
                link = package / relative
                link.parent.mkdir(parents=True, exist_ok=True)
                if link.exists():
                    shutil.rmtree(link)
                try:
                    link.symlink_to(outside, target_is_directory=True)
                except (OSError, NotImplementedError) as exc:
                    self.skipTest(f"symlinks unavailable: {exc}")
                for name in shared.CONSUMERS:
                    (outside / name).write_text("Outside repository\n", encoding="utf-8")
                before = {p: p.read_bytes() for p in outside.rglob("*") if p.is_file()}
                for write in (False, True):
                    errors = shared.sync(package, write=write)
                    self.assertTrue(any("outside the repository" in e for e in errors))
                    self.assertEqual(before, {p: p.read_bytes() for p in outside.rglob("*") if p.is_file()})
                if relative == "shared":
                    self.assertFalse((package / "skills").exists())

    def test_skills_relocate_without_shared_source_or_sibling_skills(self):
        for skill in sorted((ROOT / "skills").iterdir()):
            if not skill.is_dir():
                continue
            name = skill.name
            with self.subTest(skill=name), tempfile.TemporaryDirectory() as standalone:
                target = Path(standalone) / name
                shutil.copytree(skill, target)
                self.assertEqual(validator.validate(target), [])


if __name__ == "__main__":
    unittest.main()
