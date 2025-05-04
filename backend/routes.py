from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Request, Donation, Event
from app import db
from datetime import datetime
import stripe
import os

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Authentication Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@auth_bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
        
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
        
    user = User(
        username=data['username'],
        email=data['email'],
        role=data.get('role', 'user')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
@auth_bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_vip': user.is_vip
            }
        }), 200
        
    return jsonify({'error': 'Invalid credentials'}), 401

# Requests Blueprint
requests_bp = Blueprint('requests', __name__)

@requests_bp.route('/', methods=['POST'])
@requests_bp.route('', methods=['POST'])
@jwt_required()
def create_request():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    request_obj = Request(
        user_id=user_id,
        title=data['title'],
        description=data['description'],
        request_type=data['request_type'],
        location=data.get('location'),
        urgency=data.get('urgency', 'normal')
    )
    
    db.session.add(request_obj)
    db.session.commit()
    
    return jsonify({'message': 'Request created successfully'}), 201

@requests_bp.route('/', methods=['GET'])
@requests_bp.route('', methods=['GET'])
def get_requests():
    request_type = request.args.get('type')
    query = Request.query
    
    if request_type:
        query = query.filter_by(request_type=request_type)
        
    requests = query.all()
    return jsonify([{
        'id': req.id,
        'title': req.title,
        'description': req.description,
        'request_type': req.request_type,
        'status': req.status,
        'location': req.location,
        'urgency': req.urgency,
        'created_at': req.created_at.isoformat()
    } for req in requests]), 200

# Donations Blueprint
donations_bp = Blueprint('donations', __name__)

@donations_bp.route('/', methods=['POST'])
@donations_bp.route('', methods=['POST'])
@jwt_required()
def create_donation():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    try:
        # Create Stripe payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(data['amount'] * 100),  # Convert to cents
            currency='usd',
            payment_method=data['payment_method_id'],
            confirm=True
        )
        
        donation = Donation(
            user_id=user_id,
            amount=data['amount'],
            purpose=data.get('purpose'),
            is_recurring=data.get('is_recurring', False),
            payment_method='stripe',
            payment_status='completed'
        )
        
        db.session.add(donation)
        db.session.commit()
        
        return jsonify({
            'message': 'Donation processed successfully',
            'payment_intent': payment_intent
        }), 201
        
    except stripe.error.CardError as e:
        return jsonify({'error': str(e)}), 400

# Events Blueprint
events_bp = Blueprint('events', __name__)

@events_bp.route('/', methods=['POST'])
@events_bp.route('', methods=['POST'])
@jwt_required()
def create_event():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    event = Event(
        organizer_id=user_id,
        title=data['title'],
        description=data['description'],
        event_type=data['event_type'],
        location=data.get('location'),
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time']),
        max_participants=data.get('max_participants')
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({'message': 'Event created successfully'}), 201

@events_bp.route('/', methods=['GET'])
@events_bp.route('', methods=['GET'])
def get_events():
    event_type = request.args.get('type')
    query = Event.query
    
    if event_type:
        query = query.filter_by(event_type=event_type)
        
    events = query.all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'event_type': event.event_type,
        'location': event.location,
        'start_time': event.start_time.isoformat(),
        'end_time': event.end_time.isoformat(),
        'max_participants': event.max_participants,
        'current_participants': event.current_participants,
        'status': event.status
    } for event in events]), 200 