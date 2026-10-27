# Partition map

**VERIFIED ON DEVICE** (stock captures) and **VERIFIED OFFLINE** (image geometry). Sources:
research `docs/partition-map.md`, `C28-SLOT-B-COMPATIBILITY.md` @ `ae6dce06`.

## Verified layout

- A/B **and** Virtual A/B are enabled.
- Dynamic partitions live in `super`; LP metadata version **10.2**, `virtual_ab_device` flag set.
- `super` size: **9,663,676,416 B**. Groups `main_a` and `main_b` each allow at most
  **9,661,579,264 B**.
- Logical partitions: `system`, `system_ext`, `product`, `vendor`, `system_dlkm`,
  `vendor_dlkm`, `odm_dlkm`. Stock logical filesystems are **EROFS**.
- Boot-chain partitions: `boot`, `init_boot`, `vendor_boot`, `dtbo`, `vbmeta`,
  `vbmeta_system`, `vbmeta_vendor`.
- `vendor_boot` is **header v4, 64 MiB**, with a PLATFORM fragment, a type-2 RECOVERY fragment
  and the wrapped DTB.
- `metadata` and `userdata` are F2FS; userdata uses
  `aes-256-xts:aes-256-cts:v2+inlinecrypt_optimized` with metadata keys under
  `/metadata/vold/metadata_encryption`.

```text
super  9,663,676,416 B
├── main_a   max 9,661,579,264 B
└── main_b   max 9,661,579,264 B
```

## Slot-B capacity (verified offline)

The current Slot-B dynamic partitions hold an **Android 17 experiment**, much smaller than the
stock Android 15 userspace the C28 root `vbmeta` is bound to:

| Requirement | MiB |
|---|---:|
| Stock A15 Slot-B userspace (`system`, `system_ext`, `product`, `vendor`, `odm_dlkm`, `vendor_dlkm`, `system_dlkm`) | 4,948.9 |
| Space available to Slot B while keeping Slot A and `scratch` | 2,173.7 |
| Space available if `scratch` were deleted | 3,664.7 |

`super` free space is only **64.45 MiB**, at the tail, with no holes. Fitting the stock userspace
would require shrinking Slot-A logical partitions — out of scope and prohibited without owner
approval. See [AVB and trust](../../android/avb.md) and the [boot package](../../android/boot-package.md).

## Per-partition sizes (Slot B, verified offline)

| Partition | Kind | Allocated |
|---|---|---:|
| `boot_b` | physical | 64 MiB |
| `init_boot_b` | physical | 8 MiB |
| `vendor_boot_b` | physical | 64 MiB |
| `dtbo_b` | physical | 8 MiB |
| `vbmeta_b` | physical | 8 MiB |
| `system_dlkm_b` | logical | 7,471,104 B |
| `vendor_dlkm_b` | logical | 17,534,976 B |
| `odm_dlkm_b` | logical | 348,160 B |
| `system_b` | logical | 665,391,104 B (A17 experiment) |
| `system_ext_b` | logical | 366,891,008 B (A17 experiment) |
| `product_b` | logical | 337,686,528 B (A17 experiment) |
| `vendor_b` | logical | 816,349,184 B (A17 experiment) |

## Shared state — a Slot-B test is not risk-free for Slot A

| Shared | What |
|---|---|
| `super` metadata | one LP metadata set (3 slots); any resize rewrites it |
| `misc` | BCB at 0, `bootloader_control` at 0x800 |
| `/metadata` | FBE key directory, `aconfig`, bootstat, OTA state |
| `/data` | one FBE volume; booting another Android version may upgrade it irreversibly |
| Protected state | `nvdata`, `nvcfg`, `protect1`/`protect2`, `persist`, `nvram`, RPMB rollback storage |

## Safety invariant for recovery packaging

Recovery packaging must reconstruct the final 64 MiB `vendor_boot` from the stock PLATFORM
fragment, the generated RECOVERY fragment and the stock DTB, then apply and validate AVB.
The raw build output is **not** automatically flash-safe.

## UNKNOWN

- Final OTA payload generation and snapshot-merge behaviour (never build- or hardware-tested).
- Production AVB signing policy — an owner release decision. Stock keys must never be fabricated
  or redistributed.
