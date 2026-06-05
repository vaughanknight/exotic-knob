from decimal import Decimal

import pytest

from scripts.bluos_volume_step import assert_safe_step, planned_db_after


def test_given_volume_down_when_planned_then_max_db_does_not_block_decrease():
    """
    Test Doc:
    - Why: Turning volume down should remain safe even with a configured max dB.
    - Contract: Negative dB steps are allowed and compute the expected post-step dB.
    - Usage Notes: Live commands still require the explicit mutation flag.
    - Quality Contribution: Guards safe down-step behavior before live amplifier calls.
    - Worked Example: -48 + -1 = -49.
    """
    assert assert_safe_step(Decimal("-48"), Decimal("-1"), Decimal("-24")) == Decimal("-49")


def test_given_volume_up_below_max_when_planned_then_step_is_allowed():
    """
    Test Doc:
    - Why: Small volume-up tests should be possible when far below the safety ceiling.
    - Contract: Positive dB steps are allowed only when the planned result is <= max dB.
    - Usage Notes: -47 dB is quieter than the -24 dB ceiling, so it is allowed.
    - Quality Contribution: Proves the live one-step-up test is bounded.
    - Worked Example: -48 + 1 = -47 <= -24.
    """
    assert assert_safe_step(Decimal("-48"), Decimal("1"), Decimal("-24")) == Decimal("-47")


def test_given_volume_up_would_exceed_max_when_planned_then_step_is_refused():
    """
    Test Doc:
    - Why: The harness must prevent speaker-surprising volume increases.
    - Contract: A positive step that would exceed max dB exits before sending a command.
    - Usage Notes: The comparison is in dB, where -23 is louder than -24.
    - Quality Contribution: Enforces the safety ceiling requested before live mutation.
    - Worked Example: -24 + 1 is refused.
    """
    with pytest.raises(SystemExit):
        assert_safe_step(Decimal("-24"), Decimal("1"), Decimal("-24"))


def test_given_decimal_step_when_planned_then_decimal_precision_is_preserved():
    """
    Test Doc:
    - Why: BluOS volume responses may include decimal dB values.
    - Contract: Planning uses Decimal arithmetic rather than floats.
    - Usage Notes: Keep command values as strings at the HTTP boundary.
    - Quality Contribution: Avoids rounding surprises near the max dB ceiling.
    - Worked Example: -48.5 + 0.5 = -48.0.
    """
    assert planned_db_after(Decimal("-48.5"), Decimal("0.5")) == Decimal("-48.0")

