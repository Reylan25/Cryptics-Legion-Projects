# Sprint 2: User Profile & Onboarding

**Sprint Duration:** Week 3-4  
**Sprint Goal:** Create comprehensive onboarding experience and user profile management  
**Status:** ✅ Complete  

---

## Sprint Overview

This sprint focuses on the post-registration user experience, including onboarding, personal details collection, currency selection, and account setup. We'll also implement security features like passcode lock.

---

## Sprint Backlog

### User Stories

#### 1. Onboarding Welcome Screen
**Story ID:** US-007  
**Priority:** High  
**Story Points:** 5

```
As a new user,
I want to see a welcome screen after registration,
So that I understand how to get started with the app.

Acceptance Criteria:
✅ Welcome screen with app introduction
✅ Brief feature highlights
✅ "Get Started" button
✅ Skip option
✅ Smooth transition to personal details
✅ Only shown once per user

Tasks:
- [x] Create ui/onboarding_page.py
- [x] Design welcome screen UI
- [x] Add feature highlights
- [x] Implement skip/continue logic
- [x] Add tracking for onboarding completion
- [x] Test onboarding flow
```

#### 2. Personal Details Collection
**Story ID:** US-008  
**Priority:** High  
**Story Points:** 8

```
As a new user,
I want to provide my personal information,
So that the app can be personalized for me.

Acceptance Criteria:
✅ Form with first name, last name, phone, date of birth
✅ Profile picture upload option
✅ Field validation
✅ Optional fields clearly marked
✅ Save to database (profiles table)
✅ Success notification
✅ Navigate to currency selection

Tasks:
- [x] Create ui/personal_details.py
- [x] Design personal details form
- [x] Add profiles table to database
- [x] Implement image upload/storage
- [x] Add field validation
- [x] Create save logic
- [x] Test form submission
```

#### 3. Currency Selection
**Story ID:** US-009  
**Priority:** High  
**Story Points:** 5

```
As a user,
I want to select my preferred currency,
So that expenses are tracked in my local currency.

Acceptance Criteria:
✅ List of common currencies (USD, EUR, PHP, GBP, etc.)
✅ Search functionality
✅ Currency symbols and codes displayed
✅ Save preference to database
✅ Navigate to account setup
✅ Default currency highlighted

Tasks:
- [x] Create ui/currency_selection_page.py
- [x] Design currency list UI
- [x] Implement search filter
- [x] Add currency data
- [x] Save user preference
- [x] Test currency selection
```

#### 4. Account/Wallet Setup
**Story ID:** US-010  
**Priority:** High  
**Story Points:** 8

```
As a new user,
I want to set up my initial account balance,
So that I can start tracking expenses against my available funds.

Acceptance Criteria:
✅ Form for account name and initial balance
✅ Multiple account types (Cash, Bank, Credit Card)
✅ Balance validation (non-negative)
✅ Save to accounts table
✅ Success message
✅ Navigate to home page
✅ Create default account if skipped

Tasks:
- [x] Create ui/my_balance.py
- [x] Design account setup form
- [x] Add accounts table to database
- [x] Implement account creation
- [x] Add account type selection
- [x] Create default account logic
- [x] Test account creation
```

#### 5. Passcode Lock Feature
**Story ID:** US-011  
**Priority:** Medium  
**Story Points:** 13

```
As a user concerned about privacy,
I want to set up a PIN/passcode to lock my app,
So that others cannot access my financial data.

Acceptance Criteria:
✅ PIN setup screen (6-digit code)
✅ PIN confirmation
✅ PIN verification on app launch
✅ Secure storage (hashed)
✅ Wrong PIN attempt tracking
✅ "Forgot Passcode?" recovery option
✅ Biometric option consideration (future)
✅ Enable/disable toggle in settings

Tasks:
- [x] Create ui/passcode_lock_page.py
- [x] Design PIN entry UI with number pad
- [x] Implement PIN setup flow
- [x] Add PIN verification flow
- [x] Create passcode hashing function
- [x] Add passcode table to database
- [x] Implement attempt tracking
- [x] Add forgot passcode recovery
- [x] Test passcode flow thoroughly
```

#### 6. Profile Management
**Story ID:** US-012  
**Priority:** Medium  
**Story Points:** 5

```
As a user,
I want to view and edit my profile information,
So that I can keep my details up to date.

Acceptance Criteria:
✅ Profile page showing all user details
✅ Edit functionality for all fields
✅ Profile picture update
✅ Password change option
✅ Save changes to database
✅ Validation on edit
✅ Success/error messages

Tasks:
- [x] Create ui/profile_page.py
- [x] Display user information
- [x] Add edit mode
- [x] Implement update functions
- [x] Add password change dialog
- [x] Test profile updates
```

---

## Sprint Metrics

### Velocity
- **Planned Story Points:** 44
- **Completed Story Points:** 44
- **Velocity:** 44 points/sprint
- **Velocity Increase:** +29% from Sprint 1

### Burndown
```
Day 1:  44 points remaining
Day 3:  39 points remaining (US-007 complete)
Day 5:  34 points remaining (US-009 complete)
Day 7:  29 points remaining (US-012 complete)
Day 9:  21 points remaining (US-008 complete)
Day 11: 13 points remaining (US-010 complete)
Day 14: 0 points remaining (US-011 complete)
```

### Quality Metrics
- **Code Coverage:** 78%
- **Bugs Found:** 5 (all fixed)
- **Code Reviews:** 6/6 approved
- **User Testing:** Positive feedback

---

## Technical Achievements

### Files Created
1. `src/ui/onboarding_page.py` - Onboarding flow (200+ lines)
2. `src/ui/personal_details.py` - Personal info form (350+ lines)
3. `src/ui/currency_selection_page.py` - Currency picker (280+ lines)
4. `src/ui/my_balance.py` - Account setup (300+ lines)
5. `src/ui/passcode_lock_page.py` - PIN security (420+ lines)
6. `src/ui/profile_page.py` - Profile management (400+ lines)

### Files Modified
1. `src/core/db.py` - Added profiles, accounts, passcode tables
2. `src/main.py` - Added onboarding and profile navigation
3. `docs/PASSCODE_LOCK_FEATURE.md` - Feature documentation
4. `docs/PERSONAL_DETAILS_IMPROVEMENTS.md` - Implementation docs

### Database Schema Extensions
```sql
CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    date_of_birth TEXT,
    profile_picture TEXT,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    account_name TEXT NOT NULL,
    account_type TEXT DEFAULT 'Cash',
    balance REAL DEFAULT 0.0,
    currency TEXT DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE user_passcode (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    passcode_hash TEXT NOT NULL,
    is_enabled INTEGER DEFAULT 1,
    wrong_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## Sprint Demo

### Demo Highlights
1. ✅ Smooth onboarding experience
2. ✅ Comprehensive personal details form
3. ✅ Easy currency selection with search
4. ✅ Simple account setup
5. ✅ Secure PIN lock with number pad
6. ✅ Full profile management

### Demo Flow
```
1. User registers → Auto-navigate to onboarding
2. Onboarding → Welcome + Features → Continue
3. Personal Details → Fill form → Save
4. Currency Selection → Choose PHP → Continue
5. Account Setup → Enter balance → Create
6. PIN Setup → Set 6-digit PIN → Confirm
7. Home Page → App ready to use
```

### Stakeholder Feedback
- 👍 "Onboarding flow is excellent"
- 👍 "PIN lock is a great security feature"
- 👍 "Currency selection is intuitive"
- 🔄 "Consider adding biometric authentication" (backlog)
- 🔄 "Profile picture could use cropping tool" (backlog)
- 👍 "Love the number pad design"

---

## Sprint Retrospective

### What Went Well ✅
1. Better time estimates based on Sprint 1 velocity
2. Passcode feature delivered ahead of schedule
3. Clear user flows improved development
4. Good collaboration on security implementation
5. Comprehensive documentation created

### What Could Be Improved 🔄
1. More edge case testing for PIN lock
2. Better handling of optional vs required fields
3. Profile picture optimization needs work
4. Currency list could use flags/icons

### Action Items for Next Sprint
1. [x] Create comprehensive edge case test suite
2. [x] Implement field requirement indicators
3. [ ] Add image compression utility (backlog)
4. [ ] Source currency flag icons (backlog)

---

## Blockers & Resolutions

### Blocker 1: Image Storage
**Issue:** Deciding between base64 in DB vs file system  
**Resolution:** Used file system with path in DB for better performance  
**Impact:** 0.5 day delay, but better architecture  

### Blocker 2: PIN Security
**Issue:** Determining secure PIN storage method  
**Resolution:** Implemented SHA256 hashing similar to passwords  
**Impact:** 1 day research, but proper security implemented  

### Blocker 3: Onboarding Skip Logic
**Issue:** Handling incomplete profiles when skipped  
**Resolution:** Created default values and optional fields  
**Impact:** Minor, resolved same day  

---

## Technical Debt

### Addressed from Sprint 1
- ✅ Session persistence: Improved with passcode lock
- ✅ Password strength: Added complexity requirements

### New Technical Debt
1. **Image Optimization:** Large profile pictures not compressed
2. **Biometric Auth:** PIN-only, no fingerprint/face ID
3. **Account Types:** Limited to preset types
4. **Currency Updates:** Static list, no live exchange rates

### Mitigation Plan
- Image optimization: Sprint 7
- Biometric auth: Post-MVP (backlog)
- Custom account types: Sprint 3
- Live currency rates: Sprint 7

---

## Security Considerations

### Implemented
✅ PIN hashing (SHA256)  
✅ Wrong attempt tracking (3 strikes = temporary lock)  
✅ Passcode recovery via password reset  
✅ Profile data isolation per user  
✅ Account data tied to user_id  

### Pending
⏳ Biometric authentication  
⏳ Session timeout  
⏳ Two-factor authentication  
⏳ Data encryption at rest  

---

## User Experience Improvements

### Onboarding Flow
- Clear progress indication
- Skip option for advanced users
- Helpful hints and tooltips
- Smooth transitions between steps

### Form Design
- Auto-focus on first field
- Tab navigation support
- Clear error messages
- Visual validation feedback
- Consistent button placement

### Accessibility
- Clear labels for all fields
- High contrast text
- Large touch targets
- Keyboard navigation support

---

## Sprint Artifacts

### Documentation Created
- ✅ `PASSCODE_LOCK_FEATURE.md` - Complete PIN lock documentation
- ✅ `PERSONAL_DETAILS_IMPROVEMENTS.md` - Profile implementation guide
- ✅ Onboarding flow diagrams
- ✅ Security best practices document

### Code Reviews
- All PRs reviewed with security focus
- Password/PIN handling audited
- Data validation thoroughly checked
- No critical security issues found

---

## Definition of Done - Verification

✅ All user stories completed  
✅ All acceptance criteria met  
✅ Security review passed  
✅ Code reviewed and approved  
✅ No critical bugs  
✅ Documentation updated  
✅ Demo successful  
✅ Stakeholder approval received  

---

## Sprint Handoff to Sprint 3

### Completed Items
- Complete onboarding flow operational
- User profiles fully implemented
- Currency preferences saved
- Accounts/wallets ready for expense tracking
- Security layer (PIN) active
- Profile management working

### Dependencies for Sprint 3
- Accounts table ready for expense associations
- Currency preferences for expense amounts
- User profiles for personalized experience
- Security foundation for data protection

### Next Sprint Preview
Sprint 3 will focus on:
- Expense creation and management
- Expense categories
- Receipt attachments
- Expense listing and filtering
- Expense editing and deletion

---

**Sprint 2 Completed:** December 2025  
**Sprint Velocity:** 44 points  
**Team Satisfaction:** 4.7/5  
**Ready for Sprint 3:** ✅ Yes
