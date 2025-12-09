#!/usr/bin/env python3
"""Test the onboarding Get Started button"""
import sys
sys.path.insert(0, 'Cryptics_legion/src')

from core import db
from ui.onboarding_page import build_onboarding_content
import flet as ft

# Connect to database
db.connect_db()

# Create a mock page and state
class MockPage:
    def update(self):
        pass

page = MockPage()
state = {
    "user_id": 1,
    "current_view": "onboarding"
}

# Mock callbacks
def mock_show_home():
    print("✓ Successfully called show_home()")

# Build the onboarding content
try:
    print("Building onboarding content...")
    content = build_onboarding_content(page, mock_show_home, state)
    print("✓ Onboarding content built successfully")
    
    # Find the Get Started button and simulate a click
    print("\nSimulating Get Started button click...")
    
    # The button is nested in containers, so we need to navigate to it
    # content -> Column -> [elements] -> Container with ElevatedButton
    if hasattr(content, 'content'):
        column = content.content
        if hasattr(column, 'controls'):
            for ctrl in column.controls:
                if hasattr(ctrl, 'content'):
                    # Check if this is the button container
                    inner = ctrl.content
                    if hasattr(inner, 'on_click'):
                        print("✓ Found Get Started button")
                        # Simulate click
                        print("  Calling button on_click handler...")
                        inner.on_click(None)
                        print("✓ Button click handler executed successfully!")
                        break
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
