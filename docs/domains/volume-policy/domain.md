# volume-policy Domain

## Purpose

Future pure policy domain that will convert normalized knob events into bounded
NAD/BluOS volume intents.

## Concepts

| Concept | Entry Points | Summary |
|---|---|---|
| Consuming normalized events | Future `VolumePolicy` | Will consume `NormalizedKnobEvent` without importing HIDAPI or CLI runtime. |

## Contracts

No source contracts are implemented in this baseline. The future domain may rely
on `device-input` normalized event contracts.

## Boundary Owns

- Future dB step mapping.
- Future clamping and duplicate-event safety.
- Future volume-intent contracts.

## Boundary Excludes

- HID capture.
- CLI workflow.
- BluOS network transport.

## Dependencies

Deferred. Expected future dependency: `device-input` contracts.

## Composition

No runtime components yet.

## Source Location

Not implemented in this baseline.

## History

| Plan | Change | Date |
|---|---|---|
| 001-bluetooth-input-baseline | Documented future normalized-event consumer boundary. | 2026-06-05 |

