"""
PaymentsPage - View for Smart Parking Management System
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


class PaymentsPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()

    def build(self):
        top = tk.Frame(self, bg=BG); top.pack(fill="x", pady=10, padx=20)
        tk.Label(top, text="Payments / Receipts", font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG).pack(side="left")
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
        cols = ("id","vehicle_number","amount","paid_at","duration_hours","payment_method","generated_by")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        ctrl = tk.Frame(self, bg=BG); ctrl.pack(fill="x", padx=20)
        tk.Button(ctrl, text="Generate Receipt for Vehicle", command=self.prompt_and_generate).pack(side="left", padx=5)
        tk.Button(ctrl, text="Refresh", command=self.refresh).pack(side="right", padx=5)

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in self.app.db.list_payments():
            self.tree.insert("", "end", values=row[:7])  # Exclude receipt path column
    
    def search(self):
        search_term = self.search_entry.get().strip()
        for r in self.tree.get_children():
            self.tree.delete(r)
        results = self.app.db.search_payments(search_term)
        for row in results:
            self.tree.insert("", "end", values=row[:7])
        toast(self.app, f"Found {len(results)} results", bg=SUCCESS)
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.refresh()

    def prompt_and_generate(self):
        number = simpledialog.askstring("Receipt", "Enter vehicle number:")
        if not number: return
        self.generate_receipt_for(number)

    def generate_receipt_for(self, number):
        # find latest vehicle record
        v = self.app.db.get_last_vehicle_record(number)
        if not v:
            toast(self.app, "Vehicle not found", bg=ERROR); return
        # if still parked (exit_time is null), ask to exit first
        if not v[6]:  # exit_time is None
            if not messagebox.askyesno("Not exited", f"Vehicle {number} has not exited. Record exit now?"):
                return
            exit_time = now_str()
            self.app.db.exit_vehicle(number, exit_time)
            v = self.app.db.get_last_vehicle_record(number)
        
        # Get payment method from vehicle record (stored during parking)
        payment_method = v[7] if len(v) > 7 and v[7] else "cash"
        
        # compute duration and fee
        entry_time = v[5]
        exit_time = v[6]
        duration = hours_between(entry_time, exit_time)
        duration_rounded = math.ceil(duration * 100) / 100.0  # round up to 2 decimals
        
        # Get slot-specific rate if available
        slot_data = self.app.db.get_slot_by_id(v[4]) if v[4] else None
        if slot_data and slot_data[4] > 0:  # slot has custom rate
            rate = slot_data[4]
        else:
            # Use default rates
            rate = HOURLY_RATE_CAR if v[2].lower().startswith("c") else HOURLY_RATE_MOTOR
        
        # Calculate amount with minimum charge of 1000 UGX for 1 hour or less
        if duration <= 1.0:
            amount = 1000.0  # Flat rate for 1 hour or less
        else:
            amount = max(0, duration * rate)
        amount = round(amount, 2)
        
        # Generate PDF receipt
        fname = f"receipt_{v[1]}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        try:
            generate_pdf_receipt(v, amount, duration_rounded, payment_method, 
                               self.app.current_user, fname)
            
            # record payment
            self.app.db.record_payment(v[1], amount, duration_rounded, self.app.current_user, 
                                      os.path.abspath(fname), payment_method)
            
            toast(self.app, f"✓ PDF Receipt saved: {fname}", bg=SUCCESS)
            
            # Ask if user wants to send via email
            user_data = self.app.db.get_user(v[3])  # Get vehicle owner's details
            if user_data and len(user_data) > 3 and user_data[3]:  # Has email
                if messagebox.askyesno("Send Email", 
                                      f"Send receipt to {user_data[3]}?\n\n"
                                      f"Note: Email must be configured in Settings first."):
                    success, msg = send_email_with_attachment(
                        user_data[3],
                        f"Parking Receipt - {v[1]}",
                        f"Dear {user_data[1]},\n\n"
                        f"Thank you for using our parking service.\n\n"
                        f"Receipt Details:\n"
                        f"Vehicle Number: {v[1]}\n"
                        f"Vehicle Type: {v[2]}\n"
                        f"Entry Time: {entry_time}\n"
                        f"Exit Time: {exit_time}\n"
                        f"Duration: {duration_rounded:.2f} hours\n"
                        f"Amount Paid: {amount} {CURRENCY}\n"
                        f"Payment Method: {payment_method.upper()}\n\n"
                        f"Please find your detailed receipt attached.\n\n"
                        f"Best regards,\n"
                        f"Smart Parking Management System",
                        fname
                    )
                    if success:
                        toast(self.app, "✓ Receipt emailed successfully!", bg=SUCCESS)
                    else:
                        messagebox.showwarning("Email Failed", f"Could not send email:\n{msg}")
            else:
                # No email or user declined - just show success for PDF
                if not user_data or not user_data[3]:
                    messagebox.showinfo("Receipt Generated", 
                                       f"Receipt saved as: {fname}\n\n"
                                       f"User has no email address on file.\n"
                                       f"Email sending skipped.")
            
            self.refresh()
        except Exception as e:
            toast(self.app, f"Error generating receipt: {str(e)}", bg=ERROR)
