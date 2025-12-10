"""
Views package for Smart Parking Management System
Contains all UI page classes
"""

from .base_page import Page
from .login_page import LoginPage
from .register_page import RegisterPage
from .user_dashboard_page import UserDashboardPage
from .dashboard_page import DashboardPage
from .slot_management_page import SlotMgmtPage
from .vehicles_page import VehiclesPage
from .payments_page import PaymentsPage
from .profile_page import ProfilePage
from .settings_page import SettingsPage
from .reports_page import ReportsPage
from .admin_manage_page import AdminManagePage

__all__ = [
    'Page',
    'LoginPage',
    'RegisterPage',
    'UserDashboardPage',
    'DashboardPage',
    'SlotMgmtPage',
    'VehiclesPage',
    'PaymentsPage',
    'ProfilePage',
    'SettingsPage',
    'ReportsPage',
    'AdminManagePage'
]
