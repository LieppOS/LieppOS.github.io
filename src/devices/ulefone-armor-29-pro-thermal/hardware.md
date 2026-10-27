# Hardware

**VERIFIED ON DEVICE** means observed on stock firmware; **VERIFIED OFFLINE** means established
from authenticated images or captures; **UNKNOWN** means not established. Research source:
`docs/hardware-map.md` @ `ae6dce06`.

Only authenticated facts appear here. Board wiring that is not yet authenticated stays in the
kernel's *provenance-pending* device tree (disabled by default, `CONFIG_GQ5012BF1_PENDING_BOARD_DT=n`)
and is **not** presented as fact.

## Platform

| Block | Detail | Status |
|---|---|---|
| SoC | MediaTek MT6878 (MT6878T), arm64 | VERIFIED ON DEVICE |
| Storage | UFS; host driver is the module `ufs-mediatek-mod` | VERIFIED ON DEVICE |
| Platform DTS | `arch/arm64/boot/dts/mediatek/mt6878.dts` | SOURCE-LEVEL |
| Trusted execution | TrustKernel (tkcore) + GenieZone; secure-world binaries are stock and never redistributed | VERIFIED ON DEVICE |

## Display and touch

| Block | Detail | Status |
|---|---|---|
| Main panel | `yft-lcm-vtdr6115-drv`, DSI/DRM `card0-DSI-1`, 1080×2400, 60/90/120 Hz, density 480 | VERIFIED ON DEVICE |
| Main touch | FocalTech FT3680 on SPI3 (`fts_ts`), 10 slots | VERIFIED ON DEVICE |
| Rear display | SPI0 `spi_tiny_lcd_co5300` (`spi_tiny_co5300_lcd.ko`), `/sys/class/misc/tiny_lcd_miscdev` | VERIFIED components |
| Rear touch | Hynitron `hyn_ts`, I2C 0-0015, 340×340, one tracking ID | VERIFIED ON DEVICE |
| Rear-display architecture | vendor-managed misc framebuffer, **not** a second SurfaceFlinger/HWC display | STRONG INFERENCE |

## Cameras

Four Camera2 IDs, all `MIPI_RAW` (research `docs/camera-thermal.md`):

| ID | Facing | Sensor driver | Flash |
|---:|---|---|---|
| 0 | Back | `SENSOR_DRVNAME_IMX989_MIPI_RAW` | yes |
| 1 | Front | `SENSOR_DRVNAME_S5KJN1_MIPI_RAW` | no |
| 2 | Back | `SENSOR_DRVNAME_S5KJN1MAIN2_MIPI_RAW` | yes |
| 3 | Back | `SENSOR_DRVNAME_OV64B_MIPI_RAW` | yes |

The stock snapshot also proves four `imgsensor` I2C bindings, EEPROM devices, VCM/OIS devices and
AW36515/AW36518-family illumination drivers. Which rear sensor is marketed as "night vision"
needs a real capture/illumination test — sensor enumeration alone is not enough.

The thermal camera is **separate** from these four devices: a USB UVC module on the shared USB
fabric. See [USB and uSmart](hardware-usmart.md).

## Other identified hardware

| Block | Detail | Status |
|---|---|---|
| NFC | ST21NFC, I2C 6-0008, AIDL NFC service | VERIFIED ON DEVICE |
| Fingerprint | SPI1 `madev`, `microarray_fp_tee`, `/dev/madev0`, `/dev/tkcore_fp` | transport VERIFIED; auth UNKNOWN |
| Sensors | ICM4N607 accel/gyro, MMC5603 mag, STK3A5X ALS/prox, SPL07 pressure | VERIFIED ON DEVICE |
| Fuel gauges | MT6375 primary; SH366003 secondary (`3rd-gauge`) | VERIFIED ON DEVICE |
| Charge pumps | SC8571 master 11-0066, slave 6-0067; SC8510 6-0069 (`reg=0x69`) | VERIFIED stock binding; board nets UNKNOWN |
| Audio | MT6369 codec, two AMICs, Awinic AW88394 at 6-0034 | topology VERIFIED |
| RGB notification | AW2013 at I2C 11-0045 | VERIFIED binding |
| Consumer IR | `/irtx-pwm`, PWM0, `mt6369_vio28`, rc-core `mtk_irtx_pwm.ko`, LIRC backend | software ownership VERIFIED; emitter UNKNOWN |
| Work/warning lights | stock `YftOutdoorLightUlefone`, `YftRedBlueLight` apps | userspace VERIFIED; control ABI UNKNOWN |
| Action keys | `yft-gpio-keys` emits F1/F2 | VERIFIED ON DEVICE |
| USB / uSmart | shared MTU3/xHCI/USB2 PHY via `extcon-mtk-usb`, MT6375 `usb-otg-vbus` | VERIFIED control path |

## Not verified

- Runtime behaviour of any block under a LieppOS-built kernel (hardware validation **0**).
- Exact 120 W charging protocol, cell wiring and reverse-charge ABI.
- Audio calibration topology and the exact speaker amplifier IC.
- Work-light / warning-light control ABI.

See [Known limitations](known-limitations.md).
