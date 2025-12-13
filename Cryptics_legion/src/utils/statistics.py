import flet as ft
import sqlite3
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict

# Add the parent directory to the path to import from core
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core.db import connect_db, select_expenses_by_user

# Category colors for charts
CATEGORY_COLORS = {
    "food": "#F59E0B",
    "dining": "#F59E0B",
    "transport": "#3B82F6",
    "shopping": "#EC4899",
    "entertainment": "#8B5CF6",
    "bills": "#6366F1",
    "utilities": "#06B6D4",
    "health": "#EF4444",
    "education": "#10B981",
    "electronics": "#14B8A6",
    "groceries": "#22C55E",
    "travel": "#F97316",
    "subscription": "#A855F7",
    "rent": "#7C3AED",
    "fitness": "#DC2626",
    "salary": "#10B981",
    "income": "#059669",
    "other": "#6B7280",
}

DEFAULT_COLORS = [
    "#3B82F6", "#EF4444", "#10B981", "#F59E0B", "#8B5CF6",
    "#EC4899", "#06B6D4", "#F97316", "#6366F1", "#14B8A6",
]


def get_category_color(category: str) -> str:
    """Get color for a category."""
    cat_lower = category.lower()
    for key, color in CATEGORY_COLORS.items():
        if key in cat_lower:
            return color
    # Return a default color based on hash
    return DEFAULT_COLORS[hash(category) % len(DEFAULT_COLORS)]


def get_expense_summary(user_id: int = None):
    """Get expense summary grouped by category."""
    conn = connect_db()
    cursor = conn.cursor()

    if user_id:
        cursor.execute("""
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE user_id = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT category, SUM(amount) 
            FROM expenses 
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expense_summary_by_period(user_id: int, period: str = "1W"):
    """Get expense summary for a specific time period.
    
    Args:
        user_id: The user ID
        period: Time period - "1D", "1W", "1M", "3M", "6M", "1Y", "ALL"
    
    Returns:
        List of (category, total_amount) tuples
    """
    today = datetime.now()
    
    period_map = {
        "1D": timedelta(days=1),
        "1W": timedelta(weeks=1),
        "1M": timedelta(days=30),
        "3M": timedelta(days=90),
        "6M": timedelta(days=180),
        "1Y": timedelta(days=365),
    }
    
    conn = connect_db()
    cursor = conn.cursor()
    
    if period == "ALL":
        cursor.execute("""
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE user_id = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """, (user_id,))
    else:
        start_date = today - period_map.get(period, timedelta(weeks=1))
        cursor.execute("""
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE user_id = ? AND date >= ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """, (user_id, start_date.strftime("%Y-%m-%d")))
    
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_daily_expenses(user_id: int, days: int = 7):
    """Get daily expense totals for the last N days.
    
    Returns:
        List of (date_str, total_amount) tuples
    """
    today = datetime.now()
    start_date = today - timedelta(days=days)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, SUM(amount) 
        FROM expenses 
        WHERE user_id = ? AND date >= ?
        GROUP BY date
        ORDER BY date ASC
    """, (user_id, start_date.strftime("%Y-%m-%d")))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Fill in missing days with 0
    daily_data = {row[0]: row[1] for row in rows}
    result = []
    for i in range(days + 1):
        date = start_date + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        result.append((date_str, daily_data.get(date_str, 0)))
    
    return result


def get_weekly_expenses(user_id: int, weeks: int = 4):
    """Get weekly expense totals for the last N weeks.
    
    Returns:
        List of (week_start_date, total_amount) tuples
    """
    today = datetime.now()
    expenses = select_expenses_by_user(user_id)
    
    weekly_totals = defaultdict(float)
    for exp in expenses:
        try:
            exp_date = datetime.strptime(exp[5], "%Y-%m-%d")
            # Get the start of the week (Monday)
            week_start = exp_date - timedelta(days=exp_date.weekday())
            week_key = week_start.strftime("%Y-%m-%d")
            
            # Only include weeks within range
            weeks_ago = (today - week_start).days // 7
            if weeks_ago <= weeks:
                weekly_totals[week_key] += exp[2]
        except:
            pass
    
    # Sort by date
    result = sorted(weekly_totals.items(), key=lambda x: x[0])
    return result[-weeks:] if len(result) > weeks else result


def get_monthly_expenses(user_id: int, months: int = 6):
    """Get monthly expense totals for the last N months.
    
    Returns:
        List of (month_str, total_amount) tuples
    """
    today = datetime.now()
    expenses = select_expenses_by_user(user_id)
    
    monthly_totals = defaultdict(float)
    for exp in expenses:
        try:
            exp_date = datetime.strptime(exp[5], "%Y-%m-%d")
            month_key = exp_date.strftime("%Y-%m")
            
            # Calculate months difference
            months_diff = (today.year - exp_date.year) * 12 + (today.month - exp_date.month)
            if months_diff <= months:
                monthly_totals[month_key] += exp[2]
        except:
            pass
    
    # Sort by date
    result = sorted(monthly_totals.items(), key=lambda x: x[0])
    return result[-months:] if len(result) > months else result


def get_spending_trend(user_id: int, period: str = "1W"):
    """Calculate spending trend compared to previous period.
    
    Returns:
        dict with 'current', 'previous', 'change_percent', 'trend' (up/down/same)
    """
    today = datetime.now()
    
    period_map = {
        "1D": timedelta(days=1),
        "1W": timedelta(weeks=1),
        "1M": timedelta(days=30),
        "3M": timedelta(days=90),
        "1Y": timedelta(days=365),
    }
    
    delta = period_map.get(period, timedelta(weeks=1))
    
    current_start = today - delta
    previous_start = current_start - delta
    
    expenses = select_expenses_by_user(user_id)
    
    current_total = 0
    previous_total = 0
    
    for exp in expenses:
        try:
            exp_date = datetime.strptime(exp[5], "%Y-%m-%d")
            amount = exp[2]
            
            if exp_date >= current_start:
                current_total += amount
            elif exp_date >= previous_start:
                previous_total += amount
        except:
            pass
    
    if previous_total > 0:
        change_percent = ((current_total - previous_total) / previous_total) * 100
    elif current_total > 0:
        change_percent = 100
    else:
        change_percent = 0
    
    if change_percent > 5:
        trend = "up"
    elif change_percent < -5:
        trend = "down"
    else:
        trend = "same"
    
    return {
        "current": current_total,
        "previous": previous_total,
        "change_percent": round(change_percent, 1),
        "trend": trend,
    }


def get_top_spending_categories(user_id: int, limit: int = 5, period: str = "1M"):
    """Get top spending categories for a period.
    
    Returns:
        List of dicts with 'category', 'amount', 'percentage', 'color'
    """
    summary = get_expense_summary_by_period(user_id, period)
    total = sum(row[1] for row in summary)
    
    result = []
    for i, (category, amount) in enumerate(summary[:limit]):
        percentage = (amount / total * 100) if total > 0 else 0
        result.append({
            "category": category,
            "amount": amount,
            "percentage": round(percentage, 1),
            "color": get_category_color(category),
        })
    
    return result


def get_average_daily_spending(user_id: int, days: int = 30):
    """Calculate average daily spending over a period."""
    daily = get_daily_expenses(user_id, days)
    if not daily:
        return 0
    
    total = sum(d[1] for d in daily)
    return total / len(daily)


def get_expense_count_by_category(user_id: int, period: str = "1M"):
    """Get count of expenses per category.
    
    Returns:
        List of (category, count) tuples
    """
    today = datetime.now()
    period_map = {
        "1D": timedelta(days=1),
        "1W": timedelta(weeks=1),
        "1M": timedelta(days=30),
        "3M": timedelta(days=90),
        "1Y": timedelta(days=365),
    }
    
    start_date = today - period_map.get(period, timedelta(days=30))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, COUNT(*) 
        FROM expenses 
        WHERE user_id = ? AND date >= ?
        GROUP BY category
        ORDER BY COUNT(*) DESC
    """, (user_id, start_date.strftime("%Y-%m-%d")))
    
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_highest_expense(user_id: int, period: str = "1M"):
    """Get the highest single expense in a period.
    
    Returns:
        tuple (id, amount, category, description, date) or None
    """
    today = datetime.now()
    period_map = {
        "1D": timedelta(days=1),
        "1W": timedelta(weeks=1),
        "1M": timedelta(days=30),
        "3M": timedelta(days=90),
        "1Y": timedelta(days=365),
    }
    
    start_date = today - period_map.get(period, timedelta(days=30))
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, amount, category, description, date 
        FROM expenses 
        WHERE user_id = ? AND date >= ?
        ORDER BY amount DESC
        LIMIT 1
    """, (user_id, start_date.strftime("%Y-%m-%d")))
    
    row = cursor.fetchone()
    conn.close()
    return row


def create_pie_chart_data(user_id: int, period: str = "1M"):
    """Create pie chart sections with colors for category breakdown.
    
    Returns:
        List of ft.PieChartSection objects
    """
    summary = get_expense_summary_by_period(user_id, period)
    total = sum(row[1] for row in summary)
    
    sections = []
    for i, (category, amount) in enumerate(summary):
        percentage = (amount / total * 100) if total > 0 else 0
        color = get_category_color(category)
        
        sections.append(
            ft.PieChartSection(
                value=float(amount),
                title=f"{category}\n{percentage:.1f}%",
                title_style=ft.TextStyle(
                    size=10,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                color=color,
                radius=100 if percentage >= 20 else 90,
            )
        )
    
    return sections


def create_bar_chart_data(user_id: int, chart_type: str = "weekly"):
    """Create bar chart data for spending visualization.
    
    Args:
        user_id: User ID
        chart_type: "daily", "weekly", or "monthly"
    
    Returns:
        List of ft.BarChartGroup objects
    """
    if chart_type == "daily":
        data = get_daily_expenses(user_id, 7)
        labels = [datetime.strptime(d[0], "%Y-%m-%d").strftime("%a") for d in data]
        values = [d[1] for d in data]
    elif chart_type == "weekly":
        data = get_weekly_expenses(user_id, 4)
        labels = [f"W{i+1}" for i in range(len(data))]
        values = [d[1] for d in data]
    else:  # monthly
        data = get_monthly_expenses(user_id, 6)
        labels = [datetime.strptime(d[0] + "-01", "%Y-%m-%d").strftime("%b") for d in data]
        values = [d[1] for d in data]
    
    max_val = max(values) if values else 1
    
    groups = []
    for i, (label, value) in enumerate(zip(labels, values)):
        groups.append(
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=value,
                        width=24,
                        color="#3B82F6",
                        tooltip=f"{label}: ₱{value:,.2f}",
                        border_radius=ft.border_radius.only(top_left=4, top_right=4),
                    ),
                ],
            )
        )
    
    return groups, labels, max_val


def get_statistics_summary(user_id: int, period: str = "1M"):
    """Get a comprehensive statistics summary.
    
    Returns:
        dict with all key statistics
    """
    summary = get_expense_summary_by_period(user_id, period)
    total = sum(row[1] for row in summary)
    trend = get_spending_trend(user_id, period)
    top_categories = get_top_spending_categories(user_id, 5, period)
    highest = get_highest_expense(user_id, period)
    avg_daily = get_average_daily_spending(user_id, 30)
    expense_count = get_expense_count_by_category(user_id, period)
    
    return {
        "total_spent": total,
        "category_count": len(summary),
        "transaction_count": sum(c[1] for c in expense_count),
        "trend": trend,
        "top_categories": top_categories,
        "highest_expense": highest,
        "average_daily": avg_daily,
        "categories": summary,
    }


def create_charts_view(page: ft.Page, user_id: int = None):
    """Returns a full chart view with category totals."""
    from core.theme import get_theme
    theme = get_theme()

    data_rows = get_expense_summary(user_id)
    total = sum(row[1] for row in data_rows)
    
    chart_data = []
    for i, row in enumerate(data_rows):
        category, amount = row
        percentage = (amount / total * 100) if total > 0 else 0
        color = get_category_color(category)
        
        chart_data.append(
            ft.PieChartSection(
                value=float(amount),
                title=f"{percentage:.1f}%",
                title_style=ft.TextStyle(
                    size=12,
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                color=color,
                radius=100,
            )
        )

    # Create legend
    legend_items = []
    for row in data_rows[:6]:  # Limit to 6 items
        category, amount = row
        color = get_category_color(category)
        legend_items.append(
            ft.Row(
                controls=[
                    ft.Container(
                        width=12,
                        height=12,
                        border_radius=2,
                        bgcolor=color,
                    ),
                    ft.Text(category, size=12, color=theme.text_primary),
                    ft.Text(f"₱{amount:,.2f}", size=12, color=theme.text_secondary),
                ],
                spacing=8,
            )
        )

    return ft.View(
        route="/charts",
        padding=20,
        bgcolor=theme.bg_primary,
        controls=[
            ft.Text(
                "Expense Breakdown",
                size=28,
                color=theme.text_primary,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "Overview of total spending per category",
                size=14,
                color=theme.text_secondary,
            ),

            ft.Container(height=20),

            ft.Container(
                content=ft.PieChart(
                    sections=chart_data,
                    center_space_radius=50,
                    sections_space=2,
                ),
                height=250,
                alignment=ft.alignment.center,
            ),

            ft.Container(height=20),
            
            ft.Container(
                content=ft.Column(
                    controls=legend_items,
                    spacing=8,
                ),
                padding=16,
                border_radius=12,
                bgcolor=theme.bg_card,
            ),

            ft.Container(height=30),

            ft.ElevatedButton(
                "Back to Home",
                bgcolor=theme.accent_primary,
                color="white",
                height=48,
                width=200,
                on_click=lambda e: page.go("/home")
            ),
        ],
    )
