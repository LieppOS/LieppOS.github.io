# LieppOS — mdBook wiki

A source-controlled documentation website for **Ulefone Armor 29 Pro Thermal / GQ5012BF1**.

**Website:** `https://lieppos.github.io/` (after publishing)
**Research source:** `https://github.com/LieppOS/LieppOS-ulefone-gq5012bf1-research`

## Deploy to GitHub Pages

1. Create a PUBLIC repository under the `LieppOS` organization called `LieppOS.github.io`.
2. Unzip this project and commit its **contents** (not the containing directory) to `main`.
3. In **Settings > Pages** choose **GitHub Actions** as the deployment source.
4. In **Actions** trigger **Publish LieppOS mdBook**, or push to `main`.
5. Visit `https://lieppos.github.io/` after the workflow succeeds.

**Status: no deployment workflow exists in this checkout.** There is no `.github/workflows/` directory, so the steps above describe an intended setup, not a configured one. `src/` is curated and hand-maintained: `src/SUMMARY.md` and the pages under `src/research/` are tracked source, not generated output. The optional importer writes only to the git-ignored `src/research-archive/`.

Build locally with mdBook **0.5.4**:

```bash
mdbook build      # writes to book/
mdbook serve --open
```

**Note:** The source repository must be publicly cloneable for this workflow. If it is private, use a read-only deploy key or GitHub App credential; do not embed secrets in the repo. The GitHub-side clone could not be executed in the authoring environment, so actual published article count is not verified here.

## Preview locally

Requires mdBook installed ([official instructions](https://rust-lang.github.io/mdBook/guide/installation.html)):

```bash
git clone https://github.com/LieppOS/LieppOS-ulefone-gq5012bf1-research.git /tmp/phone-research
python3 scripts/import_research.py --source /tmp/phone-research
python3 -m unittest discover -s tests -v
mdbook serve --open
```

The importer in `scripts/import_research.py` is an optional helper: it copies allowlisted Markdown from a research checkout into the git-ignored `src/research-archive/` and appends a generated archive section to `src/SUMMARY.md` while preserving the curated head. It is **not** part of a normal build. The curated pages under `src/research/` are hand-written and tracked; research belongs in the **research repository**, never pasted raw into the book.

## Source layout

- `book.toml` — mdBook settings and default dark theme.
- `src/README.md` — site introduction.
- `src/evidence.md` — research validation status guide.
- `src/SUMMARY.md` — curated navigation.
- `src/research/` — curated methodology, provenance, evidence-index and glossary pages (tracked).
- `scripts/import_research.py` — optional public Markdown importer, relative-link rewriting, allowlist.
- `tests/` — importer tests.
- `.gitignore` — excludes `book/`, `src/research-archive/` and Python caches.

## Publishing safeguards

Only root `README.md` and Markdown in `DOCS/`, `docs/`, `reports/`, `hardware/`, `kernel/`, `reverse-engineering/`, `usb-research/`, `slot-b-investigation/` and `slot-b-invalidation/` is copied. Files in `evidence/`, `raw/`, `dumps/`, `private/`, `backups/`, `.git/`, or `workspace/` subdirectories are excluded, along with source files over 1.5 MB. Non-Markdown files are not copied into the site.

**Do a manual privacy review before publishing.** An allowlist does not guarantee that a copied Markdown document contains no private information (serial numbers, tokens, calibration data, logs or personal paths). Relative links to excluded files point back to GitHub, so public links may still reveal already-public content.

GitHub Pages documentation: <https://docs.github.com/en/pages>.
mdBook documentation: <https://rust-lang.github.io/mdBook/>.
