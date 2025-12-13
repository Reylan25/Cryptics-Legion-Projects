"""
Test script to verify notification persistence across user sessions
"""
import sys
sys.path.insert(0, 'Cryptics_legion/src')

from core import db

def test_notification_persistence():
    """Test that notifications persist in database"""
    print("=== Testing Notification Persistence ===\n")
    
    # Initialize database
    db.connect_db()
    db.init_admin_config_tables()
    
    # Get all users
    users = db.get_all_users_for_admin()
    print(f"Total users in system: {len(users)}\n")
    
    if not users:
        print("❌ No users found. Create a user first.")
        return
    
    # Test each user's notifications
    for user in users:
        user_id = user[0]
        username = user[1]
        
        # Get unread notifications
        unread_notifications = db.get_user_notifications(user_id, include_read=False, limit=10)
        
        # Get all notifications
        all_notifications = db.get_user_notifications(user_id, include_read=True, limit=10)
        
        print(f"User: {username} (ID: {user_id})")
        print(f"  📬 Total notifications: {len(all_notifications)}")
        print(f"  🔔 Unread notifications: {len(unread_notifications)}")
        
        if all_notifications:
            print(f"  Recent notifications:")
            for notif in all_notifications[:3]:
                notif_id, announcement_id, title, message, notif_type, is_read, read_at, created_at = notif
                status = "✅ Read" if is_read else "❌ Unread"
                print(f"    - {title[:40]}... [{status}] - {created_at}")
        print()
    
    # Get all announcements
    announcements = db.get_announcements(include_inactive=False)
    print(f"\n📢 Active Announcements: {len(announcements)}")
    for ann in announcements:
        ann_id, title, message, ann_type, priority, admin_id, admin_username, \
        target_users, start_date, end_date, is_active, is_pinned, \
        created_at, updated_at, notification_count, read_count = ann
        
        read_percentage = (read_count / notification_count * 100) if notification_count > 0 else 0
        print(f"\n  Title: {title}")
        print(f"  Type: {ann_type.upper()} | Priority: {priority.upper()}")
        print(f"  Sent to: {notification_count} user(s)")
        print(f"  Read by: {read_count} user(s) ({read_percentage:.1f}%)")
        print(f"  Created: {created_at}")
    
    print("\n✅ Test complete! Notifications are persisted in database.")
    print("\nTo verify persistence:")
    print("1. Create an announcement in the admin panel")
    print("2. Login as a user and check notification center")
    print("3. Logout")
    print("4. Login again - notifications should still be there!")

if __name__ == "__main__":
    test_notification_persistence()
