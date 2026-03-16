# 📚 QuickBooks Integration - Complete Tutorial

## 🎯 What QuickBooks Integration Does

QuickBooks integration automatically **syncs your expenses from Cryptics Legion to QuickBooks Online**, so:
- ✅ You enter expenses in the app
- ✅ Click one button to sync
- ✅ Expenses appear in QuickBooks
- ✅ Your accounting is automated

---

## 🚀 Getting Started (5 Steps)

### **Step 1: Get Your QuickBooks Credentials**

You need 3 pieces of information from Intuit/QuickBooks.

**What You Need:**
1. Client ID
2. Client Secret  
3. Realm ID (Company ID)

**Where to Get Them:**

#### Get Client ID & Secret:
```
1. Go to: https://developer.intuit.com
2. Sign in (or create free account)
3. Click "Create an app"
4. Select "Accounting" as product
5. Name it "Cryptics Legion" (or any name)
6. Click "Create app"
7. Go to Settings tab
8. Find "Development" section
9. Copy these values:
   - Client ID (long alphanumeric string)
   - Client Secret (keep this private!)
```

#### Get Realm ID:
```
1. In same Intuit portal
2. Look for "Authentication" or "Connect" button
3. Click "Connect to Sandbox" (for testing) 
   OR "Connect to Production" (for real)
4. Log in with your QuickBooks account
5. Accept the permissions
6. After connecting, you'll see:
   - Realm ID = Your Company ID
   - Copy this number
```

**Example Values:**
```
Client ID:     2EmPO3v7eoOdgMZUM
Client Secret: ***secret***
Realm ID:      fcd-9a1a-b97157dc4dc3
```

---

### **Step 2: Open Your App**

Run the Cryptics Legion application:

```bash
# In your terminal:
cd Cryptics-Legion-Projects
python Cryptics_legion/src/main.py
```

---

### **Step 3: Log In as Admin**

```
Username: ADMIN
Password: ADMIN256
```

You'll see the Admin Dashboard.

---

### **Step 4: Navigate to Accounting Integration**

Follow this path:

```
Admin Dashboard
    ↓
Left Sidebar → Configuration & Policy
    ↓
Click "Accounting Integration"
    ↓
You see 4 cards: QuickBooks, Xero, SAP, NetSuite
```

---

### **Step 5: Configure QuickBooks**

**In the Accounting Integration Page:**

1. **Find the QuickBooks card** (shows "Not Connected" in red)
2. **Click "Connect" button** on the card
3. **A dialog pops up:**

```
┌─────────────────────────────────┐
│ QuickBooks Online Configuration │
├─────────────────────────────────┤
│ Client ID:      [___________]   │
│ Client Secret:  [___________]   │
│ Realm ID:       [___________]   │
│                                 │
│ [Test Connection] |  [Cancel]   │
│                    |  [Save]     │
└─────────────────────────────────┘
```

4. **Fill in your 3 values:**
   - Paste Client ID
   - Paste Client Secret
   - Paste Realm ID

5. **Click "Test Connection"** 
   - Green message = ✅ Ready to save
   - Orange message = ⚠️ Check values
   - Red message = ❌ Invalid

6. **Click "Save Configuration"**
   - Success! QB card now shows "Connected" ✅

---

## 💡 Understanding the Three Credentials

### **Client ID**
- **What:** Public ID of your app
- **Where:** Intuit Developer Portal > Settings
- **How long:** 20+ characters
- **Example:** `2EmPO3v7eoOdgMZUM`
- **Security:** Safe to share

### **Client Secret**  
- **What:** Private password for your app
- **Where:** Intuit Developer Portal > Settings
- **How long:** 30+ characters
- **Example:** `hJ8kL2mN9pQ1rS4tU7wX0...`
- **Security:** ⚠️ KEEP PRIVATE! Like a password

### **Realm ID (Company ID)**
- **What:** Unique ID of your QB company
- **Where:** After connecting account in Intuit Portal
- **How long:** 12-15 digits
- **Example:** `fcd-9a1a-b97157dc4dc3`
- **Security:** Specific to your company

---

## 🔄 How to Sync Your First Expenses

### **Step 1: Add Expenses in Cryptics**

```
1. Log in as regular user (not admin)
2. Add some test expenses:
   - Amount: $50.00
   - Category: "Meals"
   - Date: Today
3. Add a few more with different categories
```

### **Step 2: Go Back to Admin → Accounting Integration**

```
1. Log in as ADMIN again
2. Go to Configuration & Policy → Accounting Integration
3. Find QuickBooks card (now shows "Connected" ✅)
```

### **Step 3: Click the Sync Button**

```
QuickBooks Card:
┌─────────────────────────────┐
│ 📊 QuickBooks              │
│ Connected ✅                │
│                             │
│ Sync with QBO              │
│                             │
│ [Configure] [↻ Sync] ←─── Click here
└─────────────────────────────┘
```

### **Step 4: Watch It Sync**

```
Blue Message Appears:
"Syncing with QuickBooks..."

System:
  1. Finds all unsync expenses
  2. For each expense:
     - Takes: description, amount, date, category
     - Finds: GL code from category
     - Creates: Bill in QB with GL code
  3. Logs results

Green Message Appears:
"✅ Synced X expenses to QuickBooks"
```

### **Step 5: Verify in QuickBooks**

```
Open your QuickBooks Online account
  ↓
Go to: Transactions → Bills
  ↓
You should see your expenses
  ↓
They'll have your GL codes mapped correctly
```

---

## 📊 What Happens in Detail

### **The Sync Flow**

```
┌──────────────────────────────────────────────────┐
│ 1. USER ADDS EXPENSE IN CRYPTICS LEGION         │
│    Amount: $150, Category: Travel, Date: 3/16   │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 2. EXPENSE STORED IN DATABASE                    │
│    marked as: synced_to_qb = 0 (not synced yet) │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 3. ADMIN CLICKS SYNC BUTTON                      │
│    System checks: What expenses need syncing?    │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 4. FOR EACH UNSYNCED EXPENSE:                    │
│                                                   │
│    a) Get expense data:                          │
│       - Description: "Team Travel"               │
│       - Amount: 150.00                           │
│       - Date: 2026-03-16                         │
│                                                   │
│    b) Look up GL code:                           │
│       - Category: Travel                         │
│       - GL Code: 4100 (from admin config)        │
│                                                   │
│    c) Create QB Bill:                            │
│       - Account: 4100 (Travel Expense)           │
│       - Amount: $150                             │
│       - Description: Team Travel                 │
│       - Date: 3/16/2026                          │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 5. UPDATE IN CRYPTICS:                           │
│    Mark expense: synced_to_qb = 1 (synced)      │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 6. LOG THE ACTIVITY:                             │
│    - Time: 3/16/2026 2:35 PM                     │
│    - Records synced: 1                           │
│    - Status: Success ✅                          │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 7. SHOW RESULT TO ADMIN:                         │
│    Green message: "Synced 1 expense to QB"      │
└──────────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────────┐
│ 8. EXPENSE NOW IN QUICKBOOKS! 🎉                │
│    QB Bills list shows the new expense           │
└──────────────────────────────────────────────────┘
```

---

## 🎨 Understanding the UI

### **When Not Connected**

```
┌─────────────────────────────────┐
│ 📊 QuickBooks                   │
│                                 │
│ Sync with QBO                   │
│ Not Connected [×]               │
│                                 │
│ [Connect]  ← Click this         │
└─────────────────────────────────┘
```

### **When Connected**

```
┌─────────────────────────────────┐
│ 📊 QuickBooks                   │
│                                 │
│ Sync with QBO                   │
│ Connected [✓]                   │
│                                 │
│ [Configure] [↻ Sync] ← Buttons  │
└─────────────────────────────────┘
```

### **After Sync**

```
Recent Sync Activity
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ QuickBooks - Expense Sync
  150 records • Mar 16, 2:35 PM

✓ QuickBooks - Expense Sync
  25 records • Mar 16, 1:15 PM

✗ QuickBooks - Expense Sync
  0 records • Mar 16, 12:00 PM
  Error: Invalid Client Secret
```

---

## ⚙️ Admin Configuration Steps

### **1. Add GL Codes to Categories**

GL codes map your expense categories to QuickBooks accounts.

**What is a GL Code?**
- GL = General Ledger
- It's the accounting code in QB for that type of expense
- Example: Travel expenses might be code "4100"

**How to Add:**

```
1. In Admin Panel, go to:
   Configuration & Policy → Expense Categories

2. For each category, add a GL Code:
   
   Category: "Travel"
   GL Code: 4100
   
   Category: "Meals"
   GL Code: 4200
   
   Category: "Office Supplies"
   GL Code: 4300

3. When you sync, expenses use these GL codes
4. QB automatically puts them in the right account
```

### **2. Set Auto-Sync Frequency** (Optional)

```
When configuring QB:
- Hourly: Sync every 60 minutes
- Daily: Sync once per day (recommended) 
- Weekly: Sync once per week
- Manual: Only sync when you click button

Default: Daily at 2:00 AM
```

---

## 🔍 Troubleshooting

### **Test Connection Shows Nothing**

**Problem:** Click test button, nothing happens

**Solution:**
1. Make sure all 3 fields are filled
2. Check for spaces or typos
3. Verify credentials from Intuit Portal
4. Try again - should show green ✅ or orange ⚠️

### **Sync Shows 0 Records**

**Problem:** Says "Synced 0 expenses"

**Solutions:**
1. Make sure you added expenses first
2. Check Recent Sync Activity for errors
3. Verify GL codes are assigned to categories
4. Check if expenses are marked as already synced

### **QB Says "Invalid Credentials"**

**Problem:** Red error message about credentials

**Solutions:**
1. Double-check each value (copy-paste to verify)
2. Make sure Client Secret is from "Development" not "Production"
3. Verify Realm ID matches your company
4. Try creating a NEW app in Intuit Portal
5. Re-connect your QB account to get fresh Realm ID

### **Sync Completes but Expenses Don't Appear in QB**

**Problem:** Says "Synced 5" but nothing in QB

**Solutions:**
1. Log into QB, check Bills > All Bills
2. Create a new bill manually to verify QB is working
3. Check if GL codes are valid in your QB chart of accounts
4. Check sync logs for specific errors
5. Try sync again with fewer expenses (2-3)

---

## 💾 What Gets Saved & Where

### **In Cryptics Database:**

```
accounting_integration table:
- Platform: "quickbooks"
- API Key: Your Client ID
- API Secret: Your Client Secret (encrypted)
- Company ID: Your Realm ID
- Sync Frequency: "daily"
- Last Sync: Timestamp of last sync
- Status: Active/Inactive

sync_logs table:
- Date & time of each sync
- How many records synced
- Success/error status
- Error messages if any
```

### **In QuickBooks:**

```
Bills created with:
- Description: Your expense description
- Amount: From your expense
- Account: From GL code mapping
- Date: From your expense date
- Notes: "Imported from Cryptics Legion"
```

---

## ✅ Step-by-Step Quick Start Checklist

```
□ Step 1: Get 3 credentials from Intuit
  └─ Client ID
  └─ Client Secret
  └─ Realm ID

□ Step 2: Open Cryptics app
  └─ python Cryptics_legion/src/main.py

□ Step 3: Log in as ADMIN / ADMIN256

□ Step 4: Go to Accounting Integration
  └─ Configuration & Policy → Accounting Integration

□ Step 5: Click "Connect" on QuickBooks card

□ Step 6: Enter your 3 credentials and test

□ Step 7: Click "Save Configuration"

□ Step 8: QB card shows "Connected" ✅

□ Step 9: Add some test expenses (as regular user)

□ Step 10: Go back to Admin → Accounting Integration

□ Step 11: Click Sync button (↻)

□ Step 12: See green message "Synced X expenses"

□ Step 13: Log into QB and verify expenses appear

□ Step 14: Success! 🎉
```

---

## 🎓 Key Concepts to Understand

### **Syncable vs Synced Expenses**

```
Syncable (Not yet synced):
- New expenses added
- Never sent to QB
- Have synced_to_qb = 0

Synced (Already sent):
- Previously sent to QB
- Won't be sent again
- Have synced_to_qb = 1
```

### **GL Code Mapping**

```
Your App Side:          QB Side:
Category: Travel  →  GL Code 4100  →  Travel Expense Account
Category: Meals   →  GL Code 4200  →  Meals & Entertainment
Category: Office  →  GL Code 4300  →  Office Supplies
```

### **Sync Process**

```
Manual Sync (click button):
You control when → You click sync → Expenses go to QB

Auto Sync (daily/weekly):
Automatic on schedule → Expenses go to QB automatically
```

---

## 🚀 Advanced: What Happens Backend

### **API Communication**

```
Your App (Cryptics)
        ↓
OAuth2 Authentication
        ↓
Gets Access Token
        ↓
Uses Token to Call QB API
        ↓
QuickBooks Online
```

### **Security**

```
Credentials → Encrypted → Stored in DB → Only used for syncing
Never logged → Never displayed → Token expires & refreshes
```

### **Error Handling**

```
If sync fails:
1. Log the error with details
2. Don't mark expense as synced
3. Try again next sync
4. Show error to admin
5. Admin can troubleshoot
```

---

## 📞 Quick Reference Card

### **Where to Find Things**

| What | Where |
|------|-------|
| Configure QB | Admin → Configuration & Policy → Accounting Integration |
| Add GL Codes | Admin → Configuration & Policy → Expense Categories |
| Sync Manually | QB Card → Click Sync (↻) button |
| View Sync History | Below integration cards → Recent Sync Activity |
| QB App Creation | https://developer.intuit.com |
| Get Credentials | QB App → Settings tab |
| QB Bills | https://quickbooks.intuit.com → Transactions → Bills |

### **Common Figures**

| Metric | Value |
|--------|-------|
| Sync Speed | ~2-5 seconds for 10 expenses |
| Max Per Sync | Up to 1000 expenses |
| Auto Sync Interval | Hourly / Daily / Weekly |
| Token Refresh | Every 60 minutes |
| Retry Logic | Auto-retries failed syncs |

---

## 🎯 Use Cases

### **Scenario 1: Small Business**
```
Day 1: 
- Set up QB integration
- Map 5 expense categories to GL codes
- Add 20 test expenses

Day 2:
- Enable Daily auto-sync
- Expenses sync every night at 2 AM

Result: Zero manual QB data entry ✅
```

### **Scenario 2: Large Team**
```
Monday:
- Admin adds new categories
- Maps new GL codes
- Communicates to team

Throughout week:
- Team enters expenses normally
- No changes needed to QB

Friday:
- Admin reviews sync history
- 500+ expenses synced
- QB is auto-updated

Result: Automated accounting process ✅
```

### **Scenario 3: Troubleshooting**
```
Problem: Sync shows 0 records

Debug:
1. Check if expenses exist
   → Yes, 15 expenses added
   
2. Check if GL codes mapped
   → No! That's the issue
   
3. Go to Expense Categories, add GL codes
   
4. Try sync again
   → Success: "Synced 15 expenses" ✅
```

---

## 🎉 That's It!

You now understand:
✅ What QB integration does
✅ How to set it up
✅ How to use it
✅ What happens behind the scenes
✅ How to troubleshoot issues

**Next Step:** Follow the checklist above and do your first sync! 🚀
