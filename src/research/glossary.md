# Glossary

Terms used across this site. See [Understanding evidence](../evidence.md) for the
evidence labels.

## Device and platform

| Term | Meaning |
|---|---|
| **GQ5012BF1** | Ulefone product / board identifier for the Armor 29 Pro Thermal |
| **MT6878T** | MediaTek platform variant; kernel strings say `mt6878` |
| **Dimensity 7400** | Marketing name for this SoC (not Dimensity 8300) |
| **Mali-G615 MC2** | GPU in this device (2 cores, not MP6) |
| **Connsys** | MediaTek connectivity subsystem (Wi-Fi/BT/GNSS/FM) |
| **MT6637** | Connectivity combo chip (`ADIE6637`) |

## Android and boot

| Term | Meaning |
|---|---|
| **AVB** | Android Verified Boot: root/chain signatures, rollback index, hashtrees |
| **GKI** | Generic Kernel Image; a stable kernel ABI shared across devices |
| **ACK** | Android Common Kernel |
| **DLKM** | Dynamically loadable kernel module |
| **`vendor_boot`** | Boot partition carrying the vendor ramdisk (first-stage modules) |
| **`init_boot`** | Partition carrying the generic ramdisk in GKI devices |
| **DTBO** | Device-tree blob overlay partition |
| **hashtree** | dm-verity Merkle tree descriptor in vbmeta |
| **chain descriptor** | vbmeta entry delegating to another signed vbmeta |
| **hash descriptor** | vbmeta entry binding an image by digest, no delegated key |
| **rollback index** | Monotonic counter preventing firmware downgrade |
| **Virtual A/B** | A/B scheme where slot B lives inside `super` as snapshots |

## Kernel build

| Term | Meaning |
|---|---|
| **modpost** | Kbuild stage that checks symbol references and CRCs |
| **strict modpost** | Build fails on any modpost warning |
| **`Module.symvers`** | Exported symbol + CRC table used to link modules |
| **vermagic** | Kernel version/ABI string a module must match to load |
| **CRC** | Symbol version checksum; a mismatch prevents loading |
| **mixed tree** | Build where some modules provide symbols to in-tree modules |
| **KCFI** | Kernel Control Flow Integrity |
| **ABI closure** | Every shipped module's imports resolve within the package |

## Measurements

| Term | Meaning |
|---|---|
| **identity** | A distinct module, counted once |
| **partition occurrence** | A module file as placed in a partition; duplicates counted separately |
| **loadable** | Module whose imports and CRCs resolve; not proof it loads |

## Project

| Term | Meaning |
|---|---|
| **Campaign (Cxx)** | A numbered research/engineering work period |
| **C28** | Latest campaign merged into this book's baseline (`OFFLINE_PREFLIGHT_FAILED`) |
| **C29** | Android 17 Slot-B integration, `011b9224` — experimental, not a LieppOS target |
| **C32** | Android 17 gate resolution, `cf36c62a` — experimental; 2 offline gates remain |
| **LieppOS** | The custom Android/kernel effort for this device |
