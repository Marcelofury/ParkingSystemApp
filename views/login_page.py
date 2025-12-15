"""
LoginPage - View for Smart Parking Management System
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


class LoginPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()

    def build(self):
        card = tk.Frame(self, bg=CARD, padx=20, pady=20) 
        card.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(card, text="Login", font=("Segoe UI", 20, "bold"), bg=CARD, fg=ACCENT).pack(pady=(0,10))
        tk.Label(card, text="Username", bg="white").pack(anchor="w")
        self.username = tk.Entry(card, width=30, font=("Segoe UI", 10))
        self.username.pack(pady=5)
        tk.Label(card, text="Password", bg="white").pack(anchor="w")
        self.password = tk.Entry(card, show="*", width=30, font=("Segoe UI", 10))
        self.password.pack(pady=5)

        tk.Button(card, text="Login", width=25, bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"), command=self.do_login).pack(pady=8)
        tk.Button(card, text="Create account", width=25, bg="#10b981", fg="white", font=("Segoe UI", 10), command=lambda: self.app.show_page("RegisterPage")).pack()

        # presentation tip
        tk.Label(card, text="(default admin/admin123)", bg="white", fg="gray", font=("Segoe UI", 9)).pack(pady=(10,0))
    
    def resize_background(self, event):
        """Resize background image to match window size"""
        try:
            # Get current window size
            width = self.winfo_width()
            height = self.winfo_height()
            
            # Ignore invalid sizes during initialization
            if width <= 1 or height <= 1:
                # Try to get parent window size if self dimensions not ready
                width = self.master.winfo_width()
                height = self.master.winfo_height()
                
            if width <= 1 or height <= 1:
                return
            
            # Calculate aspect ratios
            img_width, img_height = self.bg_image_original.size
            img_aspect = img_width / img_height
            window_aspect = width / height
            
            # Scale to cover the entire window (crop if needed)
            if img_aspect > window_aspect:
                # Image is wider - fit to height
                new_height = height
                new_width = int(height * img_aspect)
            else:
                # Image is taller - fit to width
                new_width = width
                new_height = int(width / img_aspect)
            
            # Resize image
            resized_image = self.bg_image_original.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            
            # Center the image on canvas
            x_offset = (width - new_width) // 2
            y_offset = (height - new_height) // 2
            
            # Update canvas size and background
            self.bg_canvas.config(width=width, height=height)
            self.bg_canvas.delete("bg_image")
            self.bg_canvas.create_image(x_offset, y_offset, image=self.bg_photo, anchor="nw", tags="bg_image")
            self.bg_canvas.tag_lower("bg_image")  # Keep image behind other widgets
            
        except Exception as e:
            pass  # Silently ignore resize errors

    def do_login(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        if not u or not p:
            toast(self.app, "Enter username & password", bg=ERROR)
            return
        if self.app.db.validate_user(u, p):
            self.app.current_user = u
            # Get user role
            user_data = self.app.db.get_user(u)
            if user_data:
                self.app.current_user_role = user_data[2]  # role is 3rd column
            toast(self.app, f"Welcome {u}", bg=SUCCESS)
            # Redirect based on role
            if self.app.current_user_role == "admin":
                self.app.show_page("DashboardPage")  # Admin dashboard
            else:
                self.app.show_page("UserDashboardPage")  # User dashboard
        else:
            toast(self.app, "Invalid credentials", bg=ERROR)
