"""
Admin Authentication Module
Handles admin login and verification
"""

import bcrypt
from core import db


def login_admin(username: str, password: str) -> tuple[bool, dict | None]:
    """
    Authenticate admin user
    
    Args:
        username: Admin username
        password: Admin password (plain text)
    
    Returns:
        tuple: (success: bool, admin_data: dict | None)
        admin_data contains: id, username, full_name, email, role
    """
    
    # Get admin by username
    admin = db.get_admin_by_username(username)
    
    if not admin:
        return False, None
    
    admin_id, db_username, password_blob, full_name, email, role, is_active = admin
    
    # Check if account is active
    if not is_active:
        return False, None
    
    # Verify password
    if isinstance(password_blob, str):
        password_blob = password_blob.encode("utf-8")
    if not bcrypt.checkpw(password.encode("utf-8"), password_blob):
        return False, None
    
    # Update last login
    db.update_admin_last_login(admin_id)
    
    # Log successful login
    db.log_admin_activity(admin_id, "login", None, "Admin logged in successfully")
    
    # Return admin data
    admin_data = {
        "id": admin_id,
        "username": db_username,
        "full_name": full_name,
        "email": email,
        "role": role
    }
    
    return True, admin_data


def is_admin_username(username: str) -> bool:
    """
    Check if username belongs to an admin account
    
    Args:
        username: Username to check
    
    Returns:
        bool: True if username exists in admins table
    """
    admin = db.get_admin_by_username(username)
    return admin is not None


def logout_admin(admin_id: int, username: str):
    """
    Log admin logout activity
    
    Args:
        admin_id: Admin ID
        username: Admin username for logging
    """
    db.log_admin_activity(admin_id, "logout", None, f"Admin {username} logged out")
