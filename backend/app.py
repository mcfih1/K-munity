from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///kmunity.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Import models and routes
from models import User, Request, Donation, Event
from routes import auth_bp, requests_bp, donations_bp, events_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(requests_bp, url_prefix='/api/requests')
app.register_blueprint(donations_bp, url_prefix='/api/donations')
app.register_blueprint(events_bp, url_prefix='/api/events')

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to K-munity API'})

if __name__ == '__main__':
    app.run(debug=True) 