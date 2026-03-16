# OTP-Based Password Reset Feature

## Overview
A complete OTP (One-Time Password) based password reset system has been implemented for the Cryptics Legion Expense Tracker application.

## Features

### 1. **User-Friendly Flow**
The password reset process consists of three simple stages:
- **Stage 1**: Enter username or email
- **Stage 2**: Enter the 6-digit OTP code
- **Stage 3**: Set new password

### 2. **Security Features**
- OTPs expire after 10 minutes
- OTPs can only be used once
- Previous unused OTPs are automatically invalidated when a new one is requested
- Passwords are securely hashed using bcrypt
- Automatic cleanup of expired OTPs (older than 24 hours)

### 3. **Components Created**

#### **utils/otp.py**
Contains OTP utility functions:
- `generate_otp(length=6)` - Generates a random 6-digit OTP
- `is_otp_expired(created_at, validity_minutes=10)` - Checks if OTP has expired
- `format_otp_display(otp)` - Formats OTP for display (e.g., "123 456")
- `send_otp_notification(email, otp)` - Placeholder for sending OTP (currently prints to console)

#### **core/db.py**
Added database functions:
- `create_password_reset_otp(user_id, otp)` - Store new OTP
- `verify_password_reset_otp(user_id, otp)` - Verify OTP validity
- `mark_otp_as_used(otp_id)` - Mark OTP as used after successful reset
- `cleanup_expired_otps()` - Remove OTPs older than 24 hours
- `get_user_by_email(email)` - Find user by email
- `update_password(user_id, new_password_blob)` - Update user password

#### **core/auth.py**
Added authentication functions:
- `request_password_reset(identifier)` - Request OTP for password reset
- `verify_otp_and_reset_password(user_id, otp, new_password)` - Verify OTP and reset password

#### **ui/forgot_password_page.py**
Complete UI for the password reset flow with:
- Clean, modern design matching the app theme
- Three-stage wizard interface
- Real-time validation
- Error handling and user feedback
- Resend OTP functionality
- Password visibility toggles

## How to Use

### For Users:
1. Click "Forgot Password?" on the login page
2. Enter your username or email address
3. **Important**: You must have an email address configured in your profile to receive the OTP
4. Check your email/console for the 6-digit OTP code
5. Enter the OTP code within 10 minutes
6. Set your new password
7. Login with your new password

### ⚠️ Important Requirement
**Users must have an email address in their profile to use password reset.** 

If you try to reset your password and see "No email address found for this account", you have two options:
1. **If you remember your password**: Login and add an email address in Profile Settings
2. **If you forgot your password**: Contact support for manual password reset

### Adding Email to Your Profile:
1. Login to your account
2. Go to Profile → Personal Details
3. Enter your email address
4. Save changes
5. Now you can use the Forgot Password feature

### For Developers:

#### Email Setup (Gmail SMTP):
The system now supports **actual Gmail email sending**! 

**Quick Setup:**
1. Get a Gmail App Password: https://myaccount.google.com/apppasswords
2. Edit `Cryptics_legion/.env` file:
   ```env
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_16_char_app_password
   ```
3. Run the app - OTPs will be sent via email!

**Detailed Instructions:** See `GMAIL_SETUP_GUIDE.md`

#### Fallback Behavior:
- ✅ Email configured → Sends actual email to user
- ✅ Email NOT configured → Prints OTP to console (development mode)
- ✅ Email send fails → Prints OTP to console as backup

#### Current Implementation:
```python
# Console output (always shown):
[OTP] Sending OTP to user@email.com: 123456
[OTP] This OTP will expire in 10 minutes

# Email output (if configured):
[OTP] ✅ Email sent successfully to user@email.com
# OR
[OTP] ❌ Failed to send email: [error details]
[OTP] Fallback - OTP code: 123456
```

## Database Schema

A new table `password_reset_otps` has been added:
```sql
CREATE TABLE password_reset_otps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    otp TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_used INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
```

## Testing

### Test Scenario 1: Successful Password Reset
1. Create a test user with an email address
2. Request password reset
3. Note the OTP from console
4. Enter OTP within 10 minutes
5. Set new password
6. Verify login works with new password

### Test Scenario 2: Expired OTP
1. Request password reset
2. Wait more than 10 minutes
3. Try to use the OTP
4. Should receive "OTP has expired" error

### Test Scenario 3: Used OTP
1. Request password reset
2. Complete password reset successfully
3. Try to use the same OTP again
4. Should receive "OTP already used" error

### Test Scenario 4: Invalid OTP
1. Request password reset
2. Enter wrong OTP code
3. Should receive "Invalid OTP" error

## Important Notes

1. **⚠️ Email Required**: Users MUST have an email address configured in their profile to use password reset. Users without an email will see a helpful error message directing them to:
   - Login with their current password and add an email in profile settings
   - Contact support for manual password reset if they can't login

2. **Email Configuration in Profile**: Users can add/update their email address by going to:
   - Profile → Personal Details → Email field

3. **Console Output**: Currently, OTPs are printed to the console for testing. Configure email/SMS provider in production.

4. **Security**: 
   - OTPs are stored in plaintext (consider hashing for production)
   - Implement rate limiting to prevent abuse
   - Add CAPTCHA for production environments

4. **Maintenance**: Run `cleanup_expired_otps()` periodically to remove old OTPs.

## Future Enhancements

- [ ] Email/SMS integration for OTP delivery
- [ ] Rate limiting to prevent OTP spam
- [ ] OTP attempt tracking (lock after 3 failed attempts)
- [ ] Hash OTPs in database
- [ ] Add CAPTCHA protection
- [ ] Multi-factor authentication options
- [ ] Recovery codes as backup method
- [ ] Audit log for password reset attempts
