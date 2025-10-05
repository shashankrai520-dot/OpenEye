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
   cd backend
   python app.py
   ```

4. **Access the application**
   - **Local access:** `http://127.0.0.1:5000`
   - **Network access:** `http://192.168.0.3:5000` (for devices on same network)
   - **Public access:** Use ngrok for internet access (see Network Access section)

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
- `GET /api/problems-solved` - Get solved problems data

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

## Network Access

### Local Network Access
The application is configured to run on all network interfaces (`0.0.0.0:5000`), making it accessible to other devices on the same network.

**Access URLs:**
- **Local:** `http://127.0.0.1:5000`
- **Network:** `http://192.168.0.3:5000` (replace with your actual IP)

### Public Internet Access (ngrok)

To share the application with users on different networks:

1. **Download ngrok:** https://ngrok.com/download
2. **Create free account:** https://dashboard.ngrok.com/signup
3. **Get authtoken** from dashboard
4. **Configure ngrok:**
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```
5. **Start ngrok tunnel:**
   ```bash
   ngrok http 5000
   ```
6. **Share the public URL** (e.g., `https://abc123.ngrok.io`)

### Windows Firewall Configuration
If others can't access your app, add a firewall rule:
```bash
netsh advfirewall firewall add rule name="Python Flask" dir=in action=allow protocol=TCP localport=5000
```

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

## Quick Start Guide

### For Local Development
```bash
cd OpenEye/backend
python app.py
# Access at: http://127.0.0.1:5000
```

### For Network Sharing
```bash
# Same as above, then share: http://192.168.0.3:5000
# (Replace 192.168.0.3 with your actual IP address)
```

### For Internet Sharing
```bash
# 1. Start Flask app
cd OpenEye/backend
python app.py

# 2. In another terminal, start ngrok
ngrok http 5000

# 3. Share the ngrok URL (e.g., https://abc123.ngrok.io)
```

## Support

For questions or issues, please contact the development team.
