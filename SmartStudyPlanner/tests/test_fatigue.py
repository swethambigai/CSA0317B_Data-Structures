import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from app.scheduler.fatigue_calculator import (
    calculate_fatigue_score,
    get_fatigue_level
)


def test_fatigue_score_calculation():
    score = calculate_fatigue_score(
        hours_studied=2,
        continuous_sessions=1,
        difficulty=2,
        breaks_taken=2,
        sleep_hours=8
    )

    expected = (
        (2 * 2)
        + (1 * 1.5)
        + (2 * 1)
        - (2 * 2)
        - (8 * 1.5)
    )

    assert score == expected


def test_normal_fatigue_level():
    assert get_fatigue_level(5) == "Normal"


def test_mild_fatigue_level():
    assert get_fatigue_level(8) == "Mild fatigue"


def test_high_fatigue_level():
    assert get_fatigue_level(13) == "High fatigue"


def test_critical_fatigue_level():
    assert get_fatigue_level(16) == "Critical"


def test_boundary_normal():
    assert get_fatigue_level(0) == "Normal"


def test_boundary_mild():
    assert get_fatigue_level(6) == "Mild fatigue"


def test_boundary_high():
    assert get_fatigue_level(11) == "High fatigue"


def test_boundary_critical():
    assert get_fatigue_level(15.1) == "Critical"


def test_high_fatigue_triggers_health_mode():
    score = 14

    level = get_fatigue_level(score)

    assert level == "High fatigue"

    