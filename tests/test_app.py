import pytest
import os
import tempfile
from app import app, init_db
from db import get_db_connection

@pytest.fixture
def client():
    # Configure a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    
    # We need to monkeypatch or route the db connection to this temp file
    # For this simple example, we will just manually swap the DB name in db.py context
    # ideally, db.py would read from app.config
    
    # Simpler approach for this specific setup without rewriting db.py structure:
    # We will use a setup/teardown with a specific test db name 
    import db
    old_db_name = db.DATABASE
    db.DATABASE = db_path
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    db.DATABASE = old_db_name

def test_get_tasks_empty(client):
    """Test retrieving tasks when DB is empty."""
    rv = client.get('/api/tasks')
    assert rv.status_code == 200
    assert rv.json == []

def test_create_task(client):
    """Test creating a new task."""
    rv = client.post('/api/tasks', json={
        'title': 'Test Task',
        'description': 'Test Desc',
        'due_date': '2023-12-31',
        'status': 'Pending'
    })
    assert rv.status_code == 201
    assert 'id' in rv.json

def test_get_single_task(client):
    """Test retrieving a specific task."""
    # Create first
    client.post('/api/tasks', json={'title': 'To Retrieve'})
    
    rv = client.get('/api/tasks/1')
    assert rv.status_code == 200
    assert rv.json['title'] == 'To Retrieve'

def test_update_task(client):
    """Test updating a task."""
    client.post('/api/tasks', json={'title': 'Old Title'})
    
    rv = client.put('/api/tasks/1', json={'title': 'New Title'})
    assert rv.status_code == 200
    
    # Verify update
    rv_get = client.get('/api/tasks/1')
    assert rv_get.json['title'] == 'New Title'

def test_delete_task(client):
    """Test deleting a task."""
    client.post('/api/tasks', json={'title': 'To Delete'})
    
    rv = client.delete('/api/tasks/1')
    assert rv.status_code == 200
    
    rv_get = client.get('/api/tasks/1')
    assert rv_get.status_code == 404