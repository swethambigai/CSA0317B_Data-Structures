import uuid
from datetime import date, timedelta
from app import create_app
from app.models import get_connection, initialize_database, create_student, get_dashboard_statistics
from app.datastructures.queue import StudyQueue
from app.datastructures.stack import RevisionStack
from app.datastructures.priority_queue import PriorityQueue
from app.datastructures.linked_list import RevisionLinkedList
from app.scheduler.fatigue_calculator import FatigueCalculator, calculate_fatigue_score, get_fatigue_level
from app.scheduler.study_scheduler import StudyScheduler
from app.scheduler.health_mode import HealthMaintenanceMode
from app.scheduler.revision_scheduler import RevisionScheduler
from app.utils.quotes import get_random_quote, get_motivation_message, QuoteManager


def test_priority_queue_ordering():
    pq = PriorityQueue()
    # High priority + hard topic
    pq.enqueue({"name": "Algorithms", "difficulty": 3, "urgency": 4, "deadline_days": 1, "priority": 1})
    # Low priority + easy topic
    pq.enqueue({"name": "History Basics", "difficulty": 1, "urgency": 0, "deadline_days": 10, "priority": 3})
    
    top = pq.dequeue()
    assert top["name"] == "Algorithms"


def test_revision_linked_list_cycles():
    ll = RevisionLinkedList()
    ll.append("Graph Theory", 1, date.today().isoformat())
    ll.append("Graph Theory", 2, (date.today() + timedelta(days=3)).isoformat())
    
    assert len(ll) == 2
    latest = ll.get_latest_revision("Graph Theory")
    assert latest.revision_number == 2


def test_fatigue_formula_exact_values():
    # Fatigue Score = (H * 2) + (C * 1.5) + (D * 1) - (B * 2) - (S * 1.5)
    # H=3, C=2, D=2, B=1, S=7
    # (3*2) + (2*1.5) + (2*1) - (1*2) - (7*1.5) = 6 + 3 + 2 - 2 - 10.5 = -1.5 -> clamped to 0 or raw
    calc = FatigueCalculator(hours_studied=3, continuous_sessions=2, difficulty=2, breaks=1, sleep_hours=7)
    assert calc.calculate_score() == -1.5
    assert calc.get_level(-1.5) == "Normal"

    # High fatigue scenario: H=6, C=4, D=3, B=0, S=4
    # (6*2) + (4*1.5) + (3*1) - (0*2) - (4*1.5) = 12 + 6 + 3 - 0 - 6 = 15.0
    calc2 = FatigueCalculator(hours_studied=6, continuous_sessions=4, difficulty=3, breaks=0, sleep_hours=4)
    assert calc2.calculate_score() == 15.0
    assert calc2.get_level(15.0) == "High Fatigue"
    assert calc2.is_high_fatigue(15.0) is True


def test_motivation_progress_messages():
    msg_complete = get_motivation_message(completed_tasks=5, pending_tasks=0, streak=2)
    assert "completed today's study plan" in msg_complete

    msg_streak = get_motivation_message(completed_tasks=2, pending_tasks=3, streak=5)
    assert "5-day study streak" in msg_streak

    msg_pending = get_motivation_message(completed_tasks=0, pending_tasks=3, streak=1)
    assert "Small progress every day" in msg_pending


def test_full_user_workflow():
    app = create_app()
    app.config["TESTING"] = True
    email = f"student-{uuid.uuid4().hex[:8]}@example.com"

    with app.test_client() as client:
        # 1. Register
        reg_res = client.post(
            "/register",
            data={
                "name": "Integration Student",
                "email": email,
                "password": "mypassword123",
                "confirm_password": "mypassword123",
                "sleep_hours": "8",
                "study_hours": "3",
                "mood": "happy"
            },
            follow_redirects=True
        )
        assert reg_res.status_code == 200
        assert b"Hey, Integration Student!" in reg_res.data

        # 2. Add Subject & Topics
        client.post(
            "/planner",
            data={
                "action": "add_subject",
                "subject_name": "Software Engineering",
                "description": "Design patterns and architectures"
            },
            follow_redirects=True
        )

        client.post(
            "/planner",
            data={
                "action": "add_topic",
                "subject": "Software Engineering",
                "topic": "Factory Pattern",
                "difficulty": "2",
                "duration": "45",
                "priority": "1"
            },
            follow_redirects=True
        )

        # 3. Generate Plan
        gen_res = client.post(
            "/planner",
            data={
                "action": "generate_plan",
                "study_hours": "2",
                "sessions": "1",
                "breaks": "1",
                "sleep": "7.5",
                "difficulty": "2",
                "mood": "happy",
                "available_time": "240"
            },
            follow_redirects=True
        )
        assert gen_res.status_code == 200
        assert b"Factory Pattern" in gen_res.data

        # 4. View Revision Center
        rev_res = client.get("/revision")
        assert rev_res.status_code == 200
        assert b"Revision Center" in rev_res.data

        # 5. View Analytics
        analytics_res = client.get("/analytics")
        assert analytics_res.status_code == 200
        assert b"Analytics Dashboard" in analytics_res.data

        # 6. View Health Mode
        health_res = client.get("/health-mode")
        assert health_res.status_code == 200
        assert b"Health Maintenance Mode" in health_res.data

        # 7. View Profile & Update Settings
        profile_res = client.get("/profile")
        assert profile_res.status_code == 200
        assert b"Integration Student" in profile_res.data

        # 8. Export Data CSV
        export_res = client.post(
            "/profile/update",
            data={"action": "export_data"}
        )
        assert export_res.status_code == 200
        assert export_res.headers.get("Content-Type") == "text/csv"
        assert b"study_date,duration_minutes" in export_res.data
