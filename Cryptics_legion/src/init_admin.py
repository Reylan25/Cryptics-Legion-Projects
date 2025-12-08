"""
Initialize default admin account
Run this script once to create the default admin user
"""

import bcrypt
from core import db

def create_default_admin():
    """Create the default admin account: ADMIN / ADMIN256"""
    
    # Initialize database
    db.connect_db()
    
    # Check if admin already exists
    existing_admin = db.get_admin_by_username("ADMIN")
    
    if existing_admin:
        print("Admin account 'ADMIN' already exists!")
        return
    
    # Create admin password hash
    password_hash = bcrypt.hashpw("ADMIN256".encode("utf-8"), bcrypt.gensalt())
    
    # Insert admin
    success = db.insert_admin(
        username="ADMIN",
        password_blob=password_hash,
        full_name="System Administrator",
        email="admin@expensetracker.com"
    )
    
    if success:
        print("✓ Default admin account created successfully!")
        print("  Username: ADMIN")
        print("  Password: ADMIN256")
        print("\nPlease login and change the password for security.")
    else:
        print("✗ Failed to create admin account.")


if __name__ == "__main__":
    create_default_admin()
