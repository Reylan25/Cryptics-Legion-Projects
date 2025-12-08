# ExpenseWise Admin - Quick Navigation Guide

## 🎯 Main Navigation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   ExpenseWise Admin                          │
│                                                               │
│  ┌──────────────┐  ┌───────────────────────────────────┐   │
│  │   SIDEBAR    │  │      MAIN CONTENT AREA             │   │
│  │              │  │                                     │   │
│  │ 📊 Dashboard │  │  [Top Bar: Search | Notifications | │   │
│  │              │  │           Admin User Menu]          │   │
│  │ 📁 Expense   │  │                                     │   │
│  │   Management │  │  ┌───────────────────────────┐    │   │
│  │              │  │  │    PAGE CONTENT            │    │   │
│  │ 👥 User &    │  │  │                            │    │   │
│  │   Group      │  │  │  • Stats Cards             │    │   │
│  │              │  │  │  • Data Tables             │    │   │
│  │ ⚙️ Config &  │  │  │  • Forms & Actions         │    │   │
│  │   Policy ⭐  │  │  │  • Charts & Graphs         │    │   │
│  │              │  │  │                            │    │   │
│  │ 📊 Reporting │  │  └───────────────────────────┘    │   │
│  │              │  │                                     │   │
│  └──────────────┘  └───────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Configuration & Policy Section

### Menu Structure
```
⚙️ Configuration & Policy
  ├── 📋 Policy Rules
  ├── 💱 Currencies & Exchange Rates
  └── 🔗 Accounting Integration
```

### 1️⃣ Policy Rules Page

**What you'll see:**
- List of all policy rules in a table
- "Add Rule" button (top right)
- Rule details: Name, Type, Category, Constraints, Status
- Edit/Delete actions per rule

**Actions:**
```
┌──────────────────────────────────────┐
│  + Add Rule                          │
└──────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Rule Name │ Category │ Constraints │ Status │ ⚙️│
├─────────────────────────────────────────────────┤
│ Travel    │ Travel   │ Max: ₱5,000 │ Active │ ✏️│
│ Limit     │          │ Receipt Req │        │ 🗑️│
├─────────────────────────────────────────────────┤
│ Meal      │ Meals    │ Per Diem:   │ Active │ ✏️│
│ Allowance │          │ ₱500        │        │ 🗑️│
└─────────────────────────────────────────────────┘
```

**Dialog Form (Add/Edit):**
- Rule Name
- Rule Type (Dropdown)
- Category (Optional)
- Maximum Amount
- Currency
- Per Diem Rate
- Receipt Required (Toggle)
- Approval Required (Toggle)
- Disallowed Vendors
- Description

### 2️⃣ Currencies & Exchange Rates Page

**What you'll see:**
- Stats cards: Total Rates, Base Currency, Last Updated
- "Update Rates" button (fetch from API)
- "Add Rate" button
- Currency pair table with rates

**Layout:**
```
┌─────────────┬─────────────┬─────────────┐
│ Total Rates │ Base Curr.  │ Last Update │
│     25      │    PHP      │ Dec 9, 2025 │
└─────────────┴─────────────┴─────────────┘

┌──────────────────────────────────────────────────┐
│ 🔄 Update Rates    + Add Rate                    │
└──────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ Pair      │ Rate     │ Date      │ Source │ Status│
├────────────────────────────────────────────────────┤
│ USD → PHP │ 56.5000  │ Dec 9     │ API    │ Active│
│ EUR → PHP │ 61.2000  │ Dec 9     │ API    │ Active│
│ GBP → PHP │ 71.3000  │ Dec 9     │ Manual │ Active│
└────────────────────────────────────────────────────┘
```

**Actions:**
- ✏️ Edit rate
- 🗑️ Delete rate
- 🔄 Bulk update from API

### 3️⃣ Accounting Integration Page

**What you'll see:**
- Platform cards (QuickBooks, Xero, SAP, NetSuite)
- Connection status per platform
- Recent sync activity logs
- "Add Integration" button

**Platform Cards Layout:**
```
┌─────────────────┐  ┌─────────────────┐
│  📊 QuickBooks  │  │  ☁️ Xero        │
│  Connected ✅   │  │  Not Connected  │
│                 │  │                 │
│ Sync with QB    │  │ Connect to      │
│ Online platform │  │ Xero accounting │
│                 │  │                 │
│ [Configure] 🔄  │  │ [Connect]       │
└─────────────────┘  └─────────────────┘

┌─────────────────┐  ┌─────────────────┐
│  🏢 SAP         │  │  🏛️ NetSuite    │
│  Connected ✅   │  │  Not Connected  │
│                 │  │                 │
│ Enterprise SAP  │  │ Oracle NetSuite │
│ integration     │  │ ERP platform    │
│                 │  │                 │
│ [Configure] 🔄  │  │ [Connect]       │
└─────────────────┘  └─────────────────┘
```

**Recent Sync Activity:**
```
┌────────────────────────────────────────────────┐
│ ✅ QuickBooks - Expense Sync                   │
│    25 records • Dec 9, 2:30 PM                │
├────────────────────────────────────────────────┤
│ ✅ SAP - Expense Sync                          │
│    18 records • Dec 9, 1:15 PM                │
├────────────────────────────────────────────────┤
│ ❌ Xero - Expense Sync                         │
│    0 records • Dec 9, 12:00 PM (Auth Error)   │
└────────────────────────────────────────────────┘
```

## 🎨 Color Scheme

- **Background Dark:** `#1C1C1E`
- **Surface Dark:** `#2C2C2E`
- **Surface Darker:** `#2D2D30`
- **Border:** `#383838` / `GREY_800`
- **Primary Blue:** `#2196F3` / `BLUE_700`
- **Success Green:** `GREEN_700`
- **Warning Orange:** `ORANGE_700`
- **Error Red:** `RED_700`

## 🎯 User Workflows

### Workflow 1: Add Expense Category
1. Click "Configuration & Policy" in sidebar
2. Select "Expense Categories"
3. Click "+ Add Category" button
4. Fill form:
   - Category Name: "Travel"
   - Description: "Business travel expenses"
   - GL Code: "6100"
   - Icon: Select "Flight"
   - Color: "#2196F3"
5. Click "Add Category"
6. ✅ Success! Category appears in table

### Workflow 2: Create Policy Rule
1. Navigate to "Policy Rules"
2. Click "+ Add Rule"
3. Fill form:
   - Rule Name: "Travel Expense Limit"
   - Rule Type: "Spending Limit"
   - Category: Select "Travel"
   - Max Amount: "5000"
   - Currency: "PHP"
   - Toggle "Receipt Required" ON
4. Click "Add Rule"
5. ✅ Rule is active and enforced

### Workflow 3: Update Exchange Rates
1. Go to "Currencies & Exchange Rates"
2. Click "🔄 Update Rates" button
3. System fetches latest rates from API
4. ✅ Table updates with new rates
5. Notification: "Updated 4 exchange rates!"

### Workflow 4: Configure Accounting Integration
1. Navigate to "Accounting Integration"
2. Click "Connect" on QuickBooks card
3. Fill integration form:
   - Platform: QuickBooks
   - API Key: (your key)
   - Company ID: "12345"
   - Sync Frequency: "Daily"
   - Toggle "Auto-Sync" ON
4. Click "Add Integration"
5. ✅ QuickBooks now shows "Connected"
6. Click "🔄" to sync immediately

## 📱 Responsive Behavior

### Desktop (>1200px)
- Sidebar: Expanded with text
- Stats: 6 cards per row
- Tables: All columns visible

### Tablet (768-1200px)
- Sidebar: Collapsible
- Stats: 3 cards per row
- Tables: Important columns only

### Mobile (<768px)
- Sidebar: Hidden, hamburger menu
- Stats: 1-2 cards per row
- Tables: Card-based layout

## 🎓 Tips & Tricks

### Quick Actions
- **Search:** Use universal search bar to find anything
- **Notifications:** Click bell icon for system alerts
- **User Menu:** Quick access to settings and logout

### Keyboard Shortcuts (Future)
- `Ctrl+K`: Open search
- `Ctrl+N`: Add new item (context-aware)
- `Esc`: Close dialogs

### Best Practices
1. **Always add GL codes** to categories for accounting sync
2. **Test integrations** in sandbox mode first
3. **Review sync logs** regularly for errors
4. **Keep exchange rates updated** for accuracy
5. **Document policy rules** with clear descriptions

---

**Need Help?**
- 📖 See `ADMIN_CONFIGURATION_POLICY_DOCS.md` for detailed docs
- 🚀 See `ADMIN_QUICK_START.md` for quick start guide
- 💡 See `ADMIN_FEATURES_SUMMARY.md` for feature overview
