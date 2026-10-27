# Vendor integration

`android_vendor_ulefone_gq5012bf1` is **planned**, not an available published repository. The device scaffold's extraction scripts and `proprietary-files.txt` describe its inputs; they do **not** grant redistribution rights.

The source manifest leaves this vendor project out until authorized extraction, provenance and licensing review are complete. Firmware, secure-world binaries and proprietary HALs are not copied into new public source candidates or into this book.

## Requirements before a full ROM can be accepted

- matching vendor/odm HAL and VINTF manifests;
- init service, uevent and SELinux policy relationships;
- first-stage kernel-module placement and load order;
- verified bootconfig and AVB chain;
- an actual full-device Android build and independently authorized boot validation.

The Android 16 GSI's separate `vendor/lieppos` customization is **not** the device's proprietary vendor tree.

> Declared interfaces (HAL entries, VINTF manifests, SELinux types) are static facts. They are not evidence that a service runs. See [Understanding evidence](../evidence.md).
