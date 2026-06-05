# External Research: ESP32 Battery and Bluetooth Path

**Generated**: 2026-06-05  
**Prompt**: Research future ESP32 implementation considerations for a Bluetooth
volume knob bridge that mostly idles and only acts when volume changes.

## Recommendation

Preserve an **event-driven, transport-neutral knob event contract** in the
desktop prototype. For a future ESP32 version, keep the firmware decision open
between BLE central/client and HID behavior, but assume that **always-listening
Bluetooth cannot use deep sleep**. If Bluetooth must remain responsive, **light
sleep or active low-duty operation** is the practical baseline.

## Key Findings

### BLE/HID role depends on the final product shape

An ESP32 future could either:

1. Act as a BLE client/central consuming a peripheral's events.
2. Act as a HID device emitting media-control reports to another host.
3. Use a custom BLE GATT service and translate notifications into the shared
   event model.

The desktop prototype should not bake in any one of those transport choices.

### Deep sleep conflicts with always-listening Bluetooth

Deep sleep is the lowest-power mode, but Bluetooth/Wi-Fi radio operation does
not remain available in deep sleep. If the bridge must react to Bluetooth input
while "always on", it needs a lighter sleep mode or an external wake strategy.

### Event-driven callbacks should feed queues

ESP32 Bluetooth callbacks should enqueue events into an application task rather
than doing policy work inside stack callbacks. This keeps radio handling
responsive and mirrors the desktop adapter/core boundary.

## Migration Contract to Preserve

The desktop baseline should shape events like:

```text
KnobTurned(delta, source_id, sequence)
KnobPressed(action, source_id, sequence)
TransportState(connected, bonded, rssi, retry_count)
CapabilityFlags(media_keys_supported, absolute_volume_supported)
```

Keep BLE/HID-specific fields in adapter metadata, not in the core event model.

## Battery Implications

1. Battery life will be dominated by radio availability, not application logic.
2. Prefer notifications/events over polling.
3. Avoid busy loops in the desktop design so the same mental model transfers to
   embedded firmware.
4. Use bounded queues and sequence IDs so reconnection and burst handling are
   deterministic.

## Spec Implications

The spec should require:

1. Event-driven input handling.
2. No transport-specific assumptions in the normalized event contract.
3. Sequence/correlation fields in captured events.
4. Bounded queue or explicit backpressure behavior.
5. Captured raw reports usable as fixtures.

## Citations

- Espressif HID device API: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/bluetooth/esp_hidd.html
- ESP32 sleep-mode background: https://www.instructables.com/ESP32-Deep-Sleep-Tutorial/
- Espressif low-power documentation: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/low-power-mode/low-power-mode-wifi.html
- BLE/FreeRTOS task design patterns: https://hubble.com/community/guides/freertos-task-design-patterns-for-ble-applications/
- Event-driven coupling reference: https://www.enterpriseintegrationpatterns.com/ramblings/eventdriven_coupling.html
