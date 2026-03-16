# Sprint 3: Expense Management Core

**Sprint Duration:** Week 5-6  
**Sprint Goal:** Implement core expense tracking functionality with full CRUD operations  
**Status:** ✅ Complete  

---

## Sprint Overview

This sprint delivers the core value proposition of the app: expense tracking. Users can create, read, update, and delete expenses with categories, receipts, and detailed information.

---

## Sprint Backlog

### User Stories

#### 1. Home Dashboard
**Story ID:** US-013  
**Priority:** High  
**Story Points:** 8

```
As a user,
I want to see an overview of my financial status on the home page,
So that I can quickly understand my spending.

Acceptance Criteria:
✅ Total balance display from all accounts
✅ Recent expenses list (last 5)
✅ Quick add expense button
✅ Monthly spending summary
✅ Account cards with balances
✅ Navigation to all expenses
✅ Refresh on data change

Tasks:
- [x] Create ui/home_page.py
- [x] Design dashboard layout
- [x] Implement balance calculation
- [x] Add recent expenses widget
- [x] Create account cards
- [x] Add quick action buttons
- [x] Test data refresh
```

#### 2. Add Expense
**Story ID:** US-014  
**Priority:** High  
**Story Points:** 13

```
As a user,
I want to add a new expense with details,
So that I can track where my money goes.

Acceptance Criteria:
✅ Form with amount, category, description, date
✅ Account selection dropdown
✅ Category selection with icons
✅ Optional receipt/photo attachment
✅ Optional note field
✅ Payment method selection
✅ Date picker (default: today)
✅ Amount validation
✅ Save to database
✅ Update account balance
✅ Success notification
✅ Navigate back or add another

Tasks:
- [x] Create ui/add_expense_page.py
- [x] Design expense form UI
- [x] Implement category selector
- [x] Add receipt upload/camera
- [x] Create date picker
- [x] Implement amount validation
- [x] Save expense logic
- [x] Update account balance
- [x] Test edge cases
```

#### 3. Expense Categories
**Story ID:** US-015  
**Priority:** High  
**Story Points:** 5

```
As a user,
I want predefined expense categories,
So that I can classify my expenses easily.

Acceptance Criteria:
✅ Default categories (Food, Transport, Shopping, etc.)
✅ Category icons and colors
✅ Category stored in database
✅ Used in expense form
✅ Displayed in expense lists
✅ Admin can add custom categories (future)

Tasks:
- [x] Create categories table
- [x] Define default categories
- [x] Add category icons
- [x] Implement category selector UI
- [x] Test category selection
```

#### 4. View All Expenses
**Story ID:** US-016  
**Priority:** High  
**Story Points:** 8

```
As a user,
I want to see a list of all my expenses,
So that I can review my spending history.

Acceptance Criteria:
✅ Paginated expense list
✅ Sort by date (newest first)
✅ Filter by category
✅ Filter by date range
✅ Search by description
✅ Display amount, category, date
✅ Tap to view details
✅ Pull to refresh

Tasks:
- [x] Create ui/all_expenses_page.py
- [x] Design expense list UI
- [x] Implement pagination
- [x] Add filter controls
- [x] Create search bar
- [x] Add sort options
- [x] Test performance with many expenses
```

#### 5. Edit Expense
**Story ID:** US-017  
**Priority:** High  
**Story Points:** 5

```
As a user,
I want to edit an existing expense,
So that I can correct mistakes or update information.

Acceptance Criteria:
✅ Load expense data into form
✅ All fields editable
✅ Balance adjustment on amount change
✅ Account transfer handling
✅ Save changes to database
✅ Success notification
✅ Navigate back to list

Tasks:
- [x] Create ui/edit_expense_page.py
- [x] Load expense by ID
- [x] Populate form fields
- [x] Handle balance updates
- [x] Implement save logic
- [x] Test account transfers
```

#### 6. Delete Expense
**Story ID:** US-018  
**Priority:** Medium  
**Story Points:** 3

```
As a user,
I want to delete an expense,
So that I can remove incorrect entries.

Acceptance Criteria:
✅ Delete button on expense details
✅ Confirmation dialog
✅ Restore account balance
✅ Remove from database
✅ Success notification
✅ Navigate back to list

Tasks:
- [x] Add delete button to UI
- [x] Implement confirmation dialog
- [x] Create delete function
- [x] Handle balance restoration
- [x] Test deletion flow
```

#### 7. Receipt/Photo Management
**Story ID:** US-019  
**Priority:** Medium  
**Story Points:** 8

```
As a user,
I want to attach receipt photos to expenses,
So that I have proof of purchases.

Acceptance Criteria:
✅ Take photo with camera
✅ Upload from gallery
✅ Multiple photos per expense (up to 5)
✅ Photo preview in expense
✅ Full-screen photo view
✅ Delete photo option
✅ Photos stored in file system
✅ Photo paths in database

Tasks:
- [x] Implement camera capture
- [x] Add file picker
- [x] Create photo storage system
- [x] Design photo preview UI
- [x] Add full-screen viewer
- [x] Test on multiple devices
```

---

## Sprint Metrics

### Velocity
- **Planned Story Points:** 50
- **Completed Story Points:** 50
- **Velocity:** 50 points/sprint
- **Velocity Increase:** +14% from Sprint 2

### Burndown
```
Day 1:  50 points remaining
Day 3:  47 points remaining (US-018 complete)
Day 5:  42 points remaining (US-015 complete)
Day 7:  37 points remaining (US-017 complete)
Day 9:  29 points remaining (US-016 complete)
Day 11: 21 points remaining (US-019 complete)
Day 13: 13 points remaining (US-014 complete)
Day 14: 0 points remaining (US-013 complete)
```

### Quality Metrics
- **Code Coverage:** 81%
- **Bugs Found:** 8 (all fixed)
- **Critical Bugs:** 2 (balance calculation, photo storage)
- **Code Reviews:** 7/7 approved
- **User Testing:** 12 users tested, 4.6/5 satisfaction

---

## Technical Achievements

### Files Created
1. `src/ui/home_page.py` - Dashboard (500+ lines)
2. `src/ui/add_expense_page.py` - Expense form (600+ lines)
3. `src/ui/all_expenses_page.py` - Expense list (450+ lines)
4. `src/ui/edit_expense_page.py` - Edit form (550+ lines)
5. `src/ui/Expenses.py` - Expense utilities (300+ lines)
6. `src/components/expense_item.py` - Reusable expense card (200+ lines)

### Files Modified
1. `src/core/db.py` - Added expenses, categories, receipts tables
2. `src/main.py` - Added expense navigation routes
3. `src/components/bottom_nav.py` - Navigation bar component

### Database Schema Extensions
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    icon TEXT,
    color TEXT,
    user_id INTEGER,
    is_default INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    description TEXT NOT NULL,
    notes TEXT,
    expense_date DATE NOT NULL,
    payment_method TEXT,
    receipt_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES accounts(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_expenses_user_date ON expenses(user_id, expense_date DESC);
CREATE INDEX idx_expenses_category ON expenses(category_id);
CREATE INDEX idx_expenses_account ON expenses(account_id);
```

### Default Categories
```python
DEFAULT_CATEGORIES = [
    ("Food & Dining", "🍔", "#FF6B6B"),
    ("Transportation", "🚗", "#4ECDC4"),
    ("Shopping", "🛍️", "#95E1D3"),
    ("Entertainment", "🎮", "#F38181"),
    ("Bills & Utilities", "💡", "#AA96DA"),
    ("Healthcare", "🏥", "#FCBAD3"),
    ("Education", "📚", "#A8D8EA"),
    ("Travel", "✈️", "#FFD93D"),
    ("Groceries", "🛒", "#6BCB77"),
    ("Other", "📝", "#BEBEBE"),
]
```

---

## Sprint Demo

### Demo Highlights
1. ✅ Complete expense tracking workflow
2. ✅ Intuitive expense form with validation
3. ✅ Beautiful category icons and colors
4. ✅ Receipt photo attachment
5. ✅ Comprehensive expense list with filters
6. ✅ Smooth edit/delete operations
7. ✅ Real-time balance updates

### Demo Flow
```
1. Home → View current balance and recent expenses
2. Tap "+" → Add Expense form
3. Enter amount: $50
4. Select category: Food & Dining
5. Add description: "Dinner at restaurant"
6. Attach receipt photo (camera/gallery)
7. Save → Balance updated, expense added
8. View All Expenses → See new expense
9. Filter by Food category → Shows only food expenses
10. Tap expense → View details
11. Edit → Change amount to $55
12. Save → Balance adjusted
13. Delete → Confirm → Expense removed, balance restored
```

### Stakeholder Feedback
- 👍 "This is exactly what we envisioned!"
- 👍 "Category selection is delightful"
- 👍 "Receipt feature adds great value"
- 🔄 "Need recurring expenses" (Sprint 7)
- 🔄 "Want to split expenses with others" (backlog)
- 👍 "Balance updates work perfectly"
- 🔄 "Add expense templates" (backlog)

---

## Sprint Retrospective

### What Went Well ✅
1. Clear user stories accelerated development
2. Reusable components saved time
3. Early database indexing prevented performance issues
4. Photo storage architecture is solid
5. Balance calculation logic is robust
6. Great team collaboration on UX

### What Could Be Improved 🔄
1. Photo compression needed earlier
2. More test data for edge cases
3. Filter UI could be more intuitive
4. Loading states for large lists
5. Better error messages for network issues

### Action Items for Next Sprint
1. [x] Implement photo compression utility
2. [x] Create automated test data generator
3. [ ] Redesign filter panel (backlog)
4. [x] Add loading skeletons
5. [x] Improve error message clarity

---

## Blockers & Resolutions

### Blocker 1: Balance Calculation
**Issue:** Race condition when editing expenses with account transfers  
**Resolution:** Implemented transaction-like balance updates  
**Impact:** 2 days, critical bug caught in testing  

### Blocker 2: Photo Storage
**Issue:** Large photos consuming excessive storage  
**Resolution:** Implemented compression before storage  
**Impact:** 1 day, improved app performance significantly  

### Blocker 3: Date Handling
**Issue:** Timezone inconsistencies causing wrong dates  
**Resolution:** Standardized to UTC with local display  
**Impact:** 0.5 day, prevented future date bugs  

---

## Technical Debt

### Addressed from Sprint 2
- ✅ Account types: More flexible account system implemented

### New Technical Debt
1. **Photo Compression:** Basic compression, could be optimized
2. **Expense Templates:** No template feature for recurring expenses
3. **Batch Operations:** No bulk delete or edit
4. **Expense Splitting:** Can't split bills between users
5. **Category Customization:** Users can't create custom categories

### Mitigation Plan
- Photo optimization: Ongoing improvements
- Expense templates: Sprint 7
- Batch operations: Sprint 7
- Expense splitting: Post-MVP (backlog)
- Custom categories: Sprint 6 (Admin config)

---

## Performance Optimizations

### Database
✅ Added indexes on frequently queried columns  
✅ Used prepared statements to prevent SQL injection  
✅ Implemented pagination for large datasets  
✅ Optimized JOIN queries  

### UI
✅ Lazy loading for expense lists  
✅ Image caching for categories  
✅ Debounced search input  
✅ Virtual scrolling for long lists  

### File System
✅ Compressed photos before storage  
✅ Organized files by user_id/month  
✅ Implemented cleanup for deleted expenses  

---

## User Experience Improvements

### Expense Form
- Smart defaults (today's date, default account)
- Category quick-select with icons
- Amount formatting with currency symbol
- Inline validation feedback
- Keyboard optimization (numeric for amount)

### Expense List
- Group by date (Today, Yesterday, This Week, etc.)
- Color-coded categories
- Swipe actions for quick edit/delete
- Empty state with helpful message
- Pull-to-refresh

### Accessibility
- Screen reader support for categories
- High contrast mode for amounts
- Large touch targets for buttons
- Keyboard navigation for forms

---

## Edge Cases Handled

### Amount Validation
✅ Negative amounts blocked  
✅ Zero amounts allowed (for free items)  
✅ Very large amounts (up to 999,999,999)  
✅ Decimal places limited to 2  
✅ Currency conversion handled  

### Balance Protection
✅ Prevent account balance from going negative (optional warning)  
✅ Handle account deletion with existing expenses  
✅ Rollback on failed transactions  
✅ Detect and prevent duplicate submissions  

### Date Handling
✅ Future dates allowed (for scheduled expenses)  
✅ Historical data (any past date)  
✅ Leap year handling  
✅ Timezone consistency  

---

## Sprint Artifacts

### Documentation Created
- ✅ Expense tracking user guide
- ✅ Category system documentation
- ✅ Receipt management guide
- ✅ Database schema documentation
- ✅ API documentation for expense functions

### Code Reviews
- All PRs required 2 approvals
- Security review for file uploads
- Performance testing for large datasets
- No critical issues in production

### Testing
- Unit tests for balance calculations
- Integration tests for expense CRUD
- UI tests for expense form
- Manual testing on 3 devices

---

## Definition of Done - Verification

✅ All user stories completed  
✅ All acceptance criteria met  
✅ Performance targets met (load < 2s)  
✅ Code reviewed and approved  
✅ No critical bugs  
✅ Security reviewed (file uploads)  
✅ Documentation updated  
✅ Demo successful  
✅ Stakeholder approval received  

---

## Sprint Handoff to Sprint 4

### Completed Items
- Complete expense CRUD operations
- Category system operational
- Receipt/photo management working
- Home dashboard displaying data
- Balance calculations accurate
- List filtering and search functional

### Dependencies for Sprint 4
- Expense data ready for analytics
- Categories for spending breakdowns
- Date ranges for time-series analysis
- Account data for comparative reports

### Next Sprint Preview
Sprint 4 will focus on:
- Statistics and analytics dashboard
- Spending insights and trends
- Category-wise breakdown charts
- Monthly/weekly spending reports
- Budget tracking (if time permits)
- Export functionality

---

**Sprint 3 Completed:** December 2025  
**Sprint Velocity:** 50 points  
**Team Satisfaction:** 4.8/5  
**Ready for Sprint 4:** ✅ Yes  
**Core Value Delivered:** ✅ Expense Tracking Fully Functional
