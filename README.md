# Smart Parking Management System - Complete Edition

A comprehensive desktop application for managing parking facilities with advanced features including PDF receipts, email notifications, analytics, and reporting.

Status: Complete
Python Version: 3.12
License: Educational

---

## Features

### For Regular Users
- Park vehicles with automatic slot allocation
- Exit vehicles with automatic fee calculation
- Search parking records by vehicle, user, or date
- Receive PDF receipts via email
- View comprehensive payment history
- Multiple payment methods (Cash, Card, Digital)
- Switch account functionality

### For Administrators
- Manage users (add/edit/delete accounts, reset passwords)
- Manage parking slots with configurable rates per slot
- Configure system settings (parking rates, email server)
- Generate PDF and Excel reports
- View real-time statistics (revenue, occupancy, usage patterns)
- Access to all user features
- Separate admin dashboard with advanced analytics

### Key Technical Features
- Role-based authentication (user/admin)
- Multiple payment methods tracking
- Automated receipt generation and email delivery
- Real-time dashboard with live statistics and charts
- Comprehensive reporting and analytics
- SQLite database for reliable data storage
- Built with Python/Tkinter (desktop GUI)
- Automatic database migration for updates
- Payment method stored during parking (asked once)
- Minimum charge of 1000 UGX for 1 hour or less parking

---

## Requirements

### System Requirements
- OS: Linux, Windows, or macOS
- Python: 3.8 or higher (tested on 3.12)
- RAM: 512MB minimum
- Disk Space: 100MB minimum

### Python Dependencies
```
reportlab==4.2.5    # PDF generation
openpyxl==3.1.5     # Excel export
matplotlib==3.9.2   # Charts and graphs
pillow==11.0.0      # Image processing
```

---

## Installation

### 1. Clone or Download the Project
```bash
cd "/home/top-g/Final OOP"
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python finaloop.py
```

---

## Quick Start Guide

### First Login
Default Admin Credentials:
- Username: admin
- Password: admin123

IMPORTANT: Change the admin password after first login!

### Initial Setup (5 Minutes)

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

3. Create Parking Slots
   - Click "Slots" button
   - Add slots for your parking facility
   - Set custom rates for special zones if needed

4. You're Ready!
   - Start parking vehicles
   - Generate receipts
   - View statistics

---

## Documentation

### Complete Documentation Files
- NEW_FEATURES.md - Detailed list of all features
- USAGE_GUIDE.md - Step-by-step user guide
- IMPLEMENTATION_SUMMARY.md - Technical implementation details
- EMAIL_SETUP_GUIDE.md - Email configuration guide
- PARKING_UPDATES.md - Payment method and parking flow updates
- SECURITY_FIX.md - Role-based access control details

### Quick Reference

| Task | Location | Action |
|------|----------|--------|
| Park Vehicle | Dashboard | Click "Quick Park" |
| Exit Vehicle | Vehicles Page | Select vehicle → Exit Vehicle |
| Generate Receipt | Payments Page | Generate Receipt for Vehicle |
| Search Records | Vehicles/Payments | Use search box |
| View Analytics | Dashboard or Reports | Auto-displayed |
| Export Report | Reports Page | Export to PDF/Excel |
| Manage Users | Admin Page | Add/Edit/Delete User |
| Configure Email | Settings Page | Email Configuration |
| Set Rates | Settings or Slots | Default or per-slot rates |

---

## Features Overview

### Dashboard with Real-time Statistics
- Revenue overview card
- Occupancy rate display
- Active vehicles count
- 7-day revenue trend chart
- Recent activity feed

### Advanced Search
- Search vehicles by number, user, or date
- Search payments by vehicle or date range
- Real-time filtering with clear button

### Professional PDF Receipts
- Formatted with tables and styling
- Complete parking details
- Payment method tracking
- Automatic generation and optional email delivery

### Comprehensive Reports
- PDF summary reports
- Excel data exports
- Multiple report types (Revenue, Vehicles, Payments, Slots)
- Date range filtering
- Statistical analysis

### Analytics Dashboard
- Revenue trend charts (14 days)
- Occupancy pie charts
- Summary statistics
- Visual data representation using matplotlib

---

## Email Configuration

### For Gmail
1. Enable 2-factor authentication
2. Generate an App Password: https://support.google.com/accounts/answer/185833
3. Use these settings:
   - SMTP Server: smtp.gmail.com
   - SMTP Port: 587
   - Sender Email: Your Gmail address
   - Sender Password: Your App Password (not regular password)

### For Other Email Providers
Consult your email provider's SMTP settings documentation.
See EMAIL_SETUP_GUIDE.md for detailed configuration instructions.

---

## Database

### Database File
- File: parking_system_upgraded.db
- Type: SQLite3
- Location: Project root directory

### Tables
- users - User accounts with roles and emails
- vehicles - Vehicle parking records with payment methods
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
1. Use "Quick Park" for fastest vehicle entry
2. Search by vehicle number for quick lookups
3. Generate receipts immediately upon exit
4. Review dashboard statistics regularly
5. Payment method is asked once during parking

### For Administrators
1. Backup database weekly
2. Generate monthly reports for records
3. Update rates seasonally if needed
4. Monitor occupancy trends
5. Keep user emails updated for automatic receipts
6. Test email configuration before relying on it

### For System Maintenance
1. Regular database backups
2. Clean up old receipt PDFs periodically
3. Monitor disk space usage
4. Review and update settings as needed
5. Check log files for errors

---

## Educational Use

This project demonstrates:
- Object-Oriented Programming: Classes, inheritance, encapsulation
- GUI Development: Tkinter/ttk widgets, event handling
- Database Management: SQLite, CRUD operations, schema migrations
- File Operations: PDF generation, Excel creation
- Network Programming: SMTP email integration
- Data Visualization: Matplotlib charts and graphs
- Software Architecture: Multi-page application design
- Business Logic: Real-world parking management
- Security: Password hashing, role-based access

---

## Project Statistics

- Total Lines of Code: Approximately 2000
- Number of Classes: 12 (including 10 page classes)
- Database Tables: 5
- Features Implemented: 30+
- Dependencies: 4 external libraries
- Documentation Pages: 6 comprehensive guides

---

## Known Limitations

1. Email sending blocks UI - Brief pause when sending emails
2. SQLite limitations - Best for single-user or small teams
3. No cloud sync - Local database only
4. Basic authentication - No password complexity requirements
5. No audit logging - Changes not tracked historically

### Recommended Improvements for Production
- Asynchronous email sending
- PostgreSQL/MySQL for multi-user scenarios
- Cloud backup integration
- Enhanced security features
- Comprehensive audit trail
- Mobile app companion

---

## License

This project is for educational purposes as part of a university assignment.

Institution: UTAMU
Course: Final OOP Project
Date: December 2025

---

## Support and Help

### Getting Help
1. Read the USAGE_GUIDE.md
2. Check NEW_FEATURES.md for feature details
3. Review IMPLEMENTATION_SUMMARY.md for technical info
4. Review EMAIL_SETUP_GUIDE.md for email configuration
5. Review PARKING_UPDATES.md for parking flow changes
6. Examine the code comments in finaloop.py

### Reporting Issues
Document the following:
- Python version
- Operating system
- Error message (if any)
- Steps to reproduce
- Expected vs actual behavior

---

## Project Status

Status: COMPLETE AND FULLY FUNCTIONAL

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

---

## Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python finaloop.py

# Backup database
cp parking_system_upgraded.db backup.db

# Check Python version
python --version

# View dependencies
pip list

# Create fresh virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

Last Updated: December 10, 2025
Version: 2.0 (Complete Edition)
Status: Production Ready
