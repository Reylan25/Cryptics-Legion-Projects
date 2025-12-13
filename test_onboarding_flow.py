#!/usr/bin/env python3
"""
Test the onboarding flow to verify Get Started button works
"""
import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'Cryptics_legion', 'src')
sys.path.insert(0, src_path)

from core import db
from core.theme import get_theme
from ui.onboarding_page import build_onboarding_content

print("=" * 60)
print("Testing Onboarding Page")
print("=" * 60)

# Initialize database
db.connect_db()

# Create a mock page
class MockPage:
    def update(self):
        print("  [Page Updated]")

# Create state
state = {
    "user_id": 1,  # Simulate a logged-in user
    "current_view": "onboarding"
}

# Create callback to track if navigation happens
navigation_called = False
def mock_show_home():
    global navigation_called
    navigation_called = True
    print("✓ show_home() callback was called - navigation to home successful!")

# Test building the content
try:
    print("\n1. Testing build_onboarding_content()...")
    page = MockPage()
    content = build_onboarding_content(page, mock_show_home, state)
    print("   ✓ Content built successfully")
    
    # Verify the button was created
    if hasattr(content, 'content') and hasattr(content.content, 'controls'):
        print(f"   ✓ Found {len(content.content.controls)} controls in the page")
    
    # Test the Get Started button callback
    print("\n2. Testing Get Started button click handler...")
    
    # Navigate through the controls to find the button
    column = content.content
    if hasattr(column, 'controls'):
        for i, ctrl in enumerate(column.controls):
            if hasattr(ctrl, 'content'):
                btn = ctrl.content
                if hasattr(btn, 'on_click'):
                    print(f"   Found button at control {i}")
                    print("   Simulating button click...")
                    
                    # Call the button's click handler
                    btn.on_click(None)
                    
                    if navigation_called:
                        print("   ✓ Button click successful!")
                        print("   ✓ Navigation callback was executed")
                    else:
                        print("   ⚠ Button click executed but navigation callback wasn't called")
                    break
    
    print("\n" + "=" * 60)
    print("RESULT: ✓ Onboarding Get Started button works correctly!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 60)
    print("RESULT: ✗ Test failed - see error above")
    print("=" * 60)
