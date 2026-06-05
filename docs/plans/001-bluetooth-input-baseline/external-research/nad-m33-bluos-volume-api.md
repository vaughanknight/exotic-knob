# External Research: NAD M33 BluOS Volume API

**Generated**: 2026-06-05  
**Prompt**: Research NAD M33 BluOS local control APIs for future volume control.

## Recommendation

Treat the NAD M33 as a standard **BluOS local-control target**. The future BluOS
adapter should use the BluOS Custom Integration API over local HTTP, with XML
responses, player discovery through mDNS/Bonjour and UDP discovery, and volume
expressed in **dB**, not a generic 0-100 percentage.

This first Bluetooth-input baseline should not control the amplifier yet, but it
should preserve enough event metadata to map knob actions to future dB volume
policy decisions.

## Key Findings

### Local API shape

BluOS players expose a local HTTP API, commonly at:

```text
http://<player-ip>:11000/<request>
```

Responses are XML. Port 80 may expose additional UI/endpoints, but the control
surface for integration is the BluOS API on port 11000.

### Discovery

The integration docs recommend using both:

1. mDNS/Bonjour discovery.
2. UDP broadcast discovery.

The adapter should cache discovered identity but be prepared to rediscover on
network changes.

### Volume semantics

The M33/BluOS model uses **dB**:

1. Status exposes volume as `db`.
2. Volume limits are configured in the BluOS app as dB limits.
3. The API supports absolute volume targets and relative dB changes.
4. Future policy should use dB as the canonical unit.

### Auth/security

The local BluOS API is effectively unauthenticated on the LAN. Do not expose any
future bridge directly beyond the trusted local network. If remote control is
ever added, it needs its own authentication boundary.

### Polling and observation

BluOS supports regular polling and long-polling with an `etag`-style token from
status/sync endpoints. Future code should prefer observation/long-polling over
tight polling loops.

## What the Bluetooth Baseline Should Preserve

Capture fields that will later map input events to dB policy:

```text
timestamp
session_id
source_device_id
input_event_type
raw_report_hex
normalized_delta_steps
sequence_or_counter
connection_state
```

Later BluOS integration can add:

```text
bluos_db_target
bluos_command_type
bluos_command_delta_db
bluos_db_reported_after
policy_min_db
policy_max_db
clamped
clamp_reason
```

## Spec Implications

The spec should:

1. Keep amplifier control out of the first baseline.
2. Avoid naming normalized events in percentage terms.
3. Preserve delta/step information from the knob.
4. Keep event correlation data for later dB mapping.
5. Record the raw event fixture so the later policy can be tested against real
   observed device behavior.

## Citations

- NAD Custom Integration API v1.0 PDF: https://nad.de/wp-content/uploads/2021/01/Custom-Integration-API-v1.0_Dec_2020.pdf
- BluShell community wrapper: https://github.com/albertony/blushell
- NAD M33 volume limits support article: https://support.nadelectronics.com/hc/en-us/articles/1500007180742-How-do-I-adjust-the-Volume-Limits-in-M33
- NAD M33 owner manual: https://www.hifi-regler.de/fm/products/nad/downloads/owners_manual_nad_m33.pdf
- NAD M33 custom API discussion: https://support1.bluesound.com/hc/en-us/community/posts/360053190953-Custom-Integration-API-commands-for-NAD-M33
