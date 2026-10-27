# Boot package

**VERIFIED OFFLINE. NOT DEPLOYABLE.** C28 verdict: `OFFLINE_PREFLIGHT_FAILED`.
Research: `DOCS/restructuring/c27/LIEPPOS-C27-BOOT-PACKAGE.md`, C28 delivery
receipt and `C28-PACKAGE-VALIDATION.md` @ `ae6dce06`.

## Packages

| | C27 | C28 |
|---|---|---|
| Package id | `c27-20261025` | `c28-20261026` |
| Kernel | `6.1.115-mt6878-gq5012bf1-c26+` | unchanged |
| `vendor_boot` | — | `4d737a96…` |
| `vendor_dlkm` | `80a2e9cc…` | `4f100bb3…` |
| `system_dlkm` | `d3c6ae6d…` | `87ae805d…` |
| `vbmeta` | `b5a14204…` | `39021ec7…` |

Module inventory: `vendor_boot` 195, `system_dlkm` 60, `vendor_dlkm` 215.

## Offline gate table (C28)

| Gate | Status |
|---|---|
| Kernel build | PASS (C26, checksums re-verified) |
| Full module closure | PASS (469/469 loadable, 0 unresolved, 0 CRC mismatch) |
| First-stage UFS | PASS_OFFLINE (stock list order; `ufs-mediatek-mod` source-divergent) |
| Vendor DLKM | PASS |
| System DLKM contract | PASS |
| Effective board DT | PASS_OFFLINE |
| Display / MML | PASS_OFFLINE |
| HBT driver | PASS_OFFLINE |
| AVB descriptor integrity | PASS (13/13 bindings) |
| Partition-size compatibility | PASS (all images fit) |
| **Slot-B userspace compatibility** | **FAIL** |
| Bootloader trust acceptance | UNVERIFIED |
| Google GKI signature acceptance | UNVERIFIED |
| Recovery readiness | PASS_OFFLINE (shared-state capture still required) |
| Hardware boot | **NOT TESTED** |
| Runtime acceptance | **HOLD** |

## Why it failed preflight

1. **Slot-B userspace.** The bound stock Android 15 userspace needs 4,948.9 MiB;
   Slot B holds 2,173.7 MiB (3,664.7 MiB without `scratch`). Fixing this means
   shrinking Slot-A logical partitions — an owner decision.
2. **Current Slot-B content.** The Android 17 experiment conflicts with the C28
   root (chain keys, hashtrees) and its `vendor_b` lacks the second-stage fstab.

## Independent verification

C28 package: PASS (49/49 checks). C27 negative control: FAIL (14), confirming the
verifier detects the defects C28 fixed.

## What a passing offline package still does not mean

Descriptor integrity, module closure and image-size arithmetic are offline
properties. None of them establishes that the bootloader accepts the images or
that Android starts.

> **Hazard:** this package is not flash-ready. See [AVB and trust](avb.md).

## Related

- [Boot chain](boot-chain.md) · [DLKM](dlkm.md) · [Partitions](../devices/ulefone-armor-29-pro-thermal/partitions.md)
