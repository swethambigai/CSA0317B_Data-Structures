"""
SmartStudyPlanner - Motivation Quote System

Provides original motivational messages based on:
    - Student mood
    - Fatigue level
    - Exam status
    - Productivity state
"""


import random

from app.utils.constants import (
    MOOD_HAPPY,
    MOOD_NEUTRAL,
    MOOD_TIRED,
    MOOD_STRESSED,
    QUOTE_MOTIVATION,
    QUOTE_CALMING,
    QUOTE_CONFIDENCE,
    QUOTE_CONSISTENCY
)


# =========================================================
# MOTIVATION QUOTES
# =========================================================

MOTIVATION_QUOTES = [

    "Small steps every day create big results.",

    "Your effort today becomes your strength tomorrow.",

    "You are learning, growing, and becoming stronger.",

    "Progress does not need to be perfect.",

    "Keep going. Every session adds something to your future.",

    "One focused hour can make a meaningful difference.",

    "You do not need to finish everything today.",

    "Start where you are and take the next step."
]


# =========================================================
# CALMING QUOTES
# =========================================================

CALMING_QUOTES = [

    "Rest is also part of progress.",

    "You do not have to rush your learning.",

    "Take a breath. One thing at a time.",

    "A rested mind learns better.",

    "It is okay to slow down when your mind needs it.",

    "Your wellbeing matters as much as your productivity.",

    "Pause, breathe, and return when you are ready.",

    "You are allowed to take a break."
]


# =========================================================
# CONFIDENCE QUOTES
# =========================================================

CONFIDENCE_QUOTES = [

    "You have prepared for this. Trust your preparation.",

    "You know more today than you did yesterday.",

    "Confidence grows every time you practice.",

    "You can handle difficult topics one step at a time.",

    "You have overcome difficult learning moments before.",

    "Focus on what you know, then build from there.",

    "Your preparation gives you something to rely on."
]


# =========================================================
# CONSISTENCY QUOTES
# =========================================================

CONSISTENCY_QUOTES = [

    "Consistency beats intensity when building long-term skills.",

    "Even a small session keeps your learning momentum alive.",

    "You do not need a perfect day. You need another step.",

    "Showing up regularly is already progress.",

    "A little learning today keeps tomorrow easier.",

    "Build the habit first. The results will follow.",

    "Keep the chain going, one session at a time."
]


# =========================================================
# QUOTE COLLECTION
# =========================================================

QUOTE_COLLECTION = {

    QUOTE_MOTIVATION:
        MOTIVATION_QUOTES,

    QUOTE_CALMING:
        CALMING_QUOTES,

    QUOTE_CONFIDENCE:
        CONFIDENCE_QUOTES,

    QUOTE_CONSISTENCY:
        CONSISTENCY_QUOTES
}


# =========================================================
# QUOTE MANAGER
# =========================================================

class QuoteManager:
    """Manages daily motivational messages."""

    def __init__(self):

        self.last_quote = None

    # =====================================================
    # GET CATEGORY
    # =====================================================

    def get_category(
        self,
        mood=None,
        fatigue_score=0,
        exam_day=False
    ):
        """
        Automatically determine the best quote category.
        """

        if exam_day:

            return QUOTE_CONFIDENCE

        if fatigue_score > 15:

            return QUOTE_CALMING

        if fatigue_score >= 11:

            return QUOTE_CALMING

        if mood == MOOD_STRESSED:

            return QUOTE_CALMING

        if mood == MOOD_TIRED:

            return QUOTE_CALMING

        if mood == MOOD_HAPPY:

            return QUOTE_MOTIVATION

        if mood == MOOD_NEUTRAL:

            return QUOTE_CONSISTENCY

        return QUOTE_MOTIVATION

    # =====================================================
    # GET QUOTE
    # =====================================================

    def get_quote(
        self,
        mood=None,
        fatigue_score=0,
        exam_day=False
    ):
        """
        Select a quote based on the student's
        current state.
        """

        category = self.get_category(
            mood=mood,
            fatigue_score=fatigue_score,
            exam_day=exam_day
        )

        quotes = QUOTE_COLLECTION[
            category
        ]

        quote = random.choice(
            quotes
        )

        self.last_quote = quote

        return {
            "category": category,
            "quote": quote
        }

    # =====================================================
    # GET RANDOM CATEGORY QUOTE
    # =====================================================

    def get_category_quote(
        self,
        category
    ):
        """Return a random quote from a category."""

        if category not in QUOTE_COLLECTION:

            return {
                "category": QUOTE_MOTIVATION,
                "quote": random.choice(
                    MOTIVATION_QUOTES
                )
            }

        quote = random.choice(
            QUOTE_COLLECTION[
                category
            ]
        )

        self.last_quote = quote

        return {
            "category": category,
            "quote": quote
        }

    # =====================================================
    # DAILY QUOTE
    # =====================================================

    def get_daily_quote(
        self,
        mood=None,
        fatigue_score=0,
        exam_day=False
    ):
        """
        Generate the quote shown on the dashboard.
        """

        return self.get_quote(
            mood=mood,
            fatigue_score=fatigue_score,
            exam_day=exam_day
        )

    # =====================================================
    # ALL QUOTES
    # =====================================================

    def get_all_quotes(self):
        """Return all quote categories."""

        return {
            category: quotes.copy()
            for category, quotes
            in QUOTE_COLLECTION.items()
        }

    # =====================================================
    # LAST QUOTE
    # =====================================================

    def get_last_quote(self):
        """Return the last displayed quote."""

        return self.last_quote


# =========================================================
# SIMPLE FUNCTION
# =========================================================

def get_motivation_quote(
    mood=None,
    fatigue_score=0,
    exam_day=False
):
    """
    Simple helper function for other modules.

    Example:

        quote = get_motivation_quote(
            mood="Stressed",
            fatigue_score=14
        )
    """

    manager = QuoteManager()

    return manager.get_quote(
        mood=mood,
        fatigue_score=fatigue_score,
        exam_day=exam_day
    )


def get_random_quote(category=None):
    """
    Return a random motivational quote string safely.
    """
    if category and category in QUOTE_COLLECTION:
        return random.choice(QUOTE_COLLECTION[category])

    all_quotes = []
    for q_list in QUOTE_COLLECTION.values():
        all_quotes.extend(q_list)

    if all_quotes:
        return random.choice(all_quotes)

    return "Small progress every day leads to big results. 📚"


def get_motivation_message(completed_tasks=0, pending_tasks=0, streak=1, productivity=0):
    """
    Return dynamic, progress-connected motivational feedback.
    """
    total = completed_tasks + pending_tasks

    if total > 0 and pending_tasks == 0:
        return "Excellent! You've completed today's study plan! 🎉"

    if streak and streak > 1:
        return f"You're on a {streak}-day study streak! Keep going! 🔥"

    if completed_tasks > 0:
        return "Great job! You're making steady progress. 🌟"

    if pending_tasks > 0:
        return "Small progress every day leads to big results. 📚"

    return "Ready to conquer your goals today? Let's get started! ✨"
