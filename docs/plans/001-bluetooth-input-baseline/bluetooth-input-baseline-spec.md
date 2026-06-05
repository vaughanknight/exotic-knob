# Anticater VK-01 Bluetooth Input Baseline

**Mode**: Simple

## Research Context

📚 Specification incorporates findings from `research-dossier.md` and completed
external research under `external-research/`.

Key research findings:

1. The repository has no implementation substrate yet, so the first phase must
   establish minimal Python CLI tooling and a runnable capture path.
2. Desktop Bluetooth volume knobs usually expose HID consumer-control events;
   the recommended first cut is HID-first, macOS-first Python using HIDAPI.
3. The Anticater VK-01 likely behaves as a programmable HID macro/media knob:
   rotate left/right, click/mute, and long-press+rotate are emitted as keyboard
   or consumer-control reports configured by vendor software.
4. Anticater RGB/LED behavior appears vendor-app configured and battery-limited
   in wireless modes; live CLI LED control is explicitly out of scope unless a
   vendor-defined HID output/feature-report channel is discovered.
5. Future ESP32 work should preserve a transport-neutral event contract and
   event-driven behavior; always-listening Bluetooth is not compatible with deep
   sleep.
6. Future NAD M33 control should use BluOS dB semantics; this baseline should
   preserve raw input evidence and delta/sequence data for later dB policy work.

## Summary

Create a simple CLI baseline that can identify an Anticater VK-01 volume knob,
open its HID interface, print raw reports, emit best-effort normalized input
events, and save JSONL fixtures for replay. The baseline exists to learn what
the actual device emits before building daemon behavior or amplifier control.

## Goals

- Let the user pair/connect the Anticater VK-01 through the operating system and
  select the matching HID interface from the CLI.
- Capture HID descriptors and identifying metadata for USB, Bluetooth, and 2.4
  GHz modes where available.
- Print raw HID reports for rotate left, rotate right, click/mute,
  long-press+rotate left, and long-press+rotate right.
- Emit best-effort normalized events from observed reports.
- Save JSONL fixtures suitable for deterministic replay tests.
- Establish a Python/HIDAPI baseline that can run on macOS first and remain
  portable to PC platforms.
- Keep event contracts transport-neutral for future ESP32 and BluOS dB volume
  policy work.

## Non-Goals

- No NAD M33/BluOS control in this baseline.
- No daemon installation, background service, launchd, systemd, or Windows
  service behavior.
- No live LED/RGB control unless descriptor capture clearly discovers a
  vendor-defined output or feature-report channel.
- No reverse engineering of Anticater vendor software in this phase.
- No custom Bluetooth pairing workflow; pairing remains an operating-system
  responsibility.
- No support guarantee for non-HID custom BLE/GATT devices beyond documenting
  fallback research and future extension points.

## Target Domains

| Domain | Status | Relationship | Role in This Feature |
|---|---|---|---|
| device-input | **NEW** | **create** | Own Anticater HID discovery, capture, raw report fixtures, and normalized knob events |
| cli-runtime | **NEW** | **create** | Own command-line UX, device selection, capture/replay commands, stdout/stderr behavior |
| configuration | **NEW** | **create** | Own minimal device selection/profile fields without hardcoding user-specific identifiers |
| platform-adapter | **NEW** | **create** | Own OS-specific HIDAPI/platform behavior and future macOS/Windows/Linux differences |
| volume-policy | **NEW** | **consume later** | Not implemented here; future consumer of normalized events |
| amplifier-control | **NEW** | **consume later** | Not implemented here; future BluOS/NAD adapter uses preserved event metadata |

### New Domain Sketches

#### device-input [NEW]

- **Purpose**: Capture physical knob input and translate raw HID reports into
  transport-neutral events.
- **Boundary Owns**: HID descriptor capture, raw report capture, fixture schema,
  Anticater operation mapping, normalized event schema.
- **Boundary Excludes**: CLI presentation, amplifier volume policy, BluOS
  network calls, daemon supervision.

#### cli-runtime [NEW]

- **Purpose**: Provide user-facing commands for listing devices, selecting a
  candidate, capturing reports, and replaying fixtures.
- **Boundary Owns**: argument parsing, interactive prompts if any, terminal
  output, exit codes.
- **Boundary Excludes**: HID decoding details beyond calling device-input
  contracts.

#### configuration [NEW]

- **Purpose**: Hold minimal device/profile information needed to avoid hardcoded
  Anticater identifiers.
- **Boundary Owns**: candidate profile fields such as VID/PID/product strings,
  output paths, and capture options.
- **Boundary Excludes**: secrets, amplifier target configuration, daemon
  installation settings.

#### platform-adapter [NEW]

- **Purpose**: Isolate OS/HIDAPI behavior so macOS-first work can later extend
  to Windows/Linux.
- **Boundary Owns**: platform-specific HID enumeration/open/read behavior and
  capability reporting.
- **Boundary Excludes**: normalized event semantics and CLI workflow decisions.

#### volume-policy [NEW]

- **Purpose**: Future pure policy domain that converts normalized events into
  bounded volume intents.
- **Boundary Owns**: future dB step mapping, clamping, duplicate handling.
- **Boundary Excludes**: this baseline's raw capture implementation.

#### amplifier-control [NEW]

- **Purpose**: Future BluOS/NAD M33 adapter domain.
- **Boundary Owns**: future local HTTP/XML BluOS discovery, status, and dB
  command behavior.
- **Boundary Excludes**: Anticater HID capture and CLI baseline behavior.

## Testing Strategy

**Approach**: Hybrid.

**Rationale**: Use TDD-style deterministic tests for pure parsing,
normalization, fixture replay, and configuration validation. Use lightweight
hardware smoke checks for real Anticater capture because physical HID behavior
must be observed.

**Focus Areas**:

- JSONL fixture parsing and replay.
- Normalized event generation from known reports.
- Device selection filtering and metadata shaping.
- CLI exit codes for no devices, failed open, capture interrupted, and invalid
  output path.
- Fakes for HID reader behavior and captured report streams.

**Excluded**:

- Automated tests that require the physical Anticater device.
- Automated tests that require NAD M33/BluOS.
- Automated LED/RGB control tests.

**Test Doubles Policy**: Fakes only; no mocks. Use fixture-backed fake HID
readers and fake platform adapters at external boundaries.

## Documentation Strategy

**Location**: Hybrid — README + `docs/how/`.

**Rationale**: The README should show quick pairing/list/capture/replay commands.
`docs/how/` should explain Anticater mode capture, fixture schema, HID descriptor
notes, and future ESP32/BluOS implications.

## Complexity

- **Score**: CS-3 (medium)
- **Breakdown**: S=1, I=1, D=1, N=1, F=1, T=1
- **Confidence**: 0.78

**Assumptions**:

- The Anticater VK-01 exposes at least one readable HID interface in macOS after
  OS-level pairing.
- Python + HIDAPI can enumerate and read the relevant interface on the target
  Mac.
- LED/RGB control is not required for the baseline.
- JSONL fixtures are sufficient to support deterministic replay tests.

**Dependencies**:

- Python runtime and dependency manager selection.
- HIDAPI Python package and any native system library requirements.
- Physical Anticater VK-01 device for smoke capture.
- macOS Bluetooth pairing and HID permissions.

**Risks**:

- The OS may consume or filter HID reports before the CLI can read them.
- The knob may expose different report IDs/usages across USB, Bluetooth, and 2.4
  GHz modes.
- The device may not expose vendor-defined reports for LED/profile control.
- HID report decoding may require descriptor parsing beyond the first cut.

**Phases**:

1. Establish minimal Python CLI engineering harness and fake-backed tests.
2. Implement HID enumeration and capture.
3. Add fixture replay and best-effort normalization.
4. Document Anticater capture workflow and smoke evidence.

## Acceptance Criteria

1. Given the Anticater VK-01 is paired or connected, the CLI can list candidate
   HID interfaces with manufacturer, product, path, VID/PID where available,
   usage page, usage, and transport hints where available.
2. Given the user selects a candidate HID interface, the CLI can open it and
   print raw reports with timestamp, device identity, report ID, and data bytes.
3. Given the user performs rotate left, rotate right, click/mute,
   long-press+rotate left, and long-press+rotate right, the CLI can capture
   distinguishable raw report evidence for each operation or explicitly mark any
   operation that cannot be distinguished.
4. Given raw reports are captured, the CLI saves JSONL fixtures that can be
   replayed without physical hardware.
5. Given a fixture is replayed, the CLI emits the same best-effort normalized
   events as the capture path.
6. Given obvious consumer-control reports are observed, the CLI maps them to
   normalized events such as `volume_up`, `volume_down`, `mute_toggle`,
   `brightness_up`, `brightness_down`, or `unknown`.
7. Given a vendor-defined HID interface or output/feature reports are present,
   the CLI reports their existence as capabilities but does not attempt LED/RGB
   control in this baseline.
8. Given no compatible device is found or opening fails, the CLI exits with a
   clear diagnostic and does not crash.
9. Given tests run without hardware, fixture-backed fake HID readers prove
   parser, replay, and normalized event behavior.
10. Given documentation is read by a new user, README and `docs/how/` explain
    pairing, listing, capture, replay, fixture format, and LED/RGB limitations.

## Risks & Assumptions

- HID-first is research-supported but still must be verified against the actual
  device.
- The first implementation may need to treat reports as opaque until descriptor
  parsing is understood.
- Bluetooth mode may behave differently from USB or 2.4 GHz mode; differences
  should be captured as evidence, not hidden behind assumptions.
- Future ESP32 support depends on preserving transport-neutral events and not
  coupling core logic to Python/HIDAPI.

## Open Questions

No blocking open questions remain after Round 2.

## Workshop Opportunities

| Topic | Type | Why Workshop | Key Questions |
|---|---|---|---|
| Anticater HID descriptor and event schema | API Contract | Report IDs/usages may shape fixtures and normalized event contracts | Do we need descriptor parsing now? How do we represent unknown/vendor-defined reports? |
| Future LED/RGB reverse engineering | Integration Pattern | LED control is desirable but not publicly documented | What evidence would justify a separate reverse-engineering phase? |
| ESP32 migration contract | API Contract | Desktop prototype should not block embedded future | Which fields must be shared across desktop and firmware? |

## Clarifications

### Session 2026-06-05

| Question | Answer |
|---|---|
| Workflow Mode | Simple |
| Testing Strategy | Hybrid — TDD-style deterministic tests for parsing/normalization/fixtures; lightweight hardware smoke for real Anticater capture |
| Mock Usage | Fakes only; no mocks. Update project constitution and do not ask mock-policy questions again |
| Documentation Strategy | Hybrid — README + `docs/how/` |
| Domain Review | Keep proposed boundaries: device-input, cli-runtime, configuration, platform-adapter, future volume-policy, and future amplifier-control |
| Agent/Engineering Harness Readiness | Include Phase 0 for a minimal Python CLI engineering harness before Bluetooth capture implementation |
