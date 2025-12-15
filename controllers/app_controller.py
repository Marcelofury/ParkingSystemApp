"""
Main Application Controller for Smart Parking Management System
"""

import tkinter as tk
from tkinter import messagebox

from models import DB
from utils.config import *
from utils.helpers import toast
from views import (
    LoginPage, RegisterPage, UserDashboardPage, DashboardPage,
    SlotMgmtPage, VehiclesPage, PaymentsPage, ProfilePage,
    SettingsPage, ReportsPage, AdminManagePage
)


class App(tk.Tk):
    """Main application controller managing pages and user session"""
    
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.configure(bg=BG)
        self.db = DB()
        self.current_user = None  # username
        self.current_user_role = None  # user role (admin/user)
        self.create_widgets()

    def create_widgets(self):
        """Create menu bar and page container"""
        # top menu (simple)
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        account_menu = tk.Menu(menubar, tearoff=0)
        account_menu.add_command(label="Profile", command=self.show_profile)
        account_menu.add_command(label="Switch Account", command=self.switch_account)
        account_menu.add_separator()
        account_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Account", menu=account_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        # main container
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)

        # create frames/pages dict
        self.pages = {}
        for Page in (LoginPage, RegisterPage, DashboardPage, UserDashboardPage, AdminManagePage, SlotMgmtPage, 
                     VehiclesPage, PaymentsPage, ProfilePage, SettingsPage, ReportsPage):
            page = Page(self.container, self)
            page.grid(row=0, column=0, sticky="nsew")
            self.pages[Page.__name__] = page

        # start with login
        self.show_page("LoginPage")

    def show_page(self, name):
        """Switch to specified page and call its refresh method if available"""
        page = self.pages[name]
        page.tkraise()
        if hasattr(page, "refresh"):
            page.refresh()

    def show_about(self):
        """Show beautifully designed about dialog"""
        about_window = tk.Toplevel(self)
        about_window.title("About Smart Parking System")
        about_window.geometry("500x600")
        about_window.configure(bg="#ffffff")
        about_window.resizable(False, False)
        
        # Center the window
        about_window.transient(self)
        about_window.grab_set()
        
        # Header with gradient effect using frame
        header = tk.Frame(about_window, bg=ACCENT, height=120)
        header.pack(fill="x")
        
        # App icon/title
        tk.Label(header, text="🅿️", font=("Segoe UI", 48), bg=ACCENT, fg="white").pack(pady=10)
        tk.Label(header, text="Smart Parking System", font=("Segoe UI", 18, "bold"), 
                bg=ACCENT, fg="white").pack()
        
        # Canvas and scrollbar container
        canvas_container = tk.Frame(about_window, bg="white")
        canvas_container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(canvas_container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=480)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Content area
        content = tk.Frame(scrollable_frame, bg="white", padx=30, pady=20)
        content.pack(fill="both", expand=True)
        
        # Version info
        tk.Label(content, text="Version 2.0", font=("Segoe UI", 11), 
                bg="white", fg="#666").pack(pady=(0, 5))
        
        # Divider
        tk.Frame(content, bg="#e5e7eb", height=2).pack(fill="x", pady=15)
        
        # Description
        desc_text = ("A comprehensive desktop application for managing\n"
                    "parking facilities with automated billing, PDF receipts,\n"
                    "email notifications, and real-time analytics.")
        tk.Label(content, text=desc_text, font=("Segoe UI", 10), 
                bg="white", fg="#374151", justify="center").pack(pady=10)
        
        # Features section
        features_frame = tk.Frame(content, bg="white")
        features_frame.pack(pady=15, fill="x")
        
        tk.Label(features_frame, text="Key Features", font=("Segoe UI", 12, "bold"),
                bg="white", fg=ACCENT).pack(anchor="w", pady=(0, 10))
        
        features = [
            "✓ Role-based authentication (Admin/User)",
            "✓ Real-time slot management",
            "✓ Automatic payment calculation",
            "✓ PDF receipt generation",
            "✓ Email notifications",
            "✓ Analytics dashboard with charts",
            "✓ Excel/PDF report exports",
            "✓ Multi-payment method support"
        ]
        
        for feature in features:
            tk.Label(features_frame, text=feature, font=("Segoe UI", 9),
                    bg="white", fg="#4b5563", anchor="w").pack(anchor="w", pady=2)
        
        # Technical info
        tk.Frame(content, bg="#e5e7eb", height=2).pack(fill="x", pady=15)
        
        tech_frame = tk.Frame(content, bg="white")
        tech_frame.pack(fill="x")
        
        tech_info = [
            ("Technology:", "Python 3.12 + Tkinter"),
            ("Architecture:", "MVC Pattern"),
            ("Database:", "SQLite3 (5 tables)"),
            ("Course:", "OOP + Tkinter"),
        ]
        
        for label, value in tech_info:
            row = tk.Frame(tech_frame, bg="white")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, font=("Segoe UI", 9, "bold"),
                    bg="white", fg="#374151", width=12, anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Segoe UI", 9),
                    bg="white", fg="#6b7280", anchor="w").pack(side="left")
        
        # Footer
        tk.Frame(content, bg="#e5e7eb", height=2).pack(fill="x", pady=15)
        
        tk.Label(content, text="© 2025 Smart Parking System", 
                font=("Segoe UI", 8), bg="white", fg="#9ca3af").pack()
        tk.Label(content, text="All rights reserved", 
                font=("Segoe UI", 8), bg="white", fg="#9ca3af").pack()
        
        # Close button
        btn_frame = tk.Frame(about_window, bg="white", pady=15)
        btn_frame.pack(fill="x")
        
        tk.Button(btn_frame, text="Close", command=about_window.destroy,
                 bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=40, pady=8, relief="flat", cursor="hand2").pack()

    def show_profile(self):
        """Navigate to profile page"""
        if not self.current_user:
            toast(self, "Login first!", bg=ERROR)
            return
        self.show_page("ProfilePage")
    
    def switch_account(self):
        """Log out current user and return to login page"""
        if not self.current_user:
            toast(self, "No user logged in", bg=ERROR)
            return
        
        if messagebox.askyesno("Switch Account", f"Log out from {self.current_user} and switch account?"):
            self.current_user = None
            self.current_user_role = None
            self.show_page("LoginPage")
            toast(self, "Logged out successfully", bg=SUCCESS)
