# Source layout

| Path in the kernel repository | Content |
|---|---|
| `arch/arm64/configs/gq5012bf1_defconfig` | complete board configuration (equals the effective `.config`) |
| `arch/arm64/boot/dts/mediatek/mt6878.dts` | platform DTS |
| `arch/arm64/boot/dts/mediatek/gq5012bf1-board.dts` | trusted board overlay (independently authenticated compatibles only) |
| `arch/arm64/boot/dts/mediatek/gq5012bf1-board-pending.dts` | provenance-pending board data; compiled only by an explicit experimental policy and behind `CONFIG_GQ5012BF1_PENDING_BOARD_DT` (default n) |
| `arch/arm64/boot/dts/mediatek/k6878v1_64.dts` | MediaTek reference-board overlay (comparison only) |
| `drivers/misc/mediatek/...` | MediaTek platform drivers |
| `LIEPPOS-*.md` | per-campaign handoffs, ledgers and provenance |

The kernel defconfig and the hardware DTS live in the kernel repository, **never** in the Android
device tree. Android init, SELinux, VINTF, vendor extraction, product and boot-packaging
configuration stay in the device repository.

## Toolchain

Android clang/LLD **17.0.2** (`clang-r487747c`), with recorded binary hashes. pahole 1.32 for BTF.
