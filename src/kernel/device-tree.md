# Device tree

| File | Trust | Packaged |
|---|---|---|
| `mt6878.dtb` | platform base, trusted | yes |
| `gq5012bf1-board.dtbo` | trusted board overlay | yes |
| `gq5012bf1-board-pending.dtbo` | **provenance pending** | never (experimental policy only) |
| `k6878v1_64.dtbo` | MediaTek reference board | comparison only |

Pending GPIO, regulator, bus, charging and display values are **not** enabled to make the tree look
complete. The trusted description is incomplete, which is one of the boot gates.

The engine's dev21 DTB and trusted DTBO are byte-identical to the C21 build (`b3250992…`,
`e9896d33…`).

## DTBO partition

The DTBO partition image is a separate artifact from the DTBs the kernel build emits. The
device-scaffold DTBO table layout, IDs and stock contract still need verification; the boot
package ships the stock `dtbo.img` (`9092967872d1362c45a18d62a83360b742eed58aafa4b0c15043ef159ae042d3`)
unchanged.

> Compiling a DTBO is not the same as the bootloader accepting the overlay table. See
> [AVB and trust](../android/avb.md).
