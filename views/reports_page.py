"""
ReportsPage - View for Smart Parking Management System
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


class ReportsPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.build()
    
    def _check_admin(self):
        """Check if user has admin access"""
        if self.app.current_user_role != "admin":
            toast(self.app, "Admin access required", bg=ERROR)
            self.app.show_page("DashboardPage")
            return False
        return True

    def build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", pady=10, padx=20)
        tk.Label(top, text="Reports & Analytics", font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG).pack(side="left")
        tk.Button(top, text="Back", command=lambda: self.app.show_page("DashboardPage")).pack(side="right")
        
        # Main content
        content = tk.Frame(self, bg=BG)
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left: Summary cards
        left = tk.Frame(content, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Summary statistics
        summary_frame = tk.Frame(left, bg=CARD, padx=20, pady=20)
        summary_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(summary_frame, text="Summary Statistics", bg=CARD, font=("Segoe UI", 14, "bold"), fg=ACCENT).pack(anchor="w")
        
        self.stats_text = tk.Text(summary_frame, height=10, width=50, bg=CARD, relief="flat", font=("Segoe UI", 10))
        self.stats_text.pack(fill="x", pady=10)
        
        # Chart area
        chart_frame = tk.Frame(left, bg=CARD, padx=10, pady=10)
        chart_frame.pack(fill="both", expand=True)
        
        tk.Label(chart_frame, text="Revenue & Occupancy Analysis", bg=CARD, font=("Segoe UI", 12, "bold")).pack()
        
        self.chart_canvas_frame = tk.Frame(chart_frame, bg=CARD)
        self.chart_canvas_frame.pack(fill="both", expand=True)
        
        # Right: Export options
        right = tk.Frame(content, bg=CARD, padx=20, pady=20, width=300)
        right.pack(side="right", fill="y")
        
        tk.Label(right, text="Export Reports", bg=CARD, font=("Segoe UI", 14, "bold"), fg=ACCENT).pack(pady=(0, 20))
        
        tk.Label(right, text="Select Report Type:", bg=CARD).pack(anchor="w", pady=5)
        self.report_type = tk.StringVar(value="revenue")
        tk.Radiobutton(right, text="Revenue Report", variable=self.report_type, value="revenue", bg=CARD).pack(anchor="w")
        tk.Radiobutton(right, text="Vehicle History", variable=self.report_type, value="vehicles", bg=CARD).pack(anchor="w")
        tk.Radiobutton(right, text="Payment Records", variable=self.report_type, value="payments", bg=CARD).pack(anchor="w")
        tk.Radiobutton(right, text="Slot Utilization", variable=self.report_type, value="slots", bg=CARD).pack(anchor="w")
        
        tk.Label(right, text="Date Range (optional):", bg=CARD).pack(anchor="w", pady=(15, 5))
        tk.Label(right, text="From:", bg=CARD, font=("Segoe UI", 9)).pack(anchor="w")
        self.date_from = tk.Entry(right, width=20)
        self.date_from.pack(anchor="w", pady=2)
        self.date_from.insert(0, "YYYY-MM-DD")
        
        tk.Label(right, text="To:", bg=CARD, font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 0))
        self.date_to = tk.Entry(right, width=20)
        self.date_to.pack(anchor="w", pady=2)
        self.date_to.insert(0, "YYYY-MM-DD")
        
        tk.Button(right, text="Export to PDF", bg=ACCENT, fg="white", command=self.export_pdf, width=20).pack(pady=(20, 5))
        tk.Button(right, text="Export to Excel", bg="#10b981", fg="white", command=self.export_excel, width=20).pack(pady=5)
        tk.Button(right, text="Refresh Data", bg="#6b7280", fg="white", command=self.refresh, width=20).pack(pady=5)
    
    def refresh(self):
        # Check admin access
        if not self._check_admin():
            return
        
        # Update statistics
        occupancy = self.app.db.get_occupancy_stats()
        revenue_stats = self.app.db.get_revenue_stats()
        payments = self.app.db.list_payments()
        vehicles = self.app.db.list_parked()
        
        stats_text = f"""
Total Slots: {occupancy['total']}
Occupied Slots: {occupancy['occupied']}
Free Slots: {occupancy['free']}
Occupancy Rate: {(occupancy['occupied']/occupancy['total']*100) if occupancy['total'] > 0 else 0:.1f}%

Total Revenue: {revenue_stats['total']:.2f} {CURRENCY}
Total Payments: {revenue_stats['count']}
Average Payment: {(revenue_stats['total']/revenue_stats['count']) if revenue_stats['count'] > 0 else 0:.2f} {CURRENCY}

Total Vehicle Records: {len(vehicles)}
Active Vehicles: {len([v for v in vehicles if v[6] is None])}
        """
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text.strip())
        
        # Update charts
        self.update_charts()
    
    def update_charts(self):
        # Clear previous chart
        for widget in self.chart_canvas_frame.winfo_children():
            widget.destroy()
        
        # Get data
        daily_revenue = self.app.db.get_daily_revenue(30)
        occupancy = self.app.db.get_occupancy_stats()
        
        if not daily_revenue:
            tk.Label(self.chart_canvas_frame, text="No data available", bg=CARD, fg="gray").pack(expand=True)
            return
        
        # Create figure with subplots
        fig = Figure(figsize=(8, 6), dpi=80, facecolor=CARD)
        
        # Revenue trend
        ax1 = fig.add_subplot(211)
        dates = [d[0] for d in daily_revenue[-14:]]  # Last 14 days
        revenues = [d[1] for d in daily_revenue[-14:]]
        ax1.plot(dates, revenues, marker='o', color=ACCENT, linewidth=2)
        ax1.fill_between(dates, revenues, alpha=0.3, color=ACCENT)
        ax1.set_title('Revenue Trend (Last 14 Days)', fontsize=10, fontweight='bold')
        ax1.set_ylabel(f'Revenue ({CURRENCY})', fontsize=9)
        ax1.tick_params(axis='x', rotation=45, labelsize=7)
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor(CARD)
        
        # Occupancy pie chart
        ax2 = fig.add_subplot(212)
        if occupancy['total'] > 0:
            sizes = [occupancy['occupied'], occupancy['free']]
            labels = ['Occupied', 'Free']
            colors = [ERROR, SUCCESS]
            ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Current Slot Occupancy', fontsize=10, fontweight='bold')
        ax2.set_facecolor(CARD)
        
        fig.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def export_pdf(self):
        report_type = self.report_type.get()
        filename = f"{report_type}_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph(f"<b>{report_type.upper()} REPORT</b>", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 0.3*inch))
            
            # Generated date
            date_para = Paragraph(f"Generated: {now_str()}", styles['Normal'])
            elements.append(date_para)
            elements.append(Spacer(1, 0.2*inch))
            
            # Get data based on report type
            if report_type == "revenue":
                data = [['Date', 'Vehicle', 'Amount', 'Payment Method']]
                for p in self.app.db.list_payments()[:50]:
                    data.append([p[3][:10], p[1], f"{p[2]:.2f}", p[7] if len(p) > 7 else 'N/A'])
            elif report_type == "vehicles":
                data = [['Number', 'Type', 'User', 'Entry', 'Exit']]
                for v in self.app.db.list_parked()[:50]:
                    data.append([v[1], v[2], v[3], v[5][:16], v[6][:16] if v[6] else 'Active'])
            elif report_type == "payments":
                data = [['Vehicle', 'Amount', 'Duration (hrs)', 'Paid At']]
                for p in self.app.db.list_payments()[:50]:
                    data.append([p[1], f"{p[2]:.2f}", f"{p[4]:.2f}", p[3][:16]])
            else:  # slots
                data = [['Name', 'Type', 'Status', 'Rate']]
                for s in self.app.db.list_slots():
                    data.append([s[1], s[2], s[3], f"{s[4]:.2f}"])
            
            # Create table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            toast(self.app, f"PDF report saved: {filename}", bg=SUCCESS)
        except Exception as e:
            toast(self.app, f"Error generating PDF: {str(e)}", bg=ERROR)
    
    def export_excel(self):
        report_type = self.report_type.get()
        filename = f"{report_type}_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        try:
            # Get data based on report type
            if report_type == "revenue":
                headers = ['ID', 'Vehicle', 'Amount', 'Paid At', 'Duration (hrs)', 'Generated By', 'Payment Method']
                data = [[p[0], p[1], p[2], p[3], p[4], p[5], p[7] if len(p) > 7 else 'N/A'] for p in self.app.db.list_payments()]
            elif report_type == "vehicles":
                headers = ['ID', 'Number', 'Type', 'User', 'Slot ID', 'Entry Time', 'Exit Time']
                data = list(self.app.db.list_parked())
            elif report_type == "payments":
                headers = ['ID', 'Vehicle', 'Amount', 'Paid At', 'Duration (hrs)', 'Generated By']
                data = [[p[0], p[1], p[2], p[3], p[4], p[5]] for p in self.app.db.list_payments()]
            else:  # slots
                headers = ['ID', 'Name', 'Type Allowed', 'Status', 'Hourly Rate']
                data = list(self.app.db.list_slots())
            
            export_to_excel(data, headers, filename)
            toast(self.app, f"Excel report saved: {filename}", bg=SUCCESS)
        except Exception as e:
            toast(self.app, f"Error generating Excel: {str(e)}", bg=ERROR)
