"""
SmartStudyPlanner - Analytics Engine

This module collects and processes study data for the
Analytics Dashboard.

Main responsibilities:
    - Study summary
    - Fatigue analysis
    - Stress trends
    - Sleep vs productivity
    - Revision statistics
    - Schedule quality
    - Daily analytics
"""


from datetime import date


class Analytics:
    """Main analytics engine for SmartStudyPlanner."""

    def __init__(self):

        # Stores daily study records.
        self.study_records = []

        # Stores fatigue records.
        self.fatigue_records = []

        # Stores revision records.
        self.revision_records = []

        # Stores schedule quality records.
        self.schedule_records = []

        # Stores completed topics.
        self.completed_topics = []

        # Stores pending topics.
        self.pending_topics = []

    # =========================================================
    # STUDY RECORDS
    # =========================================================

    def add_study_record(
        self,
        study_date,
        subject,
        topic,
        hours,
        difficulty=1,
        completed=True
    ):
        """
        Add a study session to analytics.

        Example:
            add_study_record(
                "2026-08-11",
                "Data Structures",
                "Stack",
                2,
                2,
                True
            )
        """

        record = {
            "date": str(study_date),
            "subject": subject,
            "topic": topic,
            "hours": float(hours),
            "difficulty": int(difficulty),
            "completed": bool(completed)
        }

        self.study_records.append(record)

        if completed:

            self.completed_topics.append(
                topic
            )

        else:

            self.pending_topics.append(
                topic
            )

        return record

    # =========================================================
    # FATIGUE RECORDS
    # =========================================================

    def add_fatigue_record(
        self,
        record_date,
        fatigue_score,
        fatigue_level,
        sleep_hours=0,
        stress_level=None
    ):
        """
        Add daily fatigue information.
        """

        record = {
            "date": str(record_date),
            "fatigue_score": float(
                fatigue_score
            ),
            "fatigue_level": fatigue_level,
            "sleep_hours": float(
                sleep_hours
            ),
            "stress_level": (
                stress_level
                if stress_level is not None
                else fatigue_level
            )
        }

        self.fatigue_records.append(
            record
        )

        return record

    # =========================================================
    # REVISION RECORDS
    # =========================================================

    def add_revision_record(
        self,
        revision_date,
        topic,
        cycle,
        completed=True
    ):
        """
        Add a revision record.
        """

        record = {
            "date": str(revision_date),
            "topic": topic,
            "cycle": int(cycle),
            "completed": bool(completed)
        }

        self.revision_records.append(
            record
        )

        return record

    # =========================================================
    # SCHEDULE RECORDS
    # =========================================================

    def add_schedule_record(
        self,
        schedule_date,
        planned_hours,
        actual_hours,
        topic_count,
        completed_topics,
        fatigue_score=0
    ):
        """
        Store information about the quality of
        a particular day's schedule.
        """

        record = {
            "date": str(schedule_date),
            "planned_hours": float(
                planned_hours
            ),
            "actual_hours": float(
                actual_hours
            ),
            "topic_count": int(
                topic_count
            ),
            "completed_topics": int(
                completed_topics
            ),
            "fatigue_score": float(
                fatigue_score
            )
        }

        record["quality"] = (
            self.calculate_schedule_quality(
                record
            )
        )

        self.schedule_records.append(
            record
        )

        return record

    # =========================================================
    # TOTAL STUDY HOURS
    # =========================================================

    def get_total_study_hours(self):
        """Return total number of study hours."""

        return round(
            sum(
                record["hours"]
                for record in self.study_records
            ),
            2
        )

    # =========================================================
    # SUBJECTS COMPLETED
    # =========================================================

    def get_subjects_completed(self):
        """
        Return subjects that have at least one
        completed topic.
        """

        subjects = set()

        for record in self.study_records:

            if record["completed"]:

                subjects.add(
                    record["subject"]
                )

        return sorted(
            list(subjects)
        )

    # =========================================================
    # SUBJECT STATISTICS
    # =========================================================

    def get_subject_statistics(self):
        """
        Calculate hours and completion information
        for every subject.
        """

        subjects = {}

        for record in self.study_records:

            subject = record["subject"]

            if subject not in subjects:

                subjects[subject] = {
                    "subject": subject,
                    "hours": 0,
                    "completed": 0,
                    "pending": 0,
                    "topics": 0
                }

            subjects[subject]["hours"] += (
                record["hours"]
            )

            subjects[subject]["topics"] += 1

            if record["completed"]:

                subjects[subject]["completed"] += 1

            else:

                subjects[subject]["pending"] += 1

        for subject in subjects:

            subjects[subject]["hours"] = round(
                subjects[subject]["hours"],
                2
            )

        return list(
            subjects.values()
        )

    # =========================================================
    # COMPLETION PERCENTAGE
    # =========================================================

    def get_completion_percentage(self):
        """Return overall topic completion percentage."""

        total = len(
            self.study_records
        )

        if total == 0:

            return 0

        completed = sum(
            1
            for record in self.study_records
            if record["completed"]
        )

        return round(
            (completed / total) * 100,
            2
        )

    # =========================================================
    # PENDING TOPICS
    # =========================================================

    def get_pending_topics(self):
        """Return pending topics."""

        return [
            record["topic"]
            for record in self.study_records
            if not record["completed"]
        ]

    # =========================================================
    # COMPLETED TOPICS
    # =========================================================

    def get_completed_topics(self):
        """Return completed topics."""

        return [
            record["topic"]
            for record in self.study_records
            if record["completed"]
        ]

    # =========================================================
    # FATIGUE TREND
    # =========================================================

    def get_fatigue_trend(self):
        """
        Return fatigue data in chronological order.

        Used by the fatigue line chart.
        """

        records = sorted(
            self.fatigue_records,
            key=lambda item: item["date"]
        )

        return [
            {
                "date": record["date"],
                "score": record["fatigue_score"],
                "level": record["fatigue_level"]
            }
            for record in records
        ]

    # =========================================================
    # STRESS TREND
    # =========================================================

    def get_stress_trend(self):
        """
        Return stress information over time.
        """

        records = sorted(
            self.fatigue_records,
            key=lambda item: item["date"]
        )

        return [
            {
                "date": record["date"],
                "stress": record["stress_level"]
            }
            for record in records
        ]

    # =========================================================
    # SLEEP VS PRODUCTIVITY
    # =========================================================

    def get_sleep_productivity_data(self):
        """
        Compare sleep hours with study productivity.
        """

        result = []

        for fatigue in self.fatigue_records:

            record_date = fatigue["date"]

            hours = sum(
                record["hours"]
                for record in self.study_records
                if record["date"] == record_date
            )

            completed = sum(
                1
                for record in self.study_records
                if (
                    record["date"] == record_date
                    and record["completed"]
                )
            )

            result.append(
                {
                    "date": record_date,
                    "sleep_hours": fatigue[
                        "sleep_hours"
                    ],
                    "study_hours": round(
                        hours,
                        2
                    ),
                    "completed_topics": completed
                }
            )

        return result

    # =========================================================
    # DAILY STUDY HOURS
    # =========================================================

    def get_daily_study_hours(self):
        """
        Return study hours grouped by day.
        """

        daily = {}

        for record in self.study_records:

            current_date = record["date"]

            if current_date not in daily:

                daily[current_date] = 0

            daily[current_date] += (
                record["hours"]
            )

        return [
            {
                "date": current_date,
                "hours": round(
                    hours,
                    2
                )
            }
            for current_date, hours
            in sorted(daily.items())
        ]

    # =========================================================
    # REVISION ANALYTICS
    # =========================================================

    def get_revision_analytics(self):
        """Return revision statistics."""

        total = len(
            self.revision_records
        )

        completed = sum(
            1
            for record in self.revision_records
            if record["completed"]
        )

        pending = total - completed

        cycles = {}

        for record in self.revision_records:

            cycle = record["cycle"]

            cycles[cycle] = (
                cycles.get(
                    cycle,
                    0
                ) + 1
            )

        return {
            "total_revisions": total,
            "completed_revisions": completed,
            "pending_revisions": pending,
            "cycles": cycles
        }

    # =========================================================
    # SCHEDULE QUALITY
    # =========================================================

    def calculate_schedule_quality(
        self,
        record
    ):
        """
        Calculate schedule quality.

        Factors:
            - completion ratio
            - difference between planned
              and actual study time
            - fatigue
        """

        planned = record["planned_hours"]

        actual = record["actual_hours"]

        completed = record[
            "completed_topics"
        ]

        topic_count = record[
            "topic_count"
        ]

        if topic_count > 0:

            completion_ratio = (
                completed /
                topic_count
            )

        else:

            completion_ratio = 0

        if planned > 0:

            time_ratio = min(
                actual / planned,
                1
            )

        else:

            time_ratio = 0

        fatigue_score = record[
            "fatigue_score"
        ]

        fatigue_penalty = min(
            fatigue_score / 30,
            1
        )

        score = (
            (completion_ratio * 60)
            + (time_ratio * 30)
            + ((1 - fatigue_penalty) * 10)
        )

        return round(
            min(score, 100),
            2
        )

    # =========================================================
    # OVERLOADED DAYS
    # =========================================================

    def get_overloaded_days(
        self,
        hour_limit=8,
        fatigue_limit=15
    ):
        """Return days considered overloaded."""

        overloaded = []

        for record in self.schedule_records:

            if (
                record["planned_hours"]
                > hour_limit
                or
                record["fatigue_score"]
                > fatigue_limit
            ):

                overloaded.append(
                    record
                )

        return overloaded

    # =========================================================
    # BALANCED DAYS
    # =========================================================

    def get_balanced_days(
        self,
        minimum_quality=70
    ):
        """Return balanced study days."""

        return [
            record
            for record in self.schedule_records
            if record["quality"]
            >= minimum_quality
        ]

    # =========================================================
    # PRODUCTIVITY SCORE
    # =========================================================

    def get_productivity_score(self):
        """
        Calculate an overall productivity score.

        Score consists of:
            - study consistency
            - topic completion
            - revision activity
            - fatigue management
        """

        if not self.study_records:

            return 0

        total_hours = (
            self.get_total_study_hours()
        )

        completion = (
            self.get_completion_percentage()
        )

        revision_score = min(
            len(
                self.revision_records
            ) * 5,
            20
        )

        study_score = min(
            total_hours * 5,
            30
        )

        fatigue_penalty = 0

        if self.fatigue_records:

            average_fatigue = (
                sum(
                    record[
                        "fatigue_score"
                    ]
                    for record
                    in self.fatigue_records
                )
                /
                len(
                    self.fatigue_records
                )
            )

            fatigue_penalty = min(
                average_fatigue,
                20
            )

        score = (
            (completion * 0.5)
            + study_score
            + revision_score
            - fatigue_penalty
        )

        return round(
            max(
                0,
                min(score, 100)
            ),
            2
        )

    # =========================================================
    # FULL DASHBOARD SUMMARY
    # =========================================================

    def get_dashboard_summary(self):
        """
        Return all major analytics required by
        the dashboard.
        """

        return {
            "total_hours": (
                self.get_total_study_hours()
            ),

            "subjects_completed": len(
                self.get_subjects_completed()
            ),

            "completed_topics": len(
                self.get_completed_topics()
            ),

            "pending_topics": len(
                self.get_pending_topics()
            ),

            "completion_percentage": (
                self.get_completion_percentage()
            ),

            "productivity_score": (
                self.get_productivity_score()
            ),

            "subject_statistics": (
                self.get_subject_statistics()
            ),

            "daily_hours": (
                self.get_daily_study_hours()
            ),

            "fatigue_trend": (
                self.get_fatigue_trend()
            ),

            "stress_trend": (
                self.get_stress_trend()
            ),

            "sleep_productivity": (
                self.get_sleep_productivity_data()
            ),

            "revision": (
                self.get_revision_analytics()
            ),

            "overloaded_days": (
                self.get_overloaded_days()
            ),

            "balanced_days": (
                self.get_balanced_days()
            )
        }

    # =========================================================
    # RESET
    # =========================================================

    def clear(self):
        """Clear all analytics data."""

        self.study_records.clear()

        self.fatigue_records.clear()

        self.revision_records.clear()

        self.schedule_records.clear()

        self.completed_topics.clear()

        self.pending_topics.clear()