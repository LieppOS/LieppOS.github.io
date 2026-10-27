# Android boot chain: independent gates

An offline kernel build does not establish Android bootability. Each layer below is a separate
check with its own evidence class.

| Layer | Verified or missing |
|---|---|
| Raw ARM64 `Image` | source-built (C23/C26) |
| `Image.lz4` | LZ4 legacy framing and decompression roundtrip verified; follows Kbuild's `lz4 -l -12 --favor-decSpeed` |
| boot header | device scaffold records stock header v4; not independently validated as a new boot image |
| platform DTB / trusted overlay | source-built, hashes equal the C21 evidence |
| DTBO partition image | **not produced**; table layout, IDs and stock contract remain to be verified (stock `dtbo.img` shipped unchanged) |
| vendor ramdisk | authorized `vendor_boot`, `modules.load`, first-stage placement and bootconfig missing |
| trusted board description | incomplete; pending wiring stays disabled |
| AVB | project keys and a verified chain absent; see [AVB and trust](avb.md) |
| module signing | packaged modules signed with the development key; runtime acceptance unverified |
| hardware | not tested |

## UFS first-stage dependency requirement

`CONFIG_SCSI_UFSHCD=y` and platform glue are built in, but the MediaTek host is
`ufs-mediatek-mod.ko`. Its built-module dependency closure, ordered before the consumer, is:

```text
aee_aed -> irq-dbg -> mrdump -> ufs-mediatek-dbg -> blocktag -> rpmb -> ufs-mediatek-mod
```

This is **one valid topological order, not an authenticated `modules.load` list**. The seven
modules exist with matching vermagic. Without authorized vendor-ramdisk evidence their early
availability and placement remain **UNKNOWN**. A module only present in later `vendor_dlkm`
cannot be assumed available before UFS is mounted.

## Three-stage module load order

| Order | Stage | Mechanism | Mount point |
|---:|---|---|---|
| 1 | `vendor_boot` platform ramdisk | first-stage init / libmodprobe | ramdisk |
| 2 | `system_dlkm` | `init.insmod.sh` loop, first entry | `/system_dlkm/lib/modules` |
| 3 | `vendor_dlkm` | same loop, second entry | `/vendor_dlkm/lib/modules` |
| 4 | init triggers | `insmod` / `modprobe -a -d` in vendor rc files | after `post-fs-data` / `boot` |

`system_dlkm` must load before `vendor_dlkm`: `vendor_dlkm`'s `bluetooth`, `cfg80211` and
`mac80211` consume `rfkill` symbols exported by `system_dlkm`. Details in [DLKM partitions](dlkm.md).

## What is still separate

Link closure, first-stage placement and runtime behaviour are three different checks. Closing
`rpmb`'s symbols does not reconstruct stock RPMB transfer-sizing behaviour, and a closed module
set does not prove Android starts.

> **Hazard:** do not treat this chain as a flashing procedure. See [Boot package](boot-package.md)
> for why the current package is not deployable.
