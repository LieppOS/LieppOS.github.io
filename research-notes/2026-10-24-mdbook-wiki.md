# LieppOS mdBook research publishing decision — 2026-10-24

The user selected **mdBook** as the website/wiki framework for Ulefone Armor 29 Pro Thermal (GQ5012BF1) research.

- Primary phone research source: `LieppOS/LieppOS-ulefone-gq5012bf1-research` (confirm repository name before committing anything).
- Planned site repository: `LieppOS/LieppOS.github.io` (GitHub Pages root domain).
- Keep primary observations, findings, logs, and corrections in the research repository, not in the mdBook generated output.
- Publish reviewed allowlisted Markdown as structured chapters, with each imported page linking back to the original research revision.
- Protect raw partition dumps, evidence binaries, private records and large artifacts from website publication; manually audit Markdown for sensitive content.
- Document validation statuses faithfully: IDENTIFIED, CONFIGURED, BUILD-VALIDATED, RUNTIME-VALIDATED, UNKNOWN.

Website implementation is packaged separately and is not a claim that the GitHub organization, domain, or GitHub Actions deployments are already configured. This decision note is intended for the research repository and has **not been committed there**.
