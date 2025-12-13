import flet as ft
import sqlite3
import os
import sys

# Add the parent directory to the path to import from core
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core.db import connect_db

def get_expense_summary():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) 
        FROM expenses 
        GROUP BY category
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def create_charts_view(page: ft.Page):
    """ Returns a full chart view with category totals """

    data_rows = get_expense_summary()
    chart_data = [
        ft.PieChartSection(
            value=float(row[1]),
            title=row[0],
        ) for row in data_rows
    ]

    return ft.View(
        route="/charts",
        padding=20,
        bgcolor="#0c0c0f",
        controls=[
            ft.Text(
                "Expense Breakdown",
                size=32,
                color="white",
                weight=ft.FontWeight.BOLD,
            ),

            ft.Text(
                "Overview of total spending per category",
                size=16,
                color="white70",
            ),

            ft.Container(height=20),

            ft.PieChart(
                sections=chart_data,
                expand=True,
                center_space_radius=40,
                sections_space=2,
            ),

            ft.Container(height=30),

            ft.ElevatedButton(
                "Back to Home",
                bgcolor="#ffaa33",
                color="black",
                height=48,
                width=200,
                on_click=lambda e: page.go("/home")
            ),
        ]
    )
