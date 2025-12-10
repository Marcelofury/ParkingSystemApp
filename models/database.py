"""
Database layer for Smart Parking Management System
Handles all SQLite operations and CRUD functionality
"""

import sqlite3
from utils.helpers import hash_password, now_str


class DB:
    """Database manager class handling all database operations"""
    
    def __init__(self, path="parking_system_upgraded.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_schema()

    def init_schema(self):
        """Initialize database schema with all required tables"""
        # USERS: username (pk), password_hash, full_name, role (admin/user), email
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT,
                full_name TEXT,
                role TEXT DEFAULT 'user',
                email TEXT
            )
        """)
        # VEHICLES: id, number, type, user (who parked), slot_id (nullable), entry_time, exit_time, payment_method
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT,
                type TEXT,
                user TEXT,
                slot_id INTEGER,
                entry_time TEXT,
                exit_time TEXT,
                payment_method TEXT DEFAULT 'cash'
            )
        """)
        # SLOTS: id, name, type_allowed (Car/Motor/Both), status (free/occupied), hourly_rate
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                type_allowed TEXT,
                status TEXT DEFAULT 'free',
                hourly_rate REAL DEFAULT 0
            )
        """)
        # PAYMENTS: id, vehicle_number, amount, paid_at, duration_hours, generated_by, receipt_path, payment_method
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_number TEXT,
                amount REAL,
                paid_at TEXT,
                duration_hours REAL,
                generated_by TEXT,
                receipt_path TEXT,
                payment_method TEXT DEFAULT 'cash'
            )
        """)
        # SETTINGS: key-value store for system configuration
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.conn.commit()
        # Migrate existing tables (add missing columns if they don't exist)
        self._migrate_schema()
        # ensure admin exists
        self.ensure_admin()

    def _migrate_schema(self):
        """Add missing columns to existing tables for backward compatibility"""
        try:
            # Check and add payment_method to vehicles table
            self.cursor.execute("PRAGMA table_info(vehicles)")
            cols = [col[1] for col in self.cursor.fetchall()]
            if 'payment_method' not in cols:
                self.cursor.execute("ALTER TABLE vehicles ADD COLUMN payment_method TEXT DEFAULT 'cash'")
            
            # Check and add email column to users
            self.cursor.execute("PRAGMA table_info(users)")
            cols = [col[1] for col in self.cursor.fetchall()]
            if 'email' not in cols:
                self.cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
            
            # Check and add hourly_rate to slots
            self.cursor.execute("PRAGMA table_info(slots)")
            cols = [col[1] for col in self.cursor.fetchall()]
            if 'hourly_rate' not in cols:
                self.cursor.execute("ALTER TABLE slots ADD COLUMN hourly_rate REAL DEFAULT 0")
            
            # Check and add payment_method to payments
            self.cursor.execute("PRAGMA table_info(payments)")
            cols = [col[1] for col in self.cursor.fetchall()]
            if 'payment_method' not in cols:
                self.cursor.execute("ALTER TABLE payments ADD COLUMN payment_method TEXT DEFAULT 'cash'")
            
            self.conn.commit()
        except Exception as e:
            print(f"Migration warning: {e}")

    def ensure_admin(self):
        """Ensure default admin account exists"""
        self.cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not self.cursor.fetchone():
            admin_pw = hash_password("admin123")  # default, tell user to change
            self.cursor.execute("INSERT INTO users(username,password_hash,full_name,role) VALUES(?,?,?,?)",
                                ("admin", admin_pw, "Administrator", "admin"))
            self.conn.commit()

    # --- users CRUD ---
    def create_user(self, username, password, full_name, role="user", email=""):
        """Create a new user account"""
        pw_hash = hash_password(password)
        self.cursor.execute("INSERT INTO users(username,password_hash,full_name,role,email) VALUES(?,?,?,?,?)",
                            (username, pw_hash, full_name, role, email))
        self.conn.commit()

    def get_user(self, username):
        """Get user details by username"""
        self.cursor.execute("SELECT username,full_name,role,email FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()

    def validate_user(self, username, password):
        """Validate user credentials"""
        self.cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if not row:
            return False
        return row[0] == hash_password(password)

    def update_password(self, username, new_password):
        """Update user password"""
        self.cursor.execute("UPDATE users SET password_hash=? WHERE username=?", (hash_password(new_password), username))
        self.conn.commit()

    def update_user(self, username, full_name=None, email=None, role=None):
        """Update user details"""
        parts = []
        vals = []
        if full_name is not None:
            parts.append("full_name=?"); vals.append(full_name)
        if email is not None:
            parts.append("email=?"); vals.append(email)
        if role is not None:
            parts.append("role=?"); vals.append(role)
        if parts:
            vals.append(username)
            self.cursor.execute(f"UPDATE users SET {', '.join(parts)} WHERE username=?", vals)
            self.conn.commit()

    def delete_user(self, username):
        """Delete a user account"""
        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))
        self.conn.commit()

    def list_users(self):
        """Get list of all users"""
        self.cursor.execute("SELECT username, full_name, role, email FROM users")
        return self.cursor.fetchall()

    # --- slots CRUD ---
    def create_slot(self, name, type_allowed, hourly_rate=0):
        """Create a new parking slot"""
        self.cursor.execute("INSERT INTO slots(name,type_allowed,status,hourly_rate) VALUES(?,?,?,?)", 
                          (name, type_allowed, "free", hourly_rate))
        self.conn.commit()

    def update_slot(self, slot_id, name=None, type_allowed=None, status=None, hourly_rate=None):
        """Update parking slot details"""
        parts = []
        vals = []
        if name is not None:
            parts.append("name=?"); vals.append(name)
        if type_allowed is not None:
            parts.append("type_allowed=?"); vals.append(type_allowed)
        if status is not None:
            parts.append("status=?"); vals.append(status)
        if hourly_rate is not None:
            parts.append("hourly_rate=?"); vals.append(hourly_rate)
        vals.append(slot_id)
        self.cursor.execute(f"UPDATE slots SET {', '.join(parts)} WHERE id=?", vals)
        self.conn.commit()

    def delete_slot(self, slot_id):
        """Delete a parking slot"""
        self.cursor.execute("DELETE FROM slots WHERE id=?", (slot_id,))
        self.conn.commit()

    def list_slots(self):
        """Get list of all parking slots"""
        self.cursor.execute("SELECT id,name,type_allowed,status,hourly_rate FROM slots")
        return self.cursor.fetchall()
    
    def get_slot_by_id(self, slot_id):
        """Get parking slot by ID"""
        self.cursor.execute("SELECT id,name,type_allowed,status,hourly_rate FROM slots WHERE id=?", (slot_id,))
        return self.cursor.fetchone()

    def get_free_slot_for_type(self, vtype):
        """Find first available free slot for vehicle type"""
        # try exact type then 'Both'
        self.cursor.execute("SELECT id,name,hourly_rate FROM slots WHERE status='free' AND (type_allowed=? OR type_allowed='Both') LIMIT 1", (vtype,))
        return self.cursor.fetchone()

    # --- vehicles CRUD ---
    def park_vehicle(self, number, vtype, username, slot_id, entry_time, payment_method='cash'):
        """Park a vehicle in a slot"""
        self.cursor.execute("""
            INSERT INTO vehicles(number,type,user,slot_id,entry_time,exit_time,payment_method)
            VALUES(?,?,?,?,?,NULL,?)
        """, (number, vtype, username, slot_id, entry_time, payment_method))
        self.cursor.execute("UPDATE slots SET status='occupied' WHERE id=?", (slot_id,))
        self.conn.commit()

    def exit_vehicle(self, number, exit_time):
        """Exit a vehicle from parking"""
        # update latest vehicle with this number that has null exit_time
        self.cursor.execute("""
            UPDATE vehicles SET exit_time=?
            WHERE number=? AND exit_time IS NULL
        """, (exit_time, number))
        # free slot(s)
        self.cursor.execute("SELECT slot_id FROM vehicles WHERE number=? ORDER BY id DESC LIMIT 1", (number,))
        r = self.cursor.fetchone()
        if r and r[0]:
            self.cursor.execute("UPDATE slots SET status='free' WHERE id=?", (r[0],))
        self.conn.commit()
        return self.cursor.rowcount

    def list_parked(self):
        """Get list of all parked vehicles"""
        self.cursor.execute("SELECT id,number,type,user,slot_id,entry_time,exit_time,payment_method FROM vehicles ORDER BY id DESC")
        return self.cursor.fetchall()

    def search_vehicles(self, search_term="", date_from="", date_to=""):
        """Search vehicles by number, user, or date range"""
        query = "SELECT id,number,type,user,slot_id,entry_time,exit_time,payment_method FROM vehicles WHERE 1=1"
        params = []
        
        if search_term:
            query += " AND (number LIKE ? OR user LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if date_from:
            query += " AND entry_time >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND entry_time <= ?"
            params.append(date_to)
        
        query += " ORDER BY id DESC"
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_last_vehicle_record(self, number):
        """Get last vehicle record by number"""
        self.cursor.execute("SELECT id,number,type,user,slot_id,entry_time,exit_time,payment_method FROM vehicles WHERE number=? ORDER BY id DESC LIMIT 1", (number,))
        return self.cursor.fetchone()

    # --- payments ---
    def record_payment(self, vehicle_number, amount, duration_hours, generated_by, receipt_path, payment_method="cash"):
        """Record a payment transaction"""
        paid_at = now_str()
        self.cursor.execute("INSERT INTO payments(vehicle_number,amount,paid_at,duration_hours,generated_by,receipt_path,payment_method) VALUES(?,?,?,?,?,?,?)",
                            (vehicle_number, amount, paid_at, duration_hours, generated_by, receipt_path, payment_method))
        self.conn.commit()

    def list_payments(self):
        """Get list of all payments"""
        self.cursor.execute("SELECT id,vehicle_number,amount,paid_at,duration_hours,generated_by,receipt_path,payment_method FROM payments ORDER BY id DESC")
        return self.cursor.fetchall()
    
    def search_payments(self, search_term="", date_from="", date_to=""):
        """Search payments by vehicle number or date range"""
        query = "SELECT id,vehicle_number,amount,paid_at,duration_hours,generated_by,receipt_path,payment_method FROM payments WHERE 1=1"
        params = []
        
        if search_term:
            query += " AND (vehicle_number LIKE ? OR generated_by LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])
        
        if date_from:
            query += " AND paid_at >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND paid_at <= ?"
            params.append(date_to)
        
        query += " ORDER BY id DESC"
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_revenue_stats(self, date_from="", date_to=""):
        """Get revenue statistics for a date range"""
        query = "SELECT SUM(amount) as total, COUNT(*) as count FROM payments WHERE 1=1"
        params = []
        
        if date_from:
            query += " AND paid_at >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND paid_at <= ?"
            params.append(date_to)
        
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        return {'total': result[0] or 0, 'count': result[1] or 0}
    
    def get_daily_revenue(self, days=7):
        """Get daily revenue for the last N days"""
        self.cursor.execute("""
            SELECT DATE(paid_at) as date, SUM(amount) as revenue
            FROM payments
            WHERE paid_at >= datetime('now', '-' || ? || ' days')
            GROUP BY DATE(paid_at)
            ORDER BY date
        """, (days,))
        return self.cursor.fetchall()
    
    def get_occupancy_stats(self):
        """Get current slot occupancy statistics"""
        self.cursor.execute("SELECT status, COUNT(*) FROM slots GROUP BY status")
        stats = dict(self.cursor.fetchall())
        return {
            'occupied': stats.get('occupied', 0),
            'free': stats.get('free', 0),
            'total': sum(stats.values())
        }
    
    # --- settings CRUD ---
    def get_setting(self, key, default=None):
        """Get a setting value by key"""
        self.cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
        row = self.cursor.fetchone()
        return row[0] if row else default
    
    def set_setting(self, key, value):
        """Set a setting value"""
        self.cursor.execute("INSERT OR REPLACE INTO settings(key, value) VALUES(?,?)", (key, value))
        self.conn.commit()
    
    def get_all_settings(self):
        """Get all settings as a dictionary"""
        self.cursor.execute("SELECT key, value FROM settings")
        return dict(self.cursor.fetchall())
