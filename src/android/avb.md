# AVB and trust boundaries

**VERIFIED OFFLINE** (descriptor integrity) · **UNVERIFIED** (bootloader acceptance).
Research: `DOCS/restructuring/c28/C28-AVB-TRUST-MODEL.md`,
`C28-BOOTLOADER-ACCEPTANCE-GATES.md`, `LIEPPOS-C28-AVB-TRUST.md` @ `ae6dce06`.

## Six mechanisms that are easy to conflate

| # | Mechanism | Status |
|---|---|---|
| 1 | **AVB root trust** | Factory root is signed with the **public AOSP `testkey_rsa2048`** (`cdbb7717…`). The C28 root uses the same key, so the root-trust relationship is *identical to stock* |
| 2 | **OEM boot chain** | Key `9d808b09…` signs the stock boot footer. **Not reproduced.** C28 binds `boot` with a root **hash descriptor** over the C26 image instead of the location-3 chain |
| 3 | **Boot-image signature metadata** | Stock `boot.img` is header v4 with `signature_size = 0`, so it has no v4 signature block. The earlier claim that the footer is a confirmed **Google GKI** key is **superseded**: it cannot be confirmed from the images |
| 4 | **Kernel module signing** | 60 GKI modules signed with the C26 kernel's own module key, whose certificate is embedded in the C26 `Image` (see [DLKM](dlkm.md)) |
| 5 | **dm-verity** | Hashtrees present for `system`, `system_ext`, `product`, `odm_dlkm`, `system_dlkm`, `vendor_dlkm`; bring-up on hardware unverified |
| 6 | **Bootloader acceptance** | **UNVERIFIED.** No gate was exercised |

> **A successful AVB verification with a development key is not proof of
> bootloader acceptance.** AVB and the GKI boot-signature mechanism are
> independent; neither replaces the other.

## Observed, not guaranteed

- Stock boots with a root signed by the AOSP test key; the live Slot-A root has
  `flags = 3` and an invalid signature, yet boots — the bootloader appears
  unlocked or permissive.
- Slot-B root `a9d8cd21…` (experiment key `d6b1afef…`) reached Android 17
  second-stage init on 2026-10-03, so LK accepted a non-stock root key.

## Hardware gates (all open)

| # | Gate | Pass criterion |
|---|---|---|
| G1 | Lock state | `ro.boot.verifiedbootstate`, `ro.boot.vbmeta.device_state` |
| G2 | Root with `flags = 0` | LK reaches kernel; `/proc/pl_lk`, pstore |
| G3 | `boot` as root hash descriptor | LK does not require the OEM chain |
| G4 | GKI boot signature | not required (`signature_size = 0`) |
| G5 | Rollback | stored indexes 0/2/4 ≤ 0; location 3 unreferenced |
| G6 | Module signing | no `-EACCES` for the 60 GKI modules |
| G7 | dm-verity | `system_dlkm` / `vendor_dlkm` verity devices appear |
| G8 | First-stage UFS | `ufs-mediatek-mod` probes, `super` appears |

None exercised. **Hardware validation: 0.**

## Rollback

Every C28 rollback index is 0, matching the factory values for locations 0, 2 and
4. Location 3 (boot chain) is no longer referenced. Device-stored rollback values
were not captured offline.

> **Hazard:** do not flash a Slot-B package to a production device. The bound
> stock Android 15 userspace needs 4,948.9 MiB; Slot B offers 2,173.7 MiB. The
> verdict is `OFFLINE_PREFLIGHT_FAILED`.

## Related

- [Boot package](boot-package.md) · [Partition map](../devices/ulefone-armor-29-pro-thermal/partitions.md)
