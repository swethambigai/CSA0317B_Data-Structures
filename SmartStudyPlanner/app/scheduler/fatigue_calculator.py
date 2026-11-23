"""
SmartStudyPlanner - Fatigue Calculator

Purpose:
    Calculates the student's fatigue score based on:
        H = Hours studied
        C = Continuous study sessions
        D = Difficulty level
        B = Breaks taken
        S = Sleep hours

Formula:
    Fatigue Score =
        (H * 2) +
        (C * 1.5) +
        (D * 1) -
        (B * 2) -
        (S * 1.5)

Fatigue levels:
    0 - 5   : Normal
    6 - 10  : Mild Fatigue
    11 - 15 : High Fatigue
    > 15    : Critical Fatigue
"""


class FatigueCalculator:
    """Calculates and interprets student fatigue."""

    def __init__(
        self,
        hours_studied=0,
        continuous_sessions=0,
        difficulty=1,
        breaks=0,
        sleep_hours=0
    ):
        self.hours_studied = float(hours_studied)
        self.continuous_sessions = float(
            continuous_sessions
        )
        self.difficulty = float(difficulty)
        self.breaks = float(breaks)
        self.sleep_hours = float(sleep_hours)

    # ---------------------------------------------------------
    # INPUT VALIDATION
    # ---------------------------------------------------------

    def validate_inputs(self):
        """Validate fatigue calculation inputs."""

        if self.hours_studied < 0:
            raise ValueError(
                "Hours studied cannot be negative."
            )

        if self.continuous_sessions < 0:
            raise ValueError(
                "Continuous sessions cannot be negative."
            )

        if self.difficulty < 1 or self.difficulty > 3:
            raise ValueError(
                "Difficulty must be between 1 and 3."
            )

        if self.breaks < 0:
            raise ValueError(
                "Breaks cannot be negative."
            )

        if self.sleep_hours < 0:
            raise ValueError(
                "Sleep hours cannot be negative."
            )

        return True

    # ---------------------------------------------------------
    # FATIGUE SCORE
    # ---------------------------------------------------------

    def calculate_score(self):
        """
        Calculate the fatigue score using the
        project's defined formula.
        """

        self.validate_inputs()

        score = (
            (self.hours_studied * 2)
            + (self.continuous_sessions * 1.5)
            + (self.difficulty * 1)
            - (self.breaks * 2)
            - (self.sleep_hours * 1.5)
        )

        return round(score, 2)

    # ---------------------------------------------------------
    # FATIGUE LEVEL
    # ---------------------------------------------------------

    def get_level(self, score=None):
        """Return the fatigue level."""

        if score is None:
            score = self.calculate_score()

        if score <= 5:
            return "Normal"

        if score <= 10:
            return "Mild Fatigue"

        if score <= 15:
            return "High Fatigue"

        return "Critical Fatigue"

    # ---------------------------------------------------------
    # HEALTH MODE REQUIRED?
    # ---------------------------------------------------------

    def requires_health_mode(self, score=None):
        """
        Determine whether Health Maintenance Mode
        should be activated.
        """

        if score is None:
            score = self.calculate_score()

        return score > 15

    # ---------------------------------------------------------
    # HIGH FATIGUE?
    # ---------------------------------------------------------

    def is_high_fatigue(self, score=None):
        """Check whether fatigue is high or critical."""

        if score is None:
            score = self.calculate_score()

        return score >= 11

    # ---------------------------------------------------------
    # RECOMMENDED ACTION
    # ---------------------------------------------------------

    def get_recommendation(self, score=None):
        """Return an action based on fatigue level."""

        if score is None:
            score = self.calculate_score()

        level = self.get_level(score)

        recommendations = {
            "Normal": (
                "Continue with the normal study schedule."
            ),

            "Mild Fatigue": (
                "Add extra breaks and avoid long "
                "continuous study sessions."
            ),

            "High Fatigue": (
                "Reduce study load and move difficult "
                "topics to a later session."
            ),

            "Critical Fatigue": (
                "Activate Health Maintenance Mode. "
                "Limit study workload and prioritize rest."
            )
        }

        return recommendations[level]

    # ---------------------------------------------------------
    # FULL ANALYSIS
    # ---------------------------------------------------------

    def analyze(self):
        """
        Return complete fatigue analysis.

        This result can later be sent to:
            - dashboard
            - health mode
            - analytics
            - database
        """

        score = self.calculate_score()
        level = self.get_level(score)

        return {
            "score": score,
            "level": level,
            "health_mode": self.requires_health_mode(score),
            "high_fatigue": self.is_high_fatigue(score),
            "recommendation": self.get_recommendation(score)
        }

    # ---------------------------------------------------------
    # UPDATE INPUTS
    # ---------------------------------------------------------

    def update(
        self,
        hours_studied=None,
        continuous_sessions=None,
        difficulty=None,
        breaks=None,
        sleep_hours=None
    ):
        """Update fatigue inputs."""

        if hours_studied is not None:
            self.hours_studied = float(
                hours_studied
            )

        if continuous_sessions is not None:
            self.continuous_sessions = float(
                continuous_sessions
            )

        if difficulty is not None:
            self.difficulty = float(
                difficulty
            )

        if breaks is not None:
            self.breaks = float(
                breaks
            )

        if sleep_hours is not None:
            self.sleep_hours = float(
                sleep_hours
            )

        return self.analyze()


def calculate_fatigue_score(
    hours_studied=0,
    continuous_sessions=0,
    difficulty=1,
    breaks_taken=0,
    sleep_hours=0
):
    """Module-level helper to calculate fatigue score (for testing/utility)."""
    calculator = FatigueCalculator(
        hours_studied=hours_studied,
        continuous_sessions=continuous_sessions,
        difficulty=difficulty,
        breaks=breaks_taken,
        sleep_hours=sleep_hours
    )
    return calculator.calculate_score()


def get_fatigue_level(score):
    """Module-level helper to return fatigue level matching test suite expectations."""
    if score <= 5:
        return "Normal"
    if score <= 10:
        return "Mild fatigue"
    if score <= 15:
        return "High fatigue"
    return "Critical"


    