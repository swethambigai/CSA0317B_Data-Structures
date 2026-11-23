"""
SmartStudyPlanner - Health Maintenance Mode

Purpose:
    Automatically protects the student's study schedule
    when fatigue becomes high or critical.

Actions:
    Normal:
        Normal schedule.

    Mild:
        Add extra breaks.

    High:
        Reduce workload and postpone difficult topics.

    Critical:
        Activate Health Maintenance Mode.
        Allow only light revision.
        Postpone heavy topics.
        Add relaxation tasks.
        Limit study time.
"""


class HealthMaintenanceMode:
    """Controls automatic protection based on fatigue."""

    def __init__(
        self,
        fatigue_calculator=None,
        study_queue=None,
        revision_stack=None
    ):

        self.fatigue_calculator = (
            fatigue_calculator
        )

        self.study_queue = study_queue

        self.revision_stack = revision_stack

        self.active = False

        self.mode = "Normal"

        self.max_study_hours = None

        self.break_duration = 0

        self.relaxation_tasks = []

        self.postponed_topics = []

    # ---------------------------------------------------------
    # ACTIVATE
    # ---------------------------------------------------------

    def activate(self):
        """Activate Health Maintenance Mode."""

        self.active = True

        self.mode = "Health Maintenance Mode"

        self.max_study_hours = 2

        self.break_duration = 15

        self.relaxation_tasks = [
            "5-minute deep breathing",
            "10-minute stretching",
            "Drink water",
            "Take a short walk",
            "Rest your eyes"
        ]

        return True

    # ---------------------------------------------------------
    # DEACTIVATE
    # ---------------------------------------------------------

    def deactivate(self):
        """Return to normal study mode."""

        self.active = False

        self.mode = "Normal"

        self.max_study_hours = None

        self.break_duration = 0

        self.relaxation_tasks = []

        return True

    # ---------------------------------------------------------
    # EVALUATE
    # ---------------------------------------------------------

    def evaluate(self, fatigue_score):
        """
        Decide which mode should be used.

        Returns:
            Normal
            Mild Fatigue
            High Fatigue
            Health Maintenance Mode
        """

        if fatigue_score <= 5:

            self.deactivate()

            return "Normal"

        if fatigue_score <= 10:

            self.active = False

            self.mode = "Mild Fatigue"

            self.max_study_hours = None

            self.break_duration = 10

            return "Mild Fatigue"

        if fatigue_score <= 15:

            self.active = False

            self.mode = "High Fatigue"

            self.max_study_hours = 3

            self.break_duration = 15

            return "High Fatigue"

        self.activate()

        return "Health Maintenance Mode"

    # ---------------------------------------------------------
    # POSTPONE DIFFICULT TOPICS
    # ---------------------------------------------------------

    def postpone_difficult_topics(self):
        """
        Move hard and critical topics to the end
        of the study queue.
        """

        if self.study_queue is None:
            return []

        original_topics = (
            self.study_queue.get_all()
        )

        self.study_queue.postpone_difficult_topics()

        postponed = []

        for topic in original_topics:

            if isinstance(topic, dict):

                difficulty = str(
                    topic.get(
                        "difficulty",
                        ""
                    )
                ).lower()

                if difficulty in (
                    "hard",
                    "critical"
                ):

                    postponed.append(topic)

        self.postponed_topics = postponed

        return postponed

    # ---------------------------------------------------------
    # LIGHT REVISION
    # ---------------------------------------------------------

    def get_light_revision_topics(
        self,
        limit=2
    ):
        """
        Return only 1-2 revision topics.

        This implements the project's requirement:

            Stack:
            Only top 1-2 revision topics allowed.
        """

        if self.revision_stack is None:
            return []

        return self.revision_stack.health_mode_limit(
            limit
        )

    # ---------------------------------------------------------
    # RELAXATION TASKS
    # ---------------------------------------------------------

    def get_relaxation_tasks(self):
        """Return recommended relaxation activities."""

        if not self.active:

            return []

        return self.relaxation_tasks.copy()

    # ---------------------------------------------------------
    # STUDY LIMIT
    # ---------------------------------------------------------

    def get_study_limit(self):
        """
        Return the maximum recommended study time.
        """

        if self.active:
            return 2

        if self.mode == "High Fatigue":
            return 3

        return None

    # ---------------------------------------------------------
    # FULL PLAN
    # ---------------------------------------------------------

    def generate_protection_plan(self):
        """
        Generate the complete Health Maintenance plan.
        """

        if not self.active:

            return {
                "active": False,
                "mode": self.mode,
                "max_study_hours": self.max_study_hours,
                "break_duration": self.break_duration,
                "light_revision_only": False,
                "postponed_topics": [],
                "relaxation_tasks": []
            }

        postponed = (
            self.postpone_difficult_topics()
        )

        revision_topics = (
            self.get_light_revision_topics(
                2
            )
        )

        return {
            "active": True,
            "mode": "Health Maintenance Mode",
            "max_study_hours": 2,
            "break_duration": 15,
            "light_revision_only": True,
            "postponed_topics": postponed,
            "light_revision_topics": revision_topics,
            "relaxation_tasks": self.get_relaxation_tasks()
        }

    # ---------------------------------------------------------
    # AUTOMATIC PROTECTION
    # ---------------------------------------------------------

    def apply(self, fatigue_score):
        """
        Automatically evaluate and apply the
        appropriate protection level.
        """

        mode = self.evaluate(
            fatigue_score
        )

        if mode in (
            "High Fatigue",
            "Health Maintenance Mode"
        ):

            self.postpone_difficult_topics()

        return self.generate_protection_plan()

    