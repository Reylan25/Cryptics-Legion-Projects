# 📱 QuickBooks Integration - Visual Quick Start

## 🎬 5-Minute Quick Start Guide

### **Phase 1: Get Your Credentials (2 minutes)**

```
STEP 1: Go to Intuit Developer Portal
┌──────────────────────────────────────┐
│ https://developer.intuit.com         │
│                                      │
│ [Sign In or Create Account]          │
└──────────────────────────────────────┘

        ↓

STEP 2: Create Your App
┌──────────────────────────────────────┐
│ Click [Create an app]                │
│ Select: "Accounting"                 │
│ Name: "Cryptics Legion"              │
│ Click [Create app]                   │
└──────────────────────────────────────┘

        ↓

STEP 3: Get Client ID & Secret
┌──────────────────────────────────────┐
│ Go to: Settings tab                  │
│ Find: Development section            │
│                                      │
│ COPY THESE:                          │
│ □ Client ID:                         │
│   2EmPO3v7eoOdgMZUM                  │
│                                      │
│ □ Client Secret:                     │
│   ***keep this secret***             │
└──────────────────────────────────────┘

        ↓

STEP 4: Get Realm ID
┌──────────────────────────────────────┐
│ Still in app settings:               │
│ Click [Connect to Sandbox]           │
│ OR [Connect to Production]           │
│                                      │
│ After connecting:                    │
│ □ Realm ID:                          │
│   fcd-9a1a-b97157dc4dc3              │
│                                      │
│ SAVE ALL 3 VALUES!                   │
└──────────────────────────────────────┘
```

### **Phase 2: Configure in App (2 minutes)**

```
STEP 5: Open Cryptics Application
┌──────────────────────────────────────┐
│ Terminal:                            │
│ $ python Cryptics_legion/src/main.py │
│                                      │
│ App loads → Shows Login Screen       │
└──────────────────────────────────────┘

        ↓

STEP 6: Log In as Admin
┌──────────────────────────────────────┐
│ Username: ADMIN                      │
│ Password: ADMIN256                   │
│                                      │
│ [Login]                              │
│                                      │
│ → Admin Dashboard appears            │
└──────────────────────────────────────┘

        ↓

STEP 7: Navigate to QB Integration
┌──────────────────────────────────────┐
│ Left Sidebar:                        │
│ ├─ Overview                          │
│ ├─ Expense Management                │
│ ├─ User & Group                      │
│ ├─ Configuration & Policy ← CLICK    │
│ │  ├─ Policy Rules                   │
│ │  ├─ Currencies & Rates             │
│ │  ├─ Expense Categories             │
│ │  └─ Accounting Integration ← CLICK │
│ └─ Reporting & Analytics             │
└──────────────────────────────────────┘

        ↓

STEP 8: Connect QuickBooks
┌──────────────────────────────────────┐
│ You see 4 Integration Cards:         │
│                                      │
│ ┌──────────────┐  ┌──────────────┐  │
│ │ 📊 QB        │  │ ☁️ Xero      │  │
│ │ Not Connect  │  │ Not Connect  │  │
│ │              │  │              │  │
│ │ [Connect]    │  │ [Connect]    │  │
│ └──────────────┘  └──────────────┘  │
│                                      │
│ Click [Connect] on QuickBooks        │
│ → Dialog pops up                     │
└──────────────────────────────────────┘

        ↓

STEP 9: Enter Your Credentials
┌─────────────────────────────────────────┐
│ QuickBooks Online Configuration         │
├─────────────────────────────────────────┤
│                                         │
│ Client ID:                              │
│ [2EmPO3v7eoOdgMZUM_________] ← Paste   │
│                                         │
│ Client Secret:                          │
│ [••••••••••••••••••••••] ← Paste        │
│                                         │
│ Realm ID (Company ID):                  │
│ [fcd-9a1a-b97157dc4dc3_] ← Paste       │
│                                         │
│ ┌──────────────────────────────────┐   │
│ │ [Test Connection]                │   │
│ └──────────────────────────────────┘   │
│                                         │
│ Status: ✅ Credentials valid           │
│                                         │
│ [Cancel]  [Save Configuration]         │
├─────────────────────────────────────────┤
└─────────────────────────────────────────┘

        ↓

STEP 10: Test & Save
┌──────────────────────────────────────┐
│ 1. Click [Test Connection]           │
│    → Green: ✅ Valid                  │
│                                      │
│ 2. Click [Save Configuration]        │
│    → Success! Dialog closes          │
│                                      │
│ 3. Back to integration page          │
│    QuickBooks now shows:             │
│    Connected ✅                       │
│                                      │
│ ✅ SETUP COMPLETE!                   │
└──────────────────────────────────────┘
```

### **Phase 3: First Sync (1 minute)**

```
STEP 11: Add Test Expenses
┌──────────────────────────────────────┐
│ 1. Log out as admin                  │
│ 2. Log in as regular user            │
│ 3. Add 2-3 test expenses:            │
│                                      │
│    Expense 1:                        │
│    Amount: $50.00                    │
│    Category: Travel                  │
│    Description: Team breakfast       │
│    [Add Expense]                     │
│                                      │
│    Expense 2:                        │
│    Amount: $100.00                   │
│    Category: Meals                   │
│    Description: Client lunch         │
│    [Add Expense]                     │
└──────────────────────────────────────┘

        ↓

STEP 12: Back to Admin
┌──────────────────────────────────────┐
│ 1. Log out of user account           │
│ 2. Log in as ADMIN / ADMIN256        │
│ 3. Go back to:                       │
│    Configuration & Policy →          │
│    Accounting Integration            │
└──────────────────────────────────────┘

        ↓

STEP 13: Click Sync
┌──────────────────────────────────────┐
│ ┌──────────────────────────────────┐ │
│ │ 📊 QuickBooks                    │ │
│ │ Connected ✅                     │ │
│ │                                  │ │
│ │ [Configure] [↻ Sync] ← CLICK    │ │
│ └──────────────────────────────────┘ │
│                                      │
│ Click [↻ Sync]                       │
│ → See: "Syncing..."                  │
│                                      │
│ Processing:                          │
│ ⟳ Finding expenses...               │
│ ⟳ Creating bills...                 │
│ ⟳ Logging activity...               │
│                                      │
│ Result:                              │
│ ✅ "Synced 2 expenses to QB"        │
│                                      │
│ You see in Recent Sync Activity:     │
│ ✓ QBO - Expense Sync                │
│   2 records • Mar 16, 2:35 PM        │
└──────────────────────────────────────┘

        ↓

STEP 14: Verify in QuickBooks
┌──────────────────────────────────────┐
│ 1. Open QuickBooks Online:           │
│    https://quickbooks.intuit.com     │
│                                      │
│ 2. Log in with your QB account       │
│                                      │
│ 3. Go to: Transactions → Bills       │
│                                      │
│ 4. You should see:                   │
│                                      │
│    Bill #1:                          │
│    Amount: $50.00                    │
│    Description: Team breakfast       │
│    Date: Today                       │
│    Account: Team Travel Account      │
│                                      │
│    Bill #2:                          │
│    Amount: $100.00                   │
│    Description: Client lunch         │
│    Date: Today                       │
│    Account: Meals Account            │
│                                      │
│ ✅ SYNC WORKS! 🎉                    │
└──────────────────────────────────────┘
```

---

## 🎨 Visual Status Indicators

### **Not Connected**
```
┌─────────────────────────────┐
│ 📊 QuickBooks              │
│ ❌ Not Connected           │
│                             │
│ [Connect] Button           │
│ (Red/Gray background)      │
└─────────────────────────────┘
```

### **Connected**
```
┌─────────────────────────────┐
│ 📊 QuickBooks              │
│ ✅ Connected               │
│                             │
│ [Configure] [↻ Sync]       │
│ (Green background)         │
└─────────────────────────────┘
```

### **Sync Results**
```
Recent Sync Activity

✅ Success (Green):
   QuickBooks - Expense Sync
   25 records • Mar 16, 2:35 PM

⚠️ Partial (Orange):
   QuickBooks - Expense Sync
   15 of 20 records • Mar 16, 1:15 PM
   Error: GL code not valid

❌ Failed (Red):
   QuickBooks - Expense Sync
   0 records • Mar 16, 12:00 PM
   Error: Invalid Client Secret
```

---

## 📋 The Three Credentials Explained Visually

```
┌─────────────────────────────────────────────────────┐
│               YOUR INTUIT APP                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  CLIENT ID (Public)      CLIENT SECRET (Private)   │
│  ━━━━━━━━━━━━━━━━━━      ━━━━━━━━━━━━━━━━━━━━     │
│  "Hello, I'm app        "Here's my password for    │
│   from Cryptics"         this app"                 │
│                                                     │
│  2EmPO3v7eoOdgMZUM      hJ8kL2mN9pQ1rS4tU7wX0...  │
│                                                     │
│  Safe to share          ⚠️ KEEP SECRET!            │
│  Like your username     Like your password         │
│                                                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│         YOUR QUICKBOOKS COMPANY                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  REALM ID (Company ID)                             │
│  ━━━━━━━━━━━━━━━━━━━━━━                           │
│  "This app syncs with MY company"                 │
│                                                     │
│  fcd-9a1a-b97157dc4dc3                            │
│                                                     │
│  Unique to your QB account                        │
│  Links app to your company                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔄 What Happens When You Sync - Visual Flow

```
START
  │
  ↓
┌─────────────────────────────────┐
│ ADMIN CLICKS [↻ SYNC] BUTTON    │
└─────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────┐
│ DATABASE QUERY:                 │
│ Find all expenses where          │
│ synced_to_qb = 0                │
│                                 │
│ Results: 5 expenses              │
└─────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────┐
│ FOR EACH EXPENSE (1-5):         │
│                                 │
│ 1️⃣ Extract data:               │
│    Description: "Team lunch"    │
│    Amount: $75.00               │
│    Category: Meals              │
│    Date: 3/16/2026              │
│                                 │
│ 2️⃣ Look up GL Code:            │
│    Meals → 4200                 │
│                                 │
│ 3️⃣ Call QB API:                │
│    Create Bill in QB            │
│    Account: 4200                │
│    Amount: $75.00               │
│    Date: 3/16                   │
│                                 │
│ 4️⃣ Log result:                 │
│    Success ✅ or Error ❌       │
└─────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────┐
│ UPDATE DATABASE:                │
│ Mark expenses: synced_to_qb = 1 │
└─────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────┐
│ LOG SYNC ACTIVITY:              │
│ - Time: Now                     │
│ - Records: 5                    │
│ - Status: Success               │
└─────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────┐
│ SHOW RESULT TO ADMIN:           │
│ ✅ "Synced 5 expenses to QB"   │
└─────────────────────────────────┘
  │
  ↓
┌─────────────────────────────────┐
│ EXPENSES NOW IN QUICKBOOKS! 🎉  │
└─────────────────────────────────┘
  │
  ↓
  END
```

---

## 💡 Understanding GL Codes Visually

```
IN YOUR CRYPTICS APP:         IN QUICKBOOKS:
═════════════════════════════════════════════════════

Category: Travel        ──→   GL Code: 4100   ──→   Travel Expense Acct
  Expense 1: $50                   $50                    $150
  Expense 2: $60        Combined   $60        Combined    Balance
  Expense 3: $40                   $40

Category: Meals         ──→   GL Code: 4200   ──→   Meals & Ent Acct
  Expense 1: $25                   $25                    $75
  Expense 2: $30        Combined   $30        Combined    Balance
  Expense 3: $20                   $20

Category: Office        ──→   GL Code: 4300   ──→   Office Supp Acct
  Expense 1: $100                  $100                   $200
  Expense 2: $100       Combined   $100       Combined    Balance


RESULT: Your QB chart of accounts automatically updated! ✅
```

---

## ⚠️ Common Issues - Visual Troubleshooting

### **Issue 1: Test Connection Shows Nothing**

```
Problem:
Click [Test Connection]
  ↓
Nothing happens
  ↓
No message appears

Solutions:
✓ Fill all 3 fields
✓ Check for typos/spaces
✓ Copy-paste credentials fresh
✓ Try again after 5 seconds
```

### **Issue 2: Sync Shows 0 Records**

```
Problem:
Click [↻ Sync]
  ↓
✅ "Synced 0 expenses"
  ↓
Nothing happened

Causes & Solutions:
┌─────────────────┬──────────────────────┐
│ Cause           │ Solution             │
├─────────────────┼──────────────────────┤
│ No expenses     │ Add expenses first    │
│ Already synced  │ Add NEW expenses      │
│ No GL codes     │ Add to categories     │
│ Wrong app       │ Create new credentials│
└─────────────────┴──────────────────────┘
```

### **Issue 3: QB Says Invalid Credentials**

```
Error Message: ❌ Invalid Client Secret

Troubleshooting Steps:
1. Go back to: https://developer.intuit.com
2. Copy Client Secret AGAIN carefully
3. Paste into dialog (check for spaces)
4. Click Test Connection
5. If still fails:
   - Create NEW app
   - Get fresh credentials
   - Try again
```

---

## 📊 Quick Look-Up Table

### **Where to Find Everything**

| Task | Where | Click Path |
|------|-------|-----------|
| **Connect QB** | Admin → Config | Configuration & Policy → Accounting Integration |
| **Add GL Codes** | Admin → Config | Configuration & Policy → Expense Categories |
| **Manual Sync** | Integration Page | QB Card → [↻ Sync] button |
| **View History** | Integration Page | Below cards → Recent Sync Activity |
| **Get Credentials** | Intuit | https://developer.intuit.com → Your App |
| **Check QB Bills** | QB Online | https://quickbooks.intuit.com → Transactions → Bills |

---

## ✅ Success Checklist

```
Setup Phase:
□ Created app on Intuit
□ Got Client ID
□ Got Client Secret
□ Connected QB account
□ Got Realm ID

Configuration Phase:
□ Opened Cryptics app
□ Logged in as ADMIN
□ Went to Accounting Integration
□ Clicked "Connect" on QB
□ Entered 3 credentials
□ Clicked "Test Connection" - shows ✅
□ Clicked "Save Configuration"

First Sync Phase:
□ Added test expenses
□ Went back to Integration page
□ Clicked [↻ Sync]
□ Saw success message
□ Verified in QuickBooks

CONGRATULATIONS! 🎉
Your QB Integration is working!
```

---

## 🎓 Beginner to Advanced

### **Beginner View**
✅ Just need to know: Click sync, expenses go to QB

### **Intermediate View**
✅ Need to know: How to configure, what GL codes do, troubleshooting

### **Advanced View**
✅ Need to know: API details, token refresh, GL code mapping logic

### **This Guide Covers:** All three levels! Start where you are, advance as needed.

---

## 🚀 Ready to Start?

1. **Collect your 3 credentials** (5 min)
2. **Open the app and log in** (1 min)
3. **Configure QB integration** (2 min)
4. **Add test expenses** (2 min)
5. **Click sync** (1 min)
6. **Verify in QB** (1 min)

**Total time: ~15 minutes** ⏱️

→ Go to [QUICKBOOKS_TUTORIAL.md] for detailed step-by-step guide
