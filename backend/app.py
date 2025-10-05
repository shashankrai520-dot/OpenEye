from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

# Configuration
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///openeye.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False, default='public')
    office = db.Column(db.String(120))  
    description = db.Column(db.String(255))  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add your fields here

class Authority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add your fields here

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add your fields here

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_register.html')
def login_register():
    return render_template('login_register.html')

@app.route('/areas.html')
def areas():
    return render_template('areas.html')

@app.route('/file_complaint.html')
def file_complaint():
    return render_template('file_complaint.html')

@app.route('/pending_problems.html')
def pending_problems():
    return render_template('pending_problems.html')

@app.route('/active_authorities.html')
def active_authorities():
    return render_template('active_authorities.html')

@app.route('/problems_solved.html')
def problems_solved():
    return render_template('problems_solved.html')

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No input data provided'}), 400

    user_type = data.get('user_type', 'public')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    office = data.get('office')
    description = data.get('description')

    # Validation
    if user_type == 'government':
        if not email or not username or not password or not office or not description:
            return jsonify({'success': False, 'message': 'Missing required fields for government user'}), 400
        # Check for existing email or username
        if User.query.filter((User.email == email) | (User.username == username)).first():
            return jsonify({'success': False, 'message': 'User already exists'}), 400
    else:  # public
        if not username or not password:
            return jsonify({'success': False, 'message': 'Missing required fields for public user'}), 400
        # Check for existing username
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400

    user = User(
        email=email, 
        username=username, 
        user_type=user_type,
        office=office,
        description=description
        )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No input data provided'}), 400

    user_type = data.get('user_type', 'public')
    identifier = data.get('identifier')  # username or email
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'success': False, 'message': 'Missing credentials'}), 400

    # For government, login with email; for public, login with username
    if user_type == 'government':
        user = User.query.filter_by(email=identifier, user_type='government').first()
    else:
        user = User.query.filter_by(username=identifier, user_type='public').first()

    if user and user.check_password(password):
        return jsonify({'success': True, 'message': 'Login successful', 'user_type': user.user_type, 'username': user.username}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

# API endpoint for statistics
@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        # For now, return mock data since the database models are not fully implemented
        # In a real application, you would query the database for actual counts
        stats = {
            'total_areas': 12,
            'resolved_complaints': 45,
            'pending_complaints': 8,
            'total_authorities': 15
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error fetching statistics',
            'error': str(e)
        }), 500

# API endpoint for problems solved
@app.route('/api/problems-solved', methods=['GET'])
def get_problems_solved():
    try:
        # Mock data for solved problems - in real app, query database
        solved_problems = [
            {
                'id': 'PWD-2023-45',
                'area': 'Central Market Roads',
                'authority': 'Public Works Department (PWD)',
                'description': 'Large pothole reported on Main Street.',
                'status': 'FIXED',
                'resolved_date': '2023-10-15'
            },
            {
                'id': 'MC-2024-102',
                'area': 'Sector 7 Residential',
                'authority': 'Municipal Corporation',
                'description': 'Illegal dumping site cleared; surveillance installed.',
                'status': 'CLEARED',
                'resolved_date': '2024-01-20'
            },
            {
                'id': 'WB-2023-78',
                'area': 'Sector 3 Water Supply',
                'authority': 'Water Board',
                'description': 'Main waterline leak reported on Oct 1st was repaired.',
                'status': 'REPAIRED',
                'resolved_date': '2023-10-05'
            }
        ]
        
        return jsonify({
            'success': True,
            'problems': solved_problems
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error fetching solved problems',
            'error': str(e)
        }), 500

# Add other API endpoints as needed

if __name__ == '__main__':
    app.run(debug=True)