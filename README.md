# Smart Parking Management System

A desktop application for managing parking facilities with PDF receipts, email notifications, and analytics.

**Course**: UTAMU CSC 1201/CS 200 OOP  
**Python**: 3.12  
**Status**: Complete

## Features

**User Features:**
- Park/exit vehicles with automatic slot assignment
- PDF receipts sent via email automatically
- Payment history and search
- Multiple payment methods (Cash, Card, Mobile Money)

**Admin Features:**
- User and slot management
- System configuration (rates, email settings)
- Analytics dashboard with charts
- PDF and Excel reports
- Revenue tracking

**Technical:**
- Role-based authentication
- SQLite database (5 tables)
- MVC architecture (refactored)
- Automatic email delivery
- Minimum charge: 1000 UGX per hour

## Installation

### Quick Start
```bash
# Run the executable
cd dist/SmartParkingSystem
./SmartParkingSystem
```

### From Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## Default Login

**Admin:**
- Username: `admin`
- Password: `admin`

**User:**
- Username: `buteramarcel`
- Password: `marcel`

## Email Setup

1. Login as admin
2. Go to Settings
3. Configure:
   - SMTP Server: `smtp.gmail.com`
   - SMTP Port: `587`
   - Email: Your Gmail address
   - Password: Google App Password (16 characters)
4. Enable Email and Save
5. Test Email

## Usage

**Park Vehicle:**
1. Quick Park button
2. Enter vehicle number and type
3. Select payment method
4. System assigns slot automatically

**Generate Receipt:**
1. Go to Payments page
2. Enter vehicle number
3. System generates PDF and emails user automatically

**View Reports:**
- Admin dashboard shows revenue trends
- Export to Excel from Reports page
- Search by vehicle/user/date

1. Update Your Profile
   - Go to Account -> Profile
   - Add your email address
   - Change your password
   - Click Save Profile

2. Configure System Settings
   - Click the "Settings" button on dashboard
   - Set default parking rates
   - Configure email (optional but recommended)
   - Click Save Settings

## Project Structure

```
Final OOP/
├── main.py                    # Application entry point
├── parking_system_upgraded.db # SQLite database
├── requirements.txt           # Dependencies
├── models/                    # Database layer
├── views/                     # UI pages (11 pages)
├── controllers/               # Application logic
├── utils/                     # Helpers (PDF, email, Excel)
├── receipts/                  # Generated receipts
└── dist/SmartParkingSystem/   # Executable (135MB)
```

## Database

**Tables:** users, vehicles, slots, payments, settings  
**File:** `parking_system_upgraded.db`  
**Type:** SQLite3
- slots - Parking slot configuration with rates
- payments - Payment records with methods
- settings - System configuration

### Backup Recommendations
```bash
# Manual backup
cp parking_system_upgraded.db backup_$(date +%Y%m%d).db

# Automated daily backup (Linux/Mac)
0 2 * * * cd /path/to/project && cp parking_system_upgraded.db backup_$(date +\%Y\%m\%d).db
```

---

## Troubleshooting

### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check for errors
python finaloop.py 2>&1 | tee error.log
```

### Email Not Sending
1. Verify SMTP settings in Settings page
2. For Gmail, use App Password not regular password
3. Click "Test Email" to diagnose issues
4. Check that "Enable Email Notifications" is checked
5. Ensure recipient has email in profile

### Charts Not Displaying
1. Ensure matplotlib is installed: pip install matplotlib
2. Check that there's data (revenue/payments) to display
3. Click "Refresh Data" button
4. Try closing and reopening the page

### Database Errors
1. Check file permissions on parking_system_upgraded.db
2. Ensure database isn't locked by another process
3. Try backing up and deleting database to recreate

### Exit Vehicle Button Not Working
1. Select a vehicle from the table first
2. The vehicle must have a null exit_time (still parked)
3. Check that the vehicle exists in the database

---

## User Roles

### Regular User
- Can park and exit vehicles
- Generate receipts for their vehicles
- View their payment history
- Search records
- Update own profile
- Switch between accounts

### Administrator
- All user capabilities plus:
- Manage all user accounts
- Configure system settings
- Manage parking slots and rates
- Generate system reports
- View all statistics
- Reset user passwords
- Access separate admin dashboard

---

## Tips and Best Practices

### For Daily Operations
## Technical Details

**OOP Concepts:**
- Classes and inheritance
- Encapsulation and abstraction
- MVC architecture

**Technologies:**
- Python/Tkinter GUI
- SQLite database
- ReportLab (PDF)
- OpenPyXL (Excel)
- Matplotlib (Charts)

**Statistics:**
- 20+ modules
- 2,444 lines of code
- 5 database tables
- 30+ features

## Troubleshooting

**Email not sending:**
- Use Google App Password (not regular password)
- Enable 2FA on Gmail first
- Check spam folder

**Receipt not found:**
- Check `/receipts/` folder
- Ensure vehicle has exited
- Verify payment recorded

**Slow startup:**
- Normal on first run (font cache building)
- Subsequent runs are faster

## Documentation

- `EMAIL_SETUP_GUIDE.md` - Email configuration
- `REFACTORING_SUMMARY.md` - Code structure
- `PROJECT_STRUCTURE.md` - Architecture details
- `FINAL_ANALYSIS.md` - Complete analysis

## Course Information

**Institution:** UTAMU  
**Course:** CSC 1201/CS 200 OOP  
**Date:** December 2025  
**Status:** Complete

All features implemented, tested, and documented. Ready for use, demonstration, or submission.

### Feature Completion: 100%
- User Management
- Slot Management
- Vehicle Tracking
- Payment Processing
- PDF Receipts
- Email Integration
- Search Functionality
- Reports and Analytics
- Real-time Statistics
- System Configuration
- Role-based Access Control
- Switch Account Feature
- Payment Method Storage

---

## Achievement Summary

### Previously Missing (Now Complete)
1. Search parking records
2. PDF receipt generation
3. Email delivery
4. Multiple payment methods
5. Configurable slot rates
6. System settings interface
7. PDF and Excel reports
8. Real-time analytics
9. User edit functionality
10. Enhanced dashboard
11. Role-based access control
12. Separate user/admin dashboards
13. Switch account functionality
14. Payment method stored during parking
15. Minimum charge implementation

Result: A complete, production-ready parking management system with all advanced features!

---

## Contact

For questions about this project, please refer to the documentation files or contact through your institution's channels.

---

Built with Python, Tkinter, SQLite, and modern best practices

## License

Educational project for UTAMU CSC 1201/CS 200 OOP course.

---

**Last Updated:** December 13, 2025  
**Version:** 2.0  
**Status:** Complete
