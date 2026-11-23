from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)
from datetime import date, datetime, timedelta

from app.models import (
    create_student,
    get_student_by_email,
    get_subjects,
    get_topics,
    get_dashboard_statistics,
    create_subject,
    create_topic,
    complete_topic,
    set_topic_completed_at,
    create_study_session,
    create_fatigue_record,
    update_student_password,
    get_student_settings,
    update_student_settings,
    get_study_sessions,
    record_revision_completion,
    get_pending_revisions,
    complete_revision,
    get_completed_revisions,
    add_revision,
    get_study_streak,
    get_fatigue_history,
    get_latest_fatigue
)

from app.datastructures.queue import StudyQueue
from app.datastructures.stack import RevisionStack
from app.datastructures.priority_queue import PriorityQueue
from app.datastructures.linked_list import RevisionLinkedList
from app.scheduler.fatigue_calculator import FatigueCalculator, calculate_fatigue_score
from app.scheduler.study_scheduler import StudyScheduler
from app.scheduler.health_mode import HealthMaintenanceMode
from app.scheduler.revision_scheduler import RevisionScheduler
from app.utils.quotes import (
    get_random_quote,
    get_motivation_quote,
    get_motivation_message,
    QuoteManager
)


# ============================================================
# BLUEPRINT
# ============================================================

routes = Blueprint(
    "routes",
    __name__
)


# ============================================================
# FATIGUE CALCULATION
# ============================================================

def calculate_fatigue(
    study_hours=0,
    continuous_sessions=0,
    breaks=0,
    sleep_hours=0,
    mood="neutral",
    difficulty=1
):
    """
    Calculate student's fatigue score using the standard formula:
    Fatigue Score = (H * 2) + (C * 1.5) + (D * 1) - (B * 2) - (S * 1.5)
    
    H = hours studied
    C = continuous sessions
    D = difficulty
    B = breaks
    S = sleep hours
    """
    try:
        h = float(study_hours)
    except (ValueError, TypeError):
        h = 0.0

    try:
        c = float(continuous_sessions)
    except (ValueError, TypeError):
        c = 0.0

    try:
        d = float(difficulty)
    except (ValueError, TypeError):
        d = 1.0

    try:
        b = float(breaks)
    except (ValueError, TypeError):
        b = 0.0

    try:
        s = float(sleep_hours)
    except (ValueError, TypeError):
        s = 0.0

    h = max(0.0, h)
    c = max(0.0, c)
    d = max(1.0, min(d, 5.0))
    b = max(0.0, b)
    s = max(0.0, min(s, 24.0))

    calc = FatigueCalculator(
        hours_studied=h,
        continuous_sessions=c,
        difficulty=d,
        breaks=b,
        sleep_hours=s
    )
    score = calc.calculate_score()
    return max(0.0, round(score, 1))


def get_fatigue_level(score):
    """
    Convert numerical fatigue score into standard level.
    0–5 = Normal
    6–10 = Mild Fatigue
    11–15 = High Fatigue
    >15 = Critical Fatigue
    """
    if score <= 5:
        return "Normal"
    elif score <= 10:
        return "Mild Fatigue"
    elif score <= 15:
        return "High Fatigue"
    else:
        return "Critical Fatigue"


# ============================================================
# SMART PLAN GENERATOR
# ============================================================

def generate_smart_plan(topics, fatigue_score, available_minutes=300):
    """
    Organize pending study topics using PriorityQueue and StudyQueue
    with adaptive fatigue awareness.
    """
    scheduler = StudyScheduler()
    scheduler.fatigue_calculator.update(
        hours_studied=max(0, fatigue_score / 2),
        continuous_sessions=1,
        difficulty=2,
        breaks=1,
        sleep_hours=7
    )

    # Filter unfinished topics
    pending = [t for t in topics if t.get("status") != "Completed"]
    if not pending:
        return []

    # Populate topics into scheduler
    for t in pending:
        scheduler.add_topic(
            name=t.get("title") or t.get("name", "Unnamed Topic"),
            title=t.get("title") or t.get("name", "Unnamed Topic"),
            subject=t.get("subject_name") or t.get("subject", "General"),
            subject_name=t.get("subject_name") or t.get("subject", "General"),
            difficulty=t.get("difficulty", 1),
            duration=t.get("estimated_minutes", 60),
            estimated_minutes=t.get("estimated_minutes", 60),
            priority=t.get("priority", 2),
            urgency=t.get("urgency", 0),
            deadline_days=t.get("deadline_days", 7),
            id=t.get("id"),
            status=t.get("status", "Pending")
        )

    # Create schedule via scheduler
    schedule_result = scheduler.create_schedule(available_minutes)
    scheduled_items = schedule_result.get("schedule", [])

    if scheduled_items:
        return scheduled_items

    # Fallback to prioritized pending topics if minutes limit excluded some
    return scheduler.prioritize_topics()


# ============================================================
# HOME PAGE
# ============================================================

@routes.route("/")
def index():
    return render_template("index.html")


# ============================================================
# REGISTER
# ============================================================

@routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        sleep_hours = request.form.get("sleep_hours", "7.5")
        study_hours = request.form.get("study_hours", "4")
        mood = request.form.get("mood", "neutral")

        if not name or not email or not password:
            flash("Please fill in all required fields.", "error")
            return render_template("register.html")

        if confirm_password and password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        student_id = create_student(name, email, password)

        if student_id is None:
            flash("An account with this email already exists.", "error")
            return render_template("register.html")

        session["student_id"] = student_id
        session["student_name"] = name
        session["student_email"] = email
        session["sleep"] = sleep_hours
        session["study_hours"] = study_hours
        session["mood"] = mood

        # Initial fatigue calculation
        init_fatigue = calculate_fatigue(
            study_hours=study_hours,
            continuous_sessions=1,
            breaks=1,
            sleep_hours=sleep_hours,
            mood=mood,
            difficulty=1
        )
        session["fatigue_score"] = init_fatigue
        session["fatigue_level"] = get_fatigue_level(init_fatigue)

        flash("Welcome to Smart Study Planner!", "success")
        return redirect(url_for("routes.dashboard"))

    return render_template("register.html")


# ============================================================
# LOGIN
# ============================================================

@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        student = get_student_by_email(email)

        if student is not None and student.get("password") == password:
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            session["student_email"] = email

            # Load latest fatigue if available
            latest_fatigue = get_latest_fatigue(student["id"])
            if latest_fatigue:
                session["fatigue_score"] = latest_fatigue.get("fatigue_score", 5)
                session["fatigue_level"] = latest_fatigue.get("fatigue_level", "Normal")

            flash(f"Welcome back, {student['name']}!", "success")
            return redirect(url_for("routes.dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================

@routes.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out safely.", "info")
    return redirect(url_for("routes.index"))


# ============================================================
# DASHBOARD
# ============================================================

@routes.route("/dashboard")
def dashboard():
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    statistics = get_dashboard_statistics(student_id)
    topics = get_topics(student_id)

    pending_topics = [t for t in topics if t.get("status") != "Completed"]
    completed_topics = [t for t in topics if t.get("status") == "Completed"]

    fatigue_score = session.get("fatigue_score", statistics.get("average_fatigue", 5))
    try:
        fatigue_score = float(fatigue_score)
    except (ValueError, TypeError):
        fatigue_score = 5.0

    fatigue_level = get_fatigue_level(fatigue_score)

    # Dynamic Smart Plan for today's schedule
    smart_plan = generate_smart_plan(topics, fatigue_score)

    # Motivational component
    streak = statistics.get("study_streak", 1)
    mood = session.get("mood", "neutral")
    quote_data = get_motivation_quote(mood=mood, fatigue_score=fatigue_score)
    motivation_msg = get_motivation_message(
        completed_tasks=len(completed_topics),
        pending_tasks=len(pending_topics),
        streak=streak,
        productivity=statistics.get("completion_percentage", 0)
    )

    return render_template(
        "dashboard.html",
        statistics=statistics,
        pending_topics=pending_topics,
        completed_topics=completed_topics,
        smart_plan=smart_plan,
        student_name=session.get("student_name", "Student"),
        fatigue_score=fatigue_score,
        fatigue_level=fatigue_level,
        daily_quote=quote_data.get("quote", "Small steps every day create big results."),
        quote_category=quote_data.get("category", "motivation"),
        motivation_message=motivation_msg,
        study_streak=streak
    )


# ============================================================
# PLANNER
# ============================================================

@routes.route("/planner", methods=["GET", "POST"])
def planner():
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    if request.method == "POST":
        action = request.form.get("action", "")

        # ----------------------------------------------------
        # ADD SUBJECT
        # ----------------------------------------------------
        if action == "add_subject":
            subject_name = request.form.get("subject_name", "").strip() or request.form.get("subject", "").strip()
            description = request.form.get("description", "").strip()

            if subject_name:
                create_subject(student_id, subject_name, description)
                flash(f"Subject '{subject_name}' added successfully.", "success")
            else:
                flash("Please enter a subject name.", "error")

            return redirect(url_for("routes.planner"))

        # ----------------------------------------------------
        # ADD TOPIC / GENERATE PLAN
        # ----------------------------------------------------
        if action in ("add_topic", "generate_plan"):
            subject_name = request.form.get("subject", "").strip() or request.form.get("subject_name", "").strip()
            title = request.form.get("topic", "").strip() or request.form.get("title", "").strip()
            difficulty = request.form.get("difficulty", "2").strip()
            deadline = request.form.get("deadline", "").strip() or request.form.get("deadline_date", "").strip()
            duration = request.form.get("duration", "").strip() or request.form.get("estimated_minutes", "60").strip()
            break_duration = request.form.get("break_duration", "").strip() or request.form.get("breaks", "15").strip()
            available_time = request.form.get("available_time", "3").strip()
            priority = request.form.get("priority", "2").strip()

            # Condition inputs
            study_hours = request.form.get("study_hours", session.get("study_hours", 0))
            sessions = request.form.get("sessions", session.get("sessions", 1))
            breaks = request.form.get("breaks", session.get("breaks", 1))
            sleep = request.form.get("sleep", session.get("sleep", 7.5))
            mood = request.form.get("mood", session.get("mood", "neutral"))

            # Convert available study time to minutes
            try:
                avail_float = float(available_time)
                avail_min = int(avail_float * 60) if avail_float <= 24 else int(avail_float)
            except (ValueError, TypeError):
                avail_min = 180

            # Convert numeric inputs
            try:
                diff_val = int(difficulty)
            except (ValueError, TypeError):
                diff_map = {"easy": 1, "medium": 2, "moderate": 2, "hard": 3, "critical": 4}
                diff_val = diff_map.get(str(difficulty).lower().strip(), 2)

            try:
                dur_val = int(duration)
            except (ValueError, TypeError):
                dur_val = 60

            try:
                prio_val = int(priority)
            except (ValueError, TypeError):
                prio_val = 2

            diff_val = max(1, min(diff_val, 5))
            dur_val = max(10, dur_val)
            prio_val = max(1, min(prio_val, 3))

            # If user typed subject and topic, add it to DB
            if title:
                if not subject_name:
                    subject_name = "General Studies"

                # Find or create subject by exact typed name
                subjects = get_subjects(student_id)
                subject_id = None
                for s in subjects:
                    if s.get("name", "").strip().lower() == subject_name.strip().lower():
                        subject_id = s.get("id")
                        break

                if not subject_id:
                    subject_id = create_subject(student_id, subject_name.strip(), "")

                try:
                    create_topic(
                        int(subject_id),
                        title,
                        difficulty=diff_val,
                        estimated_minutes=dur_val,
                        priority=prio_val
                    )
                except Exception as e:
                    print("Error creating topic:", e)

            # Calculate fatigue
            fatigue_score = calculate_fatigue(
                study_hours=study_hours,
                continuous_sessions=sessions,
                breaks=breaks,
                sleep_hours=sleep,
                mood=mood,
                difficulty=diff_val
            )
            fatigue_level = get_fatigue_level(fatigue_score)

            try:
                create_fatigue_record(
                    student_id=student_id,
                    record_date=date.today().isoformat(),
                    study_hours=float(study_hours or 0),
                    continuous_sessions=int(sessions or 0),
                    difficulty=diff_val,
                    breaks_taken=int(breaks or 0),
                    sleep_hours=float(sleep or 0),
                    mood=mood,
                    fatigue_score=fatigue_score,
                    fatigue_level=fatigue_level,
                    health_mode=1 if fatigue_score > 15 else 0
                )
            except Exception as err:
                print("Could not save fatigue record:", err)

            session["fatigue_score"] = fatigue_score
            session["fatigue_level"] = fatigue_level
            session["study_hours"] = study_hours
            session["sessions"] = sessions
            session["breaks"] = breaks
            session["sleep"] = sleep
            session["mood"] = mood

            # Refresh Smart Plan
            topics = get_topics(student_id)
            smart_plan = generate_smart_plan(topics, fatigue_score, available_minutes=avail_min)
            session["smart_plan"] = [t.get("id") for t in smart_plan if t.get("id") is not None]

            if action == "generate_plan":
                flash(f"Smart Study Plan generated! Fatigue: {fatigue_score} ({fatigue_level}).", "success")
            else:
                flash(f"Added '{subject_name} → {title}' to your queue!", "success")

            return redirect(url_for("routes.planner"))

        # ----------------------------------------------------
        # COMPLETE TOPIC
        # ----------------------------------------------------
        if action == "complete_topic":
            topic_id = request.form.get("topic_id", "")
            if topic_id:
                try:
                    topic_id_int = int(topic_id)
                    complete_topic(topic_id_int)

                    topics_all = get_topics(student_id)
                    topic_info = next((t for t in topics_all if t.get("id") == topic_id_int), None)

                    duration = int(topic_info.get("estimated_minutes", 60) or 60) if topic_info else 60

                    # Log study session for analytics
                    create_study_session(
                        student_id=student_id,
                        topic_id=topic_id_int,
                        study_date=date.today().isoformat(),
                        duration_minutes=duration,
                        continuous_sessions=1,
                        breaks_taken=1,
                        mood=session.get("mood", "neutral"),
                        completed=1
                    )

                    # Add to spaced revision schedule (1 day out for Cycle 1)
                    next_rev = (date.today() + timedelta(days=1)).isoformat()
                    add_revision(student_id, topic_id_int, revision_cycle=1, revision_date=next_rev)

                    # Update smart plan in session
                    smart_plan_ids = session.get("smart_plan", [])
                    if topic_id_int in smart_plan_ids:
                        smart_plan_ids.remove(topic_id_int)
                        session["smart_plan"] = smart_plan_ids

                    flash("Topic marked as completed and queued for spaced revision! 🎉", "success")
                except Exception as e:
                    print("Error completing topic:", e)
                    flash("Could not mark topic as completed.", "error")

            return redirect(url_for("routes.planner"))

    # --------------------------------------------------------
    # GET PLANNER VIEW
    # --------------------------------------------------------
    subjects = get_subjects(student_id)
    topics = get_topics(student_id)

    fatigue_score = session.get("fatigue_score", 5)
    try:
        fatigue_score = float(fatigue_score)
    except (ValueError, TypeError):
        fatigue_score = 5.0

    fatigue_level = get_fatigue_level(fatigue_score)

    # Recover or generate smart plan
    smart_plan_ids = session.get("smart_plan", [])
    topic_map = {t.get("id"): t for t in topics}

    smart_plan = []
    if smart_plan_ids:
        for tid in smart_plan_ids:
            if tid in topic_map and topic_map[tid].get("status") != "Completed":
                smart_plan.append(topic_map[tid])

    if not smart_plan:
        smart_plan = generate_smart_plan(topics, fatigue_score)
        session["smart_plan"] = [t.get("id") for t in smart_plan if t.get("id") is not None]

    # Calculate total estimated hours in queue
    total_est_minutes = sum(int(t.get("estimated_minutes", 60) or 60) for t in smart_plan)
    total_est_hours = round(total_est_minutes / 60, 1)

    return render_template(
        "planner.html",
        subjects=subjects,
        topics=topics,
        smart_plan=smart_plan,
        total_est_hours=total_est_hours,
        fatigue_score=fatigue_score,
        fatigue_level=fatigue_level,
        study_hours=session.get("study_hours", ""),
        sessions=session.get("sessions", ""),
        breaks=session.get("breaks", ""),
        sleep=session.get("sleep", ""),
        mood=session.get("mood", "neutral")
    )


# ============================================================
# ANALYTICS
# ============================================================

@routes.route("/analytics")
def analytics():
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    statistics = get_dashboard_statistics(student_id)
    topics = get_topics(student_id)
    sessions = get_study_sessions(student_id)
    fatigue_history = get_fatigue_history(student_id)

    return render_template(
        "analytics.html",
        statistics=statistics,
        topics=topics,
        sessions=sessions,
        fatigue_history=fatigue_history
    )


# ============================================================
# HEALTH MAINTENANCE MODE
# ============================================================

@routes.route("/health-mode")
def health_mode():
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    fatigue_score = session.get("fatigue_score", 5)
    try:
        fatigue_score = float(fatigue_score)
    except (ValueError, TypeError):
        fatigue_score = 5.0

    fatigue_level = get_fatigue_level(fatigue_score)
    statistics = get_dashboard_statistics(student_id)

    # Evaluate Health Mode
    calc = FatigueCalculator()
    health_controller = HealthMaintenanceMode(fatigue_calculator=calc)
    health_plan = health_controller.apply(fatigue_score)

    return render_template(
        "health_mode.html",
        fatigue_score=fatigue_score,
        fatigue_level=fatigue_level,
        statistics=statistics,
        health_plan=health_plan
    )


# ============================================================
# REVISION CENTER
# ============================================================

@routes.route("/revision")
def revision():
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    topics = get_topics(student_id)
    completed_topics = [t for t in topics if t.get("status") == "Completed"]
    
    # Ensure completed topics have an initial revision row if missing
    existing_pending = get_pending_revisions(student_id)
    existing_completed = get_completed_revisions(student_id)
    existing_topic_ids = {r.get("topic_id") for r in (existing_pending + existing_completed) if r.get("topic_id") is not None}
    
    for ct in completed_topics:
        if ct.get("id") not in existing_topic_ids:
            add_revision(student_id, ct["id"], revision_cycle=1, revision_date=date.today().isoformat())

    # Get updated active and completed lists
    pending_revisions = get_pending_revisions(student_id)
    completed_revisions = get_completed_revisions(student_id)

    # Use RevisionStack for completed revisions
    stack = RevisionStack()
    for t in completed_revisions:
        stack.push(t)

    recent_completed = stack.get_all()

    return render_template(
        "revision.html",
        topics=topics,
        completed_topics=completed_topics,
        recent_completed=recent_completed,
        pending_revisions=pending_revisions,
        completed_revisions=completed_revisions
    )


@routes.route("/revision/start/<int:topic_id>")
def start_revision(topic_id):
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    topics = get_topics(student_id)
    selected_topic = next((t for t in topics if t.get("id") == topic_id), None)

    if selected_topic is None:
        flash("Revision topic not found.", "error")
        return redirect(url_for("routes.revision"))

    session["revision_topic_id"] = topic_id

    # Check pending revision record cycle
    pending = get_pending_revisions(student_id)
    topic_rev = next((r for r in pending if r.get("topic_id") == topic_id), None)
    revision_cycle = topic_rev.get("revision_cycle", 1) if topic_rev else 1

    return render_template(
        "revision_session.html",
        topic=selected_topic,
        revision_cycle=revision_cycle
    )


@routes.route("/revision/finish/<int:topic_id>", methods=["POST"])
def finish_revision(topic_id):
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    try:
        revision_id = request.form.get("revision_id")
        if revision_id:
            complete_revision(revision_id=int(revision_id))
        else:
            complete_revision(student_id=student_id, topic_id=topic_id)

        # Log study session for revision
        create_study_session(
            student_id=student_id,
            topic_id=topic_id,
            study_date=date.today().isoformat(),
            duration_minutes=20,
            continuous_sessions=1,
            breaks_taken=0,
            mood=session.get("mood", "neutral"),
            completed=1
        )

        flash("Revision completed successfully! ✓", "success")
    except Exception as e:
        print("Error finishing revision:", e)
        flash("Could not complete revision record.", "error")

    return redirect(url_for("routes.revision"))


# ============================================================
# CALENDAR
# ============================================================

@routes.route("/calendar", methods=["GET", "POST"])
def calendar():
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    if request.method == "POST":
        topic_id = request.form.get("topic_id")
        date_selected = request.form.get("completed_date")

        if topic_id and date_selected:
            try:
                set_topic_completed_at(int(topic_id), date_selected)
                create_study_session(
                    student_id=student_id,
                    topic_id=int(topic_id),
                    study_date=date_selected,
                    duration_minutes=60,
                    continuous_sessions=1,
                    breaks_taken=1,
                    mood=session.get("mood", "neutral"),
                    completed=1
                )
                flash("Topic marked as completed on calendar.", "success")
            except Exception as e:
                print("Calendar error:", e)
                flash("Could not update topic completion.", "error")

        return redirect(url_for("routes.calendar"))

    topics = get_topics(student_id)
    return render_template("calendar.html", topics=topics)


# ============================================================
# PROFILE & SETTINGS
# ============================================================

@routes.route("/profile")
def profile():
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    student = get_student_by_email(session.get("student_email", ""))
    settings = get_student_settings(student_id)
    statistics = get_dashboard_statistics(student_id)

    return render_template(
        "profile.html",
        student=student,
        settings=settings,
        statistics=statistics,
        student_name=session.get("student_name", "Student")
    )


@routes.route("/profile/update", methods=["POST"])
def profile_update():
    student_id = session.get("student_id")
    if student_id is None:
        return redirect(url_for("routes.login"))

    action = request.form.get("action", "")

    if action == "change_password":
        current = request.form.get("current_password", "")
        new = request.form.get("new_password", "")

        student = get_student_by_email(session.get("student_email", ""))
        if student is None or student.get("password") != current:
            flash("Current password is incorrect.", "error")
            return redirect(url_for("routes.profile"))

        if not new or len(new) < 6:
            flash("New password must be at least 6 characters.", "error")
            return redirect(url_for("routes.profile"))

        update_student_password(student_id, new)
        flash("Password updated successfully.", "success")
        return redirect(url_for("routes.profile"))

    if action == "toggle_notifications":
        enabled = request.form.get("notifications_enabled", "0")
        update_student_settings(student_id, enabled == "1")
        flash("Notification settings updated.", "success")
        return redirect(url_for("routes.profile"))

    if action == "export_data":
        import io, csv
        sessions = get_study_sessions(student_id)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["study_date", "duration_minutes", "topic_title", "subject_name", "completed"])

        for s in sessions:
            writer.writerow([
                s.get("study_date", ""),
                s.get("duration_minutes", 0),
                s.get("topic_title", ""),
                s.get("subject_name", ""),
                s.get("completed", 0)
            ])

        csv_data = output.getvalue()
        return (
            csv_data,
            200,
            {
                "Content-Type": "text/csv",
                "Content-Disposition": "attachment; filename=study_sessions.csv"
            }
        )

    flash("Unknown action.", "error")
    return redirect(url_for("routes.profile"))


@routes.route("/api/settings")
def api_settings():
    student_id = session.get("student_id")
    if student_id is None:
        return jsonify({"error": "not_authenticated"}), 401

    settings = get_student_settings(student_id)
    return jsonify({
        "notifications_enabled": bool(settings and settings.get("notifications_enabled"))
    })


@routes.route("/health")
def health():
    return {
        "status": "running",
        "application": "Smart Study Planner"
    }
