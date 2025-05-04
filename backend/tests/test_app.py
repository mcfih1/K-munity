import pytest
from app import app, db
from models import User, Request, Donation, Event
import json
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to K-munity API' in response.data

def test_user_registration(client):
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    response = client.post('/api/auth/register/',
                         data=json.dumps(data),
                         content_type='application/json')
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_user_login(client):
    # First register a user
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    client.post('/api/auth/register/',
               data=json.dumps(data),
               content_type='application/json')
    
    # Then try to login
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    response = client.post('/api/auth/login/',
                         data=json.dumps(login_data),
                         content_type='application/json')
    assert response.status_code == 200
    assert b'access_token' in response.data

def test_create_request(client):
    # First register and login
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    client.post('/api/auth/register/',
               data=json.dumps(data),
               content_type='application/json')
    
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    login_response = client.post('/api/auth/login/',
                               data=json.dumps(login_data),
                               content_type='application/json')
    token = json.loads(login_response.data)['access_token']
    
    # Create a request
    request_data = {
        'title': 'Test Request',
        'description': 'This is a test request',
        'request_type': 'food_aid',
        'location': 'Test Location',
        'urgency': 'normal'
    }
    response = client.post('/api/requests/',
                         data=json.dumps(request_data),
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert b'Request created successfully' in response.data

def test_get_requests(client):
    response = client.get('/api/requests/')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)

def test_create_event(client):
    # First register and login
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    client.post('/api/auth/register/',
               data=json.dumps(data),
               content_type='application/json')
    
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    login_response = client.post('/api/auth/login/',
                               data=json.dumps(login_data),
                               content_type='application/json')
    token = json.loads(login_response.data)['access_token']
    
    # Create an event
    event_data = {
        'title': 'Test Event',
        'description': 'This is a test event',
        'event_type': 'mentorship',
        'location': 'Test Location',
        'start_time': (datetime.now() + timedelta(days=1)).isoformat(),
        'end_time': (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        'max_participants': 10
    }
    response = client.post('/api/events/',
                         data=json.dumps(event_data),
                         content_type='application/json',
                         headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert b'Event created successfully' in response.data

def test_get_events(client):
    response = client.get('/api/events/')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list) 