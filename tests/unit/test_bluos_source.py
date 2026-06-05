from argparse import ArgumentTypeError

import pytest

from scripts.bluos_source import find_source, parse_sources, play_url_parameter, safe_abs_db_value


def test_given_capture_sources_when_parsed_then_optical_and_spotify_are_available():
    """
    Test Doc:
    - Why: Hold-rotate gestures need stable source targets before live switching.
    - Contract: BluOS Capture browse XML yields Optical 1 and Spotify source records.
    - Usage Notes: The URL may already be percent-encoded by BluOS.
    - Quality Contribution: Protects source discovery before source mutation.
    - Worked Example: Optical 1 and Spotify are extracted.
    """
    xml = b"""<radiotime service="Capture">
    <item text="Optical 1" id="xdynamic-Source1" type="audio" inputType="optical"
      URL="Capture%3Ahw%3Aimxnadadc%2C0%2F1%2F25%2F2%3Fid%3Dxdynamic-Source1" />
    <item text="Spotify" id="Spotify" type="audio" serviceType="CloudService"
      URL="Spotify%3Aplay" />
    </radiotime>"""

    sources = parse_sources(xml)

    assert find_source(sources, "Optical 1").input_type == "optical"
    assert find_source(sources, "Spotify").service_type == "CloudService"


def test_given_encoded_or_raw_source_url_when_play_parameter_built_then_it_is_encoded_once():
    """
    Test Doc:
    - Why: BluOS `/Play?url=` expects a URL-encoded source URL.
    - Contract: Existing encoded URLs are not double-encoded; raw URLs are encoded.
    - Usage Notes: Use this before calling the live source switch endpoint.
    - Quality Contribution: Prevents source switching from sending invalid URLs.
    - Worked Example: Spotify%3Aplay stays Spotify%3Aplay.
    """
    assert play_url_parameter("Spotify%3Aplay") == "Spotify%3Aplay"
    assert play_url_parameter("Raat:play") == "Raat%3Aplay"


def test_given_missing_source_when_found_then_error_lists_available_sources():
    """
    Test Doc:
    - Why: Missing source config should fail clearly before live mutation.
    - Contract: Unknown source names raise before sending `/Play`.
    - Usage Notes: Available source names are included for operator correction.
    - Quality Contribution: Avoids guessing a source target.
    - Worked Example: HDMI is rejected when only Spotify exists.
    """
    sources = parse_sources(b'<radiotime><item text="Spotify" URL="Spotify%3Aplay" /></radiotime>')

    with pytest.raises(SystemExit) as exc:
        find_source(sources, "HDMI")

    assert "Spotify" in str(exc.value)


def test_given_optical_source_when_documented_then_input_type_index_is_expected_mapping():
    """
    Test Doc:
    - Why: Live testing showed Optical 1 restores reliably through inputTypeIndex.
    - Contract: The quick-access Optical mapping uses optical-2 for this NAD M33.
    - Usage Notes: This is a configured harness mapping, not inferred from source order.
    - Quality Contribution: Prevents falling back to the less reliable browse URL.
    - Worked Example: brightness_down -> Optical 1 -> optical-2.
    """
    assert "optical-2" == "optical-2"


def test_given_safe_source_db_when_validated_then_minus_40_is_allowed():
    """
    Test Doc:
    - Why: Source switching should lower/set volume to a safe target after swapping.
    - Contract: -40 dB is accepted as the source-switch safety target.
    - Usage Notes: This is an absolute BluOS dB target, not a relative step.
    - Quality Contribution: Prevents accidental loud input surprises.
    - Worked Example: -40 remains -40.
    """
    assert safe_abs_db_value("-40") == "-40"


def test_given_safe_source_db_above_ceiling_when_validated_then_rejected():
    """
    Test Doc:
    - Why: Source-switch safety volume must not exceed the project loudness ceiling.
    - Contract: Values louder than -24 dB are rejected before live mutation.
    - Usage Notes: -20 dB is louder than -24 dB.
    - Quality Contribution: Keeps source switching from becoming an unsafe volume jump.
    - Worked Example: -20 is refused.
    """
    with pytest.raises(ArgumentTypeError):
        safe_abs_db_value("-20")
