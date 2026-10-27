# Project overview

LieppOS is organised like a LineageOS device project: independent source repositories pinned by one manifest, one build-orchestration engine, and separate repositories for the Android device tree, recovery, research and these docs.

| Responsibility | Owner | Repository |
|---|---|---|
| Board kernel source (defconfig, platform + board DTS) | kernel maintainers | `android_kernel_ulefone_gq5012bf1` (planned) |
| Vendor kernel modules (Mali, camera, imgsensor, connectivity, MET) | kernel maintainers | one repository each (planned) |
| FPSGO/C2PS performance source | performance maintainers | `android_kernel_mediatek_performance` (planned, private) |
| Build orchestration, ABI checks, receipts | build maintainers | `android_build_lieppos` (planned) |
| Android device configuration | device maintainers | [`android_device_ulefone_gq5012bf1`](https://github.com/LieppOS/android_device_ulefone_gq5012bf1) |
| Recovery | recovery maintainers | [`OrangeFox-Ulefone-GQ5012BF1`](https://github.com/LieppOS/OrangeFox-Ulefone-GQ5012BF1) |
| Research and evidence | everyone | [`LieppOS-ulefone-gq5012bf1-research`](https://github.com/LieppOS/LieppOS-ulefone-gq5012bf1-research) |

"Planned" repositories exist locally with their full Git history but have not been published; see [Repositories](repositories.md).

Two independent workflows share the device:

- a **GSI** (LineageOS 23.2 / Android 16, TrebleDroid) on the stock kernel and vendor, and
- a **full-device ROM** (Android 15 / LineageOS 22.2-era device tree) that will eventually use the source-built LieppOS kernel.

They are never combined in one checkout. Start with [Current status](status.md).
