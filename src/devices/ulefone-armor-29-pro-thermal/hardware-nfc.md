# NFC

**VERIFIED ON DEVICE.**
Research: `docs/hardware-map.md`, `hardware/nfc/` @ `ae6dce06`.

## Controller

| Property | Value |
|---|---|
| Part | **ST21NFC** (STMicroelectronics) |
| Bus | I2C, address `6-0008` |
| Firmware | ST vendor firmware (stock binary; not redistributed) |
| Android interface | AIDL NFC service (default instance) |
| Secure element | SIM1 / SIM2 secure-element entries present in the VINTF manifest |

## What is verified

- The controller enumerates at I2C `6-0008` and the stock firmware drives it.
- The AIDL `android.hardware.nfc` default service is present.
- Secure-element entries for SIM1 and SIM2 are declared.
- `st21nfc-dumpsys-after-cycle.txt` exists in the research repository as a raw
diagnostic capture; it is **not** reproduced here.

## What is not verified

- End-to-end card emulation, tag reading and payment flows under a LieppOS build.
- The TrustKernel / secure-element relationship outside stock.
- Firmware update feasibility (see the research `TODO/` notes).

**A declared interface is not a working interface.** Static presence in the VINTF
manifest must not be read as functional NFC.

## Related

- [Hardware](hardware.md) · [Vendor integration](../../android/vendor-integration.md)
