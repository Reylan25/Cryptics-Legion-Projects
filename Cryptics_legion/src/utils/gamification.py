# src/utils/gamification.py
"""
Gamification Engine — Streaks, Badges, XP/Levels, Weekly Challenges.
Drives user engagement through psychology-backed reward mechanics.
"""

from datetime import datetime, timedelta
from core import db

# ── Level Definitions ──
LEVELS = {
    1:  {"title": "Beginner",        "xp": 0,     "icon": "🌱"},
    2:  {"title": "Tracker",         "xp": 100,   "icon": "📝"},
    3:  {"title": "Budgeter",        "xp": 300,   "icon": "📊"},
    4:  {"title": "Saver",           "xp": 600,   "icon": "💰"},
    5:  {"title": "Finance Pro",     "xp": 1000,  "icon": "⭐"},
    6:  {"title": "Money Master",    "xp": 1500,  "icon": "🏅"},
    7:  {"title": "Budget Guru",     "xp": 2500,  "icon": "🔥"},
    8:  {"title": "Wealth Builder",  "xp": 4000,  "icon": "🏆"},
    9:  {"title": "Finance Legend",  "xp": 6000,  "icon": "👑"},
    10: {"title": "Diamond Member",  "xp": 10000, "icon": "💎"},
}

# ── Badge Catalog ──
BADGES = {
    # Tracking badges
    "first_steps":      {"title": "First Steps",       "desc": "Log your first expense",              "icon": "👶", "category": "tracking"},
    "penny_counter":    {"title": "Penny Counter",     "desc": "Log 10 expenses",                     "icon": "🪙", "category": "tracking"},
    "expense_pro":      {"title": "Expense Pro",       "desc": "Log 50 expenses",                     "icon": "💼", "category": "tracking"},
    "data_machine":     {"title": "Data Machine",      "desc": "Log 200 expenses",                    "icon": "🤖", "category": "tracking"},
    "expense_legend":   {"title": "Expense Legend",    "desc": "Log 500 expenses",                    "icon": "🏆", "category": "tracking"},
    # Streak badges
    "week_warrior":     {"title": "Week Warrior",      "desc": "Maintain a 7-day streak",             "icon": "🔥", "category": "streak"},
    "fortnight_fighter":{"title": "Fortnight Fighter",  "desc": "Maintain a 14-day streak",            "icon": "⚡", "category": "streak"},
    "monthly_master":   {"title": "Monthly Master",    "desc": "Maintain a 30-day streak",            "icon": "💎", "category": "streak"},
    "legendary_tracker":{"title": "Legendary Tracker", "desc": "Maintain a 100-day streak",           "icon": "🌟", "category": "streak"},
    # Budget badges
    "budget_keeper":    {"title": "Budget Keeper",     "desc": "Stay under budget for a full week",   "icon": "🛡️", "category": "budget"},
    "savings_hero":     {"title": "Savings Hero",      "desc": "Save 30% of your budget in a month",  "icon": "💰", "category": "budget"},
    # Special badges
    "voice_commander":  {"title": "Voice Commander",   "desc": "Use voice assistant 10 times",        "icon": "🎤", "category": "special"},
    "night_owl":        {"title": "Night Owl",         "desc": "Log an expense after 11 PM",          "icon": "🦉", "category": "special"},
    "early_bird":       {"title": "Early Bird",        "desc": "Log an expense before 7 AM",          "icon": "🐦", "category": "special"},
    "category_king":    {"title": "Category King",     "desc": "Use all 13 expense categories",       "icon": "🎨", "category": "special"},
    "challenge_champ":  {"title": "Challenge Champ",   "desc": "Complete 5 weekly challenges",        "icon": "🎯", "category": "special"},
    # Level-up badges
    "level_5":          {"title": "Finance Pro",       "desc": "Reach Level 5",                       "icon": "⭐", "category": "level"},
    "level_10":         {"title": "Diamond Member",    "desc": "Reach Level 10",                      "icon": "💎", "category": "level"},
}

# ── Challenge Templates ──
CHALLENGE_TEMPLATES = [
    {"type": "daily_log", "desc": "Log at least 1 expense every day this week", "target": 7, "xp": 50},
    {"type": "total_expenses", "desc": "Log {target} expenses this week", "target": 10, "xp": 40},
    {"type": "voice_log", "desc": "Log 3 expenses using voice assistant", "target": 3, "xp": 30},
    {"type": "multi_category", "desc": "Track expenses in 4+ categories", "target": 4, "xp": 35},
    {"type": "under_budget", "desc": "Keep total spending under budget", "target": 1, "xp": 60},
]


# ═══════════════════════════════════════════════════
# STREAK MANAGER
# ═══════════════════════════════════════════════════

class StreakManager:
    """Manages daily login streaks."""

    @staticmethod
    def check_in(user_id: int) -> dict:
        """Call on login or expense log. Returns streak info + events."""
        streak = db.get_user_streak(user_id)
        today = datetime.now().strftime("%Y-%m-%d")
        last = streak["last_active"]
        events = []

        if last == today:
            # Already checked in today
            return {"streak": streak, "events": events}

        if last is None:
            # First ever check-in
            new_current = 1
            events.append("first_checkin")
        else:
            try:
                last_date = datetime.strptime(last, "%Y-%m-%d").date()
                today_date = datetime.now().date()
                diff = (today_date - last_date).days
            except (ValueError, TypeError):
                diff = 999

            if diff == 1:
                # Consecutive day!
                new_current = streak["current"] + 1
                events.append("streak_continued")
            elif diff == 2 and streak["freezes"] > 0:
                # Missed 1 day — use freeze
                new_current = streak["current"] + 1
                streak["freezes"] -= 1
                events.append("freeze_used")
            else:
                # Streak broken
                new_current = 1
                if streak["current"] > 0:
                    events.append("streak_broken")
                events.append("streak_restarted")
                # Reset freezes on Monday
                if datetime.now().weekday() == 0:
                    streak["freezes"] = 1

        new_longest = max(streak["longest"], new_current)
        new_total = streak["total_days"] + 1

        db.update_user_streak(user_id, new_current, new_longest, today, streak["freezes"], new_total)

        result_streak = {
            "current": new_current,
            "longest": new_longest,
            "last_active": today,
            "freezes": streak["freezes"],
            "total_days": new_total,
        }

        # Check streak milestones
        for threshold, badge_id in [(7, "week_warrior"), (14, "fortnight_fighter"), (30, "monthly_master"), (100, "legendary_tracker")]:
            if new_current >= threshold and not db.has_badge(user_id, badge_id):
                db.unlock_badge(user_id, badge_id)
                events.append(f"badge:{badge_id}")

        return {"streak": result_streak, "events": events}

    @staticmethod
    def get_streak_visual(current: int) -> dict:
        """Get visual representation of streak."""
        if current >= 100:
            return {"emoji": "👑🔥", "label": "LEGENDARY", "color": "#FFD700"}
        elif current >= 30:
            return {"emoji": "💎🔥", "label": "Diamond Streak", "color": "#60A5FA"}
        elif current >= 14:
            return {"emoji": "🔥🔥🔥", "label": "Blue Flame", "color": "#3B82F6"}
        elif current >= 7:
            return {"emoji": "🔥🔥", "label": "Hot Streak", "color": "#F97316"}
        elif current >= 1:
            return {"emoji": "🔥", "label": "Active", "color": "#EF4444"}
        return {"emoji": "❄️", "label": "No Streak", "color": "#6B7280"}


# ═══════════════════════════════════════════════════
# BADGE ENGINE
# ═══════════════════════════════════════════════════

class BadgeEngine:
    """Check and award badges based on user actions."""

    @staticmethod
    def check_all(user_id: int) -> list:
        """Check all badge conditions and unlock any newly earned. Returns list of newly unlocked badge_ids."""
        newly_unlocked = []

        # Get user stats
        expense_count = db.get_expense_count_by_user(user_id)
        streak = db.get_user_streak(user_id)
        categories_used = db.get_unique_categories_used(user_id)
        xp_data = db.get_user_xp(user_id)
        hour = datetime.now().hour

        # Tracking badges
        checks = [
            ("first_steps", expense_count >= 1),
            ("penny_counter", expense_count >= 10),
            ("expense_pro", expense_count >= 50),
            ("data_machine", expense_count >= 200),
            ("expense_legend", expense_count >= 500),
        ]

        # Streak badges
        checks += [
            ("week_warrior", streak["current"] >= 7),
            ("fortnight_fighter", streak["current"] >= 14),
            ("monthly_master", streak["current"] >= 30),
            ("legendary_tracker", streak["current"] >= 100),
        ]

        # Special badges
        checks += [
            ("category_king", categories_used >= 13),
            ("night_owl", hour >= 23 or hour < 4),
            ("early_bird", 4 <= hour < 7),
        ]

        # Level badges
        checks += [
            ("level_5", xp_data["level"] >= 5),
            ("level_10", xp_data["level"] >= 10),
        ]

        for badge_id, condition in checks:
            if condition and not db.has_badge(user_id, badge_id):
                if db.unlock_badge(user_id, badge_id):
                    newly_unlocked.append(badge_id)
                    # Award bonus XP for badge
                    db.add_user_xp(user_id, 25)

        return newly_unlocked

    @staticmethod
    def get_all_badges_status(user_id: int) -> list:
        """Get all badges with their unlock status."""
        unlocked = {b[0]: b[1] for b in db.get_user_badges(user_id)}
        result = []
        for bid, info in BADGES.items():
            result.append({
                "id": bid,
                "title": info["title"],
                "desc": info["desc"],
                "icon": info["icon"],
                "category": info["category"],
                "unlocked": bid in unlocked,
                "unlocked_at": unlocked.get(bid),
            })
        return result


# ═══════════════════════════════════════════════════
# XP ENGINE
# ═══════════════════════════════════════════════════

class XPEngine:
    """Award XP for user actions."""

    XP_VALUES = {
        "log_expense": 10,
        "voice_expense": 15,
        "daily_streak": 5,
        "complete_challenge": 50,
        "badge_unlocked": 25,
        "budget_check": 30,
        "daily_login": 5,
    }

    @staticmethod
    def award(user_id: int, action: str) -> dict:
        """Award XP for an action. Returns {xp, level, leveled_up}."""
        amount = XPEngine.XP_VALUES.get(action, 0)
        if amount <= 0:
            return db.get_user_xp(user_id)
        return db.add_user_xp(user_id, amount)

    @staticmethod
    def get_level_info(level: int) -> dict:
        """Get level title and icon."""
        return LEVELS.get(level, LEVELS[1])

    @staticmethod
    def get_progress(user_id: int) -> dict:
        """Get XP progress toward next level."""
        data = db.get_user_xp(user_id)
        current_level = data["level"]
        current_xp = data["xp"]

        level_info = LEVELS.get(current_level, LEVELS[1])
        next_level = min(current_level + 1, 10)
        next_info = LEVELS.get(next_level, LEVELS[10])

        xp_for_current = level_info["xp"]
        xp_for_next = next_info["xp"]

        if current_level >= 10:
            progress = 1.0
            xp_in_level = current_xp - xp_for_current
            xp_needed = 0
        else:
            xp_in_level = current_xp - xp_for_current
            xp_needed = xp_for_next - xp_for_current
            progress = min(xp_in_level / xp_needed, 1.0) if xp_needed > 0 else 1.0

        return {
            "level": current_level,
            "title": level_info["title"],
            "icon": level_info["icon"],
            "total_xp": current_xp,
            "xp_in_level": xp_in_level,
            "xp_needed": xp_needed,
            "progress": progress,
        }


# ═══════════════════════════════════════════════════
# CHALLENGE MANAGER
# ═══════════════════════════════════════════════════

class ChallengeManager:
    """Manage weekly challenges."""

    @staticmethod
    def ensure_challenges(user_id: int):
        """Create this week's challenges if they don't exist."""
        existing = db.get_active_challenges(user_id)
        if existing:
            return

        import random
        # Pick 2 random challenges for this week
        selected = random.sample(CHALLENGE_TEMPLATES, min(2, len(CHALLENGE_TEMPLATES)))
        for ch in selected:
            db.upsert_challenge(user_id, ch["type"], ch["target"], ch["xp"])

    @staticmethod
    def get_challenges_display(user_id: int) -> list:
        """Get formatted challenge data for UI display."""
        ChallengeManager.ensure_challenges(user_id)
        challenges = db.get_active_challenges(user_id)
        result = []
        for ch in challenges:
            cid, ctype, target, current, xp, completed = ch
            # Find template description
            desc = ctype
            for tpl in CHALLENGE_TEMPLATES:
                if tpl["type"] == ctype:
                    desc = tpl["desc"].replace("{target}", str(int(target)))
                    break
            progress = min(current / target, 1.0) if target > 0 else 0
            result.append({
                "id": cid,
                "type": ctype,
                "desc": desc,
                "target": target,
                "current": current,
                "progress": progress,
                "xp": xp,
                "completed": bool(completed),
            })
        return result

    @staticmethod
    def get_challenge_history_display(user_id: int) -> dict:
        """Get formatted challenge history data grouped by week."""
        challenges = db.get_all_challenges(user_id)
        history = {}
        for ch in challenges:
            cid, ctype, target, current, xp, completed, week_start = ch
            # Find template description
            desc = ctype
            for tpl in CHALLENGE_TEMPLATES:
                if tpl["type"] == ctype:
                    desc = tpl["desc"].replace("{target}", str(int(target)))
                    break
            progress = min(current / target, 1.0) if target > 0 else 0
            
            if week_start not in history:
                history[week_start] = []
                
            history[week_start].append({
                "id": cid,
                "type": ctype,
                "desc": desc,
                "target": target,
                "current": current,
                "progress": progress,
                "xp": xp,
                "completed": bool(completed),
                "week_start": week_start
            })
        return history

    @staticmethod
    def update_after_expense(user_id: int):
        """Update challenge progress after an expense is logged."""
        challenges = db.get_active_challenges(user_id)
        for ch in challenges:
            cid, ctype, target, current, xp, completed = ch
            if completed:
                continue

            new_val = current
            if ctype == "total_expenses":
                new_val = db.get_expense_count_by_user(user_id)
            elif ctype == "daily_log":
                new_val = db.get_today_expense_count(user_id)
            elif ctype == "multi_category":
                new_val = db.get_unique_categories_used(user_id)

            if new_val != current:
                db.update_challenge_progress(cid, new_val)

            if new_val >= target and not completed:
                db.complete_challenge(cid)
                db.add_user_xp(user_id, xp)


# ═══════════════════════════════════════════════════
# CONVENIENCE: Call after each expense
# ═══════════════════════════════════════════════════

def on_expense_logged(user_id: int, via_voice: bool = False) -> dict:
    """
    Call this after every expense is saved.
    Handles: XP award, streak check-in, badge checks, challenge updates.
    Returns summary of events for UI notifications.
    """
    events = {"xp_gained": 0, "new_badges": [], "leveled_up": False, "new_level": 0, "streak": 0}

    # Award XP
    action = "voice_expense" if via_voice else "log_expense"
    xp_result = XPEngine.award(user_id, action)
    events["xp_gained"] = XPEngine.XP_VALUES.get(action, 0)
    events["leveled_up"] = xp_result.get("leveled_up", False)
    events["new_level"] = xp_result.get("level", 1)

    # Update streak
    streak_result = StreakManager.check_in(user_id)
    events["streak"] = streak_result["streak"]["current"]

    # Check badges
    new_badges = BadgeEngine.check_all(user_id)
    events["new_badges"] = new_badges

    # Update challenges
    ChallengeManager.update_after_expense(user_id)

    return events


def on_user_login(user_id: int) -> dict:
    """Call on user login. Awards daily XP and checks streak."""
    events = {"xp_gained": 0, "streak": 0, "new_badges": []}

    # Daily login XP
    xp_result = XPEngine.award(user_id, "daily_login")
    events["xp_gained"] = XPEngine.XP_VALUES["daily_login"]

    # Streak check-in
    streak_result = StreakManager.check_in(user_id)
    events["streak"] = streak_result["streak"]["current"]
    events["streak_events"] = streak_result["events"]

    # Ensure challenges exist
    ChallengeManager.ensure_challenges(user_id)

    # Check badges
    new_badges = BadgeEngine.check_all(user_id)
    events["new_badges"] = new_badges

    return events
