# Admin Configuration & Policy System Documentation

## Overview
The ExpenseWise Admin system now includes comprehensive Configuration & Policy management tools that allow administrators to define rules, manage currencies, and integrate with external accounting systems.

## Features Implemented

### 1. Expense Categories Management
**Location:** Configuration & Policy → Expense Categories

**Features:**
- ✅ Create, Read, Update, Delete (CRUD) expense categories
- ✅ Assign GL (General Ledger) codes to categories
- ✅ Customize category icons and colors
- ✅ Support for subcategories (parent-child relationships)
- ✅ Active/Inactive status management

**Database Table:** `expense_categories`
- `id`: Primary key
- `name`: Category name (unique)
- `description`: Category description
- `gl_code`: General Ledger code for accounting integration
- `icon`: Icon identifier
- `color`: Hex color code
- `is_active`: Active status flag
- `parent_id`: For subcategory support
- `created_at`, `updated_at`: Timestamps

### 2. Policy Rules Configuration
**Location:** Configuration & Policy → Policy Rules

**Features:**
- ✅ Define automated expense policy constraints
- ✅ Set maximum spending limits per category
- ✅ Configure per diem rates
- ✅ Require receipts for specific categories/amounts
- ✅ Set approval requirements
- ✅ Define disallowed vendors
- ✅ Multi-currency support

**Database Table:** `policy_rules`
- `id`: Primary key
- `rule_name`: Rule identifier
- `rule_type`: Type of rule (spending_limit, per_diem, receipt_required, etc.)
- `category_id`: Associated category (optional)
- `max_amount`: Maximum allowed amount
- `currency`: Currency code
- `requires_receipt`: Boolean flag
- `requires_approval`: Boolean flag
- `disallowed_vendors`: Comma-separated vendor list
- `per_diem_rate`: Daily allowance rate
- `description`: Rule description
- `is_active`: Active status

**Rule Types:**
- `spending_limit`: Maximum spend constraint
- `per_diem`: Daily allowance configuration
- `receipt_required`: Receipt mandate
- `approval_required`: Approval workflow trigger
- `vendor_restriction`: Vendor blacklist

### 3. Currencies & Exchange Rates
**Location:** Configuration & Policy → Currencies & Exchange Rates

**Features:**
- ✅ Manage supported currencies
- ✅ Add/update exchange rates manually
- ✅ API integration for automatic rate updates
- ✅ Historical rate tracking
- ✅ Effective date management
- ✅ Rate source tracking (manual vs API)

**Database Table:** `currency_rates`
- `id`: Primary key
- `from_currency`: Source currency code
- `to_currency`: Target currency code
- `rate`: Exchange rate value
- `effective_date`: Rate effective date
- `is_active`: Active status
- `source`: Rate source (manual/api)
- `updated_at`: Last update timestamp

**Supported Operations:**
- View all active exchange rates
- Add new currency pairs
- Update existing rates
- Bulk update from API
- Deactivate obsolete rates

### 4. Accounting Integration
**Location:** Configuration & Policy → Accounting Integration

**Supported Platforms:**
- ✅ QuickBooks Online
- ✅ Xero
- ✅ SAP
- ✅ Oracle NetSuite

**Features:**
- ✅ Configure platform connections
- ✅ Secure API key management
- ✅ Auto-sync configuration
- ✅ Sync frequency settings (hourly, daily, weekly, manual)
- ✅ Sync activity logging
- ✅ Error tracking and reporting

**Database Tables:**

**`accounting_integration`:**
- `id`: Primary key
- `platform`: Platform name (quickbooks, xero, sap, netsuite)
- `api_key`: Encrypted API key
- `api_secret`: Encrypted API secret
- `company_id`: Company identifier in external system
- `sync_enabled`: Sync enabled flag
- `last_sync`: Last successful sync timestamp
- `sync_frequency`: Sync schedule
- `auto_sync`: Automatic sync flag
- `config_json`: Additional platform-specific configuration
- `is_active`: Active status

**`sync_logs`:**
- `id`: Primary key
- `integration_id`: Foreign key to accounting_integration
- `sync_type`: Type of sync operation
- `status`: Sync result (success/failure)
- `records_synced`: Number of records processed
- `error_message`: Error details if failed
- `started_at`: Sync start time
- `completed_at`: Sync completion time

## UI Design

### Sidebar Navigation
The admin interface features a professional sidebar navigation with:
- **Brand Logo:** ExpenseWise Admin branding
- **Collapsible Sections:**
  - Overview (Dashboard)
  - Expense Management
  - User & Group
  - Configuration & Policy ⭐ NEW
  - Reporting & Analytics

### Top Navigation Bar
- Universal search functionality
- Notifications center
- Admin user profile menu
- Quick logout access

### Configuration Pages
All configuration pages follow a consistent design pattern:
- **Header Section:** Page title, description, and primary action button
- **Content Area:** Data tables or card layouts
- **Action Dialogs:** Modal forms for CRUD operations
- **Status Indicators:** Visual feedback for active/inactive states
- **Responsive Design:** Adapts to different screen sizes

## API Functions

### Expense Categories
```python
# Get all categories
categories = db.get_expense_categories(include_inactive=False)

# Add category
category_id = db.add_expense_category(
    name="Travel",
    description="Business travel expenses",
    gl_code="6100",
    icon="flight",
    color="#2196F3"
)

# Update category
db.update_expense_category(
    category_id=1,
    name="Updated Name",
    is_active=1
)

# Delete category (soft delete)
db.delete_expense_category(category_id=1)
```

### Policy Rules
```python
# Get all rules
rules = db.get_policy_rules(include_inactive=False)

# Add rule
rule_id = db.add_policy_rule(
    rule_name="Travel Limit",
    rule_type="spending_limit",
    category_id=1,
    max_amount=5000.00,
    currency="PHP",
    requires_receipt=1
)

# Update rule
db.update_policy_rule(
    rule_id=1,
    max_amount=7500.00,
    requires_approval=1
)

# Delete rule
db.delete_policy_rule(rule_id=1)
```

### Currency Rates
```python
# Get rates
rates = db.get_currency_rates(from_currency="USD")

# Add rate
rate_id = db.add_currency_rate(
    from_currency="USD",
    to_currency="PHP",
    rate=56.50,
    source="manual"
)

# Update rate
db.update_currency_rate(rate_id=1, rate=57.00)
```

### Accounting Integration
```python
# Get integrations
integrations = db.get_accounting_integrations()

# Add integration
integration_id = db.add_accounting_integration(
    platform="quickbooks",
    api_key="your_api_key",
    company_id="12345",
    sync_enabled=1,
    sync_frequency="daily",
    auto_sync=1
)

# Log sync activity
db.log_sync_activity(
    integration_id=1,
    sync_type="expense_sync",
    status="success",
    records_synced=25
)

# Get sync logs
logs = db.get_sync_logs(integration_id=1, limit=50)
```

## Security Considerations

1. **API Keys:** All API keys and secrets are stored securely in the database
2. **Access Control:** Only authenticated admin users can access configuration pages
3. **Audit Logging:** All configuration changes are tracked in admin logs
4. **Data Validation:** Input validation on all forms
5. **Soft Deletes:** Critical data uses soft delete to maintain referential integrity

## Testing

To test the new features:

1. **Initialize Database:**
   ```bash
   python src/init_db.py
   ```

2. **Login as Admin:**
   - Use admin credentials
   - Navigate to Configuration & Policy section

3. **Test Each Feature:**
   - Add sample expense categories
   - Create policy rules
   - Configure exchange rates
   - Set up accounting integration

## Future Enhancements

- [ ] Real-time currency API integration
- [ ] Advanced policy rule engine with complex conditions
- [ ] Bi-directional sync with accounting platforms
- [ ] Budget allocation and tracking
- [ ] Automated policy violation alerts
- [ ] Role-based access control for config sections
- [ ] Export/import configuration templates
- [ ] Multi-currency conversion in expense entry
- [ ] Policy compliance dashboard

## Support

For questions or issues, refer to:
- `ADMIN_SYSTEM_DOCUMENTATION.md` - Overall admin system docs
- `ADMIN_IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- Database schema in `src/core/db.py`
