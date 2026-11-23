"""
SmartStudyPlanner - Productivity Analyzer

Calculates:
    - Daily productivity
    - Weekly productivity
    - Study consistency
    - Completion rate
    - Productivity score
    - Productivity category
"""


class ProductivityAnalyzer:
    """Analyzes student productivity."""

    def __init__(self):

        self.daily_records = []

    # =========================================================
    # ADD DAILY RECORD
    # =========================================================

    def add_daily_record(
        self,
        record_date,
        study_hours,
        planned_hours,
        topics_completed,
        topics_planned,
        fatigue_score=0,
        revision_completed=0
    ):
        """Add one day's productivity data."""

        record = {
            "date": str(record_date),
            "study_hours": float(
                study_hours
            ),
            "planned_hours": float(
                planned_hours
            ),
            "topics_completed": int(
                topics_completed
            ),
            "topics_planned": int(
                topics_planned
            ),
            "fatigue_score": float(
                fatigue_score
            ),
            "revision_completed": int(
                revision_completed
            )
        }

        record["productivity_score"] = (
            self.calculate_daily_score(
                record
            )
        )

        self.daily_records.append(
            record
        )

        return record

    # =========================================================
    # DAILY PRODUCTIVITY
    # =========================================================

    def calculate_daily_score(
        self,
        record
    ):
        """
        Calculate daily productivity.

        Components:
            40% study completion
            30% topic completion
            20% revision
            10% fatigue management
        """

        planned_hours = record[
            "planned_hours"
        ]

        study_hours = record[
            "study_hours"
        ]

        if planned_hours > 0:

            study_ratio = min(
                study_hours /
                planned_hours,
                1
            )

        else:

            study_ratio = 0

        planned_topics = record[
            "topics_planned"
        ]

        completed_topics = record[
            "topics_completed"
        ]

        if planned_topics > 0:

            topic_ratio = min(
                completed_topics /
                planned_topics,
                1
            )

        else:

            topic_ratio = 0

        revision_score = min(
            record[
                "revision_completed"
            ] * 10,
            20
        )

        fatigue_score = record[
            "fatigue_score"
        ]

        if fatigue_score <= 5:

            fatigue_component = 10

        elif fatigue_score <= 10:

            fatigue_component = 8

        elif fatigue_score <= 15:

            fatigue_component = 5

        else:

            fatigue_component = 2

        score = (
            (study_ratio * 40)
            + (topic_ratio * 30)
            + revision_score
            + fatigue_component
        )

        return round(
            min(score, 100),
            2
        )

    # =========================================================
    # OVERALL SCORE
    # =========================================================

    def get_overall_score(self):
        """Return average productivity score."""

        if not self.daily_records:

            return 0

        total = sum(
            record["productivity_score"]
            for record
            in self.daily_records
        )

        return round(
            total /
            len(
                self.daily_records
            ),
            2
        )

    # =========================================================
    # CATEGORY
    # =========================================================

    def get_productivity_category(
        self,
        score=None
    ):
        """Convert score into a readable category."""

        if score is None:

            score = (
                self.get_overall_score()
            )

        if score >= 80:

            return "Excellent"

        if score >= 65:

            return "Good"

        if score >= 50:

            return "Moderate"

        if score >= 30:

            return "Needs Improvement"

        return "Low"

    # =========================================================
    # CONSISTENCY
    # =========================================================

    def get_consistency_score(self):
        """
        Measure how consistently the student studies.

        More active study days = higher consistency.
        """

        if not self.daily_records:

            return 0

        active_days = sum(
            1
            for record
            in self.daily_records
            if record["study_hours"] > 0
        )

        consistency = (
            active_days /
            len(
                self.daily_records
            )
        ) * 100

        return round(
            consistency,
            2
        )

    # =========================================================
    # COMPLETION RATE
    # =========================================================

    def get_completion_rate(self):
        """Calculate topic completion rate."""

        total_planned = sum(
            record["topics_planned"]
            for record
            in self.daily_records
        )

        total_completed = sum(
            record["topics_completed"]
            for record
            in self.daily_records
        )

        if total_planned == 0:

            return 0

        return round(
            (
                total_completed /
                total_planned
            ) * 100,
            2
        )

    # =========================================================
    # DAILY TREND
    # =========================================================

    def get_productivity_trend(self):
        """Return daily productivity for a chart."""

        return [
            {
                "date": record["date"],
                "score": record[
                    "productivity_score"
                ]
            }
            for record
            in self.daily_records
        ]

    # =========================================================
    # STUDY HOURS TREND
    # =========================================================

    def get_study_hours_trend(self):
        """Return daily study hours."""

        return [
            {
                "date": record["date"],
                "hours": record[
                    "study_hours"
                ]
            }
            for record
            in self.daily_records
        ]

    # =========================================================
    # BEST DAY
    # =========================================================

    def get_best_day(self):
        """Return the most productive day."""

        if not self.daily_records:

            return None

        return max(
            self.daily_records,
            key=lambda record:
                record["productivity_score"]
        )

    # =========================================================
    # WORST DAY
    # =========================================================

    def get_worst_day(self):
        """Return the least productive day."""

        if not self.daily_records:

            return None

        return min(
            self.daily_records,
            key=lambda record:
                record["productivity_score"]
        )

    # =========================================================
    # FULL PRODUCTIVITY REPORT
    # =========================================================

    def get_report(self):
        """Return complete productivity analysis."""

        overall_score = (
            self.get_overall_score()
        )

        return {
            "overall_score": overall_score,

            "category": (
                self.get_productivity_category(
                    overall_score
                )
            ),

            "consistency": (
                self.get_consistency_score()
            ),

            "completion_rate": (
                self.get_completion_rate()
            ),

            "best_day": (
                self.get_best_day()
            ),

            "worst_day": (
                self.get_worst_day()
            ),

            "trend": (
                self.get_productivity_trend()
            ),

            "study_hours": (
                self.get_study_hours_trend()
            )
        }

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):
        """Remove all productivity records."""

        self.daily_records.clear()
        