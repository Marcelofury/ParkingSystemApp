# Email Configuration Guide

## How to Configure Email for Receipt Sending

The Smart Parking System can automatically email receipts to users. Follow these steps to set it up:

### 1. Access Settings Page
- Login as **admin** (default: admin/admin123)
- Click **Settings** button in the dashboard
- Scroll to the **Email Configuration** section

### 2. Gmail Configuration (Most Common)

#### Step 1: Enable 2-Step Verification
1. Go to your Google Account: https://myaccount.google.com
2. Navigate to **Security**
3. Enable **2-Step Verification** if not already enabled

#### Step 2: Generate App Password
1. In Google Account Security settings
2. Search for "App passwords" or go to: https://myaccount.google.com/apppasswords
3. Select app: **Mail**
4. Select device: **Other (Custom name)**
5. Type: "Smart Parking System"
6. Click **Generate**
7. Copy the 16-character password (remove spaces)

#### Step 3: Configure in Application
Fill in the settings:
```
SMTP Server: smtp.gmail.com
SMTP Port: 587
Sender Email: your-email@gmail.com
Sender Password: [paste the 16-character app password]
☑ Enable Email Notifications
```

### 3. Other Email Services

#### Outlook/Hotmail
```
SMTP Server: smtp-mail.outlook.com
SMTP Port: 587
Sender Email: your-email@outlook.com
Sender Password: [your password or app password]
```

#### Yahoo Mail
```
SMTP Server: smtp.mail.yahoo.com
SMTP Port: 587
Sender Email: your-email@yahoo.com
Sender Password: [app password required]
```

#### Office 365
```
SMTP Server: smtp.office365.com
SMTP Port: 587
Sender Email: your-email@company.com
Sender Password: [your password]
```

### 4. Testing Email Configuration

1. After entering settings, click **Save Settings**
2. Click **Test Email** button
3. Enter a test recipient email address
4. Check if you receive the test email

### 5. Common Issues & Solutions

#### "Email authentication failed"
- **Gmail**: You must use an App Password, not your regular password
- **Other services**: Verify username and password are correct
- Check if 2-factor authentication requires an app password

#### "SMTP connection failed"
- Check SMTP server address is correct
- Verify SMTP port (usually 587 for TLS)
- Check your firewall/network allows outgoing connections on port 587

#### "Email not configured"
- Make sure you clicked **Save Settings** before testing
- Verify "Enable Email Notifications" checkbox is checked
- Ensure Sender Email field is not empty

#### Emails not sending during receipt generation
- Check that users have email addresses in their profiles
- Verify email is enabled in Settings
- Test email configuration first before generating receipts

### 6. Using Email with Receipts

Once configured, the system will:
1. Generate PDF receipt when vehicle exits
2. Prompt: "Send receipt to user@email.com?"
3. If YES: Email receipt automatically with details
4. If NO: Only save PDF locally

### 7. User Email Setup

For users to receive receipts:
1. Each user must have an email in their **Profile**
2. Go to: Account → Profile
3. Enter email address
4. Click **Save Profile**

### 8. Security Best Practices

✅ **DO:**
- Use App Passwords for Gmail
- Keep passwords secure
- Test configuration regularly
- Use a dedicated email account for the system

❌ **DON'T:**
- Don't use your personal email password directly (use app passwords)
- Don't share SMTP credentials
- Don't disable email encryption (always use port 587 with TLS)

### 9. Troubleshooting Checklist

Before contacting support, verify:
- [ ] Email settings saved in Settings page
- [ ] "Enable Email Notifications" is checked
- [ ] Test email works successfully
- [ ] User has email address in their profile
- [ ] SMTP server and port are correct
- [ ] Using App Password for Gmail (not regular password)
- [ ] No firewall blocking port 587
- [ ] Internet connection is working

### 10. Example: Gmail Setup (Complete)

```
Settings Page Configuration:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SMTP Server:        smtp.gmail.com
SMTP Port:          587
Sender Email:       parking.system@gmail.com
Sender Password:    abcd efgh ijkl mnop  (16 characters)
☑ Enable Email Notifications

[Save Settings] [Test Email]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

After saving, click **Test Email** and enter any email to verify it works.

### Need Help?

If you encounter issues not covered here:
1. Check the error message displayed
2. Verify all settings are correct
3. Try the test email function
4. Check email service's SMTP documentation
