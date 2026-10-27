# Source provenance and publication limits

**Owner review required before publication.** This page describes licensing boundaries; it does not grant any redistribution right.

## Kernel history

The board kernel history is shallow at ACK `6b18f0b574ab3267615ae6ce642d5a7c3c21ac09`. All local development commits and dev15–dev21 branches are preserved outside the original directory by an exact Git metadata copy and a Git-native mirror. **Neither mechanism invents missing upstream ancestry.** A bundle alone is not treated as a faithful shallow backup.

## MediaTek / NothingOSS source

Integrated by path in the recorded import. Kernel and vendor notices require review before publication. In particular:

- the imported kernel contains a **donor module-signing private key** — it must never become a real LieppOS release key;
- Mali and connectivity contain confidential/proprietary-marked files;
- MET lacks a complete vendor Git provenance chain;
- the Codex wrapper includes proprietary-marked source and stays private;
- stock firmware, vendor blobs and secure-world binaries have separate redistribution boundaries.

## Known non-Git input

The focaltech firmware include is still absent from the dev21 Git commit because `*.i` is ignored. The build engine restores a declared, hash-pinned historical input; the build is therefore **not** claimed to be wholly reconstructible from Git alone.

## Website policy

This site reproduces **no** firmware, no extracted vendor binaries, no private signing material, no credentials, no device-unique calibration and no raw logs. Key material appears only as SHA-1/SHA-256 identifiers.

Public source candidates are prepared locally, not published. Owner license review and publication authorization remain mandatory.
