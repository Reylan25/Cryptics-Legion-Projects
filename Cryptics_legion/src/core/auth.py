# src/core/auth.py
import bcrypt
from core import db

# register: uses db.insert_user
def register_user(username: str, password: str) -> bool:
    if not username or not password:
        return False
    pw_blob = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return db.insert_user(username, pw_blob)


# login: verify against hashed blob
def login_user(username: str, password: str):
    if not username or not password:
        return None
    row = db.get_user_by_username(username)
    if not row:
        return None
    user_id, pw_blob = row[0], row[1]
    if isinstance(pw_blob, str):
        pw_blob = pw_blob.encode("utf-8")
    if bcrypt.checkpw(password.encode("utf-8"), pw_blob):
        # Update last login timestamp
        db.update_last_login(user_id)
        return user_id
    return None


# ----- Password Reset Functions -----
def request_password_reset(identifier: str) -> tuple:
    """
    Request a password reset OTP.
    identifier can be either username or email.
    Returns (success, message, user_info_dict)
    """
    from utils.otp import generate_otp, send_otp_notification
    
    # Try to find user by username first
    user_row = db.get_user_by_username(identifier)
    if user_row:
        user_id = user_row[0]
        # Get full user profile to get email
        profile = db.get_user_profile(user_id)
        email = profile.get('email', '')
    else:
        # Try to find by email
        user_row = db.get_user_by_email(identifier)
        if user_row:
            user_id, username, email = user_row
        else:
            return (False, "User not found", None)
    
    # Check if user has an email configured
    if not email:
        return (False, "No email associated with this account. Please contact support.", None)
    
    # Generate OTP
    otp = generate_otp()
    
    # Store OTP in database
    if not db.create_password_reset_otp(user_id, otp):
        return (False, "Failed to generate OTP. Please try again.", None)
    
    # Send OTP (currently prints to console)
    if not send_otp_notification(email, otp):
        return (False, "Failed to send OTP. Please try again.", None)
    
    return (True, f"OTP sent to {email}", {"user_id": user_id, "email": email})


def verify_otp_and_reset_password(user_id: int, otp: str, new_password: str) -> tuple:
    """
    Verify OTP and reset password.
    Returns (success, message)
    """
    if not new_password or len(new_password) < 4:
        return (False, "Password must be at least 4 characters")
    
    # Verify OTP
    success, message, otp_id = db.verify_password_reset_otp(user_id, otp)
    if not success:
        return (False, message)
    
    # Hash new password
    pw_blob = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
    
    # Update password
    if not db.update_password(user_id, pw_blob):
        return (False, "Failed to update password. Please try again.")
    
    # Mark OTP as used
    db.mark_otp_as_used(otp_id)
    
    return (True, "Password reset successfully!")
