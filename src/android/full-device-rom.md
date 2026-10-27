# Full-device Android ROM

The device repository at `device/ulefone/gq5012bf1` is an **Android 15 / LineageOS 22.2-era scaffold**. It is not an Android 16 device port.

## Default remains stock

Its default is `TARGET_PREBUILT_KERNEL := $(DEVICE_PATH)/prebuilt/kernel` with `BOARD_KERNEL_IMAGE_NAME := Image.lz4`, plus the stock DTB and DTBO. Campaign 23 did **not** replace those files.

## The experimental kernel profile

An isolated development branch adds `LIEPPOS_KERNEL_PROFILE=dev21-experimental`. It requires `LIEPPOS_KERNEL_ARTIFACTS` and refuses configuration unless **all** artifact and boot gates pass. Today the mandatory manual boot gates remain blocked; artifact-local JSON assertions cannot authorize deployment.

## Responsibility split

| Belongs to | Content |
|---|---|
| kernel repository | defconfig and hardware DTS |
| device repository | Android init, SELinux, VINTF, vendor extraction, product and boot packaging |

## Status

No full-device ROM build or boot has been performed. **Android 15 remains the first custom-kernel integration baseline**; migration to Android 16 is a separate task and the two are never combined in one checkout.

> A device tree that configures cleanly is not a ROM that boots. See [Boot chain](boot-chain.md) and [Vendor integration](vendor-integration.md).
