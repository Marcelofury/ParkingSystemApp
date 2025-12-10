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
        """Show about dialog"""
        messagebox.showinfo("About", 
                          "Smart Parking System\n"
                          "Upgraded for UTAMU project.\n"
                          "Author: Student\n"
                          "Features: SQLite, hashed passwords, slots, payments, receipts.")

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
