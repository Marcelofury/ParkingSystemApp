"""
ProfilePage - View for Smart Parking Management System
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


class ProfilePage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()

    def build(self):
        card = tk.Frame(self, bg=CARD, padx=20, pady=20)
        card.place(relx=0.5, rely=0.45, anchor="center")
        tk.Label(card, text="Profile", font=("Segoe UI", 18, "bold"), bg=CARD, fg=ACCENT).pack(pady=10)
        tk.Label(card, text="Username:", bg=CARD).pack(anchor="w")
        self.lbl_user = tk.Label(card, text="", bg=CARD, font=("Segoe UI", 12, "bold"))
        self.lbl_user.pack(anchor="w", pady=(0,6))
        tk.Label(card, text="Full name:", bg=CARD).pack(anchor="w")
        self.fullname = tk.Entry(card, width=30); self.fullname.pack(pady=6)
        tk.Label(card, text="Email:", bg=CARD).pack(anchor="w")
        self.email = tk.Entry(card, width=30); self.email.pack(pady=6)
        tk.Label(card, text="New Password (leave blank to keep current):", bg=CARD).pack(anchor="w")
        self.newpw = tk.Entry(card, show="*", width=30); self.newpw.pack(pady=6)
        
        # Buttons frame
        btn_frame = tk.Frame(card, bg=CARD)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Save Profile", bg=ACCENT, fg="white", command=self.save_profile, width=15).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Switch Account", bg="#f59e0b", fg="white", command=self.app.switch_account, width=15).pack(side="left", padx=5)
        
        tk.Button(card, text="Back", command=self.back_to_dashboard).pack(pady=5)

    def refresh(self):
        if not self.app.current_user:
            toast(self.app, "Not logged in", bg=ERROR); return
        data = self.app.db.get_user(self.app.current_user)
        if data:
            self.lbl_user.config(text=data[0])
            self.fullname.delete(0, tk.END)
            self.fullname.insert(0, data[1] if data[1] else "")
            self.email.delete(0, tk.END)
            self.email.insert(0, data[3] if len(data) > 3 and data[3] else "")
        else:
            toast(self.app, "User not found", bg=ERROR)

    def save_profile(self):
        new_name = self.fullname.get().strip()
        new_email = self.email.get().strip()
        new_pw = self.newpw.get().strip()
        # update user details
        if new_name or new_email:
            self.app.db.update_user(self.app.current_user, full_name=new_name, email=new_email)
        if new_pw:
            self.app.db.update_password(self.app.current_user, new_pw)
        toast(self.app, "Profile updated", bg=SUCCESS)
        self.back_to_dashboard()
    
    def back_to_dashboard(self):
        """Navigate back to appropriate dashboard based on user role"""
        if self.app.current_user_role == "admin":
            self.app.show_page("DashboardPage")
        else:
            self.app.show_page("UserDashboardPage")
