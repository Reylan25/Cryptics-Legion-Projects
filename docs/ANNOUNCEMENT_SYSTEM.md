# Announcement & Notification System

## Overview

The ExpenseWise application now includes a comprehensive announcement and notification system that allows administrators to send important messages to all users or specific user groups. Users receive these announcements as in-app notifications.

## Features

### For Administrators

#### 1. **Policy & Communications Page**
- **Location**: Admin Panel → Policy Rule (via Navigation Menu)
- **Two Main Tabs**:
  - **Policy Rules**: Manage expense policies and constraints
  - **Announcements**: Create and manage system-wide announcements

#### 2. **Announcement Management**

**Create Announcements**:
- Click "Create Announcement" button
- Fill in announcement details:
  - **Title**: Short, descriptive title
  - **Message**: Detailed announcement message (supports multi-line)
  - **Type**: Info, Warning, Success, or Urgent
  - **Priority**: Normal or High Priority
  - **Target Audience**: 
    - All Users
    - Specific Users (by user IDs)
  - **End Date**: Optional expiration date
  - **Pin to Top**: Feature important announcements

**Announcement Cards Display**:
- **Visual Indicators**:
  - Color-coded by type (Blue: Info, Orange: Warning, Green: Success, Red: Urgent)
  - High priority announcements have amber star badge
  - Pinned announcements show pin icon
- **Statistics**:
  - Total recipients count
  - Read count with percentage
  - Active/Inactive status
- **Actions**:
  - View Details: See full message and delivery statistics
  - Edit: Modify announcement content
  - Delete: Remove announcement (also deletes all notifications)

**Delivery Statistics**:
- Number of users who received the notification
- Number of users who read the notification
- Read rate percentage
- Detailed view shows all metadata

### For Users

#### 1. **Notification Center**
- **Access**: Click bell icon in app header
- **Displays**:
  - All announcements sent to the user
  - Unread notification count (badge on bell icon)
  - Color-coded by type
  - Timestamps (relative time: "2h ago", "Yesterday", etc.)

#### 2. **Notification Features**
- Automatic loading on app start
- Mark individual notifications as read
- Mark all notifications as read
- Clear notification history
- Toast notifications for new announcements

## Database Schema

### Announcements Table
```sql
CREATE TABLE announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info',                    -- info, warning, success, urgent
    priority TEXT DEFAULT 'normal',              -- normal, high
    admin_id INTEGER,                            -- Creator admin
    target_users TEXT DEFAULT 'all',             -- 'all' or comma-separated IDs
    start_date TEXT DEFAULT CURRENT_TIMESTAMP,
    end_date TEXT,                               -- Optional expiration
    is_active INTEGER DEFAULT 1,
    is_pinned INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admins(id)
)
```

### User Notifications Table
```sql
CREATE TABLE user_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    announcement_id INTEGER,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info',
    is_read INTEGER DEFAULT 0,
    read_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (announcement_id) REFERENCES announcements(id)
)
```

## API Functions

### Announcement Management
```python
# Create announcement
announcement_id = db.add_announcement(
    title="System Maintenance",
    message="The system will be down for maintenance...",
    type="warning",
    priority="high",
    admin_id=admin_id,
    target_users="all",
    end_date="2025-12-31 23:59:59",
    is_pinned=1
)

# Get all announcements
announcements = db.get_announcements(include_inactive=False)

# Get specific announcement
announcement = db.get_announcement_by_id(announcement_id)

# Update announcement
db.update_announcement(
    announcement_id,
    title="Updated Title",
    is_active=1
)

# Delete announcement
db.delete_announcement(announcement_id)
```

### User Notifications
```python
# Get user notifications
notifications = db.get_user_notifications(
    user_id=user_id,
    include_read=False,
    limit=20
)

# Mark notification as read
db.mark_notification_read(notification_id)

# Get unread count
unread_count = db.get_unread_notification_count(user_id)

# Load notifications into UI
from components.notification import NotificationHistory
NotificationHistory.load_user_notifications(user_id)
```

## UI Components

### Enhanced Policy Rules Page
**File**: `ui/admin_policy_rules_page.py`

**Key Features**:
- Tabbed interface (Policy Rules | Announcements)
- Statistics badges (rules count, announcements count)
- Beautiful card-based announcement display
- Rich dialogs for creating/editing announcements
- Detailed statistics view

### Notification Component
**File**: `components/notification.py`

**Updated Features**:
- Database integration via `NotificationHistory.load_user_notifications()`
- Automatic read/unread status synchronization
- Support for announcement-based notifications
- Persistent notification storage

## User Experience Flow

### Admin Creates Announcement
1. Admin navigates to Policy Rule → Announcements tab
2. Clicks "Create Announcement"
3. Fills in details (title, message, type, priority, target)
4. Clicks "Send Announcement"
5. System creates notification records for all target users
6. Success message confirms delivery

### User Receives Notification
1. User opens the app
2. System automatically loads notifications from database via `NotificationHistory.load_user_notifications(user_id)`
3. Bell icon shows unread count badge
4. User clicks bell to open notification center
5. Sees new announcement with colored icon
6. **All unread notifications automatically marked as read** when panel opens (saved to database)
7. User can read full message
8. **Logout**: System saves any pending read states via `on_user_logout()`
9. **Next Login**: All notifications (read/unread) are loaded from database - **fully persistent!**

### Notification Persistence Guarantee
- ✅ **Notifications persist across sessions** - stored in `user_notifications` table
- ✅ **Read status persists** - `is_read` and `read_at` saved to database
- ✅ **Survives logout/login** - database-backed storage ensures no data loss
- ✅ **Multi-device ready** - same notifications appear on any device (future)
- ✅ **No loss on app restart** - everything reloaded from database

## Announcement Types & Use Cases

### Info (Blue)
- General announcements
- Feature updates
- News and tips
- **Icon**: Info circle

### Warning (Orange)
- Policy changes
- Upcoming maintenance
- Important reminders
- **Icon**: Warning triangle

### Success (Green)
- Successful deployments
- Positive updates
- Celebrations
- **Icon**: Check circle

### Urgent (Red)
- Critical issues
- Security alerts
- Immediate action required
- **Icon**: Priority high

## Best Practices

### For Administrators
1. **Be Concise**: Keep titles under 50 characters
2. **Clear Messages**: Write clear, actionable messages
3. **Use Priority Wisely**: Reserve high priority for truly important items
4. **Target Appropriately**: Send to all users only when necessary
5. **Set Expiration**: Add end dates to time-sensitive announcements
6. **Pin Important**: Pin only the most critical announcements

### For Developers
1. **Load Early**: Call `NotificationHistory.load_user_notifications()` on app start
2. **Refresh Periodically**: Consider implementing periodic refresh for long sessions
3. **Handle Errors**: Wrap database calls in try-catch blocks
4. **Optimize Queries**: Use pagination for large notification sets
5. **Test Thoroughly**: Test with multiple users and announcement types

## Configuration

### Notification Limits
- Maximum notifications per user: 50 (older ones auto-deleted)
- Default query limit: 20 notifications
- Notification history retention: No automatic deletion

### Announcement Settings
- No automatic expiration (manual end date required)
- Pinned announcements show at top
- Inactive announcements hidden from users

## Future Enhancements

### Planned Features
1. **Push Notifications**: Desktop/mobile push notifications
2. **Scheduled Announcements**: Set future send times
3. **User Groups**: Target specific user groups
4. **Rich Text**: Support markdown or HTML in messages
5. **Attachments**: Add files or links to announcements
6. **Analytics Dashboard**: Detailed read/engagement metrics
7. **Email Integration**: Send email copies of urgent announcements
8. **Bulk Actions**: Mark multiple announcements active/inactive
9. **Templates**: Save announcement templates for reuse
10. **User Preferences**: Allow users to filter notification types

## Troubleshooting

### Notifications Not Appearing
1. Check if `init_admin_config_tables()` has been called
2. Verify user_id is correct
3. Check if announcement is active (`is_active = 1`)
4. Ensure target_users includes the user

### Read Status Not Updating
1. Verify notification ID is valid
2. Check database write permissions
3. Ensure `mark_notification_read()` is called with correct ID

### Announcement Creation Fails
1. Verify admin_id exists in admins table
2. Check all required fields are provided
3. Validate target_users format (comma-separated IDs)
4. Check database connection

## Technical Details

### Performance Considerations
- Announcements query uses LEFT JOIN for admin details
- Notification counts calculated with subqueries
- Indexes recommended on:
  - `user_notifications.user_id`
  - `user_notifications.is_read`
  - `announcements.is_active`
  - `announcements.created_at`

### Security
- Admin authentication required for announcement creation
- User can only see their own notifications
- SQL injection prevented via parameterized queries
- XSS protection in message display

### Data Integrity
- Foreign key constraints ensure referential integrity
- Cascade delete: Deleting announcement deletes related notifications
- Timestamps automatically updated on changes

## Migration Guide

### Updating from Previous Versions
1. Run `db.init_admin_config_tables()` to create new tables
2. No data migration needed (new feature)
3. Update UI imports to include `NotificationHistory`
4. Call `load_user_notifications(user_id)` in app initialization

### Testing Checklist
- [ ] Create announcement with all user types (info, warning, success, urgent)
- [ ] Test with "all users" target
- [ ] Test with specific user IDs
- [ ] Verify notification appears in user's notification center
- [ ] Confirm read status updates
- [ ] Test pinned announcements
- [ ] Verify high priority badge displays
- [ ] Test announcement editing
- [ ] Test announcement deletion
- [ ] Check notification count badge
- [ ] Test mark all as read
- [ ] Verify statistics accuracy

## Support

For questions or issues related to the announcement system:
1. Check database tables exist: `announcements`, `user_notifications`
2. Verify admin has proper permissions
3. Check application logs for errors
4. Review this documentation for proper API usage

---

**Version**: 1.0  
**Last Updated**: December 9, 2025  
**Status**: Production Ready ✅
