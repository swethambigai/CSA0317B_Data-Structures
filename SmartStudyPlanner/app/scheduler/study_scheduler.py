"""
SmartStudyPlanner - Study Scheduler

Purpose:
    Creates an intelligent study schedule.

Uses:
    - StudyQueue
    - PriorityQueue
    - FatigueCalculator
    - HealthMaintenanceMode

Scheduling behavior:
    Normal:
        Normal study workload.

    Mild fatigue:
        Extra breaks.

    High fatigue:
        Reduced workload and difficult topics postponed.

    Critical fatigue:
        Health Maintenance Mode.
        Only light revision and limited study time.
"""


from app.datastructures.queue import StudyQueue
from app.datastructures.priority_queue import PriorityQueue
from app.scheduler.fatigue_calculator import (
    FatigueCalculator
)
from app.scheduler.health_mode import (
    HealthMaintenanceMode
)


class StudyScheduler:
    """Creates and manages the student's study schedule."""

    def __init__(self):

        self.study_queue = StudyQueue()

        self.priority_queue = PriorityQueue()

        self.fatigue_calculator = (
            FatigueCalculator()
        )

        self.health_mode = (
            HealthMaintenanceMode(
                fatigue_calculator=self.fatigue_calculator,
                study_queue=self.study_queue
            )
        )

        self.schedule = []

    # ---------------------------------------------------------
    # ADD TOPIC
    # ---------------------------------------------------------

    def add_topic(
        self,
        name,
        subject="General",
        difficulty="Medium",
        duration=60,
        urgency=0,
        deadline_days=None,
        revision_due=False,
        priority=None,
        **kwargs
    ):
        """
        Add a study topic.

        Example:

            scheduler.add_topic(
                "Binary Trees",
                subject="Data Structures",
                difficulty="Hard",
                duration=90,
                urgency=4,
                deadline_days=2,
                priority=3
            )
        """

        title = kwargs.get("title", name)

        topic = {
            "name": name,
            "title": title or name,
            "subject": subject,
            "subject_name": subject,
            "difficulty": difficulty,
            "duration": duration,
            "estimated_minutes": duration,
            "urgency": urgency,
            "priority": priority,
            "deadline_days": deadline_days,
            "revision_due": revision_due,
            "status": kwargs.get("status", "Pending")
        }

        for k, v in kwargs.items():
            if k not in topic:
                topic[k] = v

        self.study_queue.enqueue(topic)

        self.priority_queue.enqueue(topic, priority=priority)

        return topic

    # ---------------------------------------------------------
    # ADD MULTIPLE TOPICS
    # ---------------------------------------------------------

    def add_topics(self, topics):
        """Add multiple topics."""

        for topic in topics:

            self.add_topic(
                name=topic.get(
                    "name",
                    "Unnamed Topic"
                ),
                subject=topic.get(
                    "subject",
                    "General"
                ),
                difficulty=topic.get(
                    "difficulty",
                    "Medium"
                ),
                duration=topic.get(
                    "duration",
                    60
                ),
                urgency=topic.get(
                    "urgency",
                    0
                ),
                deadline_days=topic.get(
                    "deadline_days"
                ),
                revision_due=topic.get(
                    "revision_due",
                    False
                )
            )

    # ---------------------------------------------------------
    # SET FATIGUE
    # ---------------------------------------------------------

    def set_fatigue(
        self,
        hours_studied,
        continuous_sessions,
        difficulty,
        breaks,
        sleep_hours
    ):
        """
        Update the student's fatigue information.
        """

        return self.fatigue_calculator.update(
            hours_studied=hours_studied,
            continuous_sessions=continuous_sessions,
            difficulty=difficulty,
            breaks=breaks,
            sleep_hours=sleep_hours
        )

    # ---------------------------------------------------------
    # SORT BY PRIORITY
    # ---------------------------------------------------------

    def prioritize_topics(self):
        """
        Recalculate priorities and create a priority-based
        study order.
        """

        self.priority_queue.update_priorities()

        prioritized = []

        for item in self.priority_queue.get_all():

            prioritized.append(
                item["topic"]
            )

        return prioritized

    # ---------------------------------------------------------
    # CREATE NORMAL SCHEDULE
    # ---------------------------------------------------------

    def create_normal_schedule(
        self,
        available_minutes
    ):
        """
        Create a normal study schedule.

        Topics are selected according to priority.
        """

        available_minutes = int(
            available_minutes
        )

        schedule = []

        remaining_time = available_minutes

        prioritized_topics = (
            self.prioritize_topics()
        )

        for topic in prioritized_topics:

            duration = int(
                topic.get(
                    "duration",
                    60
                )
            )

            if duration <= remaining_time:

                schedule.append(topic)

                remaining_time -= duration

        return schedule

    # ---------------------------------------------------------
    # CREATE FATIGUE-AWARE SCHEDULE
    # ---------------------------------------------------------

    def create_schedule(
        self,
        available_minutes
    ):
        """
        Create a schedule based on fatigue.

        This is the main scheduling function.
        """

        fatigue = (
            self.fatigue_calculator.analyze()
        )

        score = fatigue["score"]

        mode = self.health_mode.evaluate(
            score
        )

        # -----------------------------------------------------
        # NORMAL
        # -----------------------------------------------------

        if mode == "Normal":

            schedule = self.create_normal_schedule(
                available_minutes
            )

        # -----------------------------------------------------
        # MILD FATIGUE
        # -----------------------------------------------------

        elif mode == "Mild Fatigue":

            schedule = self.create_normal_schedule(
                available_minutes
            )

        # -----------------------------------------------------
        # HIGH FATIGUE
        # -----------------------------------------------------

        elif mode == "High Fatigue":

            self.health_mode.postpone_difficult_topics()

            limited_minutes = min(
                int(available_minutes),
                180
            )

            schedule = self.create_normal_schedule(
                limited_minutes
            )

            schedule = [
                topic
                for topic in schedule
                if str(
                    topic.get(
                        "difficulty",
                        ""
                    )
                ).lower()
                not in (
                    "hard",
                    "critical"
                )
            ]

        # -----------------------------------------------------
        # CRITICAL FATIGUE
        # -----------------------------------------------------

        else:

            protection_plan = (
                self.health_mode.apply(
                    score
                )
            )

            light_topics = (
                protection_plan.get(
                    "light_revision_topics",
                    []
                )
            )

            schedule = []

            for topic in light_topics:

                if isinstance(
                    topic,
                    dict
                ):

                    schedule.append(topic)

        self.schedule = schedule

        return {
            "fatigue": fatigue,
            "mode": mode,
            "schedule": schedule,
            "health_plan": (
                self.health_mode.generate_protection_plan()
            )
        }

    # ---------------------------------------------------------
    # COMPLETE TOPIC
    # ---------------------------------------------------------

    def complete_topic(self, topic_name):
        """
        Mark a topic as completed.
        """

        for topic in self.study_queue.get_all():

            if (
                isinstance(topic, dict)
                and topic.get("name") == topic_name
            ):

                topic["status"] = "Completed"

                self.study_queue.move_to_end(
                    topic
                )

                self.priority_queue.remove(
                    topic
                )

                return topic

        return None

    # ---------------------------------------------------------
    # REMOVE TOPIC
    # ---------------------------------------------------------

    def remove_topic(self, topic):
        """Remove a topic from the study queue."""

        removed = self.study_queue.move_to_end(
            topic
        )

        self.priority_queue.remove(
            topic
        )

        return removed

    # ---------------------------------------------------------
    # GET PENDING TOPICS
    # ---------------------------------------------------------

    def get_pending_topics(self):
        """Return all pending study topics."""

        topics = []

        for topic in self.study_queue.get_all():

            if isinstance(topic, dict):

                if topic.get(
                    "status",
                    "Pending"
                ) != "Completed":

                    topics.append(topic)

            else:

                topics.append(topic)

        return topics

    # ---------------------------------------------------------
    # GET CURRENT SCHEDULE
    # ---------------------------------------------------------

    def get_schedule(self):
        """Return the current schedule."""

        return self.schedule.copy()

    # ---------------------------------------------------------
    # TOPIC COUNT
    # ---------------------------------------------------------

    def topic_count(self):
        """Return the total number of topics in the study queue."""

        return self.study_queue.size()

    # ---------------------------------------------------------
    # GENERATE SCHEDULE
    # ---------------------------------------------------------

    def generate_schedule(self, available_minutes=300):
        """
        Generate schedule and return the scheduled topics list.
        """

        result = self.create_schedule(available_minutes)

        if isinstance(result, dict):
            return result.get("schedule", [])

        return self.schedule.copy()
    