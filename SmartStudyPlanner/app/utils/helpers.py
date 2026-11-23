"""
SmartStudyPlanner - Helper Functions

General-purpose utility functions used throughout
the application.
"""


from datetime import date, datetime, timedelta


# =========================================================
# DATE FUNCTIONS
# =========================================================

def get_today():
    """Return today's date as YYYY-MM-DD."""

    return date.today().isoformat()


def format_date(
    date_value,
    output_format="%d %b %Y"
):
    """Convert a date into a readable format."""

    if date_value is None:

        return ""

    if isinstance(
        date_value,
        str
    ):

        try:

            date_value = datetime.strptime(
                date_value,
                "%Y-%m-%d"
            )

        except ValueError:

            return date_value

    if isinstance(
        date_value,
        date
    ):

        return date_value.strftime(
            output_format
        )

    return str(date_value)


def add_days(
    date_value,
    days
):
    """Add a number of days to a date."""

    if isinstance(
        date_value,
        str
    ):

        date_value = date.fromisoformat(
            date_value
        )

    return (
        date_value +
        timedelta(
            days=int(days)
        )
    ).isoformat()


# =========================================================
# NUMBER FUNCTIONS
# =========================================================

def clamp(
    value,
    minimum,
    maximum
):
    """
    Keep a number within a given range.

    Example:
        clamp(120, 0, 100)
        -> 100
    """

    return max(
        minimum,
        min(
            value,
            maximum
        )
    )


def percentage(
    value,
    total
):
    """Calculate percentage safely."""

    if total == 0:

        return 0

    return round(
        (
            value /
            total
        ) * 100,
        2
    )


# =========================================================
# TIME FUNCTIONS
# =========================================================

def minutes_to_hours(
    minutes
):
    """Convert minutes to hours."""

    return round(
        float(minutes) / 60,
        2
    )


def hours_to_minutes(
    hours
):
    """Convert hours to minutes."""

    return int(
        float(hours) * 60
    )


def format_duration(
    minutes
):
    """
    Convert minutes into readable duration.

    Examples:
        45 -> "45 min"
        90 -> "1 hr 30 min"
    """

    minutes = int(minutes)

    hours = minutes // 60

    remaining_minutes = minutes % 60

    if hours == 0:

        return f"{remaining_minutes} min"

    if remaining_minutes == 0:

        return f"{hours} hr"

    return (
        f"{hours} hr "
        f"{remaining_minutes} min"
    )


# =========================================================
# FATIGUE HELPERS
# =========================================================

def get_fatigue_color_class(
    fatigue_score
):
    """
    Return a CSS class according to fatigue score.

    The frontend CSS can use these classes later.
    """

    score = float(
        fatigue_score
    )

    if score <= 5:

        return "fatigue-normal"

    if score <= 10:

        return "fatigue-mild"

    if score <= 15:

        return "fatigue-high"

    return "fatigue-critical"


def get_fatigue_level(
    score
):
    """Convert score to fatigue level."""

    score = float(score)

    if score <= 5:

        return "Normal"

    if score <= 10:

        return "Mild Fatigue"

    if score <= 15:

        return "High Fatigue"

    return "Critical Fatigue"


# =========================================================
# PRODUCTIVITY HELPERS
# =========================================================

def get_productivity_category(
    score
):
    """Convert productivity score to category."""

    score = float(score)

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
# LIST HELPERS
# =========================================================

def remove_duplicates(
    items
):
    """
    Remove duplicates while preserving order.
    """

    result = []

    seen = set()

    for item in items:

        key = str(item)

        if key not in seen:

            result.append(item)

            seen.add(key)

    return result


def sort_by_key(
    items,
    key,
    reverse=False
):
    """Sort a list of dictionaries."""

    return sorted(
        items,
        key=lambda item:
            item.get(
                key,
                0
            ),
        reverse=reverse
    )


# =========================================================
# TOPIC HELPERS
# =========================================================

def is_hard_topic(
    topic
):
    """Check whether a topic is difficult."""

    if not isinstance(
        topic,
        dict
    ):

        return False

    difficulty = str(
        topic.get(
            "difficulty",
            ""
        )
    ).lower()

    return difficulty in (
        "hard",
        "critical",
        "3"
    )


def is_completed(
    topic
):
    """Check whether a topic is completed."""

    if not isinstance(
        topic,
        dict
    ):

        return False

    return topic.get(
        "status"
    ) == "Completed"


# =========================================================
# DASHBOARD HELPERS
# =========================================================

def calculate_completion_rate(
    completed,
    total
):
    """Calculate topic completion rate."""

    return percentage(
        completed,
        total
    )


def calculate_average(
    values
):
    """Calculate average safely."""

    if not values:

        return 0

    return round(
        sum(values) /
        len(values),
        2
    )


# =========================================================
# MESSAGE HELPERS
# =========================================================

def get_schedule_message(
    fatigue_score
):
    """Return a user-friendly schedule message."""

    score = float(
        fatigue_score
    )

    if score <= 5:

        return (
            "You're doing well. "
            "Continue with your normal schedule."
        )

    if score <= 10:

        return (
            "You're showing mild fatigue. "
            "Remember to take extra breaks."
        )

    if score <= 15:

        return (
            "Your fatigue is high. "
            "Today's study load has been reduced."
        )

    return (
        "Health Maintenance Mode is active. "
        "Focus on light revision and recovery."
    )


# =========================================================
# DICTIONARY HELPER
# =========================================================

def safe_get(
    dictionary,
    key,
    default=None
):
    """
    Safely get a value from a dictionary.
    """

    if not isinstance(
        dictionary,
        dict
    ):

        return default

    return dictionary.get(
        key,
        default
    )