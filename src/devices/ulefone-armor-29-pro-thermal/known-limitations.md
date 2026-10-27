# Known limitations

Consolidated from the website's C23 baseline and research `docs/known-unknowns.md` @ `ae6dce06`.

## Boot and kernel

- The LieppOS kernel has **never been booted** on the device (hardware validation **0**).
- The trusted board device tree does not yet describe display, touch, charger or thermal-camera
  wiring; pending numeric values stay disabled behind `CONFIG_GQ5012BF1_PENDING_BOARD_DT` (default n).
- `ufs-mediatek-mod` is source-divergent from stock and is the critical first-stage runtime gate.
- `rpmb-mtk.ko` differs from stock at runtime: stock calls `rpmb_get_rw_size`, which no available
  source provides.
- `tmem_ffa.ko` lacks the TrustKernel secure-memory path that stock uses.
- The WLAN module name differs between build recipes (`wlan_drv_gen4m_6878.ko` stock name vs
  `wlan_6878_axi.ko`).
- First-stage inputs (vendor_boot `modules.load`, bootconfig) and the production AVB chain are not
  available; every hardware gate in [AVB and trust](../../android/avb.md) is open.

## Hardware behaviour

- Exact rear-display ioctl/sysfs protocol; touch routing while the main display sleeps; AOD and
  notification behaviour under LieppOS.
- Fingerprint enrollment/authentication and the TrustKernel TA relationship under a full ROM.
- Exact 120 W protocol, cell wiring and reverse-charge ABI.
- Night-vision sensor/illumination mapping (needs a real capture test).
- Consumer IR emitter circuit and measured carrier/pulse waveform; enforcing-SELinux validation.
- Thermal camera device-node transition sequence and any device-unique calibration beyond APK
  assets (unique calibration must never be packaged).
- Work-light, AW2013 RGB and red/blue warning-light control ABI.
- Complete modem/IMS compatibility and NV/calibration ownership map.
- uSmart: maximum current on the 5 V pin, the official pinout drawing, the exact role of each ID
  pin, accessory USB descriptors, and simultaneous Type-C data plus uSmart data.

## Documentation

- Nothing on this site is a deployable image. See [Understanding evidence](../../evidence.md).
- This page is curated; raw evidence and failed experiments remain in the research repository.
