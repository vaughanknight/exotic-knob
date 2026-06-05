# Domain Registry

| Domain | Status | Source Location | Contract Surface |
|---|---|---|---|
| device-input | Active | `src/exotic_knob/device_input/` | HID report, fixture, fake reader, normalized event contracts |
| cli-runtime | Active | `src/exotic_knob/cli/` | `exotic-knob` / `python -m exotic_knob.cli.main` commands |
| configuration | Active | `src/exotic_knob/configuration/` | Anticater candidate profile filters |
| platform-adapter | Active | `src/exotic_knob/platform_adapter/` | HIDAPI enumeration/open/read adapter |
| volume-policy | Deferred | Not implemented | Future consumer of normalized knob events |
| amplifier-control | Deferred | Not implemented | Future BluOS/NAD M33 control adapter |

## History

| Plan | Change | Date |
|---|---|---|
| 001-bluetooth-input-baseline | Created initial six-domain registry for the Anticater CLI baseline. | 2026-06-05 |

