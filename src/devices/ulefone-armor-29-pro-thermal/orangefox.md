# OrangeFox recovery

Unofficial [OrangeFox](https://github.com/LieppOS/OrangeFox-Ulefone-GQ5012BF1) 14.1 for this device. Current release: **Build36**.

| | |
|---|---|
| Device | Ulefone Armor 29 Pro Thermal (`GQ5012BF1`) |
| SoC | MediaTek MT6878 |
| Boot layout | A/B with Virtual A/B |
| Recovery location | `vendor_boot` v4 |
| Built against | Android 15 stock, tested with an Android 16 GSI |

There is **no standalone recovery partition**. OrangeFox lives inside `vendor_boot_a`, which is
why the image is exactly 64 MiB and why flashing it touches the boot chain.

## What works

Confirmed on hardware across Build34 and Build36.

| Feature | Status | Notes |
|---|---|---|
| Boot | Working | |
| Touch | Working | Confirmed on hardware |
| Display and orientation | Working | |
| Brightness | Partly | Backlight node verified; UI slider never moved |
| Vibration | Working | |
| SELinux | Working | Enforcing, no functional denials |
| ADB | Working | Shell, push, pull |
| MTP | Working | Added in Build34; browsable from a Linux host |
| Fastbootd | Working | |
| FBE decryption | Working | One PIN, no ADB intervention |
| PIN decryption | Working | |
| Internal storage | Working | |
| External SD / exFAT | Working | |
| Battery percentage | Working | Live updates, correct charging state |
| Charging status | Working | |
| Battery temperature | Working | |
| Dynamic partition mounts | Working | |
| Slot detection | Working | |
| Backup | Working | 64 MB `boot` backup, digest generated |
| RTC / logs | Working | |
| Reboot to recovery | Working | |

## What is not confirmed

Nothing here is known broken. It has simply not been exercised, so treat it as unknown
rather than as working.

| Feature | Status | Notes |
|---|---|---|
| USB OTG | Untested | No adapter ever attached; fstab entries exist |
| ADB sideload | Untested | Transport never exercised |
| Brightness slider | Untested | Node works; UI control never used |
| Screenshot | Untested | Never triggered |
| Restore | Untested | Backup is verified; restore is not |
| Reboot to system | Untested | |
| Reboot to bootloader | Untested | |
| Power off | Untested | |
| Zip / package flashing | Untested | Never in scope during bring-up |
| Magisk installation | Untested | Never in scope |
| Decrypted `/data` backup and restore | Untested | Never in scope |
| Theming | Untested | Never in scope |
| Wipe and format | Untested | Mappings audited; nothing was ever formatted |

> The upstream README lists the system, bootloader and power-off reboot targets as working.
> `docs/TODO.md` states only recovery and fastbootd were ever exercised. The more conservative
> claim is used here.

## Flashing

> **Warning:** flashing recovery overwrites `vendor_boot_a` and changes the boot chain. Verify
the SHA256 checksum, confirm the active slot, and make sure you can restore the stock image
first. This is not a routine operation.

```bash
adb reboot fastboot
fastboot devices
fastboot flash vendor_boot_a vendor_boot_a-orangefox-FULL64M-BUILD36.img
```

Recovery packaging rebuilds the final 64 MiB `vendor_boot` from the stock PLATFORM fragment,
the generated RECOVERY fragment and the stock DTB, then applies and validates AVB. See
[Partition map](partitions.md).

## Build provenance

Build36 (commit `7976adc`) is the current release. Build34 (`66f5e8c`) is the previous
known-good image at sha256
`c5da1ec87979f09579eb45ba73b5c3d53edccb436297d32cfad71edd6c7272c4`, differing from Build32
(`52d2f09`) only by the addition of MTP.

An isolated overlay candidate pins device revision `2d9765f5bc60aef39f125b998e1fb4bca67d1b69`
and reconstructs the Build36 device tree with Git tree ID
`c58db95bfc7ca6ed4973a90bfc130ffd210f7840`. That pin is deliberately historical: later device
commits removed the recovery files, so rebasing recovery onto today's device head is a separate
integration task.

## Open items

The repository does not yet provide the recorded OrangeFox source-state patches, a stock
`vendor_boot` template for `tools/vbrepack.py`, or an owner redistribution review for the stock
security and TA binaries it contains.
