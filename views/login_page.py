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
        tk.Label(card, text="Username", bg=CARD).pack(anchor="w")
        self.username = tk.Entry(card, width=30)
        self.username.pack(pady=5)
        tk.Label(card, text="Password", bg=CARD).pack(anchor="w")
        self.password = tk.Entry(card, show="*", width=30)
        self.password.pack(pady=5)

        tk.Button(card, text="Login", width=25, bg=ACCENT, fg="white", command=self.do_login).pack(pady=8)
        tk.Button(card, text="Create account", width=25, bg="#10b981", fg="white", command=lambda: self.app.show_page("RegisterPage")).pack()

        # presentation tip
        tk.Label(card, text="(default admin/admin123)", bg=CARD, fg="gray", font=("Segoe UI", 9)).pack(pady=(10,0))

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
