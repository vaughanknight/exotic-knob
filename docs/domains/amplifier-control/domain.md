# amplifier-control Domain

## Purpose

Future BluOS/NAD M33 adapter domain.

## Concepts

| Concept | Entry Points | Summary |
|---|---|---|
| Sending BluOS volume commands | Future adapter | Will use dB-oriented volume semantics and safe policy outputs, not raw HID reports. |

## Contracts

No source contracts are implemented in this baseline.

## Boundary Owns

- Future local BluOS HTTP/XML communication.
- Future amplifier status and command-result contracts.

## Boundary Excludes

- Anticater HID capture.
- Normalized input decoding.
- CLI fixture replay.

## Dependencies

Deferred. Expected future dependency: `volume-policy`.

## Composition

No runtime components yet.

## Source Location

Not implemented in this baseline.

## History

| Plan | Change | Date |
|---|---|---|
| 001-bluetooth-input-baseline | Documented future BluOS/NAD M33 adapter boundary. | 2026-06-05 |

