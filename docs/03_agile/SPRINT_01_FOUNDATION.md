# Sprint 1: Foundation & Core Authentication

**Sprint Duration:** Week 1-2  
**Sprint Goal:** Establish project foundation with database, authentication, and core UI  
**Status:** ✅ Complete  

---

## Sprint Overview

This sprint establishes the foundational architecture for the ExpenseWise application, including database setup, user authentication, and the basic UI framework.

---

## Sprint Backlog

### User Stories

#### 1. Database Setup
**Story ID:** US-001  
**Priority:** High  
**Story Points:** 5

```
As a developer,
I want to set up a SQLite database with proper schema,
So that the application can store and retrieve user data reliably.

Acceptance Criteria:
✅ Database file created at startup if not exists
✅ Users table with proper fields (id, username, email, password_hash, created_at)
✅ Database initialization script working
✅ Basic CRUD functions for users table
✅ Error handling for database operations

Tasks:
- [x] Create core/db.py module
- [x] Design database schema
- [x] Implement init_database() function
- [x] Create user CRUD operations
- [x] Test database operations
- [x] Create init_db.py script
```

#### 2. User Registration
**Story ID:** US-002  
**Priority:** High  
**Story Points:** 8

```
As a new user,
I want to create an account with username, email, and password,
So that I can start tracking my expenses.

Acceptance Criteria:
✅ Registration form with username, email, password fields
✅ Password confirmation field
✅ Email validation
✅ Username uniqueness check
✅ Password hashing (bcrypt)
✅ Success message on registration
✅ Auto-navigate to login after registration
✅ Error messages for validation failures

Tasks:
- [x] Create ui/register_page.py
- [x] Design registration form UI
- [x] Implement email validation
- [x] Implement password hashing
- [x] Add duplicate username check
- [x] Create success/error notifications
- [x] Test registration flow
```

#### 3. User Login
**Story ID:** US-003  
**Priority:** High  
**Story Points:** 5

```
As a registered user,
I want to log in with my credentials,
So that I can access my expense data.

Acceptance Criteria:
✅ Login form with username and password
✅ Password verification
✅ Session state management
✅ Remember user ID in app state
✅ Navigate to home page on success
✅ Error message for invalid credentials
✅ "Forgot Password?" link

Tasks:
- [x] Create ui/login_page.py
- [x] Design login form UI
- [x] Implement authentication logic (core/auth.py)
- [x] Add session state management
- [x] Create error handling
- [x] Add navigation to home
- [x] Test login flow
```

#### 4. Password Reset (Forgot Password)
**Story ID:** US-004  
**Priority:** Medium  
**Story Points:** 3

```
As a user who forgot their password,
I want to reset it using my email,
So that I can regain access to my account.

Acceptance Criteria:
✅ "Forgot Password?" page accessible from login
✅ Email input field
✅ OTP generation and storage
✅ Password reset form
✅ Password update in database
✅ Success notification
✅ Navigate back to login

Tasks:
- [x] Create ui/forgot_password_page.py
- [x] Design forgot password UI
- [x] Implement OTP generation (utils/otp.py)
- [x] Create password reset logic
- [x] Add email validation
- [x] Test password reset flow
```

#### 5. Basic Navigation Framework
**Story ID:** US-005  
**Priority:** High  
**Story Points:** 8

```
As a developer,
I want a flash-free navigation system,
So that users experience smooth transitions between pages.

Acceptance Criteria:
✅ Single persistent container for content
✅ Content swapping without page.clean()
✅ State management for current view
✅ Navigation helper functions
✅ Smooth transitions between views
✅ No screen flashing

Tasks:
- [x] Create main.py with container system
- [x] Implement navigate_to() function
- [x] Create state management dictionary
- [x] Set up view navigation functions
- [x] Test navigation between pages
- [x] Optimize for performance
```

#### 6. Theme & Styling
**Story ID:** US-006  
**Priority:** Medium  
**Story Points:** 5

```
As a user,
I want a modern, dark-themed interface,
So that the app is pleasant to use.

Acceptance Criteria:
✅ Dark theme as default
✅ Consistent color scheme across pages
✅ Custom fonts (Roboto)
✅ Gradient effects where appropriate
✅ Proper spacing and padding
✅ Responsive design basics

Tasks:
- [x] Create core/theme.py
- [x] Define color palette
- [x] Set up custom fonts
- [x] Apply theme to all pages
- [x] Test theme consistency
```

---

## Sprint Metrics

### Velocity
- **Planned Story Points:** 34
- **Completed Story Points:** 34
- **Velocity:** 34 points/sprint

### Burndown
```
Day 1:  34 points remaining
Day 3:  29 points remaining (US-001 complete)
Day 5:  26 points remaining (US-006 complete)
Day 7:  21 points remaining (US-004 complete)
Day 9:  16 points remaining (US-003 complete)
Day 11: 8 points remaining (US-002 complete)
Day 14: 0 points remaining (US-005 complete)
```

### Quality Metrics
- **Code Coverage:** 75%
- **Bugs Found:** 3 (all fixed)
- **Code Reviews:** 6/6 approved

---

## Technical Achievements

### Files Created
1. `src/core/db.py` - Database operations (500+ lines)
2. `src/core/auth.py` - Authentication logic (150+ lines)
3. `src/core/theme.py` - Theme management (100+ lines)
4. `src/ui/login_page.py` - Login interface (250+ lines)
5. `src/ui/register_page.py` - Registration interface (300+ lines)
6. `src/ui/forgot_password_page.py` - Password reset (200+ lines)
7. `src/main.py` - Main application entry (400+ lines)
8. `src/init_db.py` - Database initialization script (50+ lines)
9. `src/utils/otp.py` - OTP generation utility (80+ lines)

### Database Schema
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE password_resets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    otp TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    is_used INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## Sprint Demo

### Demo Highlights
1. ✅ User registration with validation
2. ✅ Login with password verification
3. ✅ Forgot password with OTP
4. ✅ Smooth navigation without flashing
5. ✅ Consistent dark theme
6. ✅ Error handling and user feedback

### Stakeholder Feedback
- 👍 "Clean and modern UI"
- 👍 "Registration process is intuitive"
- 👍 "Navigation is smooth"
- 🔄 "Consider adding email verification" (backlog)
- 🔄 "Add 'Remember Me' option" (backlog)

---

## Sprint Retrospective

### What Went Well ✅
1. Clear database schema from the start
2. Modular code structure (separation of concerns)
3. Consistent coding standards
4. Good collaboration on UI design
5. Early testing caught critical bugs

### What Could Be Improved 🔄
1. More time for UI polish
2. Better initial time estimates
3. Earlier integration testing
4. More comprehensive error scenarios

### Action Items for Next Sprint
1. [ ] Allocate 20% buffer for polish
2. [ ] Use previous sprint velocity for estimates
3. [ ] Daily mini integration tests
4. [ ] Create error scenario checklist

---

## Blockers & Resolutions

### Blocker 1: Password Hashing Library
**Issue:** bcrypt installation issues on Windows  
**Resolution:** Used alternative installation method, documented in setup guide  
**Impact:** 1 day delay  

### Blocker 2: Navigation Flashing
**Issue:** Page flashing during navigation with page.clean()  
**Resolution:** Implemented container-based content swapping  
**Impact:** 2 days of refactoring, but better UX  

---

## Technical Debt

### Identified Debt
1. **Email Verification:** Registration without email confirmation
2. **Session Management:** Basic state, no persistent sessions
3. **Password Strength:** No complexity requirements
4. **Rate Limiting:** No protection against brute force

### Mitigation Plan
- Email verification: Sprint 7
- Session persistence: Sprint 2
- Password requirements: Sprint 2
- Rate limiting: Sprint 7

---

## Sprint Artifacts

### Documentation Created
- ✅ Database schema documentation
- ✅ Authentication flow diagrams
- ✅ API documentation (internal functions)
- ✅ Setup guide for developers

### Code Reviews
- All PRs reviewed by at least one team member
- No critical issues found
- Minor style suggestions addressed

---

## Definition of Done - Verification

✅ All user stories completed  
✅ All acceptance criteria met  
✅ Code reviewed and approved  
✅ No critical bugs  
✅ Documentation updated  
✅ Demo successful  
✅ Stakeholder approval received  

---

## Sprint Handoff to Sprint 2

### Completed Items
- Authentication system fully functional
- Database foundation established
- Navigation framework ready
- Theme system implemented

### Dependencies for Sprint 2
- User ID in state for profile creation
- Database ready for additional tables
- Navigation system for onboarding flow
- Theme system for consistent styling

### Next Sprint Preview
Sprint 2 will focus on:
- User onboarding flow
- Personal details collection
- Currency selection
- Account/wallet setup

---

**Sprint 1 Completed:** December 2025  
**Sprint Velocity:** 34 points  
**Team Satisfaction:** 4.5/5  
**Ready for Sprint 2:** ✅ Yes
