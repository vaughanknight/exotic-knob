# External Research: Desktop Bluetooth Input Stack

**Generated**: 2026-06-05  
**Prompt**: Research the simplest practical desktop CLI approach for reading
events from a Bluetooth volume knob on macOS first, PC later, with a future ESP32
path.

## Recommendation

Start with a **macOS-first Python CLI using HIDAPI** to read the knob as a HID
consumer-control device. Most off-the-shelf Bluetooth volume knobs behave as HID
consumer-control devices, often as BLE HID-over-GATT internally, but exposed to
desktop operating systems as HID/media-key input rather than a custom GATT
service.

The first cut should:

1. Ask the user to pair the knob through the OS Bluetooth UI.
2. Enumerate HID devices.
3. Let the user select a candidate device.
4. Read raw HID reports in a blocking/event-style loop.
5. Print raw reports and a best-effort normalized event.
6. Capture reports to JSONL fixtures for replay.

## Key Findings

### HID-first is simpler than BLE-first

Commercial knobs usually present as Bluetooth HID consumer controls. On desktops,
the OS converts those into media key events unless an application opens the HID
device directly. Reading raw HID reports is more predictable for fixtures and
tests than trying to intercept global OS media key events.

### macOS UX should avoid custom pairing

The simplest macOS flow is to pair the knob in System Settings, then enumerate
HID devices from the CLI. Direct Bluetooth pairing from a CLI is fragile and
unnecessary for the first cut.

### Direct HID access avoids heavier permissions

On macOS, reading the device through HID APIs usually avoids Accessibility/Input
Monitoring prompts that would be required for global keyboard event taps. BLE
scanning through CoreBluetooth has its own privacy prompts and app metadata
requirements, so it should not be the first path unless the device is not HID.

### Capture/replay should be part of the baseline

The CLI should include a capture mode that writes raw reports as JSONL:

```json
{"timestamp_ns":123456789,"device_id":"...","report_id":1,"data_hex":"..."}
```

A replay mode can feed captured fixtures into parser/normalization tests without
requiring hardware.

## Stack Comparison

| Stack | Fit | Notes |
|---|---|---|
| Python + HIDAPI | Best first cut | Low ceremony, cross-platform HID access, easy JSON fixtures |
| Go + HIDAPI bindings | Good later | Single binary distribution, more setup/boilerplate |
| Rust + hidapi/btleplug | Best long-term if needed | Strong safety and BLE support, higher startup complexity |
| Node.js | Weak HID fit | Better for scripts/GATT experiments than raw HID |
| Native OS APIs | Useful for debugging | Best control, worst portability |

## Risks

1. The knob may expose custom BLE GATT instead of HID.
2. OS HID access may be filtered or exclusive for some devices.
3. HID reports may require descriptor parsing to decode bitfields.
4. Python is easiest now but may not be the final daemon/runtime choice.

## Spec Implications

The spec should define:

1. HID-first backend.
2. Raw fixture format.
3. Normalized event shape.
4. Device selection UX.
5. A fallback path for non-HID BLE devices.
6. No amplifier control in this first phase.

## Citations

- Apple Bluetooth pairing UX: https://support.apple.com/guide/mac-help/connect-a-wireless-accessory-blth1004/mac
- HID consumer-control example/discussion: https://community.roonlabs.com/t/remote-roon-volume-using-bluetooth-hid-consumer-control/107725
- Nordic HID consumer-control discussion: https://devzone.nordicsemi.com/f/nordic-q-a/28399/nrf51422-hid-consumer-control
- Rust BLE stack reference: https://github.com/deviceplug/btleplug
- Node BLE development context: https://punchthrough.com/how-to-use-node-js-to-speed-up-ble-app-development/
