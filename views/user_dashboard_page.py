"""
UserDashboardPage - View for Smart Parking Management System
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


class UserDashboardPage(Page):
    """Simplified dashboard for regular users"""
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()

    def build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20, pady=10)
        self.welcome_lbl = tk.Label(top, text="Welcome", bg=BG, font=("Segoe UI", 16, "bold"), fg=ACCENT)
        self.welcome_lbl.pack(side="left")
        
        # User actions - limited features
        actions = tk.Frame(top, bg=BG)
        actions.pack(side="right")
        tk.Button(actions, text="Park Vehicle", command=self.quick_park, bg=SUCCESS, fg="white", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        tk.Button(actions, text="My Vehicles", command=lambda: self.app.show_page("VehiclesPage"), bg=ACCENT, fg="white").pack(side="left", padx=5)
        tk.Button(actions, text="My Payments", command=lambda: self.app.show_page("PaymentsPage"), bg=ACCENT, fg="white").pack(side="left", padx=5)

        # Main content
        main_content = tk.Frame(self, bg=BG)
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Info card
        info_card = tk.Frame(main_content, bg=CARD, padx=30, pady=30)
        info_card.pack(fill="both", expand=True)
        
        tk.Label(info_card, text="Quick Park Your Vehicle", bg=CARD, font=("Segoe UI", 18, "bold"), fg=ACCENT).pack(pady=(0, 20))
        tk.Label(info_card, text="Click the button below to park your vehicle quickly", bg=CARD, font=("Segoe UI", 11)).pack(pady=5)
        
        tk.Button(info_card, text=" Quick Park Now", command=self.quick_park, 
                 bg=SUCCESS, fg="white", font=("Segoe UI", 14, "bold"), padx=30, pady=15).pack(pady=20)
        
        # Divider
        tk.Frame(info_card, bg="#e5e7eb", height=2).pack(fill="x", pady=20)
        
        # User info section
        user_info_frame = tk.Frame(info_card, bg=CARD)
        user_info_frame.pack(fill="x")
        
        # My Active Vehicles
        left_col = tk.Frame(user_info_frame, bg=CARD)
        left_col.pack(side="left", fill="both", expand=True, padx=10)
        
        tk.Label(left_col, text="My Active Vehicles", bg=CARD, font=("Segoe UI", 12, "bold"), fg=ACCENT).pack(anchor="w", pady=(0, 10))
        
        # Tree for user's active vehicles
        cols = ("number", "type", "entry_time", "slot")
        self.tree = ttk.Treeview(left_col, columns=cols, show="headings", height=8)
        self.tree.heading("number", text="Vehicle Number")
        self.tree.heading("type", text="Type")
        self.tree.heading("entry_time", text="Entry Time")
        self.tree.heading("slot", text="Slot")
        self.tree.column("number", width=120, anchor="center")
        self.tree.column("type", width=80, anchor="center")
        self.tree.column("entry_time", width=130, anchor="center")
        self.tree.column("slot", width=60, anchor="center")
        self.tree.pack(fill="both", expand=True)
        
        # Right column - Recent payments
        right_col = tk.Frame(user_info_frame, bg=CARD)
        right_col.pack(side="right", fill="both", expand=True, padx=10)
        
        tk.Label(right_col, text="Recent Payments", bg=CARD, font=("Segoe UI", 12, "bold"), fg=ACCENT).pack(anchor="w", pady=(0, 10))
        
        # Payment summary
        self.payment_frame = tk.Frame(right_col, bg=CARD)
        self.payment_frame.pack(fill="both", expand=True)
        
        self.lbl_total_paid = tk.Label(self.payment_frame, text="Total Paid: 0 UGX", 
                                       bg=CARD, font=("Segoe UI", 11), fg=TEXT)
        self.lbl_total_paid.pack(anchor="w", pady=5)
        
        self.lbl_last_payment = tk.Label(self.payment_frame, text="Last Payment: N/A", 
                                         bg=CARD, font=("Segoe UI", 11), fg=TEXT)
        self.lbl_last_payment.pack(anchor="w", pady=5)
        
        # Action buttons at bottom
        btn_frame = tk.Frame(info_card, bg=CARD)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        tk.Button(btn_frame, text="Exit Vehicle", command=self.exit_vehicle_prompt, 
                 bg=ERROR, fg="white", width=20).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Generate Receipt", command=self.generate_receipt_prompt, 
                 bg=ACCENT, fg="white", width=20).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh, 
                 bg="#6b7280", fg="white", width=20).pack(side="right", padx=5)
    
    def refresh(self):
        if not self.app.current_user:
            self.app.show_page("LoginPage")
            return
        
        u = self.app.current_user
        self.welcome_lbl.config(text=f"Welcome, {u}")
        
        # Get user's active vehicles
        all_vehicles = self.app.db.list_parked()
        user_vehicles = [v for v in all_vehicles if v[3] == u and v[6] is None]  # user's active vehicles
        
        # Clear and populate tree
        for r in self.tree.get_children():
            self.tree.delete(r)
        
        for v in user_vehicles:
            self.tree.insert("", "end", values=(v[1], v[2], v[5][:16], v[4]))
        
        # Get user's payment summary
        all_payments = self.app.db.list_payments()
        user_payments = [p for p in all_payments if p[5] == u]  # payments generated by this user
        
        if user_payments:
            total_paid = sum(p[2] for p in user_payments)
            last_payment = user_payments[0][2] if user_payments else 0
            last_date = user_payments[0][3][:16] if user_payments else "N/A"
            
            self.lbl_total_paid.config(text=f"Total Paid: {total_paid:.2f} {CURRENCY}")
            self.lbl_last_payment.config(text=f"Last Payment: {last_payment:.2f} {CURRENCY} on {last_date}")
        else:
            self.lbl_total_paid.config(text="Total Paid: 0 UGX")
            self.lbl_last_payment.config(text="Last Payment: N/A")
    
    def quick_park(self):
        number = simpledialog.askstring("Vehicle Number", "Enter vehicle number:")
        vtype = simpledialog.askstring("Vehicle Type", "Car or Motorcycle:")
        if not number or not vtype:
            toast(self.app, "Cancelled", bg=ERROR)
            return
        
        # Ask for payment method upfront
        payment_method = simpledialog.askstring("Payment Method", 
                                               "Enter payment method (cash/card/digital):", 
                                               initialvalue="cash")
        if not payment_method:
            toast(self.app, "Payment method required", bg=ERROR)
            return
        
        # Find free slot
        slot = self.app.db.get_free_slot_for_type(vtype)
        if not slot:
            toast(self.app, "No free slot available for this vehicle type", bg=ERROR)
            return
        
        slot_id = slot[0]
        entry_time = now_str()
        user = self.app.current_user or "unknown"
        self.app.db.park_vehicle(number, vtype, user, slot_id, entry_time, payment_method)
        toast(self.app, f"Parked {number} at slot {slot[1]} - Payment: {payment_method.upper()}", bg=SUCCESS)
        self.refresh()
    
    def exit_vehicle_prompt(self):
        sel = self.tree.selection()
        if not sel:
            toast(self.app, "Select a vehicle from your active vehicles", bg=ERROR)
            return
        
        v = self.tree.item(sel[0])["values"]
        number = v[0]
        
        if messagebox.askyesno("Exit Vehicle", f"Exit vehicle {number}?"):
            exit_time = now_str()
            count = self.app.db.exit_vehicle(number, exit_time)
            if count == 0:
                toast(self.app, "No active record to exit", bg=ERROR)
            else:
                toast(self.app, f"{number} exited at {exit_time}", bg=SUCCESS)
                # Prompt to generate receipt
                if messagebox.askyesno("Generate Receipt", "Would you like to generate a receipt now?"):
                    self.generate_receipt_for(number)
            self.refresh()
    
    def generate_receipt_prompt(self):
        number = simpledialog.askstring("Receipt", "Enter vehicle number:")
        if not number:
            return
        self.generate_receipt_for(number)
    
    def generate_receipt_for(self, number):
        # Call the payment page's receipt generation method
        pp = self.app.pages["PaymentsPage"]
        pp.generate_receipt_for(number)
        self.refresh()
