"""
VehiclesPage - View for Smart Parking Management System
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


class VehiclesPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()

    def build(self):
        top = tk.Frame(self, bg=BG); top.pack(fill="x", pady=10, padx=20)
        tk.Label(top, text="Vehicles / History", font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG).pack(side="left")
        tk.Button(top, text="Back", command=lambda: self.app.show_page("DashboardPage")).pack(side="right")
        
        # Search frame
        search_frame = tk.Frame(self, bg=BG)
        search_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(search_frame, text="Search:", bg=BG).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.search, bg=ACCENT, fg="white").pack(side="left", padx=5)
        tk.Button(search_frame, text="Clear", command=self.clear_search, bg="#6b7280", fg="white").pack(side="left", padx=5)
        
        # tree
        cols = ("id","number","type","user","slot_id","entry_time","exit_time","payment_method")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        ctrl = tk.Frame(self, bg=BG); ctrl.pack(fill="x", padx=20)
        tk.Button(ctrl, text="Exit Vehicle (record exit)", command=self.exit_vehicle).pack(side="left", padx=5)
        tk.Button(ctrl, text="Refresh", command=self.refresh).pack(side="right", padx=5)

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in self.app.db.list_parked():
            self.tree.insert("", "end", values=row)
    
    def search(self):
        search_term = self.search_entry.get().strip()
        for r in self.tree.get_children():
            self.tree.delete(r)
        results = self.app.db.search_vehicles(search_term)
        for row in results:
            self.tree.insert("", "end", values=row)
        toast(self.app, f"Found {len(results)} results", bg=SUCCESS)
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.refresh()

    def exit_vehicle(self):
        sel = self.tree.selection()
        if not sel: toast(self.app, "Select vehicle record", bg=ERROR); return
        row = self.tree.item(sel[0])["values"]
        number = row[1]
        exit_time = now_str()
        count = self.app.db.exit_vehicle(number, exit_time)
        if count == 0:
            toast(self.app, "No active record to exit", bg=ERROR)
        else:
            toast(self.app, f"{number} exited at {exit_time}", bg=SUCCESS)
        self.refresh()
