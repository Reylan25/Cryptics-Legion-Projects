# Admin System - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Run the Application
```bash
cd Cryptics_legion
flet run src/main.py
```

The default admin account is created automatically!

### Step 2: Login as Admin
On the login screen:
- **Username**: `ADMIN`
- **Password**: `ADMIN256`

### Step 3: Access Admin Features
You'll be taken directly to the Admin Dashboard where you can:
- ✅ View system statistics
- ✅ Manage users
- ✅ Review activity logs

## 📊 Admin Dashboard Features

### System Statistics (Real-time)
- Total Users
- Total Expenses  
- Total Amount Tracked
- Active Users (30 days)
- New Users This Month
- Total Accounts

### Quick Actions
- **User Management** - View and manage all users
- **Activity Logs** - See all admin activities

## 👥 User Management

### What You Can Do:
1. **View All Users** - Complete list with statistics
2. **Search Users** - By username or email
3. **Delete Users** - With confirmation dialog

### User Information Shown:
- Username & Email
- Total Expenses
- Total Amount Spent
- Registration Date

### To Delete a User:
1. Click the delete icon (🗑️) on any user card
2. Confirm deletion in the dialog
3. User and all their data will be permanently removed

## 📜 Activity Logs

### What's Tracked:
- Admin logins/logouts
- User deletions
- Page views
- All admin actions

### Information Shown:
- Action type
- Admin who performed it
- Target user (if applicable)
- Date and time
- Detailed description

### Refresh Logs:
Click the refresh button (🔄) in the header

## 🔐 Security Features

✅ Encrypted passwords  
✅ Activity logging  
✅ Confirmation dialogs for destructive actions  
✅ Automatic session tracking  

## 🎨 UI Overview

### Color Coding:
- 🔵 **Blue** - Dashboard & User Management
- 🟠 **Orange** - Activity Logs
- 🟢 **Green** - Success messages
- 🔴 **Red** - Delete/Error actions

### Navigation:
- **Back Arrow** - Return to previous page
- **Logout** - Exit admin session (goes to login)
- **Quick Action Buttons** - Fast access to features

## ⚠️ Important Notes

1. **Deletions are permanent** - Always confirm before deleting users
2. **Activity is logged** - All your admin actions are recorded
3. **Separate from user accounts** - Admin account is independent
4. **Case-sensitive login** - Username must be exactly `ADMIN`

## 🔧 Troubleshooting

### Can't login?
- Make sure username is `ADMIN` (all caps)
- Password is `ADMIN256` (case-sensitive)
- Try running `python src/init_admin.py` to recreate admin

### Dashboard not showing statistics?
- Check that users have created expenses
- Statistics update in real-time

### Need to create another admin?
Run the initialization script:
```bash
python src/init_admin.py
```

## 📱 Mobile Responsive

The admin interface adapts to:
- Desktop screens
- Tablets
- Mobile devices

All features work across all screen sizes!

## 🎯 Common Tasks

### Check how many users signed up today:
1. Go to Dashboard
2. Look at "New Users (This Month)" card

### Find a specific user:
1. Go to User Management
2. Use the search bar
3. Type username or email

### Review what happened yesterday:
1. Go to Activity Logs
2. Scroll through the timeline
3. Filter by date/admin if needed

### Delete an inactive user:
1. Go to User Management
2. Search for the user
3. Click delete icon (🗑️)
4. Confirm deletion

## 💡 Tips

- Use the search in User Management for quick access
- Refresh Activity Logs to see the latest actions
- Statistics update automatically when data changes
- Keep the admin password secure!

## 🆘 Need Help?

Check the full documentation: `ADMIN_SYSTEM_DOCUMENTATION.md`

---

**Default Admin Credentials**  
Username: `ADMIN`  
Password: `ADMIN256`

**Please change the password after first login for security!**
