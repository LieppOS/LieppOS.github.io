# Evidence index

Canonical repository: [LieppOS/LieppOS-ulefone-gq5012bf1-research](https://github.com/LieppOS/LieppOS-ulefone-gq5012bf1-research). Do not create a second similarly named repository.

**Documentation source revision: `ae6dce06`** (Campaign 28, 2026-10-26).

## Branch situation

`master` is **23 commits behind** the newest integration line. C23–C29 and C32 are on `integration/*` branches and are **not merged into master**.

- `integration/c28-slot-b-readiness` — `ae6dce06`, the baseline this book documents.
- `integration/c29-android17` — `011b9224`, Android 17 Slot-B integration (`ANDROID17_OFFLINE_PREFLIGHT_FAILED`).
- `integration/c32-android17` — `cf36c62a`, Android 17 gate resolution; 2 offline gates remain (`ANDROID17_OFFLINE_PREFLIGHT_FAILED`).

Campaigns 29 and 32 are **Android 17 Slot-B forensics only**; they are not on the LieppOS roadmap and their images were never booted. Their pages on this site are marked EXPERIMENTAL. No campaign document establishes a hardware boot.

## Evidence paths by campaign

| Path | Evidence |
|---|---|
| `KERNEL-DEVELOPMENT-19/` | C19 build-input and provider findings |
| `KERNEL-DEVELOPMENT-20/` | original C20 branch content, preserved by merge |
| `KERNEL-DEVELOPMENT-21/` | dev21 build, boot boundaries, RPMB and thermal-camera evidence |
| `DOCS/kernel-workspaces/phase11/` | independent builds, C18 reproducibility and C19 ABI verification |
| `DOCS/restructuring/c23/` | source preservation, manifest checkout, builds, licensing and migration records |
| `DOCS/restructuring/c27/` | DLKM reconciliation, load order, boot package, AVB and partitions |
| `DOCS/restructuring/c28/` | Slot-B readiness, `system_dlkm` contract, AVB trust model, acceptance gates |
| `DOCS/restructuring/c29/` | Android 17 Slot-B integration, vendor contract, signing policy (experimental) |
| `DOCS/restructuring/c32/` | Android 17 gate resolution, AEE contract, linker namespaces, capacity (experimental) |
| `reverse-engineering/kernel-source-reconstruction/` | per-driver source reconstruction batches |
| `reverse-engineering/thermal-camera/` | thermal camera, UVC/AC020, internal USB boundary |
| `android17-hidl-fixed-build-20261002/` | Android 17 Slot-B bring-up artifacts (experimental) |
| `slot-b-investigation/`, `slot-b-invalidation/` | Slot-B forensic captures |

## Authoritative local evidence roots

These are references for maintainers, not claims of website availability:

- C22 structural audit: `dk12/staging/audit/c22/C22-LIEPPOS-STRUCTURAL-AUDIT.md`;
- C21 evidence: `dk12/staging/evidence/dev21/`, including `STORAGE-CONTRACT.txt` and `THERMAL-CAMERA.txt`;
- C23 preservation: `$BUILD_ROOT/preservation/c23/`;
- build reports: `$BUILD_ROOT/gq5012bf1/engine/runs/`;
- final build receipts: `$BUILD_ROOT/gq5012bf1/kernel/`.

`$BUILD_ROOT` is a maintainer-local path variable; the concrete host location is deliberately not published.

Security-binary inventories remain private and are not embedded in this book.
