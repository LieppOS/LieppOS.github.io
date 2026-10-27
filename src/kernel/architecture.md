# Kernel architecture

The LieppOS kernel is the Android Common Kernel **android14-6.1** (ACK `6b18f0b574ab`, GKI
12901745) merged with the MediaTek MT6878 device-kernel sources and the GQ5012BF1 board
configuration, built as one tree with `CONFIG_MODVERSIONS`, KCFI and strict `modpost`.

```text
kernel/ulefone/gq5012bf1            board kernel: GKI core + MediaTek drivers + board defconfig + DTS
vendor/mediatek/kernel_modules/*    out-of-tree vendor modules, rebuilt against the same kernel output
```

Every module — in-tree and external — is built against **one** kernel identity: the same
`Module.symvers`, generated headers and release string. The build engine refuses to mix modules
from different builds, refuses modpost warnings, and never edits CRCs or vermagic.

## Release identities

| Target | Kernel release |
|---|---|
| dev21 | `6.1.115-mt6878-gq5012bf1-dev21+` |
| dev21 + performance | `6.1.115-mt6878-gq5012bf1-dev21-perf1+` |
| C26 (packaged) | `6.1.115-mt6878-gq5012bf1-c26+` |

## Mixed-tree providers

Two in-tree modules (`mtk-vmm-isp71-regulator`, `mtk-mmdvfs-ccu`) import symbols exported by the
external camera module `mtk_ccuv.ko`. The build follows the owner recipe: build the kernel, run a
strict bootstrap modpost over every other module, build the provider, then run the final strict
modpost with `KBUILD_MIXED_TREE` holding the kernel exports plus the provider exports.
**No CRC is synthesized.**

## Module signing

`CONFIG_MODULE_SIG=y` and `CONFIG_MODULE_SIG_PROTECT=y` are set. Under the GKI rules an unsigned
module cannot export any of the 349 protected exports. The packaged DLKM modules are therefore
signed with the development key named by `CONFIG_MODULE_SIG_KEY`, whose certificate is embedded
in the kernel `Image`. See [DLKM partitions](../android/dlkm.md).

## What this does not prove

An offline build of a closed, signed module set is not a boot. `ufs-mediatek-mod` is
source-divergent and is the critical runtime gate; see [Boot chain](../android/boot-chain.md).
