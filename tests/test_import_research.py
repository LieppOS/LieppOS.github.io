from pathlib import Path
import tempfile
import unittest
from scripts.import_research import import_repo, rewrite_links, collect


class ImportResearchTests(unittest.TestCase):
    def test_collect_allowlist_and_excludes_private_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ["README.md", "kernel/report.md", "kernel/evidence/secret.md", "evidence/raw.md", "reports/a.md"]:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("# Note\n")
            files = collect(root)
            self.assertEqual(set(p.as_posix() for p in files), {"README.md", "kernel/report.md", "reports/a.md"})

    def test_rewrites_links_and_preserves_fenced_code(self):
        text = "[Next](../reports/next.md#result) ![plot](fig.png)\n```md\n[Next](../reports/next.md)\n```\n"
        result = rewrite_links(text, Path("kernel/report.md"), {Path("kernel/report.md"), Path("reports/next.md")}, "abc123")
        self.assertIn("[Next](../reports/next.md#result)", result)
        self.assertIn("![plot](https://raw.githubusercontent.com/LieppOS/LieppOS-ulefone-gq5012bf1-research/abc123/kernel/fig.png)", result)
        self.assertIn("```md\n[Next](../reports/next.md)\n```", result)

    def test_import_preserves_curated_summary_head(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, dest = root / "input", root / "src"
            (source / "kernel").mkdir(parents=True)
            dest.mkdir()
            (source / "README.md").write_text("# Main Research\n")
            (source / "kernel" / "first.md").write_text("# Kernel\n")
            curated = "# Summary\n\n[Intro](README.md)\n\n- [Glossary](research/glossary.md)\n"
            (dest / "SUMMARY.md").write_text(curated)
            import_repo(source, dest)
            import_repo(source, dest)  # second run must not stack archives
            summary = (dest / "SUMMARY.md").read_text()
            self.assertEqual(summary.count("# Research archive"), 1)
            self.assertIn("[Glossary](research/glossary.md)", summary)

    def test_import_generates_navigable_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, dest = root / "input", root / "src"
            (source / "kernel").mkdir(parents=True)
            dest.mkdir()
            (source / "README.md").write_text("# Main Research\n")
            (source / "kernel" / "first.md").write_text("# Kernel Investigation\n")
            n = import_repo(source, dest)
            self.assertEqual(n, 2)
            summary = (dest / "SUMMARY.md").read_text()
            self.assertIn("research-archive/README.md", summary)
            self.assertIn("research-archive/kernel/first.md", summary)
            self.assertTrue((dest / "research-archive/kernel/first.md").exists())

if __name__ == "__main__":
    unittest.main()
