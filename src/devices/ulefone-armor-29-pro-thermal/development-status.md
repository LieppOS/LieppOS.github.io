# Development status

Project-wide numbers are on [Current status](../../project/status.md). Device-specific milestones:

| Milestone | State | Evidence |
|---|---|---|
| Stock module certification (strict) | 440 / 458 | VERIFIED OFFLINE |
| Source-built kernel dev21 | builds, ABI-verified offline | VERIFIED OFFLINE |
| dev21 + FPSGO/C2PS | 744 modules, strict modpost; acceptance **HOLD** | VERIFIED OFFLINE |
| Complete module ABI closure | 470 shipped occurrences, 0 unresolved, 0 CRC mismatch | VERIFIED OFFLINE |
| Stock first-stage UFS reconstruction | 195-module ramdisk payload, stock ordering model | VERIFIED OFFLINE |
| DLKM reconciliation (C27) | `system_dlkm` 60, `vendor_dlkm` 215 | VERIFIED OFFLINE |
| `system_dlkm` contract + signing (C28) | 469/469 loadable; 60/60 signed; stock labels and `etc/` | VERIFIED OFFLINE |
| Slot-B preflight (C28) | **`OFFLINE_PREFLIGHT_FAILED`** | VERIFIED OFFLINE |
| Android device tree | stock kernel profile is the default; dev21 profile is opt-in and fail-closed | SOURCE-LEVEL |
| OrangeFox recovery | Build36 released | VERIFIED (release artifact) |
| Boot of the custom kernel | never attempted | — |

## Milestone history (technical)

1. **Kernel source reconstruction** (C19–C21) — MediaTek source merged onto ACK `6.1`, board
   defconfig and platform DTS, dev21 build.
2. **Unified build infrastructure** (C23) — one build engine, strict modpost, artifact receipts,
   reproducible-source locks.
3. **Performance subsystem** (C24–C25) — FPSGO/C2PS integrated as a subtree plus seven reviewed
   kernel commits; FBT lifecycle and suspend/resume fixes.
4. **Stock boot reconstruction** (C26) — C26 kernel `6.1.115-mt6878-gq5012bf1-c26+`, first-stage
   UFS dependency closure.
5. **DLKM reconciliation** (C27) — vendor/system/odm DLKM images, stage-aware load order, AVB
   validation; verdict `PASS_OFFLINE_NON_DEPLOYABLE`.
6. **Slot-B readiness** (C28) — `system_dlkm` contract restored, GKI module signing, DLKM labels,
   AVB trust model, Slot-B preflight; verdict `OFFLINE_PREFLIGHT_FAILED`.

Each milestone is expanded in the linked pages: [Kernel](../../kernel/architecture.md),
[DLKM partitions](../../android/dlkm.md), [AVB and trust](../../android/avb.md),
[Boot package](../../android/boot-package.md).
