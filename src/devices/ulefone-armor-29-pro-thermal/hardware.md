# Hardware

Every identified component on the board, and what it does.

| Status | Meaning |
|---|---|
| **Verified** | Observed on the device or established from authenticated images |
| **Partly** | The connection is proven, the behaviour is not |
| **Claimed** | Manufacturer specification only, not independently confirmed |
| **Unknown** | Not established |

Board wiring that has not been authenticated lives in the kernel's *provenance-pending* device
tree, disabled by default (`CONFIG_GQ5012BF1_PENDING_BOARD_DT=n`).

No component here has been exercised under a LieppOS-built kernel. Hardware validation is **0**.

## Compute and memory

| Component | What it does | Status |
|---|---|---|
| MediaTek MT6878 (MT6878T) | Main SoC: arm64 CPU, Mali GPU, ISP, modem, and the SCP co-processor that runs the sensors | Verified |
| RAM | 16 GB LPDDR. Boot reports exactly `17179869184` bytes; LPDDR generation and part number are not identified | Verified (size) |
| RAM expansion | Up to 16 GB of storage-backed virtual RAM, sold as Dynamic RAM Expansion | Claimed |
| UFS storage | Flash holding every partition, driven by the `ufs-mediatek-mod` module | Verified |
| TrustKernel (tkcore) | Secure-world OS beside Android; handles fingerprint authentication and secure memory. Stock binaries, never redistributed | Verified |
| GenieZone | MediaTek protected execution environment for trusted workloads | Verified |

## Display and touch

| Component | What it does | Status |
|---|---|---|
| `yft-lcm-vtdr6115-drv` | Main LCD, 1080x2400, 60/90/120 Hz, density 480, on `card0-DSI-1` | Verified |
| FocalTech FT3680 | Main touchscreen on SPI3, ten simultaneous points | Verified |
| `spi_tiny_lcd_co5300` | Rear 1.04 inch 340x340 AMOLED, over SPI0 via `spi_tiny_co5300_lcd.ko` | Verified |
| Hynitron `hyn_ts` | Rear touch panel on I2C 0-0015, single tracking point | Verified |

The rear screen is **not** a second Android display. It is a vendor misc device
(`/sys/class/misc/tiny_lcd_miscdev`) that the `YftMiniScreen` app draws watch faces and
notifications onto. Android's compositor never sees it.

## Cameras

| ID | Sensor | Facing | Role | Flash |
|---:|---|---|---|---|
| 0 | Sony IMX989 | Rear | Main | Yes |
| 1 | Samsung S5KJN1 | Front | Selfie | No |
| 2 | Samsung S5KJN1MAIN2 | Rear | Ultra-wide | Yes |
| 3 | OmniVision OV64B | Rear | 64 MP night vision | Yes |

| Component | What it does | Status |
|---|---|---|
| MediaTek ISP7SP | Image processor: demosaic, denoise, HDR and colour for all sensors | Verified |
| `mtk_ccuv.ko` | Camera control unit driver coordinating sensors and ISP | Verified |
| VCM motors | Autofocus voice-coil actuators on the rear cameras | Verified |
| OIS | Optical stabilisation for the main camera | Verified |
| EEPROMs | Per-module calibration storage for each camera | Verified |
| AW36515 / AW36518 | Flash and torch LED drivers | Verified |
| ThermoVue T2 | Thermal sensor: 640x512, 25 Hz, 12 um pitch, under 40 mK, -20 to 550 C | Claimed (spec) / Verified (driver and APK) |
| `yft_tiny2c_usb` | Driver at I2C 8-003c controlling the thermal module USB and sensor mode | Partly |
| ThermoVue Pro (`com.energy.tc2c`) | Thermal camera app, AC020 and UVC native stack, 17 bundled calibration assets | Partly |

The thermal camera is **separate** from the four normal cameras: it is a USB device with its own
control path, not a Camera2 sensor. The night-vision claim on the OV64B is marketing; the sensor
and its IR illuminators are present, but low-light performance has never been measured.

## Audio

| Component | What it does | Status |
|---|---|---|
| MT6369 codec | Audio codec and headset detection, under SPMI `second_pmic@5` | Verified |
| MT6878 AFE | Audio front end at `11050000`, feeding the codec into Android audio stack | Verified |
| Two analog microphones | Bottom mic on AIN0/UL1_CH1, back mic on AIN2/UL1_CH2 | Partly |
| Awinic AW88394 | Loudspeaker amplifier at I2C 6-0034, chip ID `0x2049` | Verified |
| Loudspeaker and earpiece | At least one external speaker plus the call earpiece | Verified |
| 3.5 mm headphone jack | Wired headset output and mic input, with insert detection | Verified |

There is no built-in front microphone; the cameras use the normal two-mic array. Microphone part
numbers and acoustic orientation need PCB inspection, and stereo layout is unconfirmed.

## Sensors

All five physical sensors are driven by firmware on the SCP co-processor, not by Linux. Linux sees
only `scp.ko`, `sensorhub.ko` and `hf_manager.ko`, which relay data to Android.

| Sensor | Measures | Vendor | Status |
|---|---|---|---|
| ICM4N607 | Acceleration and rotation rate | iven_sense | Verified |
| MMC5603 | Magnetic field, for compass heading | memsic | Verified |
| STK3A5X ALS | Ambient light, for screen brightness | sensortek | Verified |
| STK3A5X PS | Proximity, blanking the screen during calls | sensortek | Verified |
| SPL07 | Atmospheric pressure, for altitude and weather | goer | Verified |

Android exposes 22 sensors. The other 17 are computed by MediaTek sensor fusion from these five:
orientation, gravity, linear acceleration, rotation vectors, step counter and detector, tilt,
significant motion, wake gestures and device orientation.

## Power and charging

| Component | What it does | Status |
|---|---|---|
| MT6375 | Primary battery gauge and charger controller at I2C 5-0034; also supplies USB OTG power | Verified |
| SH366003 | Pack fuel gauge at I2C 9-0055, exported as `3rd-gauge`; the real pack readings Android publishes | Verified |
| SC8571 (master) | Charge pump at I2C 11-0066 (`primary_dvchg`), stepping voltage down for fast charging | Verified |
| SC8571 (slave) | Second charge pump at I2C 6-0067 (`secondary_dvchg`), in parallel for high current | Verified |
| SC8510 | Switched-capacitor converter at I2C 6-0069; static configuration and IRQ shim only | Partly |

| Thermal limit | Thresholds |
|---|---|
| CPU, GPU, NPU, TPU, SoC | 85 / 90 / 100 / 117 C |
| Battery | 50 / 55 / 59 / 60 C |

The pack reads 8.4 V and charges toward 8.9 V, pointing to two cells in series; the exact wiring
needs a schematic. The 120 W negotiation is **not** in the SC8571 driver; it lives in MediaTek
charger policy, which has not been reconstructed.

## Connectivity

| Component | What it does | Status |
|---|---|---|
| ST21NFC | NFC controller at I2C 6-0008 with `st21nfc_fw.bin` and `st21nfc_fw7.bin`; exposes SIM1 and SIM2 secure elements | Verified |
| NFC antenna | Coil driven by the ST21NFC controller | Verified |
| CONNAC2 WLAN | Wi-Fi via `connsys_wifi` firmware and `wlan_*` modules | Partly |
| CONNAC2 Bluetooth | Bluetooth via `connsys_bt` and `bt_drv_6878` | Partly |
| CONNAC2 GNSS | GPS, GLONASS, BeiDou and Galileo via `connsys_gnss` and the LBS service | Partly |
| MediaTek modem | Cellular baseband with `md1dsp`, `md1arm7` and `md3img`; dual-SIM dual-standby | Partly |
| Antennas | Cellular, Wi-Fi, Bluetooth and GNSS antennas are present but not individually characterised | Unknown |

Hardware and firmware are identified for every radio, but no radio behaviour has been tested: no
band scan, no call, no data session, no cold GNSS start, no NFC poll.

> Modem identity, NV and calibration partitions are unique to each device. They must never be
> wiped, copied into a repository or regenerated from extraction.

## Expansion and I/O

| Component | What it does | Status |
|---|---|---|
| USB Type-C | Shared MTU3, xHCI and USB2 PHY; carries charging, data, OTG and the thermal camera. USB 2.0 only, no SuperSpeed evidence | Verified |
| USB-PD | Power Delivery with PPS; supports OTG host mode | Verified |
| SIM slots | Two nano-SIM slots, dual-SIM dual-standby | Verified |
| microSD slot | Dedicated slot, up to 2 TB | Verified (slot) / Claimed (capacity) |
| uSmart | Accessory interface on the same shared USB fabric | Verified |

There are three physical slots: nano-SIM, nano-SIM and microSD. No eSIM hardware was found.

## Feedback and controls

| Component | What it does | Status |
|---|---|---|
| Vibration motor | ERM type (no LRA resonance), handled by `vendor.vibrator-default`; click, tick and texture effects. Driver IC not identified | Verified (type) |
| Power button | `KEY_POWER` | Verified |
| Volume up / down | `KEY_VOLUMEUP` / `KEY_VOLUMEDOWN` | Verified |
| Two programmable keys | `yft-gpio-keys`, emitting F1 and F2; likely the rugged side buttons | Verified |
| AW2013 | RGB notification LED at I2C 11-0045, used for charging status | Verified |
| Fingerprint | SPI1 sensor with `microarray_fp_tee` and `/dev/tkcore_fp`, authenticating through TrustKernel | Partly |

The fingerprint transport is proven; whether authentication completes end to end is untested.

## Lights and infrared

| Component | What it does | Status |
|---|---|---|
| AW36515 work light | Main lamp, rated 1000 lm from 570 LEDs at 5 W, driven by `YftOutdoorLightUlefone` | Verified (driver) / Claimed (output) |
| AW36518_v2 warning light | Red and blue emergency lamp with constant and blink modes, driven by `YftRedBlueLight` | Verified (driver) / Claimed (brightness) |
| Consumer IR | Remote-control transmitter: `/dev/lirc0` to `mtk_irtx_pwm.ko` to PWM0 to `mt6369_vio28` at 2.8 V; carriers at 30, 33, 36, 38, 40 and 56 kHz | Partly |
| IR emitter | The optical emitter itself has never been confirmed to fire | Unknown |

The IR software chain is complete and the carrier frequencies are known from the stock HAL, but no
one has verified the emitter physically transmits.

## Thermal and cooling

| Component | What it does | Status |
|---|---|---|
| Active fan | None; there is no fan service | Verified |
| Passive cooling | Graphite, copper foil, heat pipe or vapour chamber; material not determined | Unknown |
| Thermal zones | CPU, GPU, NPU, TPU, SoC, skin, battery, USB port and power amplifier | Verified |
| Cooling devices | Mali GPU, charger, LCD backlight, Wi-Fi and flashlight throttling | Verified |

The thermal HAL is AIDL v3 and exposes all of these through Android thermal framework.

## Rugged construction

| Property | Value | Status |
|---|---|---|
| Dimensions | 177.35 x 85.6 x 33.8 mm | Claimed |
| Weight | 688 g | Claimed |
| Ingress protection | IP68 (2 m for 30 min) and IP69K | Claimed |
| Shock and vibration | MIL-STD-810H | Claimed |
| Underwater camera use | Photo and video start, stop and mode switching underwater | Claimed |
| Glove mode | Possibly supported by the touch controller | Unknown |
| SOS hardware | Not identified | Unknown |

These are manufacturer certifications. None has been independently tested here.

## What remains unidentified

- RAM manufacturer, part number and LPDDR generation.
- Vibration motor driver IC.
- Speaker count, stereo layout and microphone part numbers.
- Passive cooling materials.
- Individual antenna types and counts, beyond the NFC coil.
- PMIC topology and exact charger arbitration.
- PCB revision history.
- Whether the IR emitter, work light and warning light actually perform as specified.

See [Known limitations](known-limitations.md) and [Partition map](partitions.md).

Sources: research `hardware/MASTER-HARDWARE-INVENTORY.md`, and `docs/hardware-map.md`,
`sensors.md`, `connectivity.md`, `camera-thermal.md`, `display-secondary.md`,
`battery-charging.md`, `audio.md`, `ir-blaster.md`.
