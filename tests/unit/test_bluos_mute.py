import pytest

from scripts.bluos_mute import mute_value


def test_given_mute_on_when_converted_then_bluos_value_is_one():
    """
    Test Doc:
    - Why: BluOS uses explicit mute values, not a toggle command.
    - Contract: `on` maps to `/Volume?mute=1`.
    - Usage Notes: Use explicit state to avoid blind toggles.
    - Quality Contribution: Prevents inverted mute behavior against the amplifier.
    - Worked Example: on -> 1.
    """
    assert mute_value("on") == "1"


def test_given_mute_off_when_converted_then_bluos_value_is_zero():
    """
    Test Doc:
    - Why: BluOS mute-off must be explicit before testing mute-on.
    - Contract: `off` maps to `/Volume?mute=0`.
    - Usage Notes: Use explicit state to make readback expectations clear.
    - Quality Contribution: Prevents unsafe assumptions about current mute state.
    - Worked Example: off -> 0.
    """
    assert mute_value("off") == "0"


def test_given_unknown_mute_state_when_converted_then_rejected():
    """
    Test Doc:
    - Why: Live mute harness should only expose known safe states.
    - Contract: Unsupported state names are rejected before any HTTP request.
    - Usage Notes: CLI argparse also restricts choices.
    - Quality Contribution: Prevents malformed live BluOS commands.
    - Worked Example: toggle is rejected.
    """
    with pytest.raises(ValueError):
        mute_value("toggle")

