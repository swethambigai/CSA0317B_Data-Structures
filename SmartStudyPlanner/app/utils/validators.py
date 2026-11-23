"""
SmartStudyPlanner - Input Validators

Validates data entered by the student before it
is processed by the scheduler, fatigue calculator,
database, or analytics system.
"""


from app.utils.constants import (
    DIFFICULTY_EASY,
    DIFFICULTY_HARD,
    MAX_SLEEP_HOURS,
    MIN_SLEEP_HOURS,
    MAX_STUDY_HOURS,
    MIN_STUDY_HOURS,
    MAX_BREAKS,
    MIN_BREAKS,
    MAX_CONTINUOUS_SESSIONS,
    MIN_CONTINUOUS_SESSIONS,
    MOOD_OPTIONS
)


# =========================================================
# NUMBER VALIDATION
# =========================================================

def is_number(value):
    """Check whether a value can be converted to a number."""

    try:

        float(value)

        return True

    except (
        ValueError,
        TypeError
    ):

        return False


# =========================================================
# POSITIVE NUMBER
# =========================================================

def is_positive_number(value):
    """Check whether a number is greater than zero."""

    if not is_number(value):

        return False

    return float(value) > 0


# =========================================================
# STUDY HOURS
# =========================================================

def validate_study_hours(
    hours
):
    """Validate study hours."""

    if not is_number(hours):

        return False, (
            "Study hours must be a number."
        )

    hours = float(hours)

    if hours < MIN_STUDY_HOURS:

        return False, (
            "Study hours cannot be negative."
        )

    if hours > MAX_STUDY_HOURS:

        return False, (
            "Study hours cannot exceed 24 hours."
        )

    return True, "Valid study hours."


# =========================================================
# SLEEP HOURS
# =========================================================

def validate_sleep_hours(
    hours
):
    """Validate sleep hours."""

    if not is_number(hours):

        return False, (
            "Sleep hours must be a number."
        )

    hours = float(hours)

    if hours < MIN_SLEEP_HOURS:

        return False, (
            "Sleep hours cannot be negative."
        )

    if hours > MAX_SLEEP_HOURS:

        return False, (
            "Sleep hours cannot exceed 24 hours."
        )

    return True, "Valid sleep hours."


# =========================================================
# DIFFICULTY
# =========================================================

def validate_difficulty(
    difficulty
):
    """Validate topic difficulty."""

    if not is_number(difficulty):

        return False, (
            "Difficulty must be a number."
        )

    difficulty = int(
        float(difficulty)
    )

    if not (
        DIFFICULTY_EASY
        <= difficulty
        <= DIFFICULTY_HARD
    ):

        return False, (
            "Difficulty must be between 1 and 3."
        )

    return True, "Valid difficulty."


# =========================================================
# BREAKS
# =========================================================

def validate_breaks(
    breaks
):
    """Validate number of breaks."""

    if not is_number(breaks):

        return False, (
            "Number of breaks must be a number."
        )

    breaks = int(
        float(breaks)
    )

    if breaks < MIN_BREAKS:

        return False, (
            "Breaks cannot be negative."
        )

    if breaks > MAX_BREAKS:

        return False, (
            "Number of breaks is too high."
        )

    return True, "Valid number of breaks."


# =========================================================
# CONTINUOUS SESSIONS
# =========================================================

def validate_continuous_sessions(
    sessions
):
    """Validate continuous study sessions."""

    if not is_number(sessions):

        return False, (
            "Continuous sessions must be a number."
        )

    sessions = int(
        float(sessions)
    )

    if sessions < MIN_CONTINUOUS_SESSIONS:

        return False, (
            "Continuous sessions cannot be negative."
        )

    if sessions > MAX_CONTINUOUS_SESSIONS:

        return False, (
            "Too many continuous sessions."
        )

    return True, (
        "Valid number of sessions."
    )


# =========================================================
# MOOD
# =========================================================

def validate_mood(
    mood
):
    """Validate student's self-reported mood."""

    if not isinstance(
        mood,
        str
    ):

        return False, (
            "Mood must be text."
        )

    cleaned_mood = mood.strip().title()

    if cleaned_mood not in MOOD_OPTIONS:

        return False, (
            "Invalid mood. Choose "
            "Happy, Neutral, Tired, or Stressed."
        )

    return True, "Valid mood."


# =========================================================
# SUBJECT
# =========================================================

def validate_subject(
    subject
):
    """Validate subject name."""

    if not isinstance(
        subject,
        str
    ):

        return False, (
            "Subject must be text."
        )

    subject = subject.strip()

    if not subject:

        return False, (
            "Subject cannot be empty."
        )

    if len(subject) > 100:

        return False, (
            "Subject name is too long."
        )

    return True, "Valid subject."


# =========================================================
# TOPIC
# =========================================================

def validate_topic(
    topic
):
    """Validate topic name."""

    if not isinstance(
        topic,
        str
    ):

        return False, (
            "Topic must be text."
        )

    topic = topic.strip()

    if not topic:

        return False, (
            "Topic cannot be empty."
        )

    if len(topic) > 150:

        return False, (
            "Topic name is too long."
        )

    return True, "Valid topic."


# =========================================================
# STUDY SESSION
# =========================================================

def validate_study_session(
    hours,
    difficulty,
    breaks,
    continuous_sessions,
    sleep_hours,
    mood
):
    """
    Validate all fatigue-related inputs together.
    """

    errors = []

    valid, message = validate_study_hours(
        hours
    )

    if not valid:

        errors.append(message)

    valid, message = validate_difficulty(
        difficulty
    )

    if not valid:

        errors.append(message)

    valid, message = validate_breaks(
        breaks
    )

    if not valid:

        errors.append(message)

    valid, message = validate_continuous_sessions(
        continuous_sessions
    )

    if not valid:

        errors.append(message)

    valid, message = validate_sleep_hours(
        sleep_hours
    )

    if not valid:

        errors.append(message)

    valid, message = validate_mood(
        mood
    )

    if not valid:

        errors.append(message)

    if errors:

        return False, errors

    return True, []


# =========================================================
# COMPLETE TOPIC
# =========================================================

def validate_topic_data(
    subject,
    topic,
    duration,
    difficulty
):
    """Validate study topic information."""

    errors = []

    valid, message = validate_subject(
        subject
    )

    if not valid:

        errors.append(message)

    valid, message = validate_topic(
        topic
    )

    if not valid:

        errors.append(message)

    valid, message = validate_difficulty(
        difficulty
    )

    if not valid:

        errors.append(message)

    if not is_number(duration):

        errors.append(
            "Duration must be a number."
        )

    else:

        duration = float(duration)

        if duration <= 0:

            errors.append(
                "Duration must be greater than zero."
            )

        if duration > 240:

            errors.append(
                "A study session cannot exceed 240 minutes."
            )

    if errors:

        return False, errors

    return True, []


# =========================================================
# SANITIZE TEXT
# =========================================================

def clean_text(
    value
):
    """Clean user-entered text."""

    if value is None:

        return ""

    return " ".join(
        str(value).strip().split()
    )
