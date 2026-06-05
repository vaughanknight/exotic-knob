# Anticater VK-01 fixture and smoke evidence

`sample_reports.jsonl` is synthetic evidence used for deterministic tests. It is
not a claim about the real knob's exact report descriptor.

## Real-device smoke log

Real Anticater VK-01 hardware smoke capture summary:

| Field | Value |
|---|---|
| Captured | 2026-06-05 |
| Device mode | Bluetooth HID through macOS |
| Host OS | macOS |
| Fixture location | Local ignored file: `capture.local.jsonl` |
| Reports captured | 323 |
| Raw report shapes | `03e900` volume up, `03ea00` volume down, `03e200` mute, `036f00` brightness up, `037000` brightness down, `030000` release/no-op |
| Indistinguishable operations | None observed in this mixed live-probe session |
| LED/RGB capability evidence | No vendor-defined output/feature reports observed |

The local capture includes a local HID path and should not be committed without
redaction.

When capturing real evidence, record:

| Field | Value |
|---|---|
| Device mode | USB / Bluetooth / 2.4 GHz |
| Host OS | macOS / Windows / Linux version |
| HID path | Redacted before sharing |
| Operations attempted | rotate left/right, click/mute, long-press+rotate left/right |
| Fixture location | Path to local `.jsonl` capture |
| Indistinguishable operations | Any actions that produced identical/no reports |
| LED/RGB capability evidence | Vendor-defined output/feature reports only; no control attempted |

Before sharing, redact local HID paths and serial numbers from fixture rows.
