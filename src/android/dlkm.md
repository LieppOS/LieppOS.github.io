# DLKM partitions

**VERIFIED OFFLINE.** Not booted. No module has been loaded on hardware.
Research: `DOCS/restructuring/c27/LIEPPOS-C27-{VENDOR,SYSTEM}-DLKM.md`,
`C28-SYSTEM-DLKM-CONTRACT.md`, `docs/module-map.md` @ `ae6dce06`.

## Contract

| Partition | Modules | Image size |
|---|---:|---:|
| `vendor_boot` (platform ramdisk) | 195 | 64 MiB partition |
| `system_dlkm` | 60 | 7,471,104 B EROFS |
| `vendor_dlkm` | 215 | 17,534,976 B EROFS |

## How the counts relate

These numbers are different measurements, not contradictions:

| Figure | Meaning |
|---|---|
| **457** | unique stock module **identities** |
| **471** | stock **partition occurrences** = 457 + 14 duplicates |
| **456** | identities **rebuilt** loadable (`hbt.ko`, `gzvm.ko` recovered in C27) |
| **1** | **built-in**: `timer-mediatek` (`CONFIG_MTK_TIMER=y`), `.ko` deliberately not shipped |
| **470** | **shipped** occurrences = 195 + 60 + 215 (= 471 − 1) |
| **469** | **loadable**: `vendor_dlkm/bluetooth.ko` is shadowed by the signed `system_dlkm` copy, as on stock |

The 14 duplicates are stock behaviour: 13 modules ship in both `vendor_boot` and
`vendor_dlkm` (`reboot-mode`, `syscon-reboot-mode`, `spmi-mtk-mpu`, the three
`mtk_*_throttling` modules, `mtk_pbm`, `mtk_mdpm`, `mtk_rpmsg_mbox`, `mtk-mbox`,
`mtk_tinysys_ipi`, `mtk-mmdvfs-v3-start`, `yft_devinfo`), plus `bluetooth.ko` in
both `vendor_dlkm` and `system_dlkm`.

## C28 fixes that made the package coherent

1. **GKI module signatures.** The C26 kernel sets `CONFIG_MODULE_SIG_PROTECT=y`.
   C27 shipped all 60 GKI modules unsigned; 25 export protected symbols, leaving
   **58 unloadable** (incl. `cfg80211`, `mac80211`, `wlan_drv_gen4m_6878`,
   `bt_drv_6878`, `bluetooth`). C28 signed them with the C26 kernel's own module
   key. Stock signs 60/60.
2. **SELinux labels.** C27 images carried no xattrs, so 299 inodes were
   `unlabeled` and `init_insmod_sh` `module_load` was denied (neverallow). Fixed
   with `mkfs.erofs --file-contexts` using the AOSP lines.
3. **`system_dlkm` etc/.** Stock `etc/` (4 files) and the stock UUID restored.

## Load closure

195 / 60 / 215, **470 occurrences, 0 unresolved, 0 CRC mismatch**, 0 duplicate
exports. First-stage UFS order is the stock list minus the now-built-in
`timer-mediatek`:

```
aee_aed -> irq-dbg -> mrdump -> ufs-mediatek-dbg -> blocktag -> rpmb -> ufs-mediatek-mod
```

This is **one valid topological order, not an authenticated `modules.load`**.
Placement before UFS mounts stays **UNKNOWN** without an authorized vendor_boot
ramdisk.

## Unplaced modules (C28 review)

205 built modules are not shipped, classified as: 97 unused (evidenced), 87
unknown (no OF binding; userspace use cannot be excluded offline), 9 optional
(stock ships no provider), 8 incompatible (other SoCs), 4 test-only.
**Required: 0. Placement changes: 0.** Binding an optional pump-express algorithm
would change charging current and needs owner and hardware evidence.

## What this does not prove

Closure and ordering do not prove Android boot, verity bring-up, or that any
driver binds. `ufs-mediatek-mod` is source-divergent and is the critical runtime
gate.

## Related

- [Boot package](boot-package.md) · [AVB and trust](avb.md) · [External modules](../kernel/external-modules.md)
