"""
SmartStudyPlanner - Chart Data Generator

Prepares analytics data for frontend charts.

Charts supported:
    1. Hours studied per day
    2. Fatigue trend
    3. Subject completion
    4. Revision cycles
    5. Stress trend
    6. Sleep vs productivity
"""


class ChartDataGenerator:
    """Generates chart-ready datasets."""

    # =========================================================
    # HOURS STUDIED BAR CHART
    # =========================================================

    def hours_studied_chart(
        self,
        analytics
    ):
        """
        Data for:

            Bar Chart
            Hours studied per day
        """

        daily_hours = (
            analytics.get_daily_study_hours()
        )

        return {
            "type": "bar",

            "title": "Hours Studied Per Day",

            "labels": [
                record["date"]
                for record
                in daily_hours
            ],

            "data": [
                record["hours"]
                for record
                in daily_hours
            ]
        }

    # =========================================================
    # FATIGUE LINE CHART
    # =========================================================

    def fatigue_chart(
        self,
        analytics
    ):
        """
        Data for:

            Line Chart
            Fatigue trend
        """

        fatigue = (
            analytics.get_fatigue_trend()
        )

        return {
            "type": "line",

            "title": "Fatigue Trend",

            "labels": [
                record["date"]
                for record
                in fatigue
            ],

            "data": [
                record["score"]
                for record
                in fatigue
            ],

            "levels": [
                record["level"]
                for record
                in fatigue
            ]
        }

    # =========================================================
    # SUBJECT PIE CHART
    # =========================================================

    def subject_completion_chart(
        self,
        analytics
    ):
        """
        Data for:

            Pie Chart
            Subject completion percentage
        """

        subjects = (
            analytics.get_subject_statistics()
        )

        labels = []

        data = []

        for subject in subjects:

            labels.append(
                subject["subject"]
            )

            data.append(
                subject["completed"]
            )

        return {
            "type": "pie",

            "title": "Subject Completion",

            "labels": labels,

            "data": data
        }

    # =========================================================
    # REVISION CYCLE CHART
    # =========================================================

    def revision_cycle_chart(
        self,
        analytics
    ):
        """
        Data for:

            Revision cycle chart
        """

        revision = (
            analytics.get_revision_analytics()
        )

        cycles = revision[
            "cycles"
        ]

        return {
            "type": "bar",

            "title": "Revision Cycles",

            "labels": [
                f"Cycle {cycle}"
                for cycle
                in sorted(cycles.keys())
            ],

            "data": [
                cycles[cycle]
                for cycle
                in sorted(cycles.keys())
            ]
        }

    # =========================================================
    # STRESS TREND
    # =========================================================

    def stress_chart(
        self,
        analytics
    ):
        """
        Data for:

            Line Chart
            Stress trend
        """

        stress = (
            analytics.get_stress_trend()
        )

        return {
            "type": "line",

            "title": "Stress Trend",

            "labels": [
                record["date"]
                for record
                in stress
            ],

            "data": [
                record["stress"]
                for record
                in stress
            ]
        }

    # =========================================================
    # SLEEP VS PRODUCTIVITY
    # =========================================================

    def sleep_productivity_chart(
        self,
        analytics
    ):
        """
        Data for:

            Sleep vs productivity graph
        """

        records = (
            analytics.get_sleep_productivity_data()
        )

        return {
            "type": "line",

            "title": "Sleep vs Productivity",

            "labels": [
                record["date"]
                for record
                in records
            ],

            "sleep": [
                record["sleep_hours"]
                for record
                in records
            ],

            "study_hours": [
                record["study_hours"]
                for record
                in records
            ],

            "completed_topics": [
                record["completed_topics"]
                for record
                in records
            ]
        }

    # =========================================================
    # SCHEDULE QUALITY
    # =========================================================

    def schedule_quality_chart(
        self,
        analytics
    ):
        """
        Data for:

            Schedule quality graph
        """

        records = (
            analytics.schedule_records
        )

        return {
            "type": "line",

            "title": "Schedule Quality",

            "labels": [
                record["date"]
                for record
                in records
            ],

            "data": [
                record["quality"]
                for record
                in records
            ]
        }

    # =========================================================
    # DASHBOARD CHART DATA
    # =========================================================

    def get_all_charts(
        self,
        analytics
    ):
        """
        Generate all chart datasets required
        by the Analytics Dashboard.
        """

        return {

            "hours_studied": (
                self.hours_studied_chart(
                    analytics
                )
            ),

            "fatigue": (
                self.fatigue_chart(
                    analytics
                )
            ),

            "subject_completion": (
                self.subject_completion_chart(
                    analytics
                )
            ),

            "revision_cycles": (
                self.revision_cycle_chart(
                    analytics
                )
            ),

            "stress": (
                self.stress_chart(
                    analytics
                )
            ),

            "sleep_productivity": (
                self.sleep_productivity_chart(
                    analytics
                )
            ),

            "schedule_quality": (
                self.schedule_quality_chart(
                    analytics
                )
            )
        }

    # =========================================================
    # EMPTY CHART
    # =========================================================

    def empty_chart(
        self,
        chart_type="line",
        title="No Data"
    ):
        """
        Return an empty chart structure.

        Useful when a new user has not entered
        enough data yet.
        """

        return {
            "type": chart_type,
            "title": title,
            "labels": [],
            "data": []
        }