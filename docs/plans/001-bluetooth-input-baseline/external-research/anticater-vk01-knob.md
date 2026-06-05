# External Research: Anticater VK-01 Knob Capabilities

**Generated**: 2026-06-05  
**Prompt**: Research the Anticater Bluetooth/customizable desktop volume knob
for expected input behavior, click/press events, LED features, and what the CLI
baseline can realistically observe or control.

## Recommendation

Treat the Anticater VK-01 as a **generic programmable HID macro/media knob**.
The first CLI should read it through HIDAPI and experimentally confirm its HID
descriptors and reports in the actual mode being used.

Assume our CLI can reliably **observe input events**, but should not assume it
can control LEDs, profiles, or mappings at runtime.

## Identified Device Family

Search results and manuals point to the **Anticater VK-01 / VK01 customizable
desktop volume knob**. The product appears in dual-mode and tri-mode variants:

| Variant | Modes |
|---|---|
| Dual-mode | USB-C wired + Bluetooth |
| Tri-mode | USB-C wired + Bluetooth + 2.4 GHz dongle |

The Bluetooth name may appear as `ANTICATER_MINI`, `ANTICATER VK01`, or similar
depending on model/firmware. The 2.4 GHz receiver likely presents to the host as
a USB HID device.

## Default Controls

The manuals consistently describe five physical operations:

| Operation | Factory default |
|---|---|
| Rotate left | Volume down |
| Rotate right | Volume up |
| Press / click | Mute |
| Long-press + rotate left | Screen brightness down |
| Long-press + rotate right | Screen brightness up |

All five operations are described as configurable via vendor software.

## Likely HID Behavior

The VK-01 almost certainly presents as a HID keyboard/consumer-control style
device rather than as a custom Bluetooth service:

1. Rotation likely emits repeated **Consumer Page** volume-up/down reports, one
   or more reports per detent.
2. Press likely emits a mute consumer-control event, unless remapped.
3. Long-press + rotation is probably handled inside firmware and emitted as the
   resulting mapped action, not as a separately visible "long-press state".
4. Custom mappings may emit keyboard scan codes, modifier combinations,
   multimedia keys, or mouse events.

Expected usage pages to check during capture:

| Usage Page | Purpose |
|---|---|
| `0x0C` Consumer Control | volume, mute, brightness/media keys |
| `0x07` Keyboard | basic keys and shortcut macros |
| `0x01` Generic Desktop / mouse-related pages | mouse or scroll functions |
| `0xFFxx` Vendor-defined | possible but unadvertised control channel |

## LED / RGB Features

The VK-01 has built-in RGB/lighting features, but available sources strongly
suggest lighting is configured by vendor software and stored on the device.

Reported lighting facts:

1. RGB lighting exists on supported models.
2. Lighting modes include off, white, green, alternating, jump, and flashing.
3. Wireless mode disables or limits constant lighting to preserve battery.
4. Some vendors state lighting is only available in wired mode.
5. There is no public documentation of a host API for real-time LED control.

Practical implication: the CLI should **not** include live LED control in the
baseline. If HID descriptor capture finds vendor-defined output or feature
reports, LED control can become a later reverse-engineering workshop.

## What the CLI Can Realistically Do

The baseline can:

1. Enumerate HID interfaces and show vendor/product/manufacturer/product/path.
2. Filter candidate interfaces by usage page and usage where available.
3. Open the selected interface and read input reports.
4. Print raw bytes with timestamps.
5. Map obvious volume/mute reports into normalized events.
6. Capture JSONL fixtures for replay.
7. Compare behavior across USB, Bluetooth, and 2.4 GHz modes if available.

The baseline likely cannot, without reverse engineering:

1. Change RGB color/effects live.
2. Read or switch the device's current profile.
3. Change macro mappings.
4. Distinguish long-press as a raw state rather than as the emitted mapped
   action.

## What Must Be Verified Experimentally

The spec should require a capture session that records:

1. HID descriptor(s) for USB, Bluetooth, and 2.4 GHz modes where available.
2. VID/PID, manufacturer string, product string, usage page, usage, report IDs.
3. Reports emitted for:
   - rotate left
   - rotate right
   - press/click
   - long-press + left
   - long-press + right
4. Whether a vendor-defined HID interface exists.
5. Whether any output/feature reports exist that could plausibly control RGB or
   profiles.
6. Differences in reports across wired, Bluetooth, and 2.4 GHz modes.

## Impact on the Project Spec

The spec should add an Anticater-specific acceptance criterion:

> Given the Anticater VK-01 is paired/connected, the CLI can identify candidate
> HID interfaces, capture raw reports for each documented operation, and produce
> a JSONL fixture plus best-effort normalized events for rotation and press.

It should also explicitly defer LED/RGB control unless a vendor-defined HID
control channel is discovered during capture.

## Citations

- Anticater VK01 manual mirror: https://manuals.plus/id/anticater/vk01-customizable-desktop-volume-knob-manual
- Anticater VK01 manual / software reference: https://manuals.plus/fr/ae/1005009577840607
- Anticater VK-01 product/vendor listing: https://clickclack.io/products/group-buy-anticater-vk-01-desktop-volume-control-knob
- PDF manual mirror: https://ae01.alicdn.com/kf/Sf2e66dfe28d542208c7b20e0a05f0f7e4.pdf
- QMK Raw HID reference for comparison only: https://docs.qmk.fm/features/rawhid
