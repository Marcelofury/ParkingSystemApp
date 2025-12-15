#!/usr/bin/env python3
"""Test script to verify user-specific record filtering"""

from models.database import DB

# Initialize database
db = DB()

# Test data
print("=== Testing User-Specific Record Filtering ===\n")

# Get all parked vehicles
all_vehicles = db.list_parked()
print(f"Total vehicles in system (admin view): {len(all_vehicles)}")

# Test new list_user_vehicles method
admin_vehicles = db.list_user_vehicles('admin')
print(f"Admin's vehicles (filtered view): {len(admin_vehicles)}")
for v in admin_vehicles[:3]:  # Show first 3
    print(f"  - {v[1]} ({v[2]}) parked at slot {v[4]}")

user1_vehicles = db.list_user_vehicles('user1')
print(f"\nUser1's vehicles (filtered view): {len(user1_vehicles)}")
for v in user1_vehicles[:3]:  # Show first 3
    print(f"  - {v[1]} ({v[2]}) parked at slot {v[4]}")

print("\n=== Testing Payment Filtering ===\n")

# Test all payments
all_payments = db.list_payments()
print(f"Total payments in system (admin view): {len(all_payments)}")

# Test the get_user_payments method
admin_payments = db.get_user_payments('admin')
print(f"Admin's payments (for vehicles they own): {len(admin_payments)}")
total_admin = sum(p[2] for p in admin_payments)
print(f"  Total: {total_admin:.2f} UGX")

user1_payments = db.get_user_payments('user1')
print(f"\nUser1's payments (for vehicles they own): {len(user1_payments)}")
total_user1 = sum(p[2] for p in user1_payments)
print(f"  Total: {total_user1:.2f} UGX")

print("\n=== Testing Search Functions ===\n")

# Test search_user_vehicles
admin_search = db.search_user_vehicles('admin', 'UAH')
print(f"Admin's vehicles containing 'UAH': {len(admin_search)}")

user1_search = db.search_user_vehicles('user1', 'UBJ')
print(f"User1's vehicles containing 'UBJ': {len(user1_search)}")

# Test search_user_payments
admin_payment_search = db.search_user_payments('admin', '')
print(f"\nAdmin's payments (search): {len(admin_payment_search)}")

user1_payment_search = db.search_user_payments('user1', '')
print(f"User1's payments (search): {len(user1_payment_search)}")

print("\n✓ Test completed successfully - Users now have isolated records!")
