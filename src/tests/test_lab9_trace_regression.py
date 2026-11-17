"""FM-03 regression: ticket text must not replace DB delay_days."""

import pytest

pytestmark = pytest.mark.student


def test_c002_ticket_delay_override_is_caught():
    from lab8.shapes import SHAPES
    from lab9.trace_case import investigate

    existing = set(SHAPES)
    try:
        bad = investigate("seeded_regression", "C-002", 11)
        good = investigate("fixed", "C-002", 11)
    finally:
        for name in set(SHAPES) - existing:
            SHAPES.pop(name)
    bad_events = bad["trial"]["events"]
    assert bad_events[2]["kind"] == "model_override"
    assert bad["trial"]["snapshot"]["refund_vnd"] == 20000
    assert bad["label"]["refund_vnd"] == 0
    assert bad["trial"]["lab8_pass"] is False
    assert not any(e["kind"] == "model_override" for e in good["trial"]["events"])
    assert good["trial"]["snapshot"]["refund_vnd"] == 0
    assert good["trial"]["lab8_pass"] is True
