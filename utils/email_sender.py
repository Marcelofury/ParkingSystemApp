"""
Email sending utilities for notifications and receipts
"""

import os
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# Email settings (will be updated from database)
EMAIL_SETTINGS = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': '',
    'sender_password': '',
    'enabled': False
}


def send_email_with_attachment(recipient, subject, body, attachment_path=None):
    """Send email with optional PDF attachment"""
    if not EMAIL_SETTINGS['enabled']:
        return False, "Email is not enabled. Check 'Enable Email Notifications' in Settings."
    
    if not EMAIL_SETTINGS['sender_email']:
        return False, "Sender email not configured. Please set it in Settings."
    
    if not EMAIL_SETTINGS['sender_password']:
        return False, "Sender password not configured. Please set it in Settings."
    
    if not recipient or '@' not in recipient:
        return False, f"Invalid recipient email address: {recipient}"
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SETTINGS['sender_email']
        msg['To'] = recipient
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach file if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")
                attach.add_header('Content-Disposition', 'attachment', 
                                filename=os.path.basename(attachment_path))
                msg.attach(attach)
        
        # Connect and send
        server = smtplib.SMTP(EMAIL_SETTINGS['smtp_server'], EMAIL_SETTINGS['smtp_port'], timeout=10)
        server.starttls()
        server.login(EMAIL_SETTINGS['sender_email'], EMAIL_SETTINGS['sender_password'])
        server.send_message(msg)
        server.quit()
        
        return True, "Email sent successfully"
    except smtplib.SMTPAuthenticationError as e:
        return False, f"Authentication failed. For Gmail, use App Password (not regular password). Error: {str(e)}"
    except smtplib.SMTPConnectError as e:
        return False, f"Cannot connect to SMTP server. Check server address and port. Error: {str(e)}"
    except smtplib.SMTPServerDisconnected as e:
        return False, f"Server disconnected unexpectedly. Check your internet connection. Error: {str(e)}"
    except smtplib.SMTPException as e:
        return False, f"SMTP error occurred: {str(e)}"
    except socket.gaierror as e:
        return False, f"Cannot resolve SMTP server address. Check server name. Error: {str(e)}"
    except socket.timeout:
        return False, "Connection timeout. Check your internet connection and firewall settings."
    except Exception as e:
        return False, f"Unexpected error: {type(e).__name__}: {str(e)}"
