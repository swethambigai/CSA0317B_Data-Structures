import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app


def test_add_topic_updates_planner_queue():
    app = create_app()
    email = f"planner-{uuid.uuid4().hex[:8]}@example.com"

    with app.test_client() as client:
        register = client.post(
            "/register",
            data={
                "name": "Planner User",
                "email": email,
                "password": "secret123",
            },
            follow_redirects=False,
        )
        assert register.status_code == 302

        add_topic = client.post(
            "/planner",
            data={
                "action": "add_topic",
                "subject": "Mathematics",
                "title": "Algebra Basics",
                "difficulty": "1",
                "duration": "30",
                "priority": "2",
            },
            follow_redirects=False,
        )
        assert add_topic.status_code == 302

        with client.session_transaction() as session:
            assert "smart_plan" in session
            assert session["smart_plan"]

        planner_page = client.get("/planner")
        assert planner_page.status_code == 200
        assert b"Algebra Basics" in planner_page.data


def test_health_mode_page_loads_for_logged_in_student():
    app = create_app()
    email = f"health-{uuid.uuid4().hex[:8]}@example.com"

    with app.test_client() as client:
        client.post(
            "/register",
            data={
                "name": "Health User",
                "email": email,
                "password": "secret123",
            },
            follow_redirects=False,
        )

        response = client.get("/health-mode")
        assert response.status_code == 200
        assert b"Health Maintenance Mode" in response.data
