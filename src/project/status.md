# Current status

*As of Campaign 28 (2026-10-26), research revision `ae6dce06`.*

| Area | Status |
|---|---|
| Stock module certification (strict) | **440 / 458** |
| LieppOS experimental OK | **6 / 458** |
| Hardware validation of any custom image | **0** |
| Custom kernel | `6.1.115-mt6878-gq5012bf1-dev21+` builds from pinned source; **not boot-validated** |
| Kernel + FPSGO/C2PS | `…-dev21-perf1+` builds, 744 modules, strict modpost; acceptance **HOLD** |
| C26/C27 boot package | raw-image package, `PASS_OFFLINE_NON_DEPLOYABLE` |
| C28 Slot-B readiness | **`OFFLINE_PREFLIGHT_FAILED`** — 4 blockers |
| GSI | LineageOS 23.2 / Android 16 on the stock kernel |
| Full-device ROM | Android 15 device tree with **stock** kernel, DTB and DTBO |
| Recovery | OrangeFox Build36 released; overlay model prepared |

## C28 blockers

`slot_b_userspace_capacity` · `slot_b_current_a17_content_incompatible` · `bootloader_boot_hash_vs_chain_unverified` · `source_divergent_modules_runtime`.

## Research line has not been merged

The research repository's integration line is **23 commits ahead of `master`**; C23–C29 and C32 live on `integration/*` branches. This book documents the **C28 baseline** (`ae6dce06`). C29 (`011b9224`) and C32 (`cf36c62a`) are Android 17 Slot-B forensics, both `ANDROID17_OFFLINE_PREFLIGHT_FAILED`; they are experimental, off-roadmap, and never booted. See [Roadmap](roadmap.md) and [Android 17 Slot-B](../android/android17-slot-b.md).

## Kernel build reproducibility

The build engine rebuilt dev21 from committed source and compared it with the independent C21 build:

- effective config, `vmlinux.symvers`, mixed-tree export table, `modules.builtin`, kernel release: **identical**;
- `Module.symvers` (19,759 exports, every CRC): **identical**;
- 732 of 740 same-named modules: identical code and data after removing debug info and build-id;
- the remaining 8 and the kernel image still differ. Full binary equivalence is **not certified**; see [Building](../kernel/building.md#reproducibility).

## What "not boot-validated" means

The gates that cannot pass offline are listed in [Boot chain](../android/boot-chain.md) and [AVB and trust](../android/avb.md): first-stage `modules.load` placement, `dtbo.img`, the trusted board description, bootconfig, AVB/LK acceptance, module signing at runtime and hardware testing.

**Nothing on this site describes a deployable image.**
