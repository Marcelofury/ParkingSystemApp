"""
AdminManagePage - View for Smart Parking Management System
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


class AdminManagePage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()
    
    def refresh(self):
        # Check admin access on refresh
        if self.app.current_user_role != "admin":
            toast(self.app, "Admin access required", bg=ERROR)
            self.app.show_page("DashboardPage")
            return
        # Continue with normal refresh
        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in self.app.db.list_users():
            self.tree.insert("", "end", values=row)

    def build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", pady=10, padx=20)
        tk.Label(top, text="Admin - User Management", font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG).pack(side="left")
        tk.Button(top, text="Back", command=lambda: self.app.show_page("DashboardPage")).pack(side="right")
        # Tree
        cols = ("username","full_name","role","email")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=200, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        ctrl = tk.Frame(self, bg=BG); ctrl.pack(fill="x", padx=20)
        tk.Button(ctrl, text="Add User", command=self.add_user, bg=ACCENT, fg="white").pack(side="left", padx=5)
        tk.Button(ctrl, text="Edit User", command=self.edit_user, bg="#10b981", fg="white").pack(side="left", padx=5)
        tk.Button(ctrl, text="Delete User", command=self.delete_user, bg=ERROR, fg="white").pack(side="left", padx=5)
        tk.Button(ctrl, text="Reset Password", command=self.reset_password).pack(side="left", padx=5)
        tk.Button(ctrl, text="Refresh", command=self.refresh).pack(side="right", padx=5)

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in self.app.db.list_users():
            self.tree.insert("", "end", values=row)

    def add_user(self):
        uname = simpledialog.askstring("Username", "Enter username:")
        if not uname: return
        full = simpledialog.askstring("Full name", "Full name:")
        email = simpledialog.askstring("Email", "Email address (optional):")
        pw = simpledialog.askstring("Password", "Set password:")
        role = simpledialog.askstring("Role", "Role (admin/user):", initialvalue="user")
        if role not in ("admin","user"):
            toast(self.app, "Invalid role", bg=ERROR); return
        try:
            self.app.db.create_user(uname, pw, full, role=role, email=email or "")
            toast(self.app, "User added", bg=SUCCESS)
            self.refresh()
        except sqlite3.IntegrityError:
            toast(self.app, "Username exists", bg=ERROR)
    
    def edit_user(self):
        sel = self.tree.selection()
        if not sel: 
            toast(self.app, "Select user", bg=ERROR)
            return
        row = self.tree.item(sel[0])["values"]
        uname = row[0]
        
        # Get new details
        new_full = simpledialog.askstring("Full name", "Full name:", initialvalue=row[1])
        new_email = simpledialog.askstring("Email", "Email:", initialvalue=row[3] if len(row) > 3 else "")
        new_role = simpledialog.askstring("Role", "Role (admin/user):", initialvalue=row[2])
        
        if new_role not in ("admin","user"):
            toast(self.app, "Invalid role", bg=ERROR)
            return
        
        # Update user
        self.app.db.update_user(uname, full_name=new_full, email=new_email, role=new_role)
        toast(self.app, "User updated", bg=SUCCESS)
        self.refresh()

    def delete_user(self):
        sel = self.tree.selection()
        if not sel: toast(self.app, "Select user", bg=ERROR); return
        uname = self.tree.item(sel[0])["values"][0]
        if uname == self.app.current_user:
            toast(self.app, "Cannot delete logged in user", bg=ERROR); return
        if messagebox.askyesno("Confirm", f"Delete user {uname}?"):
            self.app.db.delete_user(uname)
            toast(self.app, "Deleted", bg=SUCCESS)
            self.refresh()

    def reset_password(self):
        sel = self.tree.selection()
        if not sel: toast(self.app, "Select user", bg=ERROR); return
        uname = self.tree.item(sel[0])["values"][0]
        self.app.db.update_password(uname, "user123")
        toast(self.app, f"Password reset to 'user123' for {uname}", bg=SUCCESS)
