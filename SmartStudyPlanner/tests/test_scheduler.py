import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from app.scheduler.study_scheduler import StudyScheduler


def test_scheduler_creation():
    scheduler = StudyScheduler()

    assert scheduler is not None


def test_add_topic():
    scheduler = StudyScheduler()

    scheduler.add_topic(
        "Mathematics",
        difficulty=3,
        priority=2
    )

    assert scheduler.topic_count() == 1


def test_multiple_topics():
    scheduler = StudyScheduler()

    scheduler.add_topic(
        "Mathematics",
        difficulty=3,
        priority=3
    )

    scheduler.add_topic(
        "English",
        difficulty=1,
        priority=1
    )

    scheduler.add_topic(
        "Physics",
        difficulty=2,
        priority=2
    )

    assert scheduler.topic_count() == 3


def test_generate_schedule():
    scheduler = StudyScheduler()

    scheduler.add_topic(
        "Mathematics",
        difficulty=3,
        priority=3
    )

    scheduler.add_topic(
        "English",
        difficulty=1,
        priority=1
    )

    schedule = scheduler.generate_schedule()

    assert isinstance(schedule, list)
    assert len(schedule) == 2


def test_high_priority_topic_first():
    scheduler = StudyScheduler()

    scheduler.add_topic(
        "Low Priority",
        difficulty=1,
        priority=1
    )

    scheduler.add_topic(
        "High Priority",
        difficulty=3,
        priority=3
    )

    schedule = scheduler.generate_schedule()

    assert schedule[0]["title"] == "High Priority"