"""
Test Suite: Authentication — Registration, Login, Session, and Profile API endpoints.
"""
import json

def test_register_new_user(client):
    """Test successful student registration."""
    res = client.post('/api/v1/register', json={
        'name': 'New Student',
        'email': 'newstudent@test.com',
        'password': 'securepass123',
        'department': 'Computer Science',
        'skills': 'Python, Flask'
    })
    data = json.loads(res.data)
    assert res.status_code == 201
    assert data['status'] == 'success'
    assert data['user']['name'] == 'New Student'
    assert data['user']['email'] == 'newstudent@test.com'

def test_register_duplicate_email(client):
    """Test that duplicate email returns error."""
    payload = {
        'name': 'Dup User',
        'email': 'dup@test.com',
        'password': 'pass123456',
    }
    client.post('/api/v1/register', json=payload)
    res = client.post('/api/v1/register', json=payload)
    data = json.loads(res.data)
    assert res.status_code == 400
    assert 'already registered' in data['error']

def test_register_missing_fields(client):
    """Test registration fails with missing required fields."""
    res = client.post('/api/v1/register', json={
        'name': '',
        'email': '',
        'password': ''
    })
    data = json.loads(res.data)
    assert res.status_code == 400
    assert data['status'] == 'error'

def test_login_success(client, auth_user):
    """Test successful login with valid credentials."""
    res = client.post('/api/v1/login', json={
        'email': 'teststudent@gmail.com',
        'password': 'password123'
    })
    data = json.loads(res.data)
    assert res.status_code == 200
    assert data['status'] == 'success'
    assert data['user']['email'] == 'teststudent@gmail.com'

def test_login_wrong_password(client, auth_user):
    """Test login fails with wrong password."""
    res = client.post('/api/v1/login', json={
        'email': 'teststudent@gmail.com',
        'password': 'wrongpassword'
    })
    data = json.loads(res.data)
    assert res.status_code == 401
    assert data['status'] == 'error'

def test_login_missing_fields(client):
    """Test login fails with missing fields."""
    res = client.post('/api/v1/login', json={
        'email': '',
        'password': ''
    })
    data = json.loads(res.data)
    assert res.status_code == 400

def test_logout(client, auth_user):
    """Test logout after a successful login."""
    client.post('/api/v1/login', json={
        'email': 'teststudent@gmail.com',
        'password': 'password123'
    })
    res = client.post('/api/v1/logout', json={})
    data = json.loads(res.data)
    assert res.status_code == 200
    assert data['status'] == 'success'

def test_profile_get(client, auth_user):
    """Test fetching authenticated user profile."""
    client.post('/api/v1/login', json={
        'email': 'teststudent@gmail.com',
        'password': 'password123'
    })
    res = client.get('/api/v1/profile')
    data = json.loads(res.data)
    assert res.status_code == 200
    assert data['user']['name'] == 'Test Student'

def test_profile_update(client, auth_user):
    """Test updating user profile fields."""
    client.post('/api/v1/login', json={
        'email': 'teststudent@gmail.com',
        'password': 'password123'
    })
    res = client.put('/api/v1/profile', json={
        'name': 'Updated Name',
        'skills': 'Python, TensorFlow, React'
    })
    data = json.loads(res.data)
    assert res.status_code == 200
    assert data['user']['name'] == 'Updated Name'
    assert 'TensorFlow' in data['user']['skills']
