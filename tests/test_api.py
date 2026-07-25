"""
Test Suite: REST API Endpoints — Idea generation, dashboard, validation, mentor chat.
"""
import json

def _login(client):
    """Helper: register and login a test user, return response."""
    client.post('/api/v1/register', json={
        'name': 'API Tester',
        'email': 'apitester@test.com',
        'password': 'testpass123',
        'skills': 'Python'
    })
    return client.post('/api/v1/login', json={
        'email': 'apitester@test.com',
        'password': 'testpass123'
    })

def test_generate_idea_endpoint(client, app):
    """Test POST /api/v1/generate-idea creates a startup."""
    with app.app_context():
        _login(client)
        res = client.post('/api/v1/generate-idea', json={
            'domain': 'Healthcare',
            'skills': 'Python, TensorFlow',
            'budget': '50000',
            'interest': 'Medical AI'
        })
        data = json.loads(res.data)
        assert res.status_code == 201
        assert data['status'] == 'success'
        assert 'startup_name' in data
        assert 'startup_id' in data

def test_ideas_list_endpoint(client, app):
    """Test GET /api/v1/ideas returns user's projects."""
    with app.app_context():
        _login(client)
        res = client.get('/api/v1/ideas')
        data = json.loads(res.data)
        assert res.status_code == 200
        assert 'ideas' in data

def test_dashboard_endpoint(client, app):
    """Test GET /api/v1/dashboard returns analytics stats."""
    with app.app_context():
        _login(client)
        res = client.get('/api/v1/dashboard')
        data = json.loads(res.data)
        assert res.status_code == 200
        assert 'stats' in data
        assert 'total_ideas' in data['stats']

def test_validation_endpoint(client, app):
    """Test POST /api/v1/validate returns correct weighted score."""
    with app.app_context():
        _login(client)
        res = client.post('/api/v1/validate', json={
            'innovation': 90,
            'market': 85,
            'technology': 80,
            'business': 88
        })
        data = json.loads(res.data)
        assert res.status_code == 200
        assert data['overall'] == 85.6

def test_mentor_chat_endpoint(client, app):
    """Test POST /api/v1/mentor-chat returns a reply."""
    with app.app_context():
        _login(client)
        res = client.post('/api/v1/mentor-chat', json={
            'message': 'How do I validate my market size?'
        })
        data = json.loads(res.data)
        assert res.status_code == 200
        assert data['status'] == 'success'
        assert len(data['reply']) > 10

def test_mentor_chat_empty_message(client, app):
    """Test mentor chat rejects empty messages."""
    with app.app_context():
        _login(client)
        res = client.post('/api/v1/mentor-chat', json={'message': ''})
        data = json.loads(res.data)
        assert res.status_code == 400

def test_unauthenticated_access(client):
    """Test that unauthenticated requests to protected routes return 401."""
    res = client.get('/api/v1/dashboard')
    assert res.status_code in [401, 302]
