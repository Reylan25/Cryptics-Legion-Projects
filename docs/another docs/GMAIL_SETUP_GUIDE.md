# Gmail SMTP Setup Guide for OTP Email Sending

## 📧 How to Enable Gmail Email Sending

The OTP system can now send actual emails via Gmail! Follow these steps to configure it:

## Step 1: Enable Gmail App Password

### Why App Password?
Google requires App Passwords for applications accessing Gmail via SMTP. Your regular Gmail password won't work.

### Steps to Create App Password:

1. **Go to your Google Account Settings**
   - Visit: https://myaccount.google.com/

2. **Enable 2-Step Verification** (if not already enabled)
   - Go to Security → 2-Step Verification
   - Follow the prompts to enable it

3. **Create App Password**
   - Go to Security → App passwords
   - Or visit directly: https://myaccount.google.com/apppasswords
   - Select "Mail" as the app
   - Select "Windows Computer" (or your device)
   - Click "Generate"
   - **Copy the 16-character password** (you won't see it again!)

## Step 2: Configure the Application

1. **Open the `.env` file** in the `Cryptics_legion` folder:
   ```
   Cryptics_legion/.env
   ```

2. **Fill in your credentials**:
   ```env
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_16_character_app_password
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   APP_NAME=Cryptics Legion Expense Tracker
   ```

3. **Example**:
   ```env
   EMAIL_SENDER=myapp@gmail.com
   EMAIL_PASSWORD=abcd efgh ijkl mnop
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   APP_NAME=Cryptics Legion Expense Tracker
   ```

## Step 3: Test It!

1. Run your application
2. Go to "Forgot Password"
3. Enter a username with a valid email
4. Check your email inbox for the OTP!

## 📧 What the Email Looks Like

Users will receive a beautiful HTML email with:
- 🎨 Professional gradient header
- 🔢 Large, easy-to-read OTP code (formatted as "123 456")
- ⏰ Expiration warning (10 minutes)
- 📱 Mobile-friendly responsive design
- ⚠️ Security notice if they didn't request it

## 🔒 Security Best Practices

### ✅ DO:
- Keep your `.env` file secure and private
- Never commit `.env` to version control (it's in .gitignore)
- Use a dedicated Gmail account for the app
- Regularly rotate your app password
- Monitor sent emails in your Gmail

### ❌ DON'T:
- Share your app password with anyone
- Use your personal Gmail account
- Commit credentials to Git
- Use your regular Gmail password (it won't work anyway)

## 🔄 Fallback Behavior

The system is smart:
- ✅ If email is configured → Sends actual email
- ✅ If email NOT configured → Prints OTP to console (development mode)
- ✅ Always works - never blocks the flow

## 🚨 Troubleshooting

### "Authentication failed" error
- Make sure you're using an **App Password**, not your regular password
- Check that 2-Step Verification is enabled
- Verify the email address is correct

### "SMTP connection failed"
- Check your internet connection
- Verify SMTP_SERVER=smtp.gmail.com
- Verify SMTP_PORT=587

### Email not received
- Check spam/junk folder
- Verify the recipient email is correct
- Check Gmail sent folder to confirm it was sent
- Wait a few minutes (sometimes delayed)

### Still using console output
- Check that `.env` file exists in `Cryptics_legion/` folder
- Verify EMAIL_SENDER and EMAIL_PASSWORD are filled in
- Restart the application after updating .env

## 📝 Testing Without Email Setup

If you don't want to configure email yet:
- Leave `.env` file empty or don't create it
- System will print OTP to console (current behavior)
- Everything else works normally

## 🎯 Quick Start (TL;DR)

1. Get Gmail App Password: https://myaccount.google.com/apppasswords
2. Edit `Cryptics_legion/.env`:
   ```
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password_here
   ```
3. Run app and test!

---

**Need Help?** The system will print helpful messages to the console indicating whether email was sent successfully or if it's using fallback mode.
