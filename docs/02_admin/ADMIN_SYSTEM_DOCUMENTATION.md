# Admin System Documentation

## Overview
The Smart Expense Tracker now includes a complete admin system with dedicated UI and comprehensive management features.

## Features

### 1. **Admin Authentication**
- Admins can log in through the regular login page
- Username: `ADMIN`
- Password: `ADMIN256`
- Automatic detection and routing to admin dashboard

### 2. **Admin Dashboard**
Modern dashboard displaying:
- **System Statistics**
  - Total Users
  - Total Expenses
  - Total Amount Tracked
  - Active Users (last 30 days)
  - New Users This Month
  - Total Accounts

- **Recent Activity**
  - Last 5 admin activities
  - Action type, timestamp, and details

- **Quick Actions**
  - User Management
  - Activity Logs

### 3. **User Management**
- View all registered users
- Search by username or email
- User information displayed:
  - Username and email
  - Number of expenses
  - Total amount spent
  - Registration date
- **Delete User** functionality
  - Confirmation dialog
  - Complete data deletion (user, expenses, accounts, profiles)
  - Activity logging

### 4. **Activity Logs**
- Complete audit trail of admin actions
- Shows:
  - Admin username
  - Action performed
  - Target user (if applicable)
  - Timestamp
  - Detailed description
- Refresh capability
- Last 100 activities displayed

### 5. **Security Features**
- Encrypted admin passwords (stored as BLOB)
- Activity logging for all admin actions
- Role-based access control
- Active/inactive account status
- Last login tracking

## Database Schema

### `admins` Table
```sql
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password BLOB NOT NULL,
    full_name TEXT,
    email TEXT,
    role TEXT DEFAULT 'admin',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_login TEXT,
    is_active INTEGER DEFAULT 1
)
```

### `admin_logs` Table
```sql
CREATE TABLE admin_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    target_user_id INTEGER,
    details TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id)
)
```

## File Structure

### Core Files
- `src/core/admin_auth.py` - Admin authentication module
- `src/core/db.py` - Database functions (includes admin tables and functions)
- `src/init_admin.py` - Admin initialization script (standalone)

### UI Pages
- `src/ui/admin_dashboard_page.py` - Main admin dashboard
- `src/ui/admin_users_page.py` - User management page
- `src/ui/admin_logs_page.py` - Activity logs page
- `src/ui/login_page.py` - Modified to support admin login

### Main Application
- `src/main.py` - Updated with admin routing and initialization

## Database Functions

### Authentication
- `insert_admin(username, password_blob, full_name, email)` - Create admin account
- `get_admin_by_username(username)` - Retrieve admin details
- `update_admin_last_login(admin_id)` - Update last login timestamp

### Activity Tracking
- `log_admin_activity(admin_id, action, target_user_id, details)` - Log admin actions
- `get_admin_logs(limit=100)` - Retrieve activity logs with details

### User Management
- `get_all_users_for_admin()` - Get all users with expense statistics
- `delete_user_by_admin(user_id)` - Complete user deletion with logging

### Statistics
- `get_system_statistics()` - Returns:
  - `total_users` - Total registered users
  - `total_expenses` - Total number of expenses
  - `total_amount` - Total amount tracked
  - `total_accounts` - Total user accounts
  - `active_users` - Users active in last 30 days
  - `new_users_this_month` - Users registered this month

## Usage

### First Time Setup

1. **Run the application**:
```bash
cd Cryptics_legion
flet run src/main.py
```

The default admin account will be created automatically on first run.

2. **Login as Admin**:
- Username: `ADMIN`
- Password: `ADMIN256`

3. **Change Password** (Recommended):
You'll need to update the database directly or add a password change feature.

### Navigation Flow

**For Admin Users:**
1. Login → Admin Dashboard
2. Dashboard shows system statistics and quick actions
3. Navigate to:
   - User Management (view/delete users)
   - Activity Logs (view admin activities)

**For Regular Users:**
1. Login → Passcode (if set) → Home
2. Regular app experience (unchanged)

## Admin Actions Logged

The system automatically logs:
- `login` - Admin login
- `logout` - Admin logout
- `delete_user` - User deletion
- `view_users` - User list access
- `view_logs` - Activity logs access

## UI Design

### Design Principles
- Modern Material Design
- Consistent with existing app theme
- Dark mode optimized
- Responsive layouts
- Clear visual hierarchy

### Color Scheme
- **Dashboard**: Blue (Primary)
- **User Management**: Blue (Primary)
- **Activity Logs**: Orange (Accent)
- **Success Actions**: Green
- **Delete Actions**: Red (Error)

### Components
- Statistics cards with icons
- Action buttons with gradients
- User cards with details
- Activity timeline items
- Confirmation dialogs

## Security Considerations

1. **Password Storage**: Admin passwords are encrypted (BLOB)
2. **Activity Logging**: All admin actions are tracked
3. **Role System**: Prepared for future role expansion
4. **Account Status**: Can disable admin accounts via `is_active` flag

## Future Enhancements

Potential additions:
- [ ] Admin password change functionality
- [ ] Multiple admin roles (super admin, moderator)
- [ ] Export user/expense data
- [ ] Advanced filtering and search
- [ ] Email notifications for admin actions
- [ ] Batch user operations
- [ ] System backup/restore
- [ ] Analytics and reports
- [ ] User suspension (temporary disable)

## Troubleshooting

### Admin account not created
- Check database file exists: `src/database/expense_tracker.db`
- Run initialization script: `python src/init_admin.py`
- Check console for error messages

### Cannot login as admin
- Verify username is exactly `ADMIN` (case-sensitive)
- Verify password is exactly `ADMIN256`
- Check database has admin record: Query `SELECT * FROM admins`

### Admin pages not showing
- Verify imports in `main.py`
- Check state has `is_admin` and `admin` keys
- Review console for Python errors

## Notes

- Admin accounts are completely separate from user accounts
- Admin can view but not modify their own profile (by design)
- Deleting a user is permanent and cannot be undone
- Activity logs cannot be deleted (audit trail integrity)

## Support

For issues or questions:
1. Check the console output for errors
2. Review the activity logs for clues
3. Verify database integrity
4. Check file permissions

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Created By**: Smart Expense Tracker Team
