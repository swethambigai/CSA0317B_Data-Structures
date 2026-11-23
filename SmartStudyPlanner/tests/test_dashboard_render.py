import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from app import create_app
from app.models import get_connection, initialize_database, create_student, create_subject, create_topic

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    
    # Use temporary database for testing if needed, or default database
    with app.test_client() as client:
        yield client

def test_dashboard_authenticated(client):
    # Setup test database records
    initialize_database()
    
    # Try to create a test user
    connection = get_connection()
    cursor = connection.cursor()
    
    # Clean up previous test runs if any
    cursor.execute("DELETE FROM students WHERE email = 'test@example.com'")
    connection.commit()
    connection.close()
    
    # Register/Create student
    student_id = create_student("Test Student", "test@example.com", "password123")
    assert student_id is not None
    
    # Add subject & topics
    subject_id = create_subject(student_id, "Computer Science", "Core courses")
    create_topic(subject_id, "Data Structures & Algorithms", difficulty=2, estimated_minutes=90, priority=3)
    create_topic(subject_id, "System Programming", difficulty=3, estimated_minutes=120, priority=2)
    
    with client.session_transaction() as sess:
        sess["student_id"] = student_id
        sess["student_name"] = "Test Student"
        sess["student_email"] = "test@example.com"
        
    response = client.get("/dashboard")
    assert response.status_code == 200
    
    # Verify dashboard contains our new dynamic elements
    html = response.data.decode("utf-8")
    assert "Hey, Test Student!" in html
    assert "Computer Science" in html
    assert "Data Structures &amp; Algorithms" in html or "Data Structures" in html
    assert "remaining to study" in html
