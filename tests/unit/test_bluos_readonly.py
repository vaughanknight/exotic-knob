from scripts.bluos_readonly import parse_bluos_xml, summarize


def test_given_status_xml_when_summarized_then_volume_and_input_fields_are_extracted():
    """
    Test Doc:
    - Why: The read-only BluOS harness should prove status parsing without live NAD calls.
    - Contract: `/Status` XML yields volume, dB, mute, input, and sync fields.
    - Usage Notes: Use fake XML fixtures before live harness probes.
    - Quality Contribution: Prevents parser drift before amplifier-control implementation.
    - Worked Example: Optical 1 at volume 54 and -48 dB is extracted.
    """
    xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <status etag="abc"><db>-48</db><inputTypeIndex>optical-2</inputTypeIndex>
    <mute>0</mute><service>Capture</service><state>stream</state>
    <syncStat>1726</syncStat><title1>Optical 1</title1><volume>54</volume></status>"""

    summary = summarize(parse_bluos_xml("Status", xml))

    assert summary["volume"] == "54"
    assert summary["db"] == "-48"
    assert summary["mute"] == "0"
    assert summary["inputTypeIndex"] == "optical-2"
    assert summary["syncStat"] == "1726"


def test_given_syncstatus_xml_when_summarized_then_player_identity_is_extracted():
    """
    Test Doc:
    - Why: `/SyncStatus` is the preferred read-only volume/group status endpoint.
    - Contract: Root attributes yield player identity, firmware, volume, and dB state.
    - Usage Notes: Use this for `bluos-doctor` because it is compact and safe.
    - Quality Contribution: Protects the harness from treating XML as JSON.
    - Worked Example: NAD M33 Lounge Music is extracted.
    """
    xml = (
        b'<SyncStatus etag="1726" syncStat="1726" version="4.16.6" '
        b'id="192.168.1.67:11000" db="-48" volume="54" name="Lounge Music" '
        b'model="M33" modelName="M33" brand="NAD"></SyncStatus>'
    )

    summary = summarize(parse_bluos_xml("SyncStatus", xml))

    assert summary["name"] == "Lounge Music"
    assert summary["brand"] == "NAD"
    assert summary["model"] == "M33"
    assert summary["version"] == "4.16.6"
    assert summary["volume"] == "54"


def test_given_volume_xml_when_summarized_then_no_side_effect_command_is_needed():
    """
    Test Doc:
    - Why: The first BluOS harness must be read-only to avoid speaker surprises.
    - Contract: `/Volume` without parameters returns current level, dB, mute, and etag.
    - Usage Notes: Do not add volume-up/down harness commands before safety policy exists.
    - Quality Contribution: Keeps current-volume observation separate from mutation.
    - Worked Example: <volume db="-48" mute="0">54</volume> is summarized.
    """
    xml = b'<volume db="-48" offsetDb="0" mute="0" etag="abc">54</volume>'

    summary = summarize(parse_bluos_xml("Volume", xml))

    assert summary == {
        "endpoint": "Volume",
        "volume": "54",
        "db": "-48",
        "mute": "0",
        "etag": "abc",
        "offsetDb": "0",
    }

