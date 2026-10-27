# USB and uSmart

**VERIFIED ON DEVICE** (stock control path) · **UNKNOWN** (pinout electrical limits).
Research: `docs/hardware-map.md`, `TODO_Usmart/`, `kernel/usmart/*` @ `ae6dce06`.

For the full hands-on guide — pin table, the 5.1 kΩ detect link, accessory classes,
and how to build a cable — see **[uSmart (USmart)](../../usmart.md)**. This page covers
the device-level and kernel integration view.

## Control path (VERIFIED)

```
MT6375 OTG
    -> extcon-mtk-usb
    -> shared USB0 / MTU3 / USB2 PHY / xHCI fabric + UVC routing
    -> uSmart connector
```

| Element | Detail | Evidence |
|---|---|---|
| USB controller | configfs + UDC `11201000.usb0` | VERIFIED ON DEVICE |
| Routing | `extcon-mtk-usb`, UVC switch / accessory-power GPIOs | VERIFIED ON DEVICE |
| Power | MT6375 `usb-otg-vbus` | VERIFIED ON DEVICE |
| Legacy `11211000.usb1` | userspace references exist but there is **no live DT controller** | VERIFIED |
| SC8510 / SC851x | **excluded** from the uSmart VBUS/control path | VERIFIED |

There is **no separate uSmart controller**. After the switch, traffic is handled by
the normal Linux USB host stack.

## Kernel view

| Control | Job |
|---|---|
| Detect input (`GPIO28`) | Reads the ID pin |
| Power switch (`GPIO152`) | Turns the 5 V pin on and off |
| Data switch (`GPIO55`) | Connects the USB 2.0 pair to uSmart or Type-C |

`uvc_insert_status = 1` only means the ID pin is low. It does **not** mean a camera
is streaming or that the phone recognized a USB device.

## Accessory development

Start from a plain USB 2.0 device; the phone is the host. A UVC camera or a USB
serial adapter is a safer first project than a motor or a radio.

1. Connect 5 V, GND, D+ and D−.
2. Tie pins 5 and 6 to ground through a **5.1 kΩ** resistor.
3. Keep the 5 V current low until the limit is measured.
4. Add ESD protection and inrush limiting.
5. Do not backfeed power into the phone.
6. If the accessory has its own supply, leave pin 1 disconnected.

## Confirmed limitations

- Maximum current on the 5 V pin is **not published** and has not been measured.
- The exact physical six-pin order is a **working pinout**, not a stock-firmware finding.
- The role of each of the two ID pins is not fully documented.
- Simultaneous Type-C **data** and uSmart data is unproven (concurrent charging is claimed).
- Connector part number and mating plug are unknown.

Do not invent GPIO assignments, pin voltages or USB behaviour. See
[Known limitations](known-limitations.md).

## Related

- [uSmart full guide](../../usmart.md) · [Hardware](hardware.md) · [Partition map](partitions.md)
