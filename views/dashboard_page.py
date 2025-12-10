"""
DashboardPage - View for Smart Parking Management System
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


class DashboardPage(Page):
    """Admin-only dashboard with full statistics and analytics"""
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()

    def build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=20, pady=10)
        self.welcome_lbl = tk.Label(top, text="Admin Dashboard", bg=BG, font=("Segoe UI", 16, "bold"), fg=ACCENT)
        self.welcome_lbl.pack(side="left")
        # quick actions - all admin features
        self.actions = tk.Frame(top, bg=BG)
        self.actions.pack(side="right")
        tk.Button(self.actions, text="Slots", command=lambda: self.app.show_page("SlotMgmtPage"), bg=ACCENT, fg="white").pack(side="left", padx=5)
        tk.Button(self.actions, text="Vehicles", command=lambda: self.app.show_page("VehiclesPage"), bg=ACCENT, fg="white").pack(side="left", padx=5)
        tk.Button(self.actions, text="Payments", command=lambda: self.app.show_page("PaymentsPage"), bg=ACCENT, fg="white").pack(side="left", padx=5)
        tk.Button(self.actions, text="Reports", command=lambda: self.app.show_page("ReportsPage"), bg="#10b981", fg="white").pack(side="left", padx=5)
        tk.Button(self.actions, text="Settings", command=lambda: self.app.show_page("SettingsPage"), bg="#f59e0b", fg="white").pack(side="left", padx=5)
        tk.Button(self.actions, text="Admin", command=lambda: self.app.show_page("AdminManagePage"), bg="#6b7280", fg="white").pack(side="left", padx=5)

        # Main content area with statistics
        main_content = tk.Frame(self, bg=BG)
        main_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left side: Statistics cards
        left_frame = tk.Frame(main_content, bg=BG)
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Statistics cards
        stats_frame = tk.Frame(left_frame, bg=BG)
        stats_frame.pack(fill="x", pady=(0, 10))
        
        # Revenue card
        revenue_card = tk.Frame(stats_frame, bg=CARD, padx=15, pady=15)
        revenue_card.pack(side="left", padx=5, fill="both", expand=True)
        tk.Label(revenue_card, text="Total Revenue", bg=CARD, font=("Segoe UI", 10)).pack()
        self.lbl_revenue = tk.Label(revenue_card, text="0 UGX", bg=CARD, font=("Segoe UI", 18, "bold"), fg=SUCCESS)
        self.lbl_revenue.pack()
        
        # Occupancy card
        occ_card = tk.Frame(stats_frame, bg=CARD, padx=15, pady=15)
        occ_card.pack(side="left", padx=5, fill="both", expand=True)
        tk.Label(occ_card, text="Occupancy Rate", bg=CARD, font=("Segoe UI", 10)).pack()
        self.lbl_occupancy = tk.Label(occ_card, text="0%", bg=CARD, font=("Segoe UI", 18, "bold"), fg=ACCENT)
        self.lbl_occupancy.pack()
        
        # Active vehicles card
        active_card = tk.Frame(stats_frame, bg=CARD, padx=15, pady=15)
        active_card.pack(side="left", padx=5, fill="both", expand=True)
        tk.Label(active_card, text="Active Vehicles", bg=CARD, font=("Segoe UI", 10)).pack()
        self.lbl_active = tk.Label(active_card, text="0", bg=CARD, font=("Segoe UI", 18, "bold"), fg=ERROR)
        self.lbl_active.pack()
        
        # Chart frame
        chart_frame = tk.Frame(left_frame, bg=CARD, padx=10, pady=10)
        chart_frame.pack(fill="both", expand=True)
        tk.Label(chart_frame, text="Revenue Trend (Last 7 Days)", bg=CARD, font=("Segoe UI", 12, "bold")).pack()
        
        self.chart_canvas_frame = tk.Frame(chart_frame, bg=CARD)
        self.chart_canvas_frame.pack(fill="both", expand=True)

        # quick park button
        tk.Button(left_frame, text="Quick Park (assign best slot)", bg="#10b981", fg="white", command=self.quick_park, font=("Segoe UI", 10, "bold")).pack(pady=10, fill="x")

        # Right side: Recent activity
        right_frame = tk.Frame(main_content, bg=BG, width=400)
        right_frame.pack(side="right", fill="both", padx=(10, 0))
        
        tk.Label(right_frame, text="Recent Parking Activity", bg=BG, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        
        # parked vehicles table
        cols = ("number","type","entry_time")
        self.tree = ttk.Treeview(right_frame, columns=cols, show="headings", height=20)
        self.tree.heading("number", text="Vehicle")
        self.tree.heading("type", text="Type")
        self.tree.heading("entry_time", text="Entry Time")
        self.tree.column("number", width=100, anchor="center")
        self.tree.column("type", width=80, anchor="center")
        self.tree.column("entry_time", width=130, anchor="center")
        self.tree.pack(fill="both", expand=True)

        btns = tk.Frame(right_frame, bg=BG)
        btns.pack(pady=6, fill="x")
        tk.Button(btns, text="Generate Receipt", command=self.generate_receipt_from_selection, bg=ACCENT, fg="white").pack(side="left", padx=5)
        tk.Button(btns, text="Refresh", command=self.refresh, bg="#6b7280", fg="white").pack(side="right", padx=5)

    def refresh(self):
        # Admin-only check
        if self.app.current_user_role != "admin":
            toast(self.app, "Admin access required", bg=ERROR)
            self.app.show_page("UserDashboardPage" if self.app.current_user else "LoginPage")
            return
        
        u = self.app.current_user if self.app.current_user else ""
        self.welcome_lbl.config(text=f"Admin Dashboard - Welcome, {u}")
        
        # Get statistics
        occupancy = self.app.db.get_occupancy_stats()
        revenue_stats = self.app.db.get_revenue_stats()
        
        # Update statistics cards
        self.lbl_revenue.config(text=f"{revenue_stats['total']:.2f} {CURRENCY}")
        
        if occupancy['total'] > 0:
            occ_rate = (occupancy['occupied'] / occupancy['total']) * 100
            self.lbl_occupancy.config(text=f"{occ_rate:.1f}%")
        else:
            self.lbl_occupancy.config(text="N/A")
        
        self.lbl_active.config(text=str(occupancy['occupied']))
        
        # Update revenue chart
        self.update_revenue_chart()
        
        # Update recent activity
        parked = self.app.db.list_parked()
        active_vehicles = [v for v in parked if v[6] is None]  # exit_time is None
        
        # clear tree
        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in active_vehicles[:20]:  # Show last 20
            self.tree.insert("", "end", values=(row[1], row[2], row[5]))
    
    def update_revenue_chart(self):
        """Update the revenue trend chart"""
        # Clear previous chart
        for widget in self.chart_canvas_frame.winfo_children():
            widget.destroy()
        
        # Get daily revenue data
        daily_data = self.app.db.get_daily_revenue(7)
        
        if not daily_data:
            tk.Label(self.chart_canvas_frame, text="No revenue data available", 
                    bg=CARD, fg="gray").pack(expand=True)
            return
        
        # Create matplotlib figure
        fig = Figure(figsize=(6, 3), dpi=80, facecolor=CARD)
        ax = fig.add_subplot(111)
        
        dates = [d[0] for d in daily_data]
        revenues = [d[1] for d in daily_data]
        
        ax.plot(dates, revenues, marker='o', color=ACCENT, linewidth=2, markersize=6)
        ax.fill_between(dates, revenues, alpha=0.3, color=ACCENT)
        ax.set_xlabel('Date', fontsize=9)
        ax.set_ylabel(f'Revenue ({CURRENCY})', fontsize=9)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor(CARD)
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def quick_park(self):
        # ask for vehicle number & type
        number = simpledialog.askstring("Vehicle Number", "Enter vehicle number:")
        vtype = simpledialog.askstring("Vehicle Type", "Car or Motorcycle:")
        if not number or not vtype:
            toast(self.app, "Cancelled", bg=ERROR); return
        
        # Ask for payment method upfront
        payment_method = simpledialog.askstring("Payment Method", 
                                               "Enter payment method (cash/card/digital):", 
                                               initialvalue="cash")
        if not payment_method:
            toast(self.app, "Payment method required", bg=ERROR); return
        
        # find free slot
        slot = self.app.db.get_free_slot_for_type(vtype)
        if not slot:
            toast(self.app, "No free slot available for this vehicle type", bg=ERROR); return
        slot_id = slot[0]
        entry_time = now_str()
        user = self.app.current_user or "unknown"
        self.app.db.park_vehicle(number, vtype, user, slot_id, entry_time, payment_method)
        toast(self.app, f"Parked {number} at slot {slot[1]} - Payment: {payment_method.upper()}", bg=SUCCESS)
        self.refresh()

    def generate_receipt_from_selection(self):
        sel = self.tree.selection()
        if not sel:
            toast(self.app, "Select a record", bg=ERROR); return
        v = self.tree.item(sel[0])["values"]
        number = v[0]  # Updated index for new tree structure
        # call PaymentsPage generate
        pp = self.app.pages["PaymentsPage"]
        pp.generate_receipt_for(number)
