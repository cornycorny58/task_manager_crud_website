import pytest
from Flask_app import app  
from Flask_app.models import Task 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Set up a test database 

    yield client

    # Teardown the test database 

def test_create_task(client):
    response = client.post('/create_task', data={'title': 'Test Task', 'priority': 1})
    assert response.status_code == 302  # Expecting a redirect after form submission

    # Check if the task is correctly added to the test database
    task = Task.query.filter_by(title='Test Task').first()
    assert task is not None
    assert task.priority == 1

