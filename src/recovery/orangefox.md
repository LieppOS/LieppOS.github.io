# OrangeFox recovery

**VERIFIED (release artifact) · UNVERIFIED (future overlay release).**

The established repository is [OrangeFox-Ulefone-GQ5012BF1](https://github.com/LieppOS/OrangeFox-Ulefone-GQ5012BF1). Campaign 23 left existing releases, checksums, the stock kernel and the historical duplicated `device_tree/` untouched.

## Overlay candidate

The isolated overlay candidate pins device revision `2d9765f5bc60aef39f125b998e1fb4bca67d1b69`, excludes three engineering reports and replaces only the recovery README. `tools/assemble-device-tree.py --verify-release` reconstructs the Build36 device tree with an identical Git tree ID `c58db95bfc7ca6ed4973a90bfc130ffd210f7840`, including file modes.

This pin is **historical by design**: later device commits removed the recovery files. Rebasing recovery to today's device head is a new integration task, not silently part of the overlay conversion.

## Requirements the repository does not provide

- the recorded OrangeFox source-state patches;
- a stock `vendor_boot` template for `tools/vbrepack.py` (an external artifact — the candidate does not produce a recovery image);
- owner redistribution review for the stock security/TA binaries already present in the public repository (their private inventory contains paths and hashes only).

## Packaging safety

Recovery packaging must reconstruct the final 64 MiB `vendor_boot` from the stock PLATFORM fragment, the generated RECOVERY fragment and the stock DTB, then apply and validate AVB. See [Partition map](../devices/ulefone-armor-29-pro-thermal/partitions.md).

> Flashing recovery modifies boot-chain partitions. Do not treat any command on this page as a routine instruction; the AVB and slot-state consequences must be verified first.
