"""
SlotMgmtPage - View for Smart Parking Management System
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


class SlotMgmtPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()

    def build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", pady=10, padx=20)
        tk.Label(top, text="Slot Management", font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG).pack(side="left")
        tk.Button(top, text="Back", command=lambda: self.app.show_page("DashboardPage")).pack(side="right")
        # slot list
        cols = ("id","name","type_allowed","status","hourly_rate")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=140, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        # controls
        ctrl = tk.Frame(self, bg=BG)
        ctrl.pack(fill="x", padx=20)
        tk.Button(ctrl, text="Add Slot", command=self.add_slot, bg=ACCENT, fg="white").pack(side="left", padx=5)
        tk.Button(ctrl, text="Edit Slot", command=self.edit_slot, bg="#6b7280", fg="white").pack(side="left", padx=5)
        tk.Button(ctrl, text="Delete Slot", command=self.delete_slot, bg=ERROR, fg="white").pack(side="left", padx=5)
        tk.Button(ctrl, text="Refresh", command=self.refresh).pack(side="right", padx=5)

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in self.app.db.list_slots():
            self.tree.insert("", "end", values=row)

    def add_slot(self):
        name = simpledialog.askstring("Slot name", "Enter slot name (e.g. A1):")
        if not name: return
        type_allowed = simpledialog.askstring("Type allowed", "Enter type allowed (Car, Motorcycle, Both):", initialvalue="Both")
        if type_allowed not in ("Car","Motorcycle","Both"):
            toast(self.app, "Invalid type", bg=ERROR); return
        rate = simpledialog.askfloat("Hourly Rate", f"Enter hourly rate ({CURRENCY}):", initialvalue=HOURLY_RATE_CAR)
        if rate is None: rate = 0
        try:
            self.app.db.create_slot(name, type_allowed, rate)
            toast(self.app, "Slot added", bg=SUCCESS)
            self.refresh()
        except sqlite3.IntegrityError:
            toast(self.app, "Slot name exists", bg=ERROR)

    def edit_slot(self):
        sel = self.tree.selection()
        if not sel: toast(self.app, "Select slot", bg=ERROR); return
        row = self.tree.item(sel[0])["values"]
        slot_id = row[0]
        new_name = simpledialog.askstring("New name", "Enter new slot name:", initialvalue=row[1])
        new_type = simpledialog.askstring("Type allowed", "Car, Motorcycle or Both:", initialvalue=row[2])
        if new_type not in ("Car","Motorcycle","Both"):
            toast(self.app, "Invalid type", bg=ERROR); return
        new_rate = simpledialog.askfloat("Hourly Rate", f"Enter hourly rate ({CURRENCY}):", initialvalue=row[4])
        if new_rate is None: new_rate = row[4]
        self.app.db.update_slot(slot_id, name=new_name, type_allowed=new_type, hourly_rate=new_rate)
        toast(self.app, "Slot updated", bg=SUCCESS)
        self.refresh()

    def delete_slot(self):
        sel = self.tree.selection()
        if not sel: toast(self.app, "Select slot", bg=ERROR); return
        row = self.tree.item(sel[0])["values"]
        slot_id = row[0]
        if messagebox.askyesno("Confirm", f"Delete slot {row[1]}?"):
            self.app.db.delete_slot(slot_id)
            toast(self.app, "Deleted", bg=SUCCESS)
            self.refresh()
