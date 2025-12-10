"""
Smart Parking Management System
Main Entry Point - Refactored Version

This is a comprehensive parking management system with:
- User authentication with role-based access (admin/user)
- Parking slot management
- Vehicle parking and exit tracking
- Payment processing and PDF receipt generation
- Email notifications
- Analytics and reporting
- System settings configuration

Author: Student
Course: UTAMU CSC 1201/CS 200 OOP
Date: December 2025
"""

from controllers import App
from models import DB
from utils.config import HOURLY_RATE_CAR, HOURLY_RATE_MOTOR
from utils.email_sender import EMAIL_SETTINGS


def main():
    """Initialize and run the application"""
    global HOURLY_RATE_CAR, HOURLY_RATE_MOTOR, EMAIL_SETTINGS
    
    # Create application instance
    app = App()
    
    # Load settings from database
    settings = app.db.get_all_settings()
    if settings:
        # Update rate globals
        from utils import config
        config.HOURLY_RATE_CAR = float(settings.get('car_rate', HOURLY_RATE_CAR))
        config.HOURLY_RATE_MOTOR = float(settings.get('motor_rate', HOURLY_RATE_MOTOR))
        
        # Update email settings
        EMAIL_SETTINGS['smtp_server'] = settings.get('smtp_server', EMAIL_SETTINGS['smtp_server'])
        EMAIL_SETTINGS['smtp_port'] = int(settings.get('smtp_port', EMAIL_SETTINGS['smtp_port']))
        EMAIL_SETTINGS['sender_email'] = settings.get('sender_email', '')
        EMAIL_SETTINGS['sender_password'] = settings.get('sender_password', '')
        EMAIL_SETTINGS['enabled'] = settings.get('email_enabled', 'False') == 'True'
    
    # Create default slots if none exist
    if len(app.db.list_slots()) == 0:
        try:
            app.db.create_slot("A1", "Car", HOURLY_RATE_CAR)
            app.db.create_slot("A2", "Car", HOURLY_RATE_CAR)
            app.db.create_slot("B1", "Motorcycle", HOURLY_RATE_MOTOR)
            app.db.create_slot("General1", "Both", HOURLY_RATE_CAR)
        except Exception as e:
            print(f"Note: Could not create default slots: {e}")
    
    # Start the application
    app.mainloop()


if __name__ == "__main__":
    main()
