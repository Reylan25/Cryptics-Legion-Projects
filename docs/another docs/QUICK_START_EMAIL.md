# 🚀 Quick Start: Enable Gmail OTP Emails

## ⚡ 3 Steps to Enable Email Sending

### 1️⃣ Get Gmail App Password (2 minutes)
Visit: **https://myaccount.google.com/apppasswords**
- Click "Generate"
- Copy the 16-character password

### 2️⃣ Configure `.env` File (1 minute)
Open: `Cryptics_legion/.env`

Add your credentials:
```env
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
```

### 3️⃣ Test It! (30 seconds)
- Run the app
- Click "Forgot Password"
- Check your email! 📧

---

## 📧 Email Template Preview

Users will receive a beautiful HTML email:

```
┌─────────────────────────────────┐
│   🔐 Password Reset             │
│   [Gradient Purple Header]      │
├─────────────────────────────────┤
│                                 │
│ Your verification code is:      │
│                                 │
│     ┌─────────────────┐         │
│     │   123 456       │         │
│     └─────────────────┘         │
│                                 │
│ ⏰ This code expires in         │
│    10 minutes                   │
│                                 │
│ Enter this code in the app      │
│ to reset your password.         │
│                                 │
└─────────────────────────────────┘
```

---

## ✅ System Behavior

### Email Configured:
```
[OTP] ✅ Email sent successfully to user@gmail.com
[OTP] Sending OTP to user@gmail.com: 123456
[OTP] This OTP will expire in 10 minutes
```
**→ User receives email with OTP**

### Email NOT Configured:
```
[OTP] Email not configured. OTP: 123456
[OTP] To enable email sending, configure .env file
[OTP] Sending OTP to user@gmail.com: 123456
[OTP] This OTP will expire in 10 minutes
```
**→ Check console for OTP (development mode)**

---

## 🔒 Security Notes

✅ **Safe:** `.env` file is in `.gitignore` (won't be committed)
✅ **Secure:** Uses Gmail App Password (not your real password)
✅ **Private:** Credentials stay on your machine only

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Authentication failed" | Use App Password, not regular password |
| Email not received | Check spam folder |
| Still seeing console OTP | Verify .env file has credentials |
| SMTP error | Check internet connection |

---

## 📚 Full Documentation

- **Setup Guide:** `GMAIL_SETUP_GUIDE.md`
- **Feature Overview:** `OTP_PASSWORD_RESET.md`

---

**Ready?** Configure your `.env` file now! 🚀
