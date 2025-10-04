from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import string

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
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False)  # 'government' or 'public'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.String(20), unique=True, nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, in_review, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def generate_complaint_id(self):
        prefix = 'OE'
        random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return f"{prefix}{random_part}"

class Authority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    jurisdiction = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_register.html')
def login_register():
    return render_template('login_register.html')

@app.route('/areas.html')
def areas():
    areas = Area.query.filter_by(is_active=True).all()
    return render_template('areas.html', areas=areas)

@app.route('/file_complaint.html')
def file_complaint():
    return render_template('file_complaint.html')

@app.route('/pending_problems.html')
def pending_problems():
    complaints = Complaint.query.filter_by(status='pending').all()
    return render_template('pending_problems.html', complaints=complaints)

@app.route('/active_authorities.html')
def active_authorities():
    authorities = Authority.query.filter_by(is_active=True).all()
    return render_template('active_authorities.html', authorities=authorities)

# API Routes
@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type', 'public')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        user = User(username=username, email=email, user_type=user_type)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            return jsonify({
                'success': True, 
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'user_type': user.user_type
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/complaints', methods=['POST'])
def api_submit_complaint():
    try:
        data = request.get_json()
        domain = data.get('domain')
        description = data.get('description')
        
        complaint = Complaint(domain=domain, description=description)
        complaint.complaint_id = complaint.generate_complaint_id()
        
        db.session.add(complaint)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Complaint submitted successfully',
            'complaint_id': complaint.complaint_id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/complaints', methods=['GET'])
def api_get_complaints():
    try:
        complaints = Complaint.query.all()
        complaints_data = []
        
        for complaint in complaints:
            complaints_data.append({
                'id': complaint.id,
                'complaint_id': complaint.complaint_id,
                'domain': complaint.domain,
                'description': complaint.description,
                'status': complaint.status,
                'created_at': complaint.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({'success': True, 'complaints': complaints_data})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/authorities', methods=['GET'])
def api_get_authorities():
    try:
        authorities = Authority.query.filter_by(is_active=True).all()
        authorities_data = []
        
        for authority in authorities:
            authorities_data.append({
                'id': authority.id,
                'name': authority.name,
                'department': authority.department,
                'contact_email': authority.contact_email,
                'contact_phone': authority.contact_phone,
                'jurisdiction': authority.jurisdiction
            })
        
        return jsonify({'success': True, 'authorities': authorities_data})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    try:
        total_complaints = Complaint.query.count()
        pending_complaints = Complaint.query.filter_by(status='pending').count()
        resolved_complaints = Complaint.query.filter_by(status='resolved').count()
        total_authorities = Authority.query.filter_by(is_active=True).count()
        total_areas = Area.query.filter_by(is_active=True).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_complaints': total_complaints,
                'pending_complaints': pending_complaints,
                'resolved_complaints': resolved_complaints,
                'total_authorities': total_authorities,
                'total_areas': total_areas
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()
        
        # Add sample data
        if Area.query.count() == 0:
            areas = [
                Area(name='VV Puram', description='Historical market area with food street'),
                Area(name='Chamarajapet', description='Commercial and residential locality'),
                Area(name='KR Market', description='Major wholesale vegetable and flower market')
            ]
            for area in areas:
                db.session.add(area)
            db.session.commit()
        
        if Authority.query.count() == 0:
            authorities = [
                Authority(
                    name='BBMP Commissioner',
                    department='Bruhat Bengaluru Mahanagara Palike',
                    contact_email='commissioner@bbmp.gov.in',
                    contact_phone='080-22221188',
                    jurisdiction='Entire Bengaluru City'
                ),
                Authority(
                    name='Traffic Police Commissioner',
                    department='Bengaluru Traffic Police',
                    contact_email='tp@ksp.gov.in',
                    contact_phone='080-22942222',
                    jurisdiction='Bengaluru Traffic Management'
                )
            ]
            for authority in authorities:
                db.session.add(authority)
            db.session.commit()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='127.0.0.1', port=3000)
