"""
Helper utility functions for Smart Parking Management System
"""

import hashlib
import datetime
import tkinter as tk


def hash_password(password: str) -> str:
    """Return SHA-256 hash of the provided password string."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def now_str() -> str:
    """Get current datetime as string"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hours_between(start_iso: str, end_iso: str) -> float:
    """Return hours (float) between two ISO-like time strings."""
    fmt = "%Y-%m-%d %H:%M:%S"
    a = datetime.datetime.strptime(start_iso, fmt)
    b = datetime.datetime.strptime(end_iso, fmt)
    delta = b - a
    return delta.total_seconds() / 3600.0


def toast(root, text, bg="#1e88e5", duration=1800):
    """Tiny non-blocking notification using Toplevel."""
    t = tk.Toplevel(root)
    t.overrideredirect(True)
    t.config(bg=bg)
    # position near top-right of main window
    x = root.winfo_rootx() + 20
    y = root.winfo_rooty() + 20
    t.geometry(f"+{x}+{y}")
    lbl = tk.Label(t, text=text, bg=bg, fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5)
    lbl.pack()
    t.after(duration, t.destroy)
