# Admin System Testing Guide

## 🧪 Complete Test Plan

### Prerequisites
- Application is running: `flet run src/main.py`
- Database is initialized
- Default admin account created

---

## Test Suite 1: Admin Login

### Test 1.1: Admin Login Success ✅
**Steps:**
1. Open the app
2. Enter username: `ADMIN`
3. Enter password: `ADMIN256`
4. Click Login

**Expected Result:**
- ✅ Success message: "Welcome back, Administrator! System access granted"
- ✅ Redirected to Admin Dashboard
- ✅ Dashboard shows statistics

**Status:** [ ] Pass [ ] Fail

---

### Test 1.2: Admin Login Wrong Password ❌
**Steps:**
1. Enter username: `ADMIN`
2. Enter password: `wrongpassword`
3. Click Login

**Expected Result:**
- ✅ Error message: "Invalid username or password"
- ✅ Stay on login page

**Status:** [ ] Pass [ ] Fail

---

### Test 1.3: Case Sensitivity ✅
**Steps:**
1. Try username: `admin` (lowercase)
2. Password: `ADMIN256`
3. Click Login

**Expected Result:**
- ✅ Should NOT login (username is case-sensitive)
- ✅ Show error message

**Status:** [ ] Pass [ ] Fail

---

## Test Suite 2: Admin Dashboard

### Test 2.1: Dashboard Statistics Display ✅
**Steps:**
1. Login as admin
2. View dashboard

**Expected Result:**
- ✅ Shows Total Users count
- ✅ Shows Total Expenses count
- ✅ Shows Total Amount (in currency)
- ✅ Shows Active Users (30 days)
- ✅ Shows New Users This Month
- ✅ Shows Total Accounts
- ✅ All numbers are correct and non-negative

**Status:** [ ] Pass [ ] Fail

---

### Test 2.2: Recent Activity Display ✅
**Steps:**
1. On dashboard, scroll to Recent Activity

**Expected Result:**
- ✅ Shows at least 1 activity (admin login)
- ✅ Each activity has icon, action, timestamp
- ✅ Activities are sorted by newest first
- ✅ Shows "No recent activity" if empty

**Status:** [ ] Pass [ ] Fail

---

### Test 2.3: Quick Actions Navigation ✅
**Steps:**
1. Click "User Management" button

**Expected Result:**
- ✅ Navigates to User Management page

**Steps:**
2. Go back, click "Activity Logs" button

**Expected Result:**
- ✅ Navigates to Activity Logs page

**Status:** [ ] Pass [ ] Fail

---

### Test 2.4: Logout Function ✅
**Steps:**
1. Click logout icon in header
2. Check where you land

**Expected Result:**
- ✅ Logged out successfully
- ✅ Redirected to login page
- ✅ Cannot go back to admin pages

**Status:** [ ] Pass [ ] Fail

---

## Test Suite 3: User Management

### Test 3.1: View All Users ✅
**Steps:**
1. Navigate to User Management
2. View the user list

**Expected Result:**
- ✅ Shows all registered users
- ✅ Each user card shows:
  - Username
  - Email
  - Expense count
  - Total spent
  - Join date
- ✅ Delete button is visible

**Status:** [ ] Pass [ ] Fail

---

### Test 3.2: Search Functionality ✅
**Steps:**
1. Type a username in search bar
2. Observe results

**Expected Result:**
- ✅ List filters to matching users
- ✅ Updates in real-time as you type
- ✅ Shows "No users found" if no matches

**Steps:**
3. Clear search
4. Type an email address

**Expected Result:**
- ✅ Also searches by email

**Status:** [ ] Pass [ ] Fail

---

### Test 3.3: Summary Statistics ✅
**Steps:**
1. View the summary chips at top

**Expected Result:**
- ✅ Shows total user count
- ✅ Shows total expense count
- ✅ Shows total amount spent
- ✅ Numbers match individual user data

**Status:** [ ] Pass [ ] Fail

---

### Test 3.4: Delete User - Confirmation ✅
**Steps:**
1. Click delete icon on any user
2. View the confirmation dialog

**Expected Result:**
- ✅ Dialog appears with warning message
- ✅ Shows username being deleted
- ✅ Lists what will be deleted:
  - User account
  - All expenses
  - All accounts
  - All personal data
- ✅ Has Cancel and Delete buttons

**Status:** [ ] Pass [ ] Fail

---

### Test 3.5: Delete User - Cancel ✅
**Steps:**
1. Click delete on a user
2. Click "Cancel" in dialog

**Expected Result:**
- ✅ Dialog closes
- ✅ User is NOT deleted
- ✅ User still appears in list

**Status:** [ ] Pass [ ] Fail

---

### Test 3.6: Delete User - Confirm ✅
**Steps:**
1. Note the total user count
2. Click delete on a user
3. Click "Delete" in confirmation

**Expected Result:**
- ✅ Success message appears
- ✅ User removed from list
- ✅ Total user count decreased by 1
- ✅ User's expenses deleted
- ✅ User's data completely removed

**Verification:**
1. Go to Activity Logs
2. Check for delete activity

**Expected:**
- ✅ "Deleted user '[username]'" logged

**Status:** [ ] Pass [ ] Fail

---

### Test 3.7: Back Navigation ✅
**Steps:**
1. Click back arrow in header

**Expected Result:**
- ✅ Returns to Admin Dashboard

**Status:** [ ] Pass [ ] Fail

---

## Test Suite 4: Activity Logs

### Test 4.1: View Activity Logs ✅
**Steps:**
1. Navigate to Activity Logs
2. View the timeline

**Expected Result:**
- ✅ Shows admin activities
- ✅ Each log has:
  - Icon (color-coded)
  - Action description
  - Admin username
  - Date and time
  - Details
- ✅ Sorted newest first

**Status:** [ ] Pass [ ] Fail

---

### Test 4.2: Activity Types ✅
**Steps:**
1. Perform various actions:
   - Login
   - View users
   - Delete a user
   - View logs
   - Logout
   - Login again
2. Check Activity Logs

**Expected Result:**
- ✅ All actions are logged
- ✅ Each has appropriate icon:
  - 🟢 Login (green)
  - 🔴 Delete (red)
  - 🟣 View (purple)
  - 🟠 Logs (orange)
  - 🔵 Logout (blue)

**Status:** [ ] Pass [ ] Fail

---

### Test 4.3: Refresh Functionality ✅
**Steps:**
1. Note the log count
2. Perform an action (e.g., go to users)
3. Return to logs
4. Click refresh button

**Expected Result:**
- ✅ Logs reload
- ✅ New activity appears
- ✅ Success message shown

**Status:** [ ] Pass [ ] Fail

---

### Test 4.4: Summary Statistics ✅
**Steps:**
1. View summary section

**Expected Result:**
- ✅ Shows total activities count
- ✅ Shows unique admins count

**Status:** [ ] Pass [ ] Fail

---

### Test 4.5: Target User Tracking ✅
**Steps:**
1. Delete a user
2. Check activity logs

**Expected Result:**
- ✅ Delete log shows target username
- ✅ Format: "Delete User - Target: [username]"

**Status:** [ ] Pass [ ] Fail

---

## Test Suite 5: Regular User Login

### Test 5.1: Regular User Not Affected ✅
**Steps:**
1. Logout from admin
2. Create/login with regular user account
3. Navigate through app

**Expected Result:**
- ✅ Regular user flow unchanged
- ✅ Goes to Home page (not admin dashboard)
- ✅ No access to admin features
- ✅ Can use all regular features

**Status:** [ ] Pass [ ] Fail

---

### Test 5.2: Admin Cannot Access User Features ✅
**Steps:**
1. Login as admin
2. Try to access regular user pages

**Expected Result:**
- ✅ Admin stays in admin area
- ✅ Cannot access home/expenses/etc

**Status:** [ ] Pass [ ] Fail

---

## Test Suite 6: Data Integrity

### Test 6.1: Database Persistence ✅
**Steps:**
1. Login as admin
2. Note statistics
3. Close app
4. Restart app
5. Login as admin again

**Expected Result:**
- ✅ Statistics unchanged
- ✅ Activity logs preserved
- ✅ User data intact

**Status:** [ ] Pass [ ] Fail

---

### Test 6.2: Activity Logging Complete ✅
**Steps:**
1. Perform 10 different actions
2. Check activity logs

**Expected Result:**
- ✅ All 10 actions logged
- ✅ Correct timestamps
- ✅ Correct details

**Status:** [ ] Pass [ ] Fail

---

### Test 6.3: Statistics Accuracy ✅
**Steps:**
1. Login as admin, note user count
2. Create a new regular user account
3. Logout, login as admin again
4. Check statistics

**Expected Result:**
- ✅ User count increased by 1
- ✅ New users this month increased by 1

**Status:** [ ] Pass [ ] Fail

---

## Test Suite 7: UI/UX Testing

### Test 7.1: Responsive Design ✅
**Steps:**
1. Resize window to different sizes:
   - Small (mobile)
   - Medium (tablet)
   - Large (desktop)

**Expected Result:**
- ✅ UI adapts to all sizes
- ✅ All elements remain accessible
- ✅ No layout breaks

**Status:** [ ] Pass [ ] Fail

---

### Test 7.2: Visual Consistency ✅
**Steps:**
1. Navigate through all admin pages

**Expected Result:**
- ✅ Consistent color scheme
- ✅ Same header style
- ✅ Matching buttons
- ✅ Coherent design language

**Status:** [ ] Pass [ ] Fail

---

### Test 7.3: Loading States ✅
**Steps:**
1. Click various buttons
2. Observe button states

**Expected Result:**
- ✅ Buttons show hover effects
- ✅ Clear visual feedback
- ✅ No UI freezing

**Status:** [ ] Pass [ ] Fail

---

### Test 7.4: Error Messages ✅
**Steps:**
1. Trigger errors (wrong password, etc.)

**Expected Result:**
- ✅ Clear error messages
- ✅ Red color for errors
- ✅ User-friendly text

**Status:** [ ] Pass [ ] Fail

---

## Test Suite 8: Security Testing

### Test 8.1: Password Encryption ✅
**Steps:**
1. Check database directly
2. Query: `SELECT password FROM admins WHERE username='ADMIN'`

**Expected Result:**
- ✅ Password is BLOB (encrypted)
- ✅ Not plain text
- ✅ Not easily reversible

**Status:** [ ] Pass [ ] Fail

---

### Test 8.2: Confirmation Required ✅
**Steps:**
1. Try to delete user

**Expected Result:**
- ✅ Confirmation dialog appears
- ✅ Cannot delete without confirming

**Status:** [ ] Pass [ ] Fail

---

### Test 8.3: Session Handling ✅
**Steps:**
1. Login as admin
2. Close app (force close)
3. Restart app

**Expected Result:**
- ✅ Logged out automatically
- ✅ Must login again

**Status:** [ ] Pass [ ] Fail

---

## Test Results Summary

### Overall Statistics:
- Total Tests: ___
- Passed: ___
- Failed: ___
- Pass Rate: ___%

### Critical Issues Found:
1. _________________________________
2. _________________________________
3. _________________________________

### Minor Issues Found:
1. _________________________________
2. _________________________________
3. _________________________________

### Notes:
_________________________________
_________________________________
_________________________________

---

## Performance Checklist

- [ ] Dashboard loads in < 2 seconds
- [ ] User list loads in < 3 seconds
- [ ] Search responds instantly
- [ ] Delete completes in < 2 seconds
- [ ] Activity logs load in < 2 seconds
- [ ] Navigation is smooth
- [ ] No UI lag or freezing

---

## Browser/Platform Testing

### Desktop:
- [ ] Windows
- [ ] macOS
- [ ] Linux

### Mobile:
- [ ] Android
- [ ] iOS

### Browsers (if web):
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari

---

## Final Approval

**Tested By:** ________________
**Date:** ________________
**Approved:** [ ] Yes [ ] No
**Notes:** _________________________________

---

**Testing completed successfully means the admin system is production-ready! 🎉**
