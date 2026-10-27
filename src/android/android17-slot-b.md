# Android 17 Slot-B experiment

**EXPERIMENTAL · UNVERIFIED · UNSUPPORTED.** Not a LieppOS product.
Research: `android17-hidl-fixed-build-20261002/` (86 artifacts, 2026-10-02/03),
`DOCS/restructuring/c28/C28-SLOT-B-COMPATIBILITY.md` @ `ae6dce06`.

Android 17 was exercised **only as Slot-B content** for bring-up forensics. It was
never a LieppOS-supported configuration, and it is not on the roadmap.

## What the artifacts record

- An `init_boot` reconstruction with two device-tree patch revisions and a
  generic-ramdisk variant.
- A first-stage mount contract, followed by a series of first-boot failures:
  metadata fix, `dm` resolution, `vendor_b` boundary proof, zygote/adbd service
  resolution, logo hang, and static audits.
- A Slot-B first-boot activation record and a live B bootmode capture.

## What was actually achieved

| Claim | Status |
|---|---|
| A17 Slot-B reached **second-stage init** on 2026-10-03 | **VERIFIED ON DEVICE (historical)** |
| A17 boots to a usable Android interface | **UNVERIFIED** — no such result exists |
| A17 is supported by LieppOS | **NO** |

Reaching second-stage init means early userspace started. It does **not** establish a
working framework, display, radio, or any user-visible function.

## Why it blocks C28

The current Slot-B A17 content **conflicts with the C28 root**: chain keys and
hashtrees differ, and its `vendor_b` lacks the second-stage fstab. It is one of the
two stated C28 blockers.

## Campaign status

C29 (`011b9224`) and C32 (`cf36c62a`) are **Android 17 Slot-B forensics only**, both
`ANDROID17_OFFLINE_PREFLIGHT_FAILED`. C32 resolved SELinux root-cause localisation,
MediaTek AEE contract recovery, framework provenance and linker namespaces; **2 offline
gates remain** (strict SELinux cross-version compatibility and framework reproducible
rebuild). Neither campaign changed Android 17's status: it is experimental,
off-roadmap, and never booted to a usable interface.

Android 15 remains the first custom-kernel integration baseline.

## Related

- [Boot package](boot-package.md) · [AVB and trust](avb.md) · [Partitions](../devices/ulefone-armor-29-pro-thermal/partitions.md)
