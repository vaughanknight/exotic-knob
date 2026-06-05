# BluOS read-only harness

Use these commands to verify NAD/BluOS connectivity without changing amplifier
state:

```bash
just bluos-doctor 192.168.1.67
just bluos-status 192.168.1.67
just bluos-syncstatus 192.168.1.67
just bluos-volume 192.168.1.67
```

Or set the host once for a shell:

```bash
export BLUOS_HOST=192.168.1.67
just bluos-doctor
just bluos-status
just bluos-syncstatus
just bluos-volume
```

These commands only call read-only endpoints:

| Command | Endpoint | Side effects |
|---|---|---|
| `bluos-doctor` | `/SyncStatus` | None |
| `bluos-status` | `/Status` | None |
| `bluos-syncstatus` | `/SyncStatus` | None |
| `bluos-volume` | `/Volume` without parameters | None |

## Guarded one-step volume test

Live volume mutation is guarded by dB ceiling checks and an explicit mutation
acknowledgement inside the script. The harness currently exposes only one-step
test commands:

```bash
just bluos-step-down 192.168.1.67 1 -24
just bluos-step-up 192.168.1.67 1 -24
```

The third argument is the maximum allowed post-step dB. `-24` means the harness
will refuse any positive step that would make the amplifier louder than `-24 dB`.
Do not add unbounded volume commands.

## Guarded mute test

Mute tests use explicit on/off commands rather than a blind toggle:

```bash
just bluos-mute-off 192.168.1.67
just bluos-mute-on 192.168.1.67
```

`mute=0` means unmuted; `mute=1` means muted.

## Guarded source switching

Source discovery is read-only:

```bash
just bluos-sources 192.168.1.67
```

The current quick-access mapping is:

| Knob event | BluOS harness command | Source |
|---|---|---|
| `brightness_down` | `just bluos-source-optical 192.168.1.67` | Optical 1 via `inputTypeIndex=optical-2` |
| `brightness_up` | `just bluos-source-spotify 192.168.1.67` | Resume/start Spotify via `Spotify%3Aplay` |

These commands use explicit source names discovered from
`/RadioBrowse?service=Capture` and require an internal source-change
acknowledgement flag. Live testing showed Optical 1 restores reliably through
`/Play?inputTypeIndex=optical-2`; Spotify is not a passive input index on this
NAD. It uses the discovered `Spotify%3Aplay` URL and should be treated as
"resume Spotify".

Both source-switch commands also set the amplifier to **`-40 dB` absolute**
immediately after switching. This is a safety target to avoid blasting the room
if the selected source is unexpectedly loud. The command refuses safe targets
louder than `-24 dB`.
