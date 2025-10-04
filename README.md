# OpenEye - Anonymous Complaint Portal

A comprehensive web application for anonymous complaint submission and tracking, built with Python Flask backend and modern HTML/CSS frontend.

## Features

- **Anonymous Complaint Submission**: Submit complaints without revealing identity
- **User Management**: Separate registration for Government and Public users
- **Complaint Tracking**: Monitor complaint status and progress
- **Authority Management**: View active government authorities
- **Area Coverage**: Display active service areas
- **Responsive Design**: Modern, mobile-friendly interface

## Project Structure

```
OpenEye/
├── backend/
│   ├── __init__.py
│   └── app.py              # Main Flask application
├── templates/              # HTML templates
│   ├── index.html         # Home page
│   ├── login_register.html # User authentication
│   ├── areas.html         # Active areas page
│   ├── file_complaint.html # Complaint submission
│   ├── pending_problems.html # Complaint tracking
│   └── active_authorities.html # Government authorities
├── static/                # Static assets (CSS, JS, images)
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd OpenEye
   ```

2. **Install Python dependencies**
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python backend/app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://127.0.0.1:3000`

## Usage

### For Public Users
1. Visit the homepage to see available features
2. Click "File a Complaint" to submit anonymous complaints
3. Use "Complaint Tracker" to monitor submitted complaints
4. View "Active Areas" to see service coverage
5. Check "Active Authorities" for government contacts

### For Government Users
1. Register or login with Government user type
2. Access complaint management features
3. View and respond to submitted complaints
4. Upload solutions and updates

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login

### Complaints
- `GET /api/complaints` - Get all complaints
- `POST /api/complaints` - Submit new complaint

### Authorities
- `GET /api/authorities` - Get active authorities

### Statistics
- `GET /api/stats` - Get system statistics

## Database Models

### User
- User authentication and role management
- Supports Government and Public user types

### Complaint
- Anonymous complaint storage
- Unique complaint ID generation
- Status tracking (pending, in_review, resolved)

### Authority
- Government authority information
- Contact details and jurisdiction

### Area
- Service area definitions
- Coverage information

## Technology Stack

### Backend
- **Python 3.x**
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **Flask-Migrate** - Database migrations
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern features
- **JavaScript** - Interactive functionality
- **Font Awesome** - Icons
- **Responsive Design** - Mobile-friendly layouts

## Development

### Adding New Features
1. Update database models in `backend/app.py`
2. Add new routes for API endpoints
3. Create corresponding HTML templates
4. Update frontend JavaScript for new functionality

### Database Management
The application uses SQLite by default. For production, consider:
- PostgreSQL or MySQL for better performance
- Update `SQLALCHEMY_DATABASE_URI` in configuration
- Use environment variables for sensitive data

## Security Features

- Password hashing using Werkzeug
- CORS protection
- Input validation
- Anonymous complaint submission
- Secure session management

## Contributing

1. Follow the existing code structure
2. Maintain responsive design principles
3. Add proper error handling
4. Include user feedback for all actions
5. Test on multiple browsers and devices

## License

This project is developed for educational and demonstration purposes.

## Support

For questions or issues, please contact the development team.
