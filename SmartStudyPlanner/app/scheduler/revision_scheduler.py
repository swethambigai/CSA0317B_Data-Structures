"""
SmartStudyPlanner - Revision Scheduler

Purpose:
    Manages spaced repetition and revision scheduling.

Data structures used:
    - RevisionStack
    - RevisionLinkedList

Revision intervals:
    Cycle 1 -> 1 day
    Cycle 2 -> 3 days
    Cycle 3 -> 7 days
    Cycle 4 -> 14 days
    Cycle 5 -> 30 days
"""


from datetime import date, timedelta

from app.datastructures.stack import RevisionStack
from app.datastructures.linked_list import (
    RevisionLinkedList
)


class RevisionScheduler:
    """Manages spaced repetition."""

    def __init__(self):

        self.revision_stack = (
            RevisionStack()
        )

        self.revision_history = (
            RevisionLinkedList()
        )

        self.revision_intervals = {
            1: 1,
            2: 3,
            3: 7,
            4: 14,
            5: 30
        }

        self.revision_tasks = []

    # ---------------------------------------------------------
    # CALCULATE NEXT DATE
    # ---------------------------------------------------------

    def calculate_next_revision(
        self,
        revision_number,
        revision_date=None
    ):
        """
        Calculate the next revision date.

        Example:

            Revision 1
            + 1 day
            = Revision 2
        """

        if revision_date is None:
            revision_date = date.today()

        if isinstance(
            revision_date,
            str
        ):

            revision_date = date.fromisoformat(
                revision_date
            )

        interval = self.revision_intervals.get(
            revision_number,
            30
        )

        return revision_date + timedelta(
            days=interval
        )

    # ---------------------------------------------------------
    # ADD COMPLETED TOPIC
    # ---------------------------------------------------------

    def add_completed_topic(
        self,
        topic,
        completed_date=None
    ):
        """
        Add a completed topic to the revision system.

        The topic starts at Revision Cycle 1.
        """

        if completed_date is None:

            completed_date = date.today()

        if isinstance(
            completed_date,
            str
        ):

            completed_date = date.fromisoformat(
                completed_date
            )

        next_revision = (
            self.calculate_next_revision(
                1,
                completed_date
            )
        )

        record = {

            "name": (
                topic.get(
                    "name",
                    "Unnamed Topic"
                )
                if isinstance(topic, dict)
                else str(topic)
            ),

            "topic": topic,

            "revision_number": 1,

            "completed_date": (
                completed_date.isoformat()
            ),

            "next_revision": (
                next_revision.isoformat()
            ),

            "status": "Scheduled"
        }

        self.revision_stack.push(
            record
        )

        self.revision_history.append(
            topic,
            1,
            next_revision.isoformat()
        )

        self.revision_tasks.append(
            record
        )

        return record

    # ---------------------------------------------------------
    # COMPLETE REVISION
    # ---------------------------------------------------------

    def complete_revision(
        self,
        topic_name,
        completed_date=None
    ):
        """
        Complete a revision and schedule
        the next revision cycle.
        """

        if completed_date is None:

            completed_date = date.today()

        if isinstance(
            completed_date,
            str
        ):

            completed_date = date.fromisoformat(
                completed_date
            )

        target = None

        for task in self.revision_tasks:

            if (
                task["name"] == topic_name
                and task["status"] == "Scheduled"
            ):

                target = task
                break

        if target is None:
            return None

        current_cycle = (
            target["revision_number"]
        )

        next_cycle = current_cycle + 1

        next_revision = (
            self.calculate_next_revision(
                current_cycle,
                completed_date
            )
        )

        target["status"] = "Completed"

        new_record = {

            "name": topic_name,

            "topic": target["topic"],

            "revision_number": next_cycle,

            "completed_date": (
                completed_date.isoformat()
            ),

            "next_revision": (
                next_revision.isoformat()
            ),

            "status": "Scheduled"
        }

        self.revision_stack.push(
            new_record
        )

        self.revision_history.complete_revision(
            target["topic"],
            current_cycle,
            next_revision.isoformat()
        )

        self.revision_tasks.append(
            new_record
        )

        return new_record

    # ---------------------------------------------------------
    # GET DUE REVISIONS
    # ---------------------------------------------------------

    def get_due_revisions(
        self,
        current_date=None
    ):
        """
        Return all revisions that are due today
        or overdue.
        """

        if current_date is None:

            current_date = date.today()

        if isinstance(
            current_date,
            str
        ):

            current_date = date.fromisoformat(
                current_date
            )

        due = []

        for task in self.revision_tasks:

            if task["status"] != "Scheduled":
                continue

            revision_date = date.fromisoformat(
                task["next_revision"]
            )

            if revision_date <= current_date:

                due.append(task)

        return due

    # ---------------------------------------------------------
    # UPCOMING REVISIONS
    # ---------------------------------------------------------

    def get_upcoming_revisions(
        self,
        days=7,
        current_date=None
    ):
        """
        Return revisions scheduled within
        the next number of days.
        """

        if current_date is None:

            current_date = date.today()

        if isinstance(
            current_date,
            str
        ):

            current_date = date.fromisoformat(
                current_date
            )

        end_date = (
            current_date +
            timedelta(days=days)
        )

        upcoming = []

        for task in self.revision_tasks:

            if task["status"] != "Scheduled":
                continue

            revision_date = date.fromisoformat(
                task["next_revision"]
            )

            if (
                current_date
                <= revision_date
                <= end_date
            ):

                upcoming.append(task)

        return upcoming

    # ---------------------------------------------------------
    # REVISION COUNT
    # ---------------------------------------------------------

    def get_revision_count(
        self,
        topic_name
    ):
        """Return number of revision cycles."""

        count = 0

        for task in self.revision_tasks:

            if task["name"] == topic_name:

                count += 1

        return count

    # ---------------------------------------------------------
    # REVISION PROGRESS
    # ---------------------------------------------------------

    def get_revision_progress(
        self,
        topic_name
    ):
        """
        Return revision progress for a topic.
        """

        count = self.get_revision_count(
            topic_name
        )

        if count >= 5:

            percentage = 100

        else:

            percentage = (
                count / 5
            ) * 100

        return {
            "topic": topic_name,
            "cycles_completed": count,
            "target_cycles": 5,
            "progress": round(
                percentage,
                2
            )
        }

    # ---------------------------------------------------------
    # GET ALL TASKS
    # ---------------------------------------------------------

    def get_all_tasks(self):
        """Return all revision tasks."""

        return self.revision_tasks.copy()

    # ---------------------------------------------------------
    # GET HISTORY
    # ---------------------------------------------------------

    def get_history(self):
        """Return linked-list revision history."""

        return self.revision_history.get_all()

    # ---------------------------------------------------------
    # DISPLAY
    # ---------------------------------------------------------

    def display(self):
        """Return revision tasks as readable text."""

        if not self.revision_tasks:

            return "No revision tasks scheduled."

        result = []

        for task in self.revision_tasks:

            result.append(
                f"{task['name']} | "
                f"Cycle {task['revision_number']} | "
                f"Next: {task['next_revision']} | "
                f"{task['status']}"
            )

        return "\n".join(result)
    