
import sqlite3
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INSTANCE_FOLDER = PROJECT_ROOT / "instance"

DATABASE_PATH = INSTANCE_FOLDER / "studyplanner.db"


INSTANCE_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


def get_connection():
    connection = sqlite3.connect(
        str(DATABASE_PATH)
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def initialize_database():

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
            description TEXT DEFAULT '',
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
            difficulty INTEGER NOT NULL DEFAULT 1,
            estimated_minutes INTEGER NOT NULL DEFAULT 60,
            status TEXT NOT NULL DEFAULT 'Pending',
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
            subject_id INTEGER,
            study_date TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL DEFAULT 0,
            continuous_sessions INTEGER NOT NULL DEFAULT 0,
            breaks_taken INTEGER NOT NULL DEFAULT 0,
            mood TEXT,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE,
            FOREIGN KEY (topic_id)
                REFERENCES topics(id)
                ON DELETE SET NULL,
            FOREIGN KEY (subject_id)
                REFERENCES subjects(id)
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
            study_hours REAL NOT NULL DEFAULT 0,
            continuous_sessions INTEGER NOT NULL DEFAULT 0,
            difficulty INTEGER NOT NULL DEFAULT 1,
            breaks_taken INTEGER NOT NULL DEFAULT 0,
            sleep_hours REAL NOT NULL DEFAULT 0,
            mood TEXT,
            fatigue_score REAL NOT NULL DEFAULT 0,
            fatigue_level TEXT NOT NULL DEFAULT 'Normal',
            health_mode INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
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
            revision_cycle INTEGER NOT NULL DEFAULT 1,
            revision_date TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            completed_at TEXT,
            created_at TEXT NOT NULL,
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
            productivity_date TEXT NOT NULL,
            total_study_minutes INTEGER NOT NULL DEFAULT 0,
            completed_topics INTEGER NOT NULL DEFAULT 0,
            pending_topics INTEGER NOT NULL DEFAULT 0,
            productivity_score REAL NOT NULL DEFAULT 0,
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
            created_at TEXT NOT NULL,
            FOREIGN KEY (student_id)
                REFERENCES students(id)
                ON DELETE CASCADE
        )
        """
    )

    connection.commit()

    connection.close()


def create_student(name, email, password):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO students
            (name, email, password, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                name.strip(),
                email.strip().lower(),
                password,
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return cursor.lastrowid

    except sqlite3.IntegrityError:

        return None

    finally:

        connection.close()


def get_student_by_email(email):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM students
            WHERE email = ?
            """,
            (email.strip().lower(),)
        )

        row = cursor.fetchone()

        if row:

            return dict(row)

        return None

    finally:

        connection.close()


def get_student_by_id(student_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM students
            WHERE id = ?
            """,
            (student_id,)
        )

        row = cursor.fetchone()

        if row:

            return dict(row)

        return None

    finally:

        connection.close()


def add_subject(
    student_id,
    name,
    description=""
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO subjects
            (student_id, name, description, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                student_id,
                name.strip(),
                description.strip(),
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


def get_subjects(student_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM subjects
            WHERE student_id = ?
            ORDER BY name ASC
            """,
            (student_id,)
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()


def add_topic(
    subject_id,
    title,
    difficulty=1,
    estimated_minutes=60
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO topics
            (
                subject_id,
                title,
                difficulty,
                estimated_minutes,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                subject_id,
                title.strip(),
                int(difficulty),
                int(estimated_minutes),
                "Pending",
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


def get_topics(subject_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM topics
            WHERE subject_id = ?
            ORDER BY difficulty DESC, id ASC
            """,
            (subject_id,)
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()


def get_student_topics(student_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                topics.*,
                subjects.name AS subject_name
            FROM topics
            INNER JOIN subjects
                ON topics.subject_id = subjects.id
            WHERE subjects.student_id = ?
            ORDER BY topics.difficulty DESC
            """,
            (student_id,)
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()


def update_topic_status(
    topic_id,
    status
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        completed_at = None

        if status == "Completed":

            completed_at = datetime.now().isoformat()

        cursor.execute(
            """
            UPDATE topics
            SET status = ?,
                completed_at = ?
            WHERE id = ?
            """,
            (
                status,
                completed_at,
                topic_id
            )
        )

        connection.commit()

    finally:

        connection.close()


def add_study_session(
    student_id,
    topic_id,
    subject_id,
    study_date,
    duration_minutes,
    continuous_sessions,
    breaks_taken,
    mood,
    completed=False
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO study_sessions
            (
                student_id,
                topic_id,
                subject_id,
                study_date,
                duration_minutes,
                continuous_sessions,
                breaks_taken,
                mood,
                completed,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                topic_id,
                subject_id,
                study_date,
                int(duration_minutes),
                int(continuous_sessions),
                int(breaks_taken),
                mood,
                int(completed),
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


def get_study_sessions(
    student_id,
    limit=30
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM study_sessions
            WHERE student_id = ?
            ORDER BY study_date DESC, id DESC
            LIMIT ?
            """,
            (
                student_id,
                int(limit)
            )
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()


def add_fatigue_record(
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
    health_mode=False
):

    connection = get_connection()

    try:

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
                float(study_hours),
                int(continuous_sessions),
                int(difficulty),
                int(breaks_taken),
                float(sleep_hours),
                mood,
                float(fatigue_score),
                fatigue_level,
                int(health_mode),
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


def get_fatigue_history(
    student_id,
    limit=30
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM fatigue_records
            WHERE student_id = ?
            ORDER BY record_date DESC, id DESC
            LIMIT ?
            """,
            (
                student_id,
                int(limit)
            )
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()


def get_latest_fatigue(student_id):

    connection = get_connection()

    try:

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

        if row:

            return dict(row)

        return None

    finally:

        connection.close()


def add_revision(
    student_id,
    topic_id,
    revision_cycle,
    revision_date
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO revisions
            (
                student_id,
                topic_id,
                revision_cycle,
                revision_date,
                completed,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                topic_id,
                int(revision_cycle),
                revision_date,
                0,
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


def get_pending_revisions(student_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                revisions.*,
                revisions.id AS revision_id,
                topics.title AS topic_title,
                topics.estimated_minutes AS estimated_minutes,
                subjects.name AS subject_name
            FROM revisions
            INNER JOIN topics
                ON revisions.topic_id = topics.id
            INNER JOIN subjects
                ON topics.subject_id = subjects.id
            WHERE revisions.student_id = ?
            AND revisions.completed = 0
            ORDER BY revisions.id ASC
            """,
            (student_id,)
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()


def complete_revision(revision_id=None, student_id=None, topic_id=None):

    connection = get_connection()

    try:

        cursor = connection.cursor()
        now_str = datetime.now().isoformat()

        if revision_id is not None:
            cursor.execute(
                """
                UPDATE revisions
                SET completed = 1,
                    completed_at = ?
                WHERE id = ?
                """,
                (
                    now_str,
                    int(revision_id)
                )
            )
        elif student_id is not None and topic_id is not None:
            cursor.execute(
                """
                UPDATE revisions
                SET completed = 1,
                    completed_at = ?
                WHERE student_id = ?
                AND topic_id = ?
                AND completed = 0
                """,
                (
                    now_str,
                    int(student_id),
                    int(topic_id)
                )
            )

        connection.commit()

    finally:

        connection.close()


def get_completed_revisions(student_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                revisions.*,
                topics.title AS topic_title
            FROM revisions
            INNER JOIN topics
                ON revisions.topic_id = topics.id
            WHERE revisions.student_id = ?
            AND revisions.completed = 1
            ORDER BY revisions.completed_at DESC
            """,
            (student_id,)
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()


def save_productivity(
    student_id,
    productivity_date,
    total_study_minutes,
    completed_topics,
    pending_topics,
    productivity_score
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO productivity
            (
                student_id,
                productivity_date,
                total_study_minutes,
                completed_topics,
                pending_topics,
                productivity_score,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_id,
                productivity_date,
                int(total_study_minutes),
                int(completed_topics),
                int(pending_topics),
                float(productivity_score),
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


def get_productivity_history(
    student_id,
    limit=30
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM productivity
            WHERE student_id = ?
            ORDER BY productivity_date DESC, id DESC
            LIMIT ?
            """,
            (
                student_id,
                int(limit)
            )
        )

        return [
            dict(row)
            for row in cursor.fetchall()
        ]

    finally:

        connection.close()


def save_daily_quote(
    student_id,
    quote_date,
    category,
    quote
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO daily_quotes
            (
                student_id,
                quote_date,
                category,
                quote,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student_id,
                quote_date,
                category,
                quote,
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


def get_daily_quote(
    student_id,
    quote_date
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM daily_quotes
            WHERE student_id = ?
            AND quote_date = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                student_id,
                quote_date
            )
        )

        row = cursor.fetchone()

        if row:

            return dict(row)

        return None

    finally:

        connection.close()


def get_dashboard_statistics(student_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM topics
            INNER JOIN subjects
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
            INNER JOIN subjects
                ON topics.subject_id = subjects.id
            WHERE subjects.student_id = ?
            AND topics.status = 'Completed'
            """,
            (student_id,)
        )

        completed_topics = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM topics
            INNER JOIN subjects
                ON topics.subject_id = subjects.id
            WHERE subjects.student_id = ?
            AND topics.status != 'Completed'
            """,
            (student_id,)
        )

        pending_topics = cursor.fetchone()[0]

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

        total_study_minutes = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM subjects
            WHERE student_id = ?
            """,
            (student_id,)
        )

        subject_count = cursor.fetchone()[0]

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

        if total_topics > 0:

            completion_rate = round(
                (
                    completed_topics /
                    total_topics
                ) * 100,
                2
            )

        else:

            completion_rate = 0

        return {
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "pending_topics": pending_topics,
            "total_study_minutes": total_study_minutes,
            "total_study_hours": round(
                total_study_minutes / 60,
                2
            ),
            "subject_count": subject_count,
            "average_fatigue": round(
                average_fatigue,
                2
            ),
            "completion_rate": completion_rate
        }

    finally:

        connection.close()


initialize_database()
