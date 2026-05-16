# src/utils/reminders.py
"""
Reminder Engine — Background service that monitors user activity,
budget thresholds, and scheduled reminders to fire notifications.
"""

import threading
import time
from datetime import datetime, timedelta
from core import db
from utils.currency import get_currency_symbol


# Reminder type metadata
REMINDER_TYPES = {
    "daily_expense": {
        "title": "Daily Expense Log",
        "description": "Remind me to log expenses every day",
        "icon": "📝",
        "default_time": "20:00",
    },
    "budget_warning": {
        "title": "Budget Warning",
        "description": "Alert when account balance drops below threshold",
        "icon": "⚠️",
        "default_threshold": 20.0,
    },
    "weekly_summary": {
        "title": "Weekly Summary",
        "description": "Show spending recap every week",
        "icon": "📊",
        "default_time": "09:00",
    },
    "idle_reminder": {
        "title": "Idle Reminder",
        "description": "Remind if no expenses logged for X days",
        "icon": "💤",
        "default_days": 3,
    },
    "recurring_expense": {
        "title": "Recurring Expenses",
        "description": "Remind about upcoming recurring bills",
        "icon": "🔄",
    },
}


class ReminderEngine:
    """
    Background reminder engine that periodically checks conditions
    and fires notifications via the ImmersiveNotification system.
    """

    CHECK_INTERVAL = 300  # Check every 5 minutes (seconds)

    def __init__(self, page, user_id: int):
        self.page = page
        self.user_id = user_id
        self._running = False
        self._thread = None
        self._last_budget_check = {}
        self._last_daily_check = None
        self._last_weekly_check = None
        self._last_idle_check = None

    def start(self):
        """Start the reminder engine in background."""
        if self._running:
            return
        
        # Initialize default reminders if first time
        try:
            db.init_default_reminders(self.user_id)
        except Exception as e:
            print(f"[ReminderEngine] Init defaults note: {e}")
        
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        print(f"[ReminderEngine] Started for user {self.user_id}")

    def stop(self):
        """Stop the reminder engine."""
        self._running = False
        print(f"[ReminderEngine] Stopped for user {self.user_id}")

    def _run_loop(self):
        """Main loop that checks reminder conditions periodically."""
        # Wait a bit before first check (let app fully load)
        time.sleep(5)
        
        while self._running:
            try:
                self._check_all_reminders()
            except Exception as e:
                print(f"[ReminderEngine] Check error: {e}")
            
            # Sleep in small increments so we can stop quickly
            for _ in range(self.CHECK_INTERVAL):
                if not self._running:
                    break
                time.sleep(1)

    def _check_all_reminders(self):
        """Check all reminder conditions for the current user."""
        reminders = db.get_user_reminders(self.user_id)
        
        for reminder in reminders:
            rid, rtype, enabled, rtime, threshold, days_inactive, custom_msg, last_triggered, _ = reminder
            
            if not enabled:
                continue
            
            # Skip if recently triggered (within last hour for most types)
            if last_triggered:
                try:
                    last_dt = datetime.strptime(last_triggered, "%Y-%m-%d %H:%M:%S")
                    cooldown = timedelta(hours=12) if rtype != "budget_warning" else timedelta(hours=4)
                    if datetime.now() - last_dt < cooldown:
                        continue
                except (ValueError, TypeError):
                    pass
            
            if rtype == "daily_expense":
                self._check_daily_expense(rid, rtime)
            elif rtype == "budget_warning":
                self._check_budget_warning(rid, threshold)
            elif rtype == "weekly_summary":
                self._check_weekly_summary(rid, rtime)
            elif rtype == "idle_reminder":
                self._check_idle_reminder(rid, days_inactive)
            elif rtype == "recurring_expense":
                self._check_recurring_expenses(rid)

    def _fire_notification(self, title: str, message: str, notif_type: str = "info"):
        """Fire an in-app notification via overlay."""
        try:
            from components.notification import ImmersiveNotification
            notif = ImmersiveNotification(self.page)
            notif.show(message, notif_type, title=title, duration=6000)
        except Exception as e:
            print(f"[ReminderEngine] Notification error: {e}")

    def _check_daily_expense(self, rid: int, reminder_time: str):
        """Check if it's time for the daily expense logging reminder."""
        now = datetime.now()
        
        # Parse reminder time
        try:
            hour, minute = map(int, reminder_time.split(":"))
        except (ValueError, TypeError):
            hour, minute = 20, 0
        
        # Check if we're within the reminder window (±15 minutes)
        target_time = now.replace(hour=hour, minute=minute, second=0)
        diff_minutes = abs((now - target_time).total_seconds()) / 60
        
        if diff_minutes <= 15:
            # Check if user already logged expenses today
            today_count = db.get_today_expense_count(self.user_id)
            if today_count == 0:
                self._fire_notification(
                    "📝 Daily Expense Reminder",
                    "Don't forget to log your expenses today! Tap + to add one.",
                    "info"
                )
                db.update_reminder_last_triggered(rid)

    def _check_budget_warning(self, rid: int, threshold: float):
        """Check if any account balance is below threshold percentage."""
        accounts = db.get_accounts_by_user(self.user_id)
        
        for acc in accounts:
            acc_id = acc[0]
            acc_name = acc[1]
            balance = acc[4]
            currency = acc[5] if len(acc) > 5 else "PHP"
            symbol = get_currency_symbol(currency)
            
            # Calculate original budget
            total_expenses = db.total_expenses_by_account(self.user_id, acc_id)
            original_budget = balance + total_expenses
            
            if original_budget <= 0:
                continue
            
            remaining_pct = (balance / original_budget) * 100
            
            # Skip if already warned about this account recently
            cache_key = f"{acc_id}_{int(remaining_pct / 5) * 5}"  # Group by 5% bands
            if cache_key in self._last_budget_check:
                continue
            
            if remaining_pct <= 5:
                # Critical
                self._fire_notification(
                    "🚨 Critical Balance Alert",
                    f"{acc_name} has only {symbol}{balance:,.2f} left ({remaining_pct:.0f}% remaining). Consider adding funds!",
                    "error"
                )
                self._last_budget_check[cache_key] = True
                db.update_reminder_last_triggered(rid)
            elif remaining_pct <= threshold:
                # Warning
                self._fire_notification(
                    "⚠️ Low Balance Warning",
                    f"{acc_name} is at {remaining_pct:.0f}% ({symbol}{balance:,.2f} remaining). Watch your spending!",
                    "warning"
                )
                self._last_budget_check[cache_key] = True
                db.update_reminder_last_triggered(rid)

    def _check_weekly_summary(self, rid: int, reminder_time: str):
        """Show weekly summary on Sunday."""
        now = datetime.now()
        
        # Only on Sunday (weekday 6) OR Monday morning (weekday 0)
        if now.weekday() not in (6, 0):
            return
        
        try:
            hour, minute = map(int, reminder_time.split(":"))
        except (ValueError, TypeError):
            hour, minute = 9, 0
        
        target_time = now.replace(hour=hour, minute=minute, second=0)
        diff_minutes = abs((now - target_time).total_seconds()) / 60
        
        if diff_minutes <= 15:
            weekly_total = db.get_weekly_total(self.user_id)
            
            # Get user currency
            profile = db.get_user_profile(self.user_id)
            currency = profile.get("currency", "PHP") if profile else "PHP"
            symbol = get_currency_symbol(currency)
            
            self._fire_notification(
                "📊 Weekly Spending Summary",
                f"You spent {symbol}{weekly_total:,.2f} this week. Keep tracking to stay on budget!",
                "info"
            )
            db.update_reminder_last_triggered(rid)

    def _check_idle_reminder(self, rid: int, days_inactive: int):
        """Remind user if they haven't logged expenses recently."""
        last_expense = db.get_last_expense_date(self.user_id)
        
        if not last_expense:
            # No expenses ever — remind after 1 day
            days_inactive = 1
            self._fire_notification(
                "💤 No Expenses Yet",
                "Start tracking! Log your first expense to begin managing your money.",
                "info"
            )
            db.update_reminder_last_triggered(rid)
            return
        
        try:
            # Parse date — handle both "YYYY-MM-DD" and "YYYY-MM-DD HH:MM:SS"
            last_date_str = last_expense.split(" ")[0]
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
            days_since = (datetime.now() - last_date).days
            
            if days_since >= days_inactive:
                self._fire_notification(
                    "💤 Expense Tracking Reminder",
                    f"You haven't logged any expenses in {days_since} days. Don't forget to track your spending!",
                    "warning"
                )
                db.update_reminder_last_triggered(rid)
        except (ValueError, TypeError):
            pass

    def _check_recurring_expenses(self, rid: int):
        """Check for upcoming recurring expenses."""
        recurring = db.get_recurring_expenses(self.user_id)
        now = datetime.now()
        today_day = now.day
        
        for rec in recurring:
            rec_id, name, amount, category, due_day, frequency, enabled, last_reminded, _ = rec
            
            if not enabled:
                continue
            
            # Skip if already reminded today
            if last_reminded:
                try:
                    last_dt = datetime.strptime(last_reminded, "%Y-%m-%d %H:%M:%S")
                    if (now - last_dt).days < 1:
                        continue
                except (ValueError, TypeError):
                    pass
            
            # Check if due within 3 days
            days_until_due = due_day - today_day
            if days_until_due < 0:
                # Already past this month — check next month
                days_until_due += 30
            
            if 0 <= days_until_due <= 3:
                profile = db.get_user_profile(self.user_id)
                currency = profile.get("currency", "PHP") if profile else "PHP"
                symbol = get_currency_symbol(currency)
                
                if days_until_due == 0:
                    msg = f"{name} ({symbol}{amount:,.2f}) is due today!"
                elif days_until_due == 1:
                    msg = f"{name} ({symbol}{amount:,.2f}) is due tomorrow."
                else:
                    msg = f"{name} ({symbol}{amount:,.2f}) is due in {days_until_due} days."
                
                self._fire_notification(
                    "🔄 Recurring Expense Due",
                    msg,
                    "warning"
                )
                db.update_recurring_last_reminded(rec_id)
