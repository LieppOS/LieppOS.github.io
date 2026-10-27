# Hardware

Every component identified on the board, and what it does.

| Status | Meaning |
|---|---|
| **Verified** | Observed on the device or established from authenticated images |
| **Partly** | The connection is proven, the behaviour is not |
| **Unknown** | Not established |

Only authenticated facts are listed. Board wiring that has not been authenticated lives in the
kernel's *provenance-pending* device tree, disabled by default (`CONFIG_GQ5012BF1_PENDING_BOARD_DT=n`).

Nothing here has been exercised under a LieppOS-built kernel. Hardware validation is **0**.

## Compute and storage

| Component | What it does | Status |
|---|---|---|
| MediaTek MT6878 (MT6878T) | Main SoC: eight-core arm64 CPU, Mali GPU, ISP, modem and the SCP sensor co-processor | Verified |
| UFS storage | Fast flash storage holding every partition; driven by the `ufs-mediatek-mod` module | Verified |
| TrustKernel (tkcore) | Secure-world OS running alongside Android; handles fingerprint auth and secure memory. Stock binaries, never redistributed | Verified |
| GenieZone | MediaTek's protected execution environment for trusted workloads | Verified |

## Display and touch

| Component | What it does | Status |
|---|---|---|
| `yft-lcm-vtdr6115-drv` | Main LCD panel, 1080x2400, 60/90/120 Hz, density 480, on `card0-DSI-1` | Verified |
| FocalTech FT3680 | Main touchscreen controller on SPI3, ten simultaneous touch points | Verified |
| `spi_tiny_lcd_co5300` | Rear 340x340 round display, driven over SPI0 by `spi_tiny_co5300_lcd.ko` | Partly |
| Hynitron `hyn_ts` | Rear display touch panel on I2C 0-0015, single tracking point | Verified |

The rear screen is **not** a second Android display. It is driven through a vendor misc device
(`/sys/class/misc/tiny_lcd_miscdev`) with the `YftMiniScreen` app drawing watch faces and
notifications. Android's display compositor never sees it as a second screen.

## Cameras

| ID | Sensor | Facing | Flash |
|---:|---|---|---|
| 0 | Sony IMX989 | Rear | Yes |
| 1 | Samsung S5KJN1 | Front | No |
| 2 | Samsung S5KJN1MAIN2 | Rear | Yes |
| 3 | OmniVision OV64B | Rear | Yes |

| Component | What it does | Status |
|---|---|---|
| MediaTek ISP7SP | Image signal processor: demosaic, denoise, HDR and colour processing for all sensors | Verified |
| `mtk_ccuv.ko` | Camera control unit driver coordinating the sensors and ISP | Verified |
| AW36515 / AW36518 | Camera flash and illumination LED drivers | Verified |
| ThermoVue Pro (`com.energy.tc2c`) | Thermal camera application, with AC020 and UVC native libraries and 17 calibration assets | Partly |
| `yft_tiny2c_usb` | Kernel driver at I2C 8-003c controlling the thermal module's USB and sensor mode | Partly |

The thermal camera is **separate** from the four normal cameras. It is a USB device with its own
control path, not a Camera2 sensor. Which rear sensor is sold as "night vision" needs a real
capture test; the sensor list alone does not answer it.

## Audio

| Component | What it does | Status |
|---|---|---|
| MT6369 codec | Audio codec and headset detection, under SPMI `second_pmic@5` | Verified |
| Two analog microphones | Bottom mic on AIN0/UL1_CH1, back mic on AIN2/UL1_CH2 | Partly |
| Awinic AW88394 | Loudspeaker amplifier at I2C 6-0034, chip ID `0x2049` | Verified |
| MT6878 AFE | Audio front end at `11050000`, feeds the codec into Android's audio stack | Verified |

There is no built-in front microphone. The front and rear cameras both use the normal
two-microphone array. Microphone part numbers and acoustic orientation need PCB inspection.

## Sensors

All six physical sensors are driven by firmware on the SCP co-processor, not by Linux drivers.
Linux only sees `scp.ko`, `sensorhub.ko` and `hf_manager.ko`, which relay SCP data to Android.

| Sensor | Measures | Vendor | Status |
|---|---|---|---|
| ICM4N607 | Acceleration and rotation rate (accelerometer + gyroscope) | iven_sense | Verified |
| MMC5603 | Magnetic field, for compass heading | memsic | Verified |
| STK3A5X ALS | Ambient light level, for screen brightness | sensortek | Verified |
| STK3A5X PS | Proximity, to blank the screen during calls | sensortek | Verified |
| SPL07 | Atmospheric pressure, for altitude and weather | goer | Verified |

Android exposes 22 sensors in total. The extra 16 are computed by MediaTek's sensor fusion from
these five parts: orientation, gravity, linear acceleration, rotation vectors, step counter and
detector, tilt, significant motion and wake gestures.

## Power and charging

| Component | What it does | Status |
|---|---|---|
| MT6375 | Primary battery gauge and charger controller at I2C 5-0034, also provides USB OTG power | Verified |
| SH366003 | Secondary pack fuel gauge at I2C 9-0055, exported as `3rd-gauge`; supplies the real pack readings Android publishes | Verified |
| SC8571 (master) | Charge pump at I2C 11-0066 (`primary_dvchg`), steps voltage down efficiently for fast charging | Verified |
| SC8571 (slave) | Second charge pump at I2C 6-0067 (`secondary_dvchg`), runs in parallel for high current | Verified |
| SC8510 | Switched-capacitor converter at I2C 6-0069, static configuration and IRQ shim only | Partly |

The pack reads 8.4 V and charges toward 8.9 V, which points to a two-cell series design. The
exact cell wiring needs a schematic. The 120 W negotiation protocol is **not** in the SC8571
driver; it lives in MediaTek's charger policy, which has not been reconstructed.

## Connectivity

| Component | What it does | Status |
|---|---|---|
| ST21NFC | NFC controller at I2C 6-0008, with `st21nfc_fw.bin` and `st21nfc_fw7.bin`; exposes SIM1 and SIM2 secure elements | Verified |
| CONNAC2 WLAN | Wi-Fi, driven by `connsys_wifi` firmware and `wlan_*` modules | Partly |
| CONNAC2 Bluetooth | Bluetooth, driven by `connsys_bt` firmware and `bt_drv_6878` | Partly |
| CONNAC2 GNSS | GPS, GLONASS, BeiDou and Galileo via `connsys_gnss` and the MediaTek LBS service | Partly |
| MediaTek modem | Cellular baseband with `md1dsp`, `md1arm7` and `md3img` firmware; dual SIM | Partly |

For all of these the hardware and firmware are identified, but no radio behaviour has been
tested: no band scan, no call, no data session, no cold GNSS start. NFC polling and payment are
likewise untested.

> Modem identity, NV and calibration partitions are unique to each device. They must never be
> wiped, copied into a repository or regenerated from extraction.

## Other hardware

| Component | What it does | Status |
|---|---|---|
| Fingerprint (`madev`) | SPI1 sensor with `microarray_fp_tee` and `/dev/tkcore_fp`, authenticating through TrustKernel | Partly |
| AW2013 | RGB notification LED controller at I2C 11-0045 | Verified |
| Consumer IR | Remote-control transmitter: `/dev/lirc0` -> `mtk_irtx_pwm.ko` -> PWM0 -> `mt6369_vio28` at 2.8 V | Partly |
| `yft-gpio-keys` | Physical action buttons, emitting F1 and F2 key codes | Verified |
| Work and warning lights | High-current lamps controlled by the stock `YftOutdoorLightUlefone` and `YftRedBlueLight` apps | Partly |
| USB / uSmart | Shared MTU3, xHCI and USB2 PHY; carries charging, data, OTG and the thermal camera | Verified |

The IR blaster has a complete, proven software chain and a confirmed 30/33/36/38/40/56 kHz
carrier set, but nobody has confirmed the emitter physically fires. The fingerprint transport
works; whether authentication succeeds end to end is untested.

## What is not verified

- Any block running under a LieppOS-built kernel.
- The exact 120 W charging protocol, cell wiring and reverse-charge behaviour.
- Microphone part numbers, acoustic orientation and audio calibration.
- The work-light and warning-light control interface.
- Wi-Fi, Bluetooth, GNSS, NFC, modem and SIM behaviour under any ROM.
- The physical IR emitter and its optical path.

See [Known limitations](known-limitations.md) and [Partition map](partitions.md).

Sources: research `docs/hardware-map.md`, `sensors.md`, `connectivity.md`, `camera-thermal.md`,
`display-secondary.md`, `battery-charging.md`, `audio.md`, `ir-blaster.md`.
