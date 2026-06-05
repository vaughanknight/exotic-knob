# Research Report: Bluetooth Input Baseline

**Generated**: 2026-06-04T23:52:30Z  
**Research Query**: "let's create a baseline to get the input from the bluetooth device. we will want to run this on esp32 possibly in future, for now it's on my mac (or a pc) via CLI, we'll need to do some technology choices and simple is best, this is unlikely to be a complex app, but i do want to be mindful of battery consumption etc for when we go to esp32, it won't be running often (when volume is changed) but it will be running all the time. First cut can just be a basic CLI that outputs when it gets the messages from the device, selects the device etc"  
**Mode**: Pre-Plan  
**Location**: `docs/plans/001-bluetooth-input-baseline/research-dossier.md`  
**FlowSpace**: Not Available  
**Findings**: 76 raw scout findings synthesized

## Executive Summary

### What It Does

This feature starts the project with a desktop CLI baseline that can discover or
select a Bluetooth volume knob and print incoming device messages/events. It is
not yet the full amplifier-control daemon; it is the evidence-gathering layer
that will reveal what the knob actually emits.

### Business Purpose

The baseline reduces uncertainty before the daemon and NAD M33 BluOS control
layers are built. It lets the project choose a simple technology path for macOS
and PC while preserving future options for ESP32 and low-power always-on use.

### Key Insights

1. There is no implementation yet; the repo currently contains doctrine and this
   active plan only, so all technology choices are still open.
2. The project doctrine already gives strong boundaries: Bluetooth adapter,
   deterministic normalized event contract, pure volume policy, BluOS adapter,
   configuration, and daemon runtime.
3. The immediate CLI should focus on raw capture plus normalized-event output,
   not amplifier control, so the first implementation can validate the device
   contract safely.

### Quick Stats

- **Components**: 0 source files; 4 doctrine files; 1 active flow plan folder.
- **Dependencies**: 0 declared dependencies; runtime/Bluetooth stack undecided.
- **Test Coverage**: No tests yet; testing doctrine is already defined.
- **Complexity**: Medium, driven by external Bluetooth/platform unknowns.
- **Prior Learnings**: 0 relevant discoveries; no prior implementation corpus.
- **Domains**: No domain system; 6 potential domains identified.

## How It Currently Works

### Entry Points

No code entry points exist yet.

| Entry Point | Type | Location | Purpose |
|---|---|---|---|
| Active flow state | Plan metadata | `docs/plans/001-bluetooth-input-baseline/.the-flow-state.json` | Tracks research-first planning state |
| Original ask | Plan input | `docs/plans/001-bluetooth-input-baseline/original-ask.md` | Captures the requested Bluetooth CLI baseline |
| Architecture doctrine | Governance | `docs/project-rules/architecture.md` | Defines intended daemon/adapters/policy boundaries |

### Core Execution Flow

The intended future flow is defined by doctrine, not code:

1. **Bluetooth Adapter**: Connect to the configured knob and translate raw
   Bluetooth events into normalized knob events.
   - Reference: `docs/project-rules/architecture.md`
2. **Volume Policy**: Convert normalized events into safe volume intents.
   - Reference: `docs/project-rules/architecture.md`
3. **BluOS Adapter**: Send bounded commands to the NAD M33.
   - Reference: `docs/project-rules/architecture.md`

The first cut should exercise only the first step and print both raw and
normalized event information where feasible.

### Data Flow

```mermaid
graph LR
    A[Bluetooth knob] --> B[Desktop CLI Bluetooth adapter]
    B --> C[Raw device event]
    C --> D[Normalized knob event]
    D --> E[stdout/log output]
```

### State Management

State is not implemented yet. The first baseline likely needs only ephemeral
runtime state:

- selected device identity
- connection status
- last raw event
- last normalized event
- optional event counter or ordering token

Persistent configuration should wait until the device contract and runtime stack
are chosen.

## Architecture & Design

### Component Map

#### Current Documentation Components

- **Constitution**: `docs/project-rules/constitution.md`
  - Responsibility: safety-first principles, deterministic mapping, daemon
    resilience, explicit configuration, adapter boundaries.
- **Rules**: `docs/project-rules/rules.md`
  - Responsibility: enforceable coding/testing rules.
- **Architecture**: `docs/project-rules/architecture.md`
  - Responsibility: high-level daemon, adapter, contract, and failure-mode map.
- **Idioms**: `docs/project-rules/idioms.md`
  - Responsibility: adapter-core-adapter flow, safe volume policy, config,
    observability, testing idioms.

### Design Patterns Identified

1. **Ports and Adapters**
   - Bluetooth and BluOS integrations must sit behind adapters.
   - Core policy must be plain-data and deterministic.
2. **Capture Before Control**
   - First implementation should discover device behavior without sending
     amplifier commands.
3. **Fake/Fixture First**
   - Tests should use simulated Bluetooth events and fixtures before hardware
     smoke checks.
4. **Configuration Boundary**
   - Device identity and safe limits should be configuration once behavior
     moves beyond exploratory CLI capture.

### System Boundaries

- **Internal Boundary**: normalized knob event contract.
- **External Boundary**: Bluetooth host stack and physical knob.
- **Deferred Boundary**: BluOS/NAD amplifier control.
- **Future Boundary**: ESP32 firmware/runtime and low-power wake behavior.

## Dependencies & Integration

### What This Depends On

#### Internal Dependencies

| Dependency | Type | Purpose | Risk if Changed |
|---|---|---|---|
| Project doctrine | Required | Defines safety and architecture constraints | Medium; changes affect spec and design |
| Active flow plan | Required | Tracks SDD state | Low |

#### External Dependencies to Decide

| Dependency | Purpose | Criticality |
|---|---|---|
| Language/runtime | Implement CLI and future daemon | High |
| Bluetooth API/library | Discover/select knob and read events | High |
| Platform support | macOS now; PC likely Windows/Linux | High |
| Test framework | Deterministic event parser and adapter tests | Medium |
| ESP32 stack | Future battery-aware implementation path | Medium |

### What Depends on This

No code depends on this yet. Future work will depend on the device contract
discovered here:

- normalized event schema
- device identity strategy
- raw event capture examples
- platform Bluetooth capability notes

## Quality & Testing

### Current Test Coverage

- **Unit Tests**: none.
- **Integration Tests**: none.
- **E2E Tests**: none.
- **Gaps**: all implementation testing is future work.

### Test Strategy Analysis

The first implementation should create deterministic checks for:

1. parsing raw events into a normalized event representation
2. de-duplicating or tagging duplicate messages if the device emits them
3. validating CLI arguments/config once introduced
4. separating hardware smoke checks from automated tests

Hardware interaction should initially be documented as manual smoke evidence:

```text
select device -> connect -> turn knob -> observe raw event -> observe normalized event
```

### Known Issues & Technical Debt

| Issue | Severity | Location | Impact |
|---|---|---|---|
| No runtime/tooling selected | High | `docs/project-rules/architecture.md` | Blocks implementation plan |
| No Bluetooth stack selected | High | `docs/project-rules/architecture.md` | Blocks CLI design |
| No test harness | High | Repository root | Blocks deterministic validation |
| No engineering harness boot command | High | Repository root | Agents cannot validate runnable software yet |
| ESP32 power model unknown | Medium | Original ask | May influence abstractions |

### Performance and Power Characteristics

No measured characteristics exist. Future ESP32 constraints suggest the design
should avoid unnecessary polling and prefer event/notification-driven input where
the selected stack supports it.

## Modification Considerations

### Safe to Modify

1. **Plan artifacts**: The active plan folder is new and isolated.
2. **Doctrine TODOs**: Runtime, Bluetooth stack, and tooling TODOs are expected
   to be resolved by this planning flow.

### Modify with Caution

1. **Architecture boundaries**: Changing adapter/policy separation would affect
   the constitution and rules.
2. **Testing doctrine**: The project already requires deterministic tests and
   hardware-free defaults.

### Danger Zones

1. **Raw Bluetooth callback to amplifier command**
   - Doctrine explicitly identifies this as an anti-pattern.
2. **Hardcoded device identity**
   - The first exploratory CLI may accept a one-off argument, but durable daemon
     behavior needs explicit configuration.
3. **Default tests requiring hardware**
   - This would make validation fragile and block CI.

### Extension Points

1. **Bluetooth adapter contract**: add concrete implementation after stack choice.
2. **Normalized event schema**: define during first cut from captured evidence.
3. **Platform adapter**: later split macOS/Windows/Linux/ESP32 concerns.
4. **Volume policy**: later consume normalized events without knowing Bluetooth.

## Prior Learnings

No prior learnings found directly related to Bluetooth, CLI input capture, ESP32,
or daemon behavior.

Scanned:

- `docs/plans/**/tasks.md`: none present.
- `docs/plans/**/execution.log.md`: none present.
- `docs/harness/agents/**/*.retro.md`: none present.
- `docs/retros/*.md`: none present.

Compound activity: 0 entries surfaced; no compound retros exist yet.

## Domain Context

No domain registry found. Consider running `/plan-v2-extract-domain` once source
code exists and boundaries are concrete.

Potential domains identified:

| Proposed Domain | Evidence | Boundary |
|---|---|---|
| Device Input | Architecture Bluetooth Adapter section | Raw Bluetooth -> normalized knob event |
| Volume Policy | Architecture Volume Policy section | Normalized event -> bounded intent |
| Amplifier Control | Architecture BluOS Adapter section | Intent/result around NAD M33 |
| Configuration | Constitution and idioms | Device identity, safety limits, startup behavior |
| Daemon Runtime | Architecture runtime section | lifecycle, wiring, local status |
| Platform Adapter | Service manager TODO and ESP32 future | host-specific runtime/supervision/power |

## Critical Discoveries

### Critical Finding 01: No implementation substrate exists

**Impact**: Critical  
**Source**: IA-01, QT-01, DC-01  
**What**: There are no source files, manifests, tests, CI, or boot commands.  
**Why It Matters**: The next plan must include establishing minimal tooling and a
runnable CLI harness before feature work can be validated.  
**Required Action**: Treat runtime/tooling selection as part of the first phase.

### Critical Finding 02: Bluetooth stack choice is the central unknown

**Impact**: Critical  
**Source**: DC-06, IC-08, DE-10  
**What**: The repo does not yet know whether the knob behaves as HID, BLE/GATT,
or another Bluetooth profile.  
**Why It Matters**: This choice determines runtime, permissions, device
selection UX, and cross-platform feasibility.  
**Required Action**: Spec must require discovery/capture evidence before durable
daemon behavior.

### Critical Finding 03: Hardware must not become the default test dependency

**Impact**: High  
**Source**: QT-02, QT-05, PS-06  
**What**: Doctrine requires deterministic tests and hardware-free defaults.  
**Why It Matters**: The first cut can be exploratory, but durable logic must move
behind fakes/fixtures quickly.  
**Required Action**: Capture sample raw events as fixtures and test parsing or
normalization against them.

## Supporting Documentation

### Related Documentation

- `docs/project-rules/constitution.md`: project principles and safety rules.
- `docs/project-rules/rules.md`: enforceable testing and integration standards.
- `docs/project-rules/architecture.md`: daemon/adapters/contracts/failure modes.
- `docs/project-rules/idioms.md`: implementation patterns and examples.
- `docs/plans/001-bluetooth-input-baseline/original-ask.md`: feature intent.

### Historical Context

The repository was initialized with doctrine only. The first commit established
the project rules and architecture before any implementation choices were made.

## Recommendations

### If Modifying This System

1. Start with a minimal CLI, not a daemon.
2. Print raw event data and normalized event data if possible.
3. Avoid amplifier control in the first baseline.
4. Save representative raw events as fixtures once observed.
5. Keep runtime and Bluetooth code behind an adapter boundary from the first
   source file.

### If Extending This System

1. Add volume policy only after the input contract is known.
2. Add BluOS/NAD control only after safe volume clamping is testable.
3. Add daemon supervision only after the CLI behavior is stable.
4. Preserve an ESP32-friendly boundary by keeping platform-specific Bluetooth
   APIs out of core policy.

### If Refactoring This System

No refactoring exists yet. The main opportunity is to establish clean boundaries
up front: device input, policy, amplifier control, config, runtime.

## External Research Opportunities

The codebase could not answer these initially. The prompts below were run on
2026-06-05 and the results are saved under `external-research/`.

### Completed External Research Summary

1. **Desktop Bluetooth stack**:
   `external-research/desktop-bluetooth-input-stack.md`
   - Recommendation: HID-first, macOS-first Python CLI using HIDAPI.
   - Preserve raw HID reports as JSONL fixtures and normalize into a transport-
     neutral event model.
2. **ESP32 / battery path**:
   `external-research/esp32-battery-bluetooth-path.md`
   - Recommendation: keep the desktop prototype event-driven and
     transport-neutral; deep sleep is not compatible with always-listening
     Bluetooth.
3. **NAD M33 BluOS API**:
   `external-research/nad-m33-bluos-volume-api.md`
   - Recommendation: future BluOS adapter should use the local BluOS HTTP/XML
     API on port 11000 and treat dB as the canonical volume unit.
4. **Anticater VK-01 knob**:
   `external-research/anticater-vk01-knob.md`
   - Recommendation: treat the knob as a programmable HID macro/media device.
     Expect rotation/click/long-press mappings as HID keyboard/consumer events;
     defer LED/RGB control unless descriptor capture reveals a vendor-defined
     output or feature-report channel.

The original opportunities are retained below for traceability.

### Research Opportunity 1: Desktop Bluetooth input stack

**Why Needed**: The project needs a simple CLI on macOS and PC, but the device
profile is unknown.  
**Impact on Plan**: Determines implementation language/runtime and first-cut CLI
shape.  
**Source Findings**: DC-06, IC-08, DE-10

**Ready-to-use prompt:**

```text
/deepresearch "Research a simple cross-platform desktop CLI approach for reading events from a Bluetooth volume knob. Context: new project, macOS first and PC later, future ESP32 possible. Need to determine whether typical Bluetooth volume knobs expose HID consumer-control reports, BLE GATT notifications, or both; compare practical stacks for Node.js, Python, Go, Rust, and native OS tools; include macOS permission constraints, Windows/Linux feasibility, device discovery UX, event-driven vs polling behavior, and how to capture raw events for test fixtures. Recommend the simplest first-cut technology path and note risks."
```

**Results location**: `docs/plans/001-bluetooth-input-baseline/external-research/desktop-bluetooth-input-stack.md`
**Status**: Complete.

### Research Opportunity 2: ESP32 future path and battery model

**Why Needed**: The user wants to preserve an ESP32 path and be mindful of
always-on battery consumption.  
**Impact on Plan**: Influences whether abstractions should prefer BLE events,
sleep/wake patterns, and message schemas compatible with microcontroller code.  
**Source Findings**: IA-04, QT-07, DC-09

**Ready-to-use prompt:**

```text
/deepresearch "Research future ESP32 implementation considerations for a Bluetooth volume knob bridge that mostly idles and only acts when volume changes. Context: desktop CLI baseline first, future ESP32 possible. Compare ESP32 BLE central vs HID host feasibility, light sleep/deep sleep tradeoffs for always-listening Bluetooth, battery impact, event-driven design, reconnection behavior, and how to structure shared event/command contracts so a desktop prototype can migrate later. Recommend constraints the desktop CLI should preserve now."
```

**Results location**: `docs/plans/001-bluetooth-input-baseline/external-research/esp32-battery-bluetooth-path.md`
**Status**: Complete.

### Research Opportunity 3: NAD M33 BluOS volume API

**Why Needed**: Amplifier control is deferred, but the architecture already
depends on knowing BluOS volume semantics and safety limits.  
**Impact on Plan**: Helps avoid input-contract choices that are awkward for
future volume intent handling.  
**Source Findings**: DC-07, IC-04, DE-07

**Ready-to-use prompt:**

```text
/deepresearch "Research NAD M33 BluOS local control APIs for volume control. Context: future phase of a Bluetooth volume knob daemon. Identify discovery mechanisms, endpoints or protocols, volume range/units, relative vs absolute volume support, auth requirements, error behavior, rate limits, and safe integration patterns. Recommend what the current Bluetooth input baseline should log or preserve so later volume policy and BluOS adapter work is straightforward."
```

**Results location**: `docs/plans/001-bluetooth-input-baseline/external-research/nad-m33-bluos-volume-api.md`
**Status**: Complete.

## Appendix: File Inventory

### Core Files

| File | Purpose |
|---|---|
| `docs/project-rules/constitution.md` | Project principles and governance |
| `docs/project-rules/rules.md` | Enforceable rules and testing doctrine |
| `docs/project-rules/idioms.md` | Preferred patterns |
| `docs/project-rules/architecture.md` | Intended daemon architecture |
| `docs/plans/001-bluetooth-input-baseline/original-ask.md` | Captured user intent |
| `docs/plans/001-bluetooth-input-baseline/the-flow.json` | Flow source of truth |
| `docs/plans/001-bluetooth-input-baseline/the-flow.md` | Rendered flow view |

### Test Files

None yet.

### Configuration Files

None yet.

## Next Steps

Recommended path:

1. Run `/plan-1b-v3-specify-and-clarify`
   for the Bluetooth input baseline.
2. Expect the spec to resolve: runtime/language, supported desktop OS, raw-vs-
   normalized CLI output, device selection UX, hardware smoke test shape, and
   ESP32 constraints to preserve.

**Research Complete**: 2026-06-04T23:52:30Z  
**Report Location**: `docs/plans/001-bluetooth-input-baseline/research-dossier.md`
