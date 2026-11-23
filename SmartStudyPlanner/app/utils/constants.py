"""
SmartStudyPlanner - Project Constants

Central location for fixed values used throughout
the application.
"""


# =========================================================
# APPLICATION
# =========================================================

APP_NAME = "SmartStudyPlanner"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = (
    "An intelligent study planning and "
    "student wellness management system."
)


# =========================================================
# FATIGUE LEVELS
# =========================================================

FATIGUE_NORMAL_MAX = 5

FATIGUE_MILD_MAX = 10

FATIGUE_HIGH_MAX = 15


FATIGUE_NORMAL = "Normal"

FATIGUE_MILD = "Mild Fatigue"

FATIGUE_HIGH = "High Fatigue"

FATIGUE_CRITICAL = "Critical Fatigue"


# =========================================================
# DIFFICULTY LEVELS
# =========================================================

DIFFICULTY_EASY = 1

DIFFICULTY_MEDIUM = 2

DIFFICULTY_HARD = 3


DIFFICULTY_NAMES = {
    1: "Easy",
    2: "Medium",
    3: "Hard"
}


# =========================================================
# STUDY LIMITS
# =========================================================

NORMAL_MAX_STUDY_HOURS = 8

MILD_EXTRA_BREAK_MINUTES = 10

HIGH_MAX_STUDY_HOURS = 3

CRITICAL_MAX_STUDY_HOURS = 2

CRITICAL_BREAK_MINUTES = 15


# =========================================================
# HEALTH MAINTENANCE MODE
# =========================================================

HEALTH_MODE_NAME = (
    "Health Maintenance Mode"
)

HEALTH_MODE_MAX_HOURS = 2

HEALTH_MODE_BREAK_MINUTES = 15

HEALTH_MODE_REVISION_LIMIT = 2


# =========================================================
# REVISION
# =========================================================

REVISION_INTERVALS = {
    1: 1,
    2: 3,
    3: 7,
    4: 14,
    5: 30
}


MAX_REVISION_CYCLES = 5


# =========================================================
# PRODUCTIVITY
# =========================================================

PRODUCTIVITY_EXCELLENT = 80

PRODUCTIVITY_GOOD = 65

PRODUCTIVITY_MODERATE = 50

PRODUCTIVITY_NEEDS_IMPROVEMENT = 30


# =========================================================
# STRESS LEVELS
# =========================================================

STRESS_LOW = "Low"

STRESS_MODERATE = "Moderate"

STRESS_HIGH = "High"

STRESS_CRITICAL = "Critical"


# =========================================================
# MOOD VALUES
# =========================================================

MOOD_HAPPY = "Happy"

MOOD_NEUTRAL = "Neutral"

MOOD_TIRED = "Tired"

MOOD_STRESSED = "Stressed"


MOOD_OPTIONS = [
    MOOD_HAPPY,
    MOOD_NEUTRAL,
    MOOD_TIRED,
    MOOD_STRESSED
]


# =========================================================
# QUOTE CATEGORIES
# =========================================================

QUOTE_MOTIVATION = "Motivation"

QUOTE_CALMING = "Calming"

QUOTE_CONFIDENCE = "Confidence Boost"

QUOTE_CONSISTENCY = "Consistency"


# =========================================================
# SESSION SETTINGS
# =========================================================

DEFAULT_SESSION_MINUTES = 60

MIN_SESSION_MINUTES = 15

MAX_SESSION_MINUTES = 180


# =========================================================
# BREAK SETTINGS
# =========================================================

DEFAULT_BREAK_MINUTES = 5

LONG_BREAK_MINUTES = 15

HEALTH_BREAK_MINUTES = 15


# =========================================================
# VALIDATION LIMITS
# =========================================================

MIN_SLEEP_HOURS = 0

MAX_SLEEP_HOURS = 24

MIN_STUDY_HOURS = 0

MAX_STUDY_HOURS = 24

MIN_BREAKS = 0

MAX_BREAKS = 30

MIN_CONTINUOUS_SESSIONS = 0

MAX_CONTINUOUS_SESSIONS = 20


# =========================================================
# TOPIC STATUS
# =========================================================

STATUS_PENDING = "Pending"

STATUS_IN_PROGRESS = "In Progress"

STATUS_COMPLETED = "Completed"

STATUS_POSTPONED = "Postponed"

STATUS_REVISION = "Revision"


# =========================================================
# SCHEDULE STATUS
# =========================================================

SCHEDULE_NORMAL = "Normal Schedule"

SCHEDULE_MILD = "Break-Enhanced Schedule"

SCHEDULE_HIGH = "Reduced Study Load"

SCHEDULE_HEALTH = "Health Maintenance Mode"
