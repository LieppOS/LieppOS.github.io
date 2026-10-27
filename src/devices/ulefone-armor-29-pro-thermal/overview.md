# Ulefone Armor 29 Pro Thermal

| | |
|---|---|
| Board | **GQ5012BF1** |
| SoC | MediaTek **MT6878T** (kernel strings say `mt6878`) |
| Stock kernel | `6.1.115-android14-11-g945dff7bc1bf` (GKI, android14-6.1) |
| Boot image | header v4, `Image.lz4`, A/B |
| Storage | UFS; the MediaTek host driver is a **module** (`ufs-mediatek-mod`) |
| Dynamic partitions | `super`, LP metadata 10.2, Virtual A/B |
| Special hardware | thermal camera (USB UVC module), secondary rear display, uSmart port |
| Verification baseline | Campaign 28, research revision `ae6dce06` |

## Pages

- [Hardware](hardware.md) — identified blocks with evidence labels
- [Partition map](partitions.md) — `super`, A/B layout and Slot-B capacity
- [NFC](hardware-nfc.md) — ST21NFC transport
- [USB and uSmart](hardware-usmart.md) — shared USB fabric and accessory port
- [Known limitations](known-limitations.md) — what is still unknown
- [Development status](development-status.md) — milestones and gates

## Important

The LieppOS custom kernel has **never been booted** on this device. Hardware validation is **0**.
Everything in the hardware pages that is labelled VERIFIED was observed on **stock** firmware.
A capability existing in stock does not prove it works under a LieppOS build.

Manufacturer marketing names (Dimensity 7400, Mali-G615 MC2, "uSmart 2.0", "ThermoVue Pro") are
reported as marketing names, not as independently verified electrical facts.
