# QuickBooks Integration - Quick Reference Guide

## 🎯 Access QuickBooks Integration

### Step 1: Admin Login
```
Login Page
  ↓
Username: ADMIN
Password: ADMIN256
  ↓
Admin Dashboard
```

### Step 2: Navigate to Accounting Integration
```
Admin Dashboard
  ↓
Left Sidebar → Configuration & Policy
  ↓
Click "Accounting Integration"
  ↓
Accounting Integration Page
```

---

## 📋 Accounting Integration Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Accounting Integration                                      │
│  Connect and sync with external accounting platforms    [+]  │
└─────────────────────────────────────────────────────────────┘

Available Integrations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────────┐  ┌──────────────────────┐
│ 📊 QuickBooks       │  │ ☁️ Xero             │
│ Not Connected    [×]│  │ Not Connected    [×]│
│                      │  │                      │
│ Sync with QBO       │  │ Connect to Xero     │
│                      │  │                      │
│ [Connect] [↻]       │  │ [Connect]           │
└──────────────────────┘  └──────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│ 💼 SAP              │  │ 🏢 NetSuite         │
│ Not Connected    [×]│  │ Not Connected    [×]│
│                      │  │                      │
│ Enterprise SAP      │  │ Oracle NetSuite     │
│                      │  │                      │
│ [Connect]           │  │ [Connect]           │
└──────────────────────┘  └──────────────────────┘

Recent Sync Activity
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ No sync history yet
```

---

## 🔗 QuickBooks Configuration Flow

### First Connection

```
Click "Connect" on QuickBooks
        ↓
Configuration Dialog Opens
        ↓
Enter Credentials:
  • Client ID: [__________________]
  • Client Secret: [__________________]
  • Realm ID: [__________________]
        ↓
[Test Connection] Button
        ↓
Success: "Connected to [Company Name]"
        ↓
[Save Configuration] Button
        ↓
Success Message
        ↓
QuickBooks Card now shows "Connected"
```

### Reconnecting (Update Credentials)

```
Click "Configure" on connected QBO card
        ↓
Dialog opens with existing settings
        ↓
Update any field (Client ID, Secret, Realm ID)
        ↓
[Test Connection] to verify
        ↓
[Save Configuration]
```

---

## 📊 Manual Sync Process

```
QuickBooks Card (Connected)
        ↓
Click Sync Button (↻)
        ↓
Sync Starts (Blue Progress)
  "Syncing with QuickBooks..."
        ↓
System:
  1. Fetches unsynced expenses
  2. Creates bills in QuickBooks
  3. Maps GL codes to accounts
  4. Logs activity
        ↓
Sync Completes
        ↓
Success/Error Message
  "Synced X expenses to QuickBooks"
        ↓
Recent Sync Activity Updated
```

---

## 📋 Recent Sync Activity Display

```
Recent Sync Activity
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ QuickBooks - Expense Sync
  25 records • Mar 16, 10:35 AM

✗ QuickBooks - Expense Sync
  0 records • Mar 16, 09:15 AM
  Error: API authentication failed

✓ QuickBooks - Expense Sync
  12 records • Mar 16, 08:00 AM

[Load More...]
```

---

## ⚙️ Configuration Details

### Client ID
**What it is:** Public identifier for your application
**Where to get:** Intuit Developer Portal > Your App > Settings
**Format:** Long alphanumeric string (e.g., `ABCDEFjd8jfkDLkfjdlfj...`)
**Security:** Safe to share, not sensitive

### Client Secret
**What it is:** Private authentication key
**Where to get:** Intuit Developer Portal > Your App > Settings
**Format:** Encrypted string
**Security:** ⚠️ KEEP PRIVATE - Don't share!
**Action if compromised:** Generate new secret immediately

### Realm ID
**What it is:** Your QuickBooks company identifier
**Where to get:** After connecting QBook account in Intuit Portal
**Format:** Numeric (e.g., `1234567890`)
**Security:** Tied to specific company - not widely sensitive

---

## 🔄 Sync Frequency Options

### ⏰ Hourly
- **Frequency:** Every hour
- **Best for:** High-volume expenses (100+ per day)
- **Database Impact:** Moderate
- **API Calls:** 24 per day

### 📅 Daily (Recommended)
- **Frequency:** Once per day (default 2 AM)
- **Best for:** Most businesses (default)
- **Database Impact:** Low
- **API Calls:** 1 per day

### 📆 Weekly
- **Frequency:** Once per week
- **Best for:** Low-volume expenses (<10 per week)
- **Database Impact:** Very low
- **API Calls:** 4 per month

### 🖱️ Manual
- **Frequency:** Only when you click sync
- **Best for:** Testing or irregular usage
- **Database Impact:** Minimal
- **API Calls:** As needed

---

## 🛠️ Status Indicators

### Connection Status

```
NOT CONNECTED [×]              CONNECTED [✓]
(Gray background)              (Green background)
                               
Click: [Connect]               Click: [Configure]
Only shows in setup dialog     See sync button (↻)
```

### Sync Status

```
SUCCESS ✓                PARTIAL ⚠️              ERROR ✗
(Green checkmark)        (Orange warning)       (Red X)

All expenses synced      Some failed            Sync failed entirely

Example:                 Example:                Example:
✓ 25 records synced      ⚠️ 15 of 25 synced     ✗ 0 records synced
                            (10 errors)            API offline
```

---

## 📋 Expected Behavior

### Before First Sync
- QuickBooks card shows "Not Connected"
- No sync button visible
- Recent Sync Activity is empty

### After Configuration
- QuickBooks card shows "Connected"
- Sync button (↻) appears
- Status badge shows green checkmark

### After Successful Sync
- Success message appears
- Recent Sync Activity updated with results
- Expenses marked as "synced" in database

### On Sync Error
- Error message displayed with details
- Sync log shows error status
- Failed expenses not marked as synced (will retry next run)

---

## 🔐 Security Features

✅ **Auto-Refresh Tokens**
- Access tokens expire every 60 minutes
- System automatically refreshes before expiry
- No manual re-authentication needed

✅ **Encrypted Storage**
- Client secrets encrypted in database
- API keys never logged in plain text
- Credentials encrypted at rest

✅ **Limited Permissions**
- Only "Accounting" scope requested
- No access to personal data
- Read-only or write-only as appropriate

✅ **Audit Logs**
- All syncs logged with timestamp
- Success/failure tracked
- Error messages captured for troubleshooting

---

## 🚀 Tips & Tricks

### Best Practices
1. **Test first:** Always click "Test Connection" after setup
2. **Start manual:** Use manual sync first before enabling auto-sync
3. **Map GL codes:** Assign GL codes to all expense categories
4. **Monitor logs:** Check Recent Sync Activity regularly
5. **Backup:** Ensure database backups before large syncs

### Quick Troubleshooting
| Problem | Quick Fix |
|---------|-----------|
| Connection fails | Copy-paste credentials again (check spaces) |
| 0 records synced | Verify expenses exist & categories have GL codes |
| Sync takes long | Check internet connection & QB server status |
| Old expenses vanish | Likely already synced (check QB account) |

### Common Questions
**Q: How often can I sync?**
A: As often as you want - no rate limits, but default is daily

**Q: Do synced expenses show in QB immediately?**
A: Yes, usually within 1-2 seconds per expense

**Q: Can I undo a sync?**
A: You must manually delete from QB or configure GL code differently

**Q: Will this affect my expenses in Cryptics?**
A: No, expenses stay in both systems independently

---

## 📞 Support Resources

### For Setup Help
1. Read: `QUICKBOOKS_INTEGRATION_SETUP.md`
2. Get credentials from: https://developer.intuit.com
3. Find Realm ID in: QBO Settings after connecting

### For Issues
1. Check sync logs for error details
2. Verify GL codes on categories
3. Test connection to refresh token
4. Check internet connectivity

### For Feature Requests
- Email: support@crypticslabs.com
- Portal: Check documentation for latest updates

---

## 📈 Performance Notes

**Typical Sync Times:**
- 10 expenses: ~5 seconds
- 25 expenses: ~10 seconds
- 50 expenses: ~20 seconds
- 100 expenses: ~40 seconds

**Database Growth:**
- Each sync adds 1-2 log entries
- Logs archived monthly
- No performance impact

---

## 🎓 Getting Your Credentials

### Intuit Developer Portal Flow

```
1. Visit: https://developer.intuit.com

2. Sign In / Create Account
   └─ Use Intuit ID or Apple/Google sign-in

3. Go to Apps
   └─ Click "Create an app"
      └─ Select "Accounting"
      └─ Name it "Cryptics Legion QBO Sync"

4. Get Credentials (Development tab)
   ├─ Client ID: Copy this
   ├─ Client Secret: Copy this
   └─ Keep both secure!

5. Connect to QuickBooks
   ├─ Click "Connect to Sandbox" or "Connect to Production"
   ├─ Log in with QBO credentials
   ├─ Accept permissions
   └─ Note down Realm ID shown after connection

6. Copy credentials to Cryptics Admin
   └─ Paste in Configuration dialog
```

---

## ✅ Go-Live Checklist

Before using in production:

- [ ] Created app in Intuit Developer Portal
- [ ] Got credentials (Sandbox tested first)
- [ ] Connected to QuickBooks Successfully
- [ ] Test sync working (shows in Recent Activity)
- [ ] Added GL codes to expense categories
- [ ] Reviewed recent sync activity
- [ ] Documented company's expense categories
- [ ] Set sync frequency
- [ ] Trained admin users on how to use
- [ ] Tested error scenarios
- [ ] Set up backup procedures
- [ ] ✅ Ready for production!
