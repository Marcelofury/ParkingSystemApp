#!/usr/bin/env python3
"""
Helper script to update email password in database
"""
from models import DB

print("=== UPDATE EMAIL PASSWORD ===")
print()
print("Enter your Google App Password below.")
print("Important: Remove ALL spaces (should be 16 characters)")
print("Example: abcdefghijklmnop")
print()

password = input("Paste App Password: ").strip()

# Remove any spaces
password = password.replace(" ", "")

print(f"\nPassword length: {len(password)} characters")

if len(password) != 16:
    print(f"⚠️  WARNING: App Password should be exactly 16 characters!")
    print(f"You entered: {len(password)} characters")
    confirm = input("Continue anyway? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        exit(0)

# Update database
db = DB()
db.update_setting('sender_password', password)

print("\n✅ Password updated in database!")
print("\nNow test it:")
print("1. Open the app")
print("2. Go to Admin > Settings")
print("3. Click 'Test Email'")
