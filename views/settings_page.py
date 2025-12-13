"""
SettingsPage - View for Smart Parking Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
import datetime
import math
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

from views.base_page import Page
from utils.config import *
from utils.helpers import now_str, hours_between, toast
from utils.pdf_generator import generate_pdf_receipt
from utils.email_sender import send_email_with_attachment, EMAIL_SETTINGS
from utils.excel_exporter import export_to_excel


class SettingsPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()
    
    def _check_admin(self):
        """Check if user has admin access"""
        if self.app.current_user_role != "admin":
            toast(self.app, "Admin access required", bg=ERROR)
            self.app.show_page("DashboardPage")
            return False
        return True

    def build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", pady=10, padx=20)
        tk.Label(top, text="System Settings", font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG).pack(side="left")
        tk.Button(top, text="Back", command=lambda: self.app.show_page("DashboardPage")).pack(side="right")
        
        # Settings form in a card
        card = tk.Frame(self, bg=CARD, padx=30, pady=30)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(card, text="Default Rates", bg=CARD, font=("Segoe UI", 14, "bold"), fg=ACCENT).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")
        
        tk.Label(card, text="Car Hourly Rate (UGX):", bg=CARD).grid(row=1, column=0, sticky="w", pady=5)
        self.car_rate = tk.Entry(card, width=20)
        self.car_rate.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(card, text="Motorcycle Hourly Rate (UGX):", bg=CARD).grid(row=2, column=0, sticky="w", pady=5)
        self.motor_rate = tk.Entry(card, width=20)
        self.motor_rate.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(card, text="Email Configuration", bg=CARD, font=("Segoe UI", 14, "bold"), fg=ACCENT).grid(row=3, column=0, columnspan=2, pady=(20, 5), sticky="w")
        
        # Email configuration help text
        help_text = tk.Label(card, text="Configure email to send receipts automatically.\nFor Gmail: Use App Password (not regular password)", 
                            bg=CARD, fg="#6b7280", font=("Segoe UI", 9), justify="left")
        help_text.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        tk.Label(card, text="SMTP Server:", bg=CARD).grid(row=5, column=0, sticky="w", pady=5)
        self.smtp_server = tk.Entry(card, width=25)
        self.smtp_server.grid(row=5, column=1, pady=5, padx=10)
        
        tk.Label(card, text="SMTP Port:", bg=CARD).grid(row=6, column=0, sticky="w", pady=5)
        self.smtp_port = tk.Entry(card, width=25)
        self.smtp_port.grid(row=6, column=1, pady=5, padx=10)
        
        tk.Label(card, text="Sender Email:", bg=CARD).grid(row=7, column=0, sticky="w", pady=5)
        self.sender_email = tk.Entry(card, width=25)
        self.sender_email.grid(row=7, column=1, pady=5, padx=10)
        
        tk.Label(card, text="Sender Password:", bg=CARD).grid(row=8, column=0, sticky="w", pady=5)
        self.sender_password = tk.Entry(card, show="*", width=25)
        self.sender_password.grid(row=8, column=1, pady=5, padx=10)
        
        self.email_enabled = tk.BooleanVar()
        tk.Checkbutton(card, text="Enable Email Notifications", variable=self.email_enabled, bg=CARD).grid(row=9, column=0, columnspan=2, pady=10)
        
        btn_frame = tk.Frame(card, bg=CARD)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)
        tk.Button(btn_frame, text="Save Settings", bg=ACCENT, fg="white", command=self.save_settings, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Test Email", bg="#10b981", fg="white", command=self.test_email, width=15).pack(side="left", padx=5)
    
    def refresh(self):
        # Check admin access
        if not self._check_admin():
            return
        
        # Load settings from database
        settings = self.app.db.get_all_settings()
        
        self.car_rate.delete(0, tk.END)
        self.car_rate.insert(0, settings.get('car_rate', str(HOURLY_RATE_CAR)))
        
        self.motor_rate.delete(0, tk.END)
        self.motor_rate.insert(0, settings.get('motor_rate', str(HOURLY_RATE_MOTOR)))
        
        self.smtp_server.delete(0, tk.END)
        self.smtp_server.insert(0, settings.get('smtp_server', EMAIL_SETTINGS['smtp_server']))
        
        self.smtp_port.delete(0, tk.END)
        self.smtp_port.insert(0, settings.get('smtp_port', str(EMAIL_SETTINGS['smtp_port'])))
        
        self.sender_email.delete(0, tk.END)
        self.sender_email.insert(0, settings.get('sender_email', ''))
        
        self.sender_password.delete(0, tk.END)
        self.sender_password.insert(0, settings.get('sender_password', ''))
        
        self.email_enabled.set(settings.get('email_enabled', 'False') == 'True')
    
    def save_settings(self):
        global HOURLY_RATE_CAR, HOURLY_RATE_MOTOR
        
        try:
            # Save rates
            car_rate = float(self.car_rate.get())
            motor_rate = float(self.motor_rate.get())
            
            if car_rate <= 0 or motor_rate <= 0:
                toast(self.app, "Rates must be positive numbers", bg=ERROR)
                return
            
            # Validate SMTP port
            smtp_port_str = self.smtp_port.get().strip()
            if smtp_port_str:
                try:
                    smtp_port = int(smtp_port_str)
                    if smtp_port <= 0 or smtp_port > 65535:
                        raise ValueError("Port out of range")
                except ValueError:
                    toast(self.app, "SMTP Port must be a valid number (1-65535)", bg=ERROR)
                    return
            
            self.app.db.set_setting('car_rate', str(car_rate))
            self.app.db.set_setting('motor_rate', str(motor_rate))
            
            # Update global variables
            HOURLY_RATE_CAR = car_rate
            HOURLY_RATE_MOTOR = motor_rate
            
            # Save email settings
            self.app.db.set_setting('smtp_server', self.smtp_server.get())
            self.app.db.set_setting('smtp_port', self.smtp_port.get())
            self.app.db.set_setting('sender_email', self.sender_email.get())
            self.app.db.set_setting('sender_password', self.sender_password.get())
            self.app.db.set_setting('email_enabled', str(self.email_enabled.get()))
            
            # Update global email settings
            EMAIL_SETTINGS['smtp_server'] = self.smtp_server.get()
            EMAIL_SETTINGS['smtp_port'] = int(self.smtp_port.get()) if self.smtp_port.get().strip() else 587
            EMAIL_SETTINGS['sender_email'] = self.sender_email.get()
            EMAIL_SETTINGS['sender_password'] = self.sender_password.get()
            EMAIL_SETTINGS['enabled'] = self.email_enabled.get()
            
            toast(self.app, "Settings saved successfully!", bg=SUCCESS)
        except ValueError as e:
            toast(self.app, f"Invalid values: {str(e)}", bg=ERROR)
        except Exception as e:
            toast(self.app, f"Error saving settings: {str(e)}", bg=ERROR)
    
    def test_email(self):
        test_email = simpledialog.askstring("Test Email", "Enter email address to send test:")
        if not test_email:
            return
        
        try:
            # Validate inputs
            smtp_server = self.smtp_server.get().strip()
            smtp_port_str = self.smtp_port.get().strip()
            sender_email = self.sender_email.get().strip()
            sender_password = self.sender_password.get()
            
            if not smtp_server:
                toast(self.app, "SMTP Server is required", bg=ERROR)
                return
            
            if not smtp_port_str:
                toast(self.app, "SMTP Port is required", bg=ERROR)
                return
            
            try:
                smtp_port = int(smtp_port_str)
                if smtp_port <= 0 or smtp_port > 65535:
                    raise ValueError("Port out of range")
            except ValueError:
                toast(self.app, "SMTP Port must be a valid number (1-65535)", bg=ERROR)
                return
            
            if not sender_email:
                toast(self.app, "Sender Email is required", bg=ERROR)
                return
            
            if not sender_password:
                toast(self.app, "Sender Password is required", bg=ERROR)
                return
            
            # Update email settings temporarily
            EMAIL_SETTINGS['smtp_server'] = smtp_server
            EMAIL_SETTINGS['smtp_port'] = smtp_port
            EMAIL_SETTINGS['sender_email'] = sender_email
            EMAIL_SETTINGS['sender_password'] = sender_password
            EMAIL_SETTINGS['enabled'] = True
            
            # Show loading message
            toast(self.app, "Sending test email...", bg="#f59e0b")
            
            success, msg = send_email_with_attachment(
                test_email,
                "Test Email from Smart Parking System",
                "This is a test email. If you received this, your email configuration is working correctly!",
                None
            )
            
            if success:
                messagebox.showinfo("Success", f"Test email sent successfully to {test_email}!\n\nCheck your inbox (and spam folder).")
            else:
                messagebox.showerror("Email Test Failed", 
                    f"Failed to send test email.\n\n"
                    f"Error: {msg}\n\n"
                    f"Common issues:\n"
                    f"• Gmail: Use App Password (not regular password)\n"
                    f"• Check SMTP server and port are correct\n"
                    f"• Verify email and password\n"
                    f"• Check internet connection")
        except Exception as e:
            messagebox.showerror("Error", f"Error testing email:\n\n{str(e)}")
