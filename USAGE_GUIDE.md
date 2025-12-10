# Smart Parking Management System - Quick Usage Guide

## 🚀 Getting Started

### Running the Application
```bash
cd "/home/top-g/Final OOP"
source .venv/bin/activate  # Activate virtual environment
python finaloop.py
```

Or use the Python path directly:
```bash
"/home/top-g/Final OOP/.venv/bin/python" finaloop.py
```

### Default Login
- **Username**: `admin`
- **Password**: `admin123`

---

## 📱 User Guide

### 1. First Login & Profile Setup
1. Login with admin credentials
2. Click **Account → Profile** from menu
3. Add your email address
4. Change your password (recommended)
5. Click **Save Profile**

### 2. Configure System Settings
1. Click **Settings** button on dashboard
2. Set default parking rates:
   - Car Hourly Rate: e.g., 1000 UGX
   - Motorcycle Hourly Rate: e.g., 500 UGX
3. Configure email (optional but recommended):
   - SMTP Server: `smtp.gmail.com`
   - SMTP Port: `587`
   - Your email address
   - App password (not regular password!)
   - Check "Enable Email Notifications"
4. Click **Test Email** to verify
5. Click **Save Settings**

### 3. Set Up Parking Slots
1. Click **Slots** button on dashboard
2. Click **Add Slot**
   - Name: e.g., "A1", "B2"
   - Type: Car/Motorcycle/Both
   - Hourly Rate: Custom rate (or 0 for default)
3. Repeat for all your parking spaces
4. Use **Edit Slot** to modify existing slots

### 4. Park a Vehicle (Quick Method)
1. From Dashboard, click **Quick Park**
2. Enter vehicle number (e.g., "ABC-123")
3. Enter vehicle type ("Car" or "Motorcycle")
4. System automatically assigns best available slot
5. Vehicle is now parked!

### 5. Park a Vehicle (Manual Method)
1. Go to **Vehicles** page
2. Use the quick park or manually record entry
3. Note the assigned slot

### 6. Exit Vehicle & Generate Receipt
**Method 1 - From Vehicles Page:**
1. Go to **Vehicles** page
2. Select the vehicle record
3. Click **Exit Vehicle**
4. Go to **Payments** page
5. Click **Generate Receipt for Vehicle**
6. Enter vehicle number
7. Choose payment method (cash/card/digital)
8. If user has email, choose whether to send receipt
9. PDF receipt is saved!

**Method 2 - From Dashboard:**
1. Select vehicle from recent activity list
2. Click **Generate Receipt**
3. System will prompt to exit if not already done
4. Choose payment method
5. Optionally send via email

### 7. Search Records
**Search Vehicles:**
1. Go to **Vehicles** page
2. Enter search term (vehicle number, user name)
3. Click **Search**
4. Click **Clear** to show all records

**Search Payments:**
1. Go to **Payments** page
2. Enter search term (vehicle number, user)
3. Click **Search**
4. Click **Clear** to reset

### 8. View Statistics & Analytics
**Dashboard Statistics:**
- View at a glance:
  - Total revenue
  - Occupancy rate
  - Active vehicles
  - Revenue trend chart (7 days)

**Detailed Analytics:**
1. Click **Reports** button
2. View comprehensive statistics
3. See revenue trend (14 days)
4. View occupancy pie chart
5. Click **Refresh Data** to update

### 9. Generate Reports
1. Go to **Reports** page
2. Select report type:
   - Revenue Report
   - Vehicle History
   - Payment Records
   - Slot Utilization
3. Optional: Enter date range (YYYY-MM-DD format)
4. Click **Export to PDF** or **Export to Excel**
5. Files are saved in project directory

### 10. User Management (Admin Only)
1. Click **Admin** button on dashboard
2. View all users
3. **Add User**: Create new accounts
4. **Edit User**: Modify name, email, role
5. **Delete User**: Remove accounts (can't delete yourself)
6. **Reset Password**: Reset to "user123"

---

## 👥 User Workflows

### Regular User Workflow
1. Login with your credentials
2. Park vehicle using Quick Park
3. View your active vehicles
4. Generate receipt when leaving
5. View payment history

### Admin Workflow
1. Login as admin
2. Check dashboard statistics
3. Manage slots and rates
4. Handle user accounts
5. Generate reports for management
6. Configure system settings

### Parking Attendant Workflow
1. Customer arrives → Quick Park
2. Customer leaves → Generate Receipt
3. Choose payment method
4. Send receipt via email (if customer has email)
5. Hand over paper receipt or confirm email sent

---

## 🎯 Common Tasks

### Set Custom Rate for VIP Parking
1. Go to **Slots** page
2. **Add Slot**: Name "VIP-1", Type "Both", Rate "2000"
3. VIP customers will be charged 2000/hour in this slot

### Send Receipt via Email
**Prerequisites:**
- User must have email in profile
- Email must be configured in Settings

**Steps:**
1. Generate receipt for vehicle
2. When prompted, click "Yes" to send email
3. Check for success message

### View Yesterday's Revenue
1. Go to **Reports** page
2. Enter date range:
   - From: Yesterday's date
   - To: Yesterday's date
3. Click **Export to Excel** or **Export to PDF**

### Find All Active Vehicles
1. Go to **Vehicles** page
2. Look for records with "exit_time" = empty
3. Or check Dashboard recent activity (shows active only)

---

## 📊 Understanding the Dashboard

### Statistics Cards
- **Total Revenue** (Green): All-time revenue
- **Occupancy Rate** (Blue): % of slots occupied
- **Active Vehicles** (Red): Currently parked vehicles

### Revenue Chart
- Shows last 7 days
- Blue line = daily revenue
- Shaded area = revenue trend

### Recent Activity
- Shows currently parked vehicles only
- Latest entries at top
- Quick access to generate receipts

---

## 🔧 Troubleshooting

### Email Not Sending
1. Check Settings → Email configuration
2. Verify SMTP server and port
3. Use App Password for Gmail (not regular password)
4. Click "Test Email" to diagnose
5. Make sure "Enable Email Notifications" is checked

### Can't Park Vehicle
- Check if free slots available (Slots page)
- Ensure vehicle type matches slot type
- Create more slots if needed

### Receipt Not Generating
- Make sure vehicle has exited (exit_time must be set)
- Check that vehicle record exists
- Verify payment method is entered

### Chart Not Showing
- Make sure there's revenue data
- Try clicking "Refresh Data"
- Check that matplotlib is installed

---

## 💡 Tips & Best Practices

1. **Regular Backups**: Copy `parking_system_upgraded.db` file regularly
2. **Email Setup**: Configure email early for best user experience
3. **Custom Rates**: Use slot-specific rates for special areas (VIP, handicap, etc.)
4. **Reports**: Generate weekly reports for management review
5. **User Emails**: Encourage users to add emails for automated receipts
6. **Search**: Use search to quickly find specific transactions
7. **Settings**: Update default rates based on your pricing strategy

---

## 🎓 Training New Users

### For Regular Users (5 minutes)
1. Show login process
2. Demonstrate Quick Park
3. Show how to generate receipt
4. Explain payment methods

### For Admins (15 minutes)
1. Cover all basic user features
2. Show user management
3. Demonstrate slot configuration
4. Walk through Settings page
5. Show reports generation
6. Explain statistics dashboard

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review NEW_FEATURES.md for detailed feature explanations
3. Check the application code for technical details

---

## ✅ Quick Reference

| Task | Location | Button/Action |
|------|----------|---------------|
| Park Vehicle | Dashboard | Quick Park |
| Exit Vehicle | Vehicles Page | Exit Vehicle |
| Generate Receipt | Payments Page | Generate Receipt |
| Search Records | Vehicles/Payments | Search box |
| View Statistics | Dashboard | Auto-displayed |
| Generate Report | Reports Page | Export to PDF/Excel |
| Add User | Admin Page | Add User |
| Edit User | Admin Page | Edit User |
| Configure Email | Settings Page | Email settings |
| Set Slot Rates | Slots Page | Add/Edit Slot |
| Change Password | Profile Page | New Password field |

---

**Need help?** All features are accessible from the main dashboard with clearly labeled buttons!
