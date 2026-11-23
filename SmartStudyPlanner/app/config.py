from pathlib import Path


class Config:
    """Application configuration."""

    # Project root directory
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Instance directory
    INSTANCE_DIR = BASE_DIR / "instance"

    # SQLite database location
    DATABASE_PATH = INSTANCE_DIR / "studyplanner.db"

    # Flask settings
    SECRET_KEY = "smart-study-planner-secret-key"

    DEBUG = True

    # Application name
    APP_NAME = "Smart Study Planner"