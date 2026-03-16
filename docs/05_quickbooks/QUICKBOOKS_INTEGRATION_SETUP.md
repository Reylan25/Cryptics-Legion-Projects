# QuickBooks Online Integration Setup Guide

## Overview
This guide walks you through setting up QuickBooks Online integration with Cryptics Legion Admin Panel.

## Prerequisites
- Active QuickBooks Online account
- Admin access to Cryptics Legion
- Intuit Developer account

---

## Step 1: Create Intuit Developer App

### 1.1 Go to Intuit Developer Portal
- Visit: https://developer.intuit.com
- Sign in with your Intuit account (or create one if needed)

### 1.2 Create or Select an App
1. Click **"Create an app"** button in your dashboard
2. Choose **"Accounting"** as the product
3. Click **"Create app"**
4. Give your app a name (e.g., "Cryptics Legion QBO Sync")

### 1.3 Get Your Credentials
1. Navigate to your app's **Settings** page
2. Under **Development** section, find:
   - **Client ID** - Copy this value
   - **Client Secret** - Copy this value (keep it secret!)

---

## Step 2: Get Your Realm ID (Company ID)

### 2.1 Connect Your QuickBooks Account
1. Go to your app's **Development** page
2. In the **QuickBooks Sandbox** section, click **"Connect to Sandbox"** (or **"Connect to Production"** if using live data)
3. Log in with your QuickBooks Online credentials
4. Accept the permissions

### 2.2 Find Your Realm ID
After connecting, you'll see your **Realm ID** displayed on the page. This is your Company ID.

**Format:** `1234567890`

---

## Step 3: Configure in Cryptics Legion Admin

### 3.1 Access Admin Panel
1. Log in to Cryptics Legion with admin credentials
2. Navigate to **Configuration & Policy** → **Accounting Integration**

### 3.2 Connect QuickBooks
1. Click the **"Connect"** button on the **QuickBooks** card
2. A dialog box will appear
3. Fill in the following fields:
   - **Client ID:** Paste your Client ID from Step 1.3
   - **Client Secret:** Paste your Client Secret from Step 1.3
   - **Realm ID (Company ID):** Paste your Realm ID from Step 2.2

### 3.3 Test Connection
1. Click **"Test Connection"** button
2. Wait for the verification result
3. If successful, you'll see: "Connected to [Your Company Name]"
4. If failed, verify all credentials are correct

### 3.4 Save Configuration
1. Click **"Save Configuration"** button
2. You'll see a success message
3. QuickBooks card will now show **"Connected"**

---

## Step 4: Configure Sync Settings

Once connected, you can configure:

### Auto-Sync (Optional)
- **Frequency:** Hourly, Daily, Weekly, or Manual
- **Default:** Daily
- Leave **Auto-Sync** disabled initially to control when syncs happen

### Sync Frequency Options
- **Hourly:** Sync every hour (best for high-volume expenses)
- **Daily:** Sync once per day (default, recommended)
- **Weekly:** Sync once per week (for lower volume)
- **Manual:** Only sync when you click "Sync Now"

---

## Step 5: First Sync

### 5.1 Manual Sync
1. Find the connected **QuickBooks** card
2. Click the **Sync** icon (↻) to start your first sync
3. Monitor the progress bar
4. Check sync logs for results

### 5.2 Check Sync Logs
1. Scroll down to **"Recent Sync Activity"** section
2. You'll see:
   - Sync status (Success/Error/Warning)
   - Number of records synced
   - Timestamp
   - Any error messages

---

## Step 6: Map Expense Categories (Important!)

For proper accounting classification:

1. Go to **Configuration & Policy** → **Expense Categories**
2. For each category, add a **GL Code** that matches your QuickBooks Chart of Accounts:
   - Example: "Travel" → GL Code "4100"
   - Example: "Meals" → GL Code "4200"

**Note:** GL codes help expenses automatically map to the correct QuickBooks accounts.

---

## Troubleshooting

### Connection Fails
**Issue:** "Connection failed" or authentication error

**Solutions:**
1. Verify Client ID and Secret are exactly correct (check for spaces)
2. Verify Realm ID (Company ID) is correct
3. Ensure your Intuit Developer account is active
4. Check if you're using Sandbox (development) or Production credentials

### Sync Shows 0 Records
**Issue:** Sync completes but syncs 0 expenses

**Solutions:**
1. Verify you have expenses added in Cryptics Legion
2. Check if expense dates are recent
3. Ensure categories have GL codes assigned
4. Contact support if problem persists

### Access Denied / Permission Error
**Issue:** "Insufficient Permissions" error during sync

**Solutions:**
1. Re-connect your QuickBooks account
2. In the connection dialog, ensure you grant all requested permissions
3. Verify your QuickBooks user has admin access

### Token Expired
**Issue:** Sync fails with "Invalid token" after weeks of use

**Solutions:**
1. This is normal - tokens expire periodically
2. Re-test the connection to refresh the token
3. The system will auto-refresh tokens if possible

---

## Best Practices

✅ **DO:**
- Test connection before enabling auto-sync
- Add GL codes to all expense categories
- Review sync logs after each sync
- Keep Client Secret secure - never share it
- Use Production credentials after testing in Sandbox

❌ **DON'T:**
- Share your Client Secret publicly
- Manually edit synced expenses in QuickBooks (causes conflicts)
- Disable the integration without archiving sync history
- Forget to map GL codes (expenses may not sync properly)

---

## Expected Workflow

1. **Admin adds expenses** → Marked as "unsynced" in database
2. **Manual/Auto sync runs** → Expenses sent to QuickBooks
3. **QuickBooks creates bills** → Based on expense data and GL codes
4. **Sync log updated** → Shows success/errors
5. **Expenses marked synced** → Won't be sent again

---

## Security Notes

- All API credentials are encrypted in the database
- Sync logs do not store sensitive data
- Use API keys with limited scopes (QuickBooks only)
- Rotate Client Secret periodically for security
- Monitor sync logs for unauthorized activity

---

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review sync logs in Recent Sync Activity
3. Verify GL codes are assigned to categories
4. Contact your system administrator

---

## Additional Resources

- QuickBooks Online API Docs: https://developer.intuit.com/docs/api/quickbooks-online
- Intuit Developer Portal: https://developer.intuit.com
- QuickBooks Chart of Accounts: Your QBO account under Settings → Chart of Accounts
