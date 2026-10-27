# Untapped capabilities

Hardware this phone has, and what it could do that nothing currently asks it to.

This is not a wishlist. Each entry is grounded in something the research established about the
actual board. Where a limit is real, it is stated rather than glossed over.

| Readiness | Meaning |
|---|---|
| **Ready** | Hardware and software path proven; only an application is missing |
| **Buildable** | Host-side work can deliver it, no firmware changes needed |
| **Blocked** | A hardware or firmware boundary stops it |
| **Unknown** | Needs measurement before anyone can say |

## NFC as a research tool

The phone has a full ST21 NFC controller, and it is used as a payment reader and nothing more.
Android's `TagTechnology.transceive()` already allows arbitrary APDU exchange with NFC-A, B, F
and V tags, which covers everything a normal reader can do.

**Already proven:** Type-4 host card emulation works and is externally readable and
reboot-stable. The phone can present itself as a tag that another reader sees.

| Capability | Readiness | Note |
|---|---|---|
| Raw APDU console and scripting | Buildable | `transceive()` after activation |
| Tag dump, compare and write | Buildable | Standard Android APIs |
| Custom HCE applications | Buildable | Type-4 AID routing |
| Native NCI diagnostics | Buildable | Host-side, controller-mediated |
| MIFARE Classic read | Unknown | Depends on whether the NFCC firmware exposes it |
| Arbitrary UID or ATQA emulation | Blocked | Needs vendor NCI support that is not exposed |
| Type-2 / NTAG emulation | Blocked | No host listen path; Type-4 is the viable route |
| MIFARE Classic emulation | Blocked | Requires NXP-provisioned keys in the secure element, not ROM patches |
| Raw RF sniffing or transparent mode | Blocked | Controller firmware does not expose it |

> The honest comparison: this phone can match a Flipper Zero for reading, writing, APDU work and
> programmable card emulation, because Android is a far better application platform. It cannot
> match it for card cloning, MIFARE Classic tooling, raw frame injection or RF analysis, because
> those live below a firmware boundary that cannot be crossed from the host.

NFC controller firmware *is* updatable in principle; ST documents eFlash and a secure update
mechanism, and the stock HAL contains the update state machine. That mechanism authenticates
vendor firmware independently of the Android bootloader, so an unlocked phone does not grant
the ability to install custom NFC firmware.

## A real thermal camera stack

The thermal module is a USB device with its own private stack, driven only by the stock
ThermoVue Pro app. Nothing else on the phone can use it, and none of its radiometric data is
exposed to other applications.

| Capability | Readiness | Note |
|---|---|---|
| Live thermal preview in a third-party app | Buildable | UVC path is known |
| Per-pixel temperature, not just colour | Unknown | Depends on whether the module emits radiometric frames |
| Region and point measurement | Buildable | Once raw frames are available |
| Palette and range control | Buildable | Host-side rendering |
| Thermal and visible camera fusion | Buildable | Both sensors are reachable |
| NUC / shutter control | Unknown | Needs the module command set |
| A documented API for other apps | Buildable | The real gap today |

The module is rated 640x512 at 25 Hz, 12 um pitch, under 40 mK sensitivity, -20 to 550 C. Those
are manufacturer figures. Nobody has measured them.

## uSmart as a general expansion port

uSmart is a six-pin USB 2.0 host port: 5 V, ground, D+, D-, and two ID pins. There is no
proprietary protocol and no authentication chip. Anything that speaks USB 2.0 can attach.

| Capability | Readiness | Note |
|---|---|---|
| Power and talk to any USB 2.0 device | Ready | Requires a 5.1 kOhm link on pins 5-6 |
| Meshtastic radio link | Buildable | Serial over USB; no Bluetooth needed |
| RF walkie-talkie accessory | Buildable | USB audio plus CDC control |
| Storage, serial, network adapters | Ready | Ordinary USB devices |
| Charge the phone through uSmart | Blocked | It is an output port, not an input |
| Identify which accessory is attached | Blocked | Detect pin only, no model ID |

The port stays available while USB-C is charging, which is the main reason to use it. Current
limit is unpublished. The phone switches 5 V on through GPIO152 only after it sees the detect
pin pulled low.

## On-device language models

The SoC has an NPU 655, 16 GB of RAM, a 10,600 mAh battery and unusually large cooling for a
phone. That is a better sustained-inference platform than most midrange devices.

| Model class | Role | Readiness |
|---|---|---|
| 1-2B quantised | Always-available command router | Buildable |
| 3-4B quantised | Default local assistant | Buildable |
| 7-8B quantised | Quality local chat | Buildable |
| 12-14B quantised | Heavy local model | Unknown |
| 20B+ | Research only | Unknown |

Nothing here is implemented. The work is benchmarking CPU, Vulkan on the Mali-G615, and the
NeuroPilot NPU path, then measuring tokens per joule rather than peak speed. Do not count the
storage-backed RAM expansion as model capacity; it is swap, not memory.

## Battery data nobody reads

The phone has **two** fuel gauges. MT6375 publishes to Android, and SH366003 sits behind it as
`3rd-gauge` with its own pack-level measurements. Android shows a percentage; the hardware
reports far more.

| Capability | Readiness | Note |
|---|---|---|
| Deep power telemetry | Buildable | Both gauges are readable |
| Where the energy went | Buildable | Needs wakelock and runtime-PM accounting |
| Battery health estimate | Buildable | Inferred from charge curves, not a single number |
| Charge efficiency | Buildable | Input power versus stored energy |
| Per-subsystem power attribution | Unknown | Needs kernel instrumentation |

The real constraint is honesty: health cannot be read from one sensor sample. It is a hidden
state inferred over hours of charging and resting. A number that updates every second but never
changes its confidence is worse than no number.

## Display refresh rate

The panel supports 60, 90 and 120 Hz, and Android picks between them with its own policy. A
per-app or per-scene policy could cut screen-on power meaningfully, since the display is the
largest consumer when the phone is awake.

Readiness: **Buildable**. Needs measurement first, because a refresh-rate change that is not
properly synced causes visible stutter.

## The rear display

The 340x340 AMOLED is currently a watch-face and notification panel driven by `YftMiniScreen`
through a vendor misc device. Android's compositor never sees it.

| Capability | Readiness | Note |
|---|---|---|
| Always-on status display | Buildable | The panel already does this |
| Third-party app output | Unknown | ioctl protocol not documented |
| A second real Android display | Blocked | Not wired as a DRM display |
| Touch gestures while main screen sleeps | Unknown | Ownership not established |

## Work light, warning light and IR

Three separate emitters, each currently reachable only through a stock app.

| Emitter | Hardware | Readiness |
|---|---|---|
| Work light | AW36515, rated 1000 lm from 570 LEDs at 5 W | Buildable (driver known, ABI unknown) |
| Warning light | AW36518_v2, red and blue, constant and blink | Buildable (driver known, ABI unknown) |
| RGB notification | AW2013 at I2C 11-0045 | Buildable |
| IR blaster | `mtk_irtx_pwm`, carriers at 30-56 kHz | Unknown (emitter never confirmed) |

The IR chain is complete on the software side and the carrier frequencies are known. What has
never been established is whether the emitter physically fires. That is a five-minute test with
a camera, and it has not been done.

## Sensors beyond the obvious

The SCP co-processor drives five physical sensors and computes 17 more, including step counting,
tilt, significant motion and wake gestures. Most are declared but barely used.

| Capability | Readiness | Note |
|---|---|---|
| Step and activity tracking | Ready | Already computed in firmware |
| Wake gestures | Unknown | Declared; behaviour untested |
| Barometric altitude | Ready | SPL07 is present |
| Compass heading | Ready | MMC5603 is present |
| Sensor batching and low-power modes | Unknown | Firmware policy, not documented |

## Reverse power and USB host

The phone can act as a USB host through Type-C with OTG, and the charging research indicates a
roughly 10 W reverse-power path. That is enough to charge a small accessory from the phone.

Readiness: **Partly**. The OTG path is proven; the exact reverse-power limits and behaviour are
not.

## What is genuinely out of reach

- Installing custom NFC controller firmware. The secure update mechanism is separate from the
  Android boot chain and rejects unsigned images.
- A second Android display on the rear panel. It is not wired as one.
- Charging the phone through uSmart. The port only outputs power.
- Raw RF capture or transmission on NFC. The controller does not expose a transparent mode.
- SuperSpeed USB. There is no evidence the Type-C port routes USB 3 lanes.

## Where to start

The highest value for the least risk is the NFC laboratory stack and the thermal camera API.
Both run entirely in userspace, need no kernel changes, and turn hardware that is already
working into something other software can use. uSmart accessories come next, because the port
is ready today and only needs a device to plug into it.

Sources: research `TODO/st21-lieppos.md`, `TODO/phase4-nfc-vs-flipper-zero-capabilities.md`,
`TODO/thermal-camera-app.md`, `TODO/kernel-enhancement-roadmap.md`,
`TODO/scientific-live-battery-health-estimator.md`, `TODO_Usmart/`, `TODO_AI/`, and
`docs/hardware-map.md`.
