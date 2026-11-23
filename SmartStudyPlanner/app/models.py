import sqlite3
from datetime import datetime

from app.config import Config


def get_connection():
    """Create a connection to the SQLite database."""

    Config.DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        str(Config.DATABASE_PATH)
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def initialize_database():
    """Create the database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            difficulty INTEGER DEFAULT 1,
            estimated_minutes INTEGER DEFAULT 60,
            priority INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Pending',
            created_at TEXT NOT NULL,
            completed_at TEXT,
            FOREIGN KEY (subject_id)
                REFERENCES subjects(id)
                ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            topic_id INTEGER,
            study_date TEXT NOT NULL,
            duration_minutes INTEGER DEFAULT 0,
            continuous_sessions INTEGER DEFAULT 0,
            breaks_taken INTEGER DEFAULT 0,
            mood TEXT,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE,
            FOREIGN KEY (topic_id)
                REFERENCES topics(id)
                ON DELETE SET NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS fatigue_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            record_date TEXT NOT NULL,
            study_hours REAL DEFAULT 0,
            continuous_sessions INTEGER DEFAULT 0,
            difficulty INTEGER DEFAULT 1,
            breaks_taken INTEGER DEFAULT 0,
            sleep_hours REAL DEFAULT 0,
            mood TEXT,
            fatigue_score REAL DEFAULT 0,
            fatigue_level TEXT DEFAULT 'Normal',
            health_mode INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS health_mode (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            activated_at TEXT NOT NULL,
            reason TEXT,
            fatigue_score REAL DEFAULT 0,
            study_limit_minutes INTEGER DEFAULT 120,
            break_duration_minutes INTEGER DEFAULT 15,
            active INTEGER DEFAULT 1,
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS revisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            revision_cycle INTEGER DEFAULT 1,
            revision_date TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            completed_at TEXT,
            created_at TEXT DEFAULT '',
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE,
            FOREIGN KEY (topic_id)
                REFERENCES topics(id)
                ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS productivity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            record_date TEXT NOT NULL,
            total_study_minutes INTEGER DEFAULT 0,
            topics_completed INTEGER DEFAULT 0,
            topics_pending INTEGER DEFAULT 0,
            productivity_score REAL DEFAULT 0,
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS student_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL UNIQUE,
            notifications_enabled INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            quote_date TEXT NOT NULL,
            category TEXT NOT NULL,
            quote TEXT NOT NULL,
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE
        )
        """
    )

    # Safe migrations for existing databases
    try:
        cursor.execute("ALTER TABLE revisions ADD COLUMN created_at TEXT DEFAULT ''")
    except Exception:
        pass

    try:
        cursor.execute("ALTER TABLE topics ADD COLUMN priority INTEGER DEFAULT 1")
    except Exception:
        pass

    connection.commit()
    connection.close()


def create_student(name, email, password):
    """Create a new student account."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students
            (
                name,
                email,
                password,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                password,
                datetime.now().isoformat()
            )
        )

        connection.commit()

        student_id = cursor.lastrowid

        return student_id

    except sqlite3.IntegrityError:
        return None

    finally:
        connection.close()


def get_student_by_email(email):
    """Find a student using their email."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM students
        WHERE email = ?
        """,
        (email,)
    )

    student = cursor.fetchone()

    connection.close()

    if student is None:
        return None

    return dict(student)


def create_subject(
    student_id,
    name,
    description=""
):
    """Create a new subject."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO subjects
        (
            student_id,
            name,
            description,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            student_id,
            name,
            description,
            datetime.now().isoformat()
        )
    )

    connection.commit()

    subject_id = cursor.lastrowid

    connection.close()

    return subject_id


def get_subjects(student_id):
    """Get all subjects for a student."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM subjects
        WHERE student_id = ?
        ORDER BY name
        """,
        (student_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


def create_topic(
    subject_id,
    title,
    difficulty=1,
    estimated_minutes=60,
    priority=1
):
    """Create a study topic."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO topics
        (
            subject_id,
            title,
            difficulty,
            estimated_minutes,
            priority,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            subject_id,
            title,
            difficulty,
            estimated_minutes,
            priority,
            "Pending",
            datetime.now().isoformat()
        )
    )

    connection.commit()

    topic_id = cursor.lastrowid

    connection.close()

    return topic_id


def get_topics(student_id):
    """Get all topics belonging to a student."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            topics.*,
            subjects.name AS subject_name
        FROM topics
        JOIN subjects
            ON topics.subject_id = subjects.id
        WHERE subjects.student_id = ?
        ORDER BY
            topics.priority DESC,
            topics.difficulty DESC
        """,
        (student_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


def complete_topic(topic_id):
    """Mark a topic as completed."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE topics
        SET
            status = 'Completed',
            completed_at = ?
        WHERE id = ?
        """,
        (
            datetime.now().isoformat(),
            topic_id
        )
    )

    connection.commit()
    connection.close()


def set_topic_completed_at(topic_id, completed_at):
    """Set a topic's status to Completed and set completed_at to provided date string."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE topics
        SET status = 'Completed', completed_at = ?
        WHERE id = ?
        """,
        (
            completed_at,
            topic_id
        )
    )

    connection.commit()
    connection.close()


def record_revision_completion(student_id, topic_id, revision_cycle=1):
    """Record that a revision was completed for a topic."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO revisions
        (student_id, topic_id, revision_cycle, revision_date, completed, completed_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            topic_id,
            int(revision_cycle),
            datetime.now().date().isoformat(),
            1,
            datetime.now().isoformat()
            ,datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


def create_study_session(
    student_id,
    topic_id,
    study_date,
    duration_minutes,
    continuous_sessions,
    breaks_taken,
    mood,
    completed
):
    """Save a study session."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO study_sessions
        (
            student_id,
            topic_id,
            study_date,
            duration_minutes,
            continuous_sessions,
            breaks_taken,
            mood,
            completed
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            topic_id,
            study_date,
            duration_minutes,
            continuous_sessions,
            breaks_taken,
            mood,
            completed
        )
    )

    connection.commit()

    session_id = cursor.lastrowid

    connection.close()

    return session_id


def create_fatigue_record(
    student_id,
    record_date,
    study_hours,
    continuous_sessions,
    difficulty,
    breaks_taken,
    sleep_hours,
    mood,
    fatigue_score,
    fatigue_level,
    health_mode
):
    """Save a fatigue record."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO fatigue_records
        (
            student_id,
            record_date,
            study_hours,
            continuous_sessions,
            difficulty,
            breaks_taken,
            sleep_hours,
            mood,
            fatigue_score,
            fatigue_level,
            health_mode,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            student_id,
            record_date,
            study_hours,
            continuous_sessions,
            difficulty,
            breaks_taken,
            sleep_hours,
            mood,
            fatigue_score,
            fatigue_level,
            health_mode,
            datetime.now().isoformat()
        )
    )

    connection.commit()

    record_id = cursor.lastrowid

    connection.close()

    return record_id


def get_dashboard_statistics(student_id):
    """Get statistics for the student dashboard."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM subjects
        WHERE student_id = ?
        """,
        (student_id,)
    )

    total_subjects = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM topics
        JOIN subjects
            ON topics.subject_id = subjects.id
        WHERE subjects.student_id = ?
        """,
        (student_id,)
    )

    total_topics = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM topics
        JOIN subjects
            ON topics.subject_id = subjects.id
        WHERE subjects.student_id = ?
        AND topics.status = 'Completed'
        """,
        (student_id,)
    )

    completed_topics = cursor.fetchone()[0]

    pending_topics = (
        total_topics - completed_topics
    )

    cursor.execute(
        """
        SELECT COALESCE(
            SUM(duration_minutes),
            0
        )
        FROM study_sessions
        WHERE student_id = ?
        AND completed = 1
        AND duration_minutes > 0
        AND study_date IS NOT NULL
        AND study_date != ''
        """,
        (student_id,)
    )

    total_minutes = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COALESCE(
            AVG(fatigue_score),
            0
        )
        FROM fatigue_records
        WHERE student_id = ?
        AND fatigue_score > 0
        """,
        (student_id,)
    )

    average_fatigue = cursor.fetchone()[0]

    # Completed revisions count
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM revisions
        WHERE student_id = ?
        AND completed = 1
        """,
        (student_id,)
    )

    completed_revisions_count = cursor.fetchone()[0]

    # Calculate study streak
    cursor.execute(
        """
        SELECT DISTINCT study_date
        FROM study_sessions
        WHERE student_id = ? AND completed = 1 AND study_date IS NOT NULL AND study_date != ''
        ORDER BY study_date DESC
        """,
        (student_id,)
    )
    date_rows = [r[0] for r in cursor.fetchall()]
    
    streak = 0
    if date_rows:
        try:
            from datetime import date, timedelta
            today = date.today()
            current_check = today
            # Check if there is an entry for today, if not check from yesterday
            dates_set = {d.split("T")[0] for d in date_rows if d}
            if today.isoformat() not in dates_set:
                current_check = today - timedelta(days=1)
            
            while current_check.isoformat() in dates_set:
                streak += 1
                current_check -= timedelta(days=1)
        except Exception:
            streak = max(1, len(date_rows))
    if total_topics > 0:
        completion_percentage = (completed_topics / total_topics) * 100
    else:
        completion_percentage = 0

    connection.close()

    return {
        "total_subjects": total_subjects,
        "total_topics": total_topics,
        "completed_topics": completed_topics,
        "pending_topics": pending_topics,
        "total_study_minutes": total_minutes,
        "total_study_hours": round(
            total_minutes / 60,
            2
        ),
        "average_fatigue": round(
            average_fatigue,
            2
        ),
        "completed_revisions": completed_revisions_count,
        "completion_percentage": round(
            completion_percentage,
            2
        ),
        "study_streak": streak
    }


def get_study_streak(student_id):
    """Calculate the consecutive days study streak for a student."""
    stats = get_dashboard_statistics(student_id)
    return stats.get("study_streak", 1)


def add_revision(student_id, topic_id, revision_cycle=1, revision_date=None):
    """Add a revision schedule entry."""
    connection = get_connection()
    cursor = connection.cursor()

    if revision_date is None:
        from datetime import date
        revision_date = date.today().isoformat()

    cursor.execute(
        """
        INSERT INTO revisions
        (student_id, topic_id, revision_cycle, revision_date, completed, created_at)
        VALUES (?, ?, ?, ?, 0, ?)
        """,
        (student_id, topic_id, int(revision_cycle), revision_date, datetime.now().isoformat())
    )
    connection.commit()
    rev_id = cursor.lastrowid
    connection.close()
    return rev_id


def get_pending_revisions(student_id):
    """Get pending revisions for a student."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT revisions.*,
               revisions.id AS revision_id,
               topics.title AS topic_title,
               topics.estimated_minutes AS estimated_minutes,
               subjects.name AS subject_name
        FROM revisions
        INNER JOIN topics ON revisions.topic_id = topics.id
        INNER JOIN subjects ON topics.subject_id = subjects.id
        WHERE revisions.student_id = ? AND revisions.completed = 0
        ORDER BY revisions.id ASC
        """,
        (student_id,)
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(r) for r in rows]


def complete_revision(revision_id=None, student_id=None, topic_id=None):
    """Mark a revision entry as completed."""
    connection = get_connection()
    cursor = connection.cursor()
    now_str = datetime.now().isoformat()

    if revision_id is not None:
        cursor.execute(
            """
            UPDATE revisions
            SET completed = 1, completed_at = ?
            WHERE id = ?
            """,
            (now_str, int(revision_id))
        )
    elif student_id is not None and topic_id is not None:
        cursor.execute(
            """
            UPDATE revisions
            SET completed = 1, completed_at = ?
            WHERE student_id = ? AND topic_id = ? AND completed = 0
            """,
            (now_str, int(student_id), int(topic_id))
        )
    connection.commit()
    connection.close()


def get_completed_revisions(student_id):
    """Get completed revisions for a student."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT revisions.*, topics.title AS topic_title
        FROM revisions
        INNER JOIN topics ON revisions.topic_id = topics.id
        WHERE revisions.student_id = ? AND revisions.completed = 1
        ORDER BY revisions.completed_at DESC
        """,
        (student_id,)
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(r) for r in rows]


def get_fatigue_history(student_id, limit=30):
    """Get fatigue record history for a student."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM fatigue_records
        WHERE student_id = ?
        ORDER BY record_date DESC, id DESC
        LIMIT ?
        """,
        (student_id, int(limit))
    )
    rows = cursor.fetchall()
    connection.close()
    return [dict(r) for r in rows]


def get_latest_fatigue(student_id):
    """Get the most recent fatigue record for a student."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM fatigue_records
        WHERE student_id = ?
        ORDER BY record_date DESC, id DESC
        LIMIT 1
        """,
        (student_id,)
    )
    row = cursor.fetchone()
    connection.close()
    if row:
        return dict(row)
    return None


def update_student_password(student_id, new_password):
    """Update a student's password."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE students
        SET password = ?
        WHERE id = ?
        """,
        (new_password, student_id)
    )

    connection.commit()
    connection.close()


def get_student_settings(student_id):
    """Return settings for a student, creating defaults if missing."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM student_settings
        WHERE student_id = ?
        """,
        (student_id,)
    )

    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            """
            INSERT INTO student_settings
            (student_id, notifications_enabled, created_at)
            VALUES (?, ?, ?)
            """,
            (student_id, 1, datetime.now().isoformat())
        )

        connection.commit()

        cursor.execute(
            """
            SELECT *
            FROM student_settings
            WHERE student_id = ?
            """,
            (student_id,)
        )

        row = cursor.fetchone()

    settings = dict(row)

    connection.close()

    return settings


def update_student_settings(student_id, notifications_enabled):
    """Update or create student settings."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO student_settings
        (student_id, notifications_enabled, created_at)
        VALUES (?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET
            notifications_enabled = excluded.notifications_enabled
        """,
        (student_id, int(bool(notifications_enabled)), datetime.now().isoformat())
    )

    connection.commit()
    connection.close()


def get_study_sessions(student_id):
    """Return study sessions for a student (for export)."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT ss.*, t.title AS topic_title, s.name AS subject_name
        FROM study_sessions ss
        LEFT JOIN topics t ON ss.topic_id = t.id
        LEFT JOIN subjects s ON t.subject_id = s.id
        WHERE ss.student_id = ?
        ORDER BY ss.study_date DESC
        """,
        (student_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(r) for r in rows]


initialize_database()