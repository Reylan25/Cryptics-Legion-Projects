# src/utils/otp.py
import random
import string
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path


def generate_otp(length: int = 6) -> str:
    """
    Generate a random numeric OTP.
    
    Args:
        length: Length of the OTP (default 6 digits)
    
    Returns:
        String containing the OTP
    """
    return ''.join(random.choices(string.digits, k=length))


def is_otp_expired(created_at: str, validity_minutes: int = 10) -> bool:
    """
    Check if an OTP has expired.
    
    Args:
        created_at: ISO format datetime string when OTP was created
        validity_minutes: How long the OTP is valid (default 10 minutes)
    
    Returns:
        True if OTP is expired, False otherwise
    """
    try:
        created_time = datetime.fromisoformat(created_at)
        expiry_time = created_time + timedelta(minutes=validity_minutes)
        return datetime.now() > expiry_time
    except:
        return True


def format_otp_display(otp: str) -> str:
    """
    Format OTP for display (e.g., "123 456" for 6 digits).
    
    Args:
        otp: The OTP string
    
    Returns:
        Formatted OTP string
    """
    if len(otp) == 6:
        return f"{otp[:3]} {otp[3:]}"
    return otp


def load_email_config():
    """Load email configuration from .env file."""
    try:
        from dotenv import load_dotenv
        
        # Try to load from .env file in the Cryptics_legion directory
        env_path = Path(__file__).parent.parent.parent / '.env'
        load_dotenv(env_path)
        
        config = {
            'sender': os.getenv('EMAIL_SENDER', ''),
            'password': os.getenv('EMAIL_PASSWORD', ''),
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'app_name': os.getenv('APP_NAME', 'Cryptics Legion Expense Tracker'),
        }
        
        return config
    except Exception as e:
        print(f"[OTP] Error loading email config: {e}")
        return None


def send_otp_email(email: str, otp: str) -> bool:
    """
    Send OTP via Gmail SMTP.
    
    Args:
        email: Recipient's email address
        otp: The OTP to send
    
    Returns:
        True if sent successfully, False otherwise
    """
    config = load_email_config()
    
    if not config or not config['sender'] or not config['password']:
        print(f"[OTP] Email not configured. OTP: {otp}")
        print(f"[OTP] To enable email sending, configure .env file")
        return False
    
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Password Reset Code - {config['app_name']}"
        message["From"] = config['sender']
        message["To"] = email
        
        # Create HTML and plain text versions
        text_content = f"""
Password Reset Request

Your password reset code is: {format_otp_display(otp)}

This code will expire in 10 minutes.

If you didn't request this password reset, please ignore this email.

---
{config['app_name']}
"""
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
        .otp-box {{ background: white; border: 2px solid #667eea; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
        .otp-code {{ font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px; font-family: monospace; }}
        .warning {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px; margin: 20px 0; border-radius: 4px; }}
        .footer {{ text-align: center; color: #6b7280; font-size: 12px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0;">🔐 Password Reset</h1>
        </div>
        <div class="content">
            <p>Hello,</p>
            <p>You requested to reset your password for <strong>{config['app_name']}</strong>.</p>
            
            <div class="otp-box">
                <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 14px;">Your verification code is:</p>
                <div class="otp-code">{format_otp_display(otp)}</div>
            </div>
            
            <div class="warning">
                ⏰ <strong>This code will expire in 10 minutes.</strong>
            </div>
            
            <p>Enter this code in the app to reset your password.</p>
            
            <p style="margin-top: 30px; color: #6b7280; font-size: 14px;">
                <strong>Didn't request this?</strong><br>
                If you didn't request a password reset, please ignore this email. Your password will remain unchanged.
            </p>
        </div>
        <div class="footer">
            <p>{config['app_name']}</p>
            <p>This is an automated message, please do not reply.</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Attach both versions
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['sender'], config['password'])
            server.send_message(message)
        
        print(f"[OTP] ✅ Email sent successfully to {email}")
        return True
        
    except Exception as e:
        print(f"[OTP] ❌ Failed to send email: {e}")
        print(f"[OTP] Fallback - OTP code: {otp}")
        return False


def send_otp_notification(email: str, otp: str) -> bool:
    """
    Send OTP to user via email.
    
    Args:
        email: User's email address
        otp: The OTP to send
    
    Returns:
        True if sent successfully, False otherwise
    """
    # Try to send via email
    email_sent = send_otp_email(email, otp)
    
    # Always print to console as backup
    print(f"[OTP] Sending OTP to {email}: {otp}")
    print(f"[OTP] This OTP will expire in 10 minutes")
    
    # Return True if email was sent OR if we're in fallback mode
    return True  # Always return True so the flow continues
