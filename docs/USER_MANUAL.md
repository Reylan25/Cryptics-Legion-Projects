# Smart Expense Tracker - User Manual

## Overview

Welcome to **Smart Expense Tracker**, a comprehensive personal finance management application built with Flet. This manual will guide you through using all features of the app to effectively manage your expenses, accounts, and financial goals.

### What You Can Do
- Track personal and business expenses
- Manage multiple bank accounts and wallets
- View detailed financial analytics and reports
- Convert between 10 different currencies
- Secure your data with passcode protection
- Reset passwords via email OTP
- Access admin features (if you have admin privileges)

---

## Getting Started

### First Time Setup

1. **Launch the App**
   - Run `python Cryptics_legion/src/main.py` from the project root
   - Or use your preferred package manager: `uv run flet run`

2. **Create Your Account**
   - Click "Register" on the login screen
   - Fill in your personal details (name, email, phone, etc.)
   - Set your preferred currency and timezone
   - Create a secure passcode for app protection

3. **Complete Onboarding**
   - Follow the guided setup process
   - Set up your first account (bank, wallet, etc.)
   - Review the app features

### Default Admin Account
For testing purposes, a default admin account is available:
- **Username:** ADMIN
- **Password:** ADMIN256

---

## Main Navigation

### Bottom Navigation Bar
The app uses a persistent bottom navigation for easy access:

- **🏠 Home**: Dashboard with balance overview and recent activity
- **💰 Expenses**: View and manage all expenses
- **📊 Statistics**: Charts and financial analytics
- **👤 Profile**: Account settings and personal information

### Quick Actions
From the Home screen, you can quickly:
- Add new expenses
- View recent transactions
- Check account balances
- Access settings

---

## Managing Accounts

### Adding Your First Account

1. Go to **Profile** → **Account Settings**
2. Click **"Add Account"**
3. Choose account type:
   - **Bank Account**: Traditional banking
   - **Wallet**: Cash or digital wallet
   - **Credit Card**: Credit accounts
   - **Savings**: Savings accounts
4. Fill in details:
   - Account name (e.g., "Main Checking")
   - Account number (optional)
   - Initial balance
   - Currency
   - Color (for visual identification)

### Managing Multiple Accounts

- **Switch Accounts**: Use the account selector in expense forms
- **Edit Accounts**: Modify details, update balances
- **Archive Accounts**: Hide inactive accounts
- **Primary Account**: Set one account as your main account

---

## Expense Tracking

### Adding Expenses

1. **Quick Add** (from Home screen):
   - Tap the **"+"** button
   - Select account
   - Enter amount and category
   - Add description (optional)

2. **Detailed Add** (from Expenses screen):
   - Go to **Expenses** → **Add Expense**
   - Fill in comprehensive details:
     - Amount and currency
     - Category (Food, Transport, Entertainment, etc.)
     - Date and time
     - Description
     - Receipt photo (future feature)

### Expense Categories

Pre-defined categories include:
- 🍽️ Food & Dining
- 🚗 Transportation
- 🏠 Housing
- 🛍️ Shopping
- 🎬 Entertainment
- 💼 Business
- 🏥 Health & Medical
- 📚 Education
- ✈️ Travel
- 💡 Utilities
- 📱 Phone & Internet
- 🎁 Gifts
- 💰 Income
- 🔄 Transfer

### Editing and Deleting Expenses

1. Go to **Expenses** screen
2. Find the expense you want to modify
3. Tap the expense item
4. Choose **Edit** or **Delete**
5. Confirm changes

---

## Financial Analytics

### Dashboard Overview

The **Home** screen shows:
- **Balance Gauge**: Visual representation of your financial health
- **Recent Expenses**: Last 5 transactions
- **Quick Stats**: Total expenses this month
- **Account Balances**: Current balances across all accounts

### Detailed Statistics

Access **Statistics** screen for:
- **Monthly Trends**: Expense patterns over time
- **Category Breakdown**: Spending by category (pie chart)
- **Account Analysis**: Performance per account
- **Currency Conversion**: View expenses in different currencies

### Export Options

- **PDF Reports**: Generate monthly/yearly reports
- **CSV Export**: Download transaction data
- **Print Reports**: Print-friendly formats

---

## Currency Management

### Supported Currencies

The app supports 10 currencies:
- 🇵🇭 PHP (Philippine Peso)
- 🇺🇸 USD (US Dollar)
- 🇪🇺 EUR (Euro)
- 🇬🇧 GBP (British Pound)
- 🇯🇵 JPY (Japanese Yen)
- 🇰🇷 KRW (South Korean Won)
- 🇸🇬 SGD (Singapore Dollar)
- 🇦🇺 AUD (Australian Dollar)
- 🇨🇦 CAD (Canadian Dollar)
- 🇮🇳 INR (Indian Rupee)

### Setting Your Currency

1. Go to **Profile** → **Personal Details**
2. Select your preferred currency
3. Set your timezone and first day of week

### Real-time Exchange Rates

- Automatic rate updates using Fixer.io API
- Manual rate override capability
- Historical rate tracking
- Multi-currency expense viewing

---

## Security Features

### Passcode Protection

1. **Setup Passcode**:
   - Go to **Profile** → **Security**
   - Set a 4-6 digit numeric passcode
   - Confirm passcode

2. **Using Passcode**:
   - App requires passcode on launch
   - Automatic lock after period of inactivity
   - Forgot passcode? Use email reset

### Password Reset

1. On login screen, click **"Forgot Password?"**
2. Enter your registered email
3. Check email for OTP code
4. Enter OTP and set new password

### Biometric Authentication (Future)

- Fingerprint recognition
- Face ID support
- Device-specific security

---

## Admin Features (Admin Users Only)

### Accessing Admin Panel

1. Login with admin credentials
2. Admin dashboard loads automatically
3. Navigate using sidebar menu

### Admin Functions

#### User Management
- View all registered users
- Manage user accounts
- Reset user passwords
- View user activity logs

#### System Configuration
- **Expense Categories**: Add/edit/delete categories
- **Policy Rules**: Set spending limits and approval workflows
- **Currency Rates**: Manage exchange rates
- **Accounting Integration**: Connect to external accounting software

#### Activity Monitoring
- View system logs
- Monitor user activity
- Track expense patterns
- Generate reports

### Admin Navigation

```
Admin Dashboard
├── Overview (Stats & Metrics)
├── Expense Management
├── User & Group Management
├── Configuration & Policy
│   ├── Expense Categories
│   ├── Policy Rules
│   ├── Currencies & Exchange Rates
│   └── Accounting Integration
└── Reporting & Analytics
```

---

## Data Management

### Backup Your Data

The app automatically saves data to:
- `Cryptics_legion/src/database/expense_tracker.db`

**Manual Backup**:
1. Locate the database file
2. Copy to external storage
3. Store securely

### Data Export

1. Go to **Profile** → **Data Export**
2. Choose export format (CSV/PDF)
3. Select date range
4. Download file

### Privacy Settings

- **Data Retention**: Control how long data is kept
- **Sharing Preferences**: Opt-in/out of analytics
- **Account Deletion**: Permanently remove your account

---

## Troubleshooting

### Common Issues

#### App Won't Start
- Ensure Python 3.9+ is installed
- Check if all dependencies are installed
- Verify database file exists

#### Database Errors
- Close and restart the app
- Check file permissions on database folder
- Contact support if persistent

#### Currency Rates Not Loading
- Check internet connection
- Verify API service status
- Use manual rate entry as fallback

#### Email OTP Not Received
- Check spam/junk folder
- Verify Gmail credentials in settings
- Ensure app password is correct

#### Performance Issues
- Clear app cache
- Restart device
- Update to latest app version

### Getting Help

1. **In-App Help**: Access help from Profile menu
2. **Documentation**: Check `docs/` folder for detailed guides
3. **Community Support**: GitHub issues and discussions
4. **Admin Support**: Contact system administrator

---

## Advanced Features

### Custom Categories

Create personalized expense categories:
1. Go to **Settings** → **Categories**
2. Add custom category with icon and color
3. Use in expense tracking

### Budget Alerts (Planned)

Set spending limits and get notifications:
- Daily spending alerts
- Monthly budget warnings
- Category-specific limits

### Recurring Expenses (In Development)

Automate regular expenses:
- Set up recurring transactions
- Monthly subscriptions
- Automatic expense creation

### Multi-Device Sync (Future)

Access data across devices:
- Cloud synchronization
- Real-time updates
- Secure data encryption

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New expense |
| `Ctrl+F` | Search expenses |
| `Ctrl+E` | Export data |
| `Ctrl+P` | Print report |
| `Ctrl+,` | Open settings |
| `F1` | Help |
| `Esc` | Go back |

---

## Best Practices

### Daily Habits
- Record expenses immediately
- Categorize accurately
- Review weekly spending
- Update account balances regularly

### Monthly Routines
- Generate monthly reports
- Review category spending
- Adjust budgets as needed
- Archive old data

### Security Tips
- Use strong passcode
- Enable biometric auth (when available)
- Regular password changes
- Keep app updated

### Data Management
- Regular backups
- Clean old data periodically
- Export important reports
- Monitor storage usage

---

## Frequently Asked Questions

### General Questions

**Q: Is my data secure?**
A: Yes, data is encrypted and stored locally. Admin features include audit logging.

**Q: Can I use the app offline?**
A: Yes, basic features work offline. Currency rates require internet.

**Q: How many accounts can I add?**
A: Unlimited accounts supported.

**Q: Can I share expenses with others?**
A: Currently individual use only. Multi-user sharing planned for future.

### Technical Questions

**Q: What are the system requirements?**
A: Python 3.9+, 512MB RAM, 500MB storage.

**Q: Which platforms are supported?**
A: Windows, macOS, Linux, iOS, Android, Web.

**Q: How do I update the app?**
A: Pull latest changes from GitHub and reinstall dependencies.

**Q: Can I customize the interface?**
A: Dark theme available. More customization options coming soon.

---

## Version Information

- **Current Version**: 0.2.0
- **Last Updated**: December 2025
- **Platform**: Cross-platform (Flet framework)
- **Database**: SQLite
- **UI Framework**: Flet (Flutter-inspired)

---

## Support & Contact

### Getting Help
- **Documentation**: `docs/` folder in project
- **GitHub Issues**: Report bugs and request features
- **Community**: Join discussions on GitHub

### Contact Information
- **Project Repository**: https://github.com/Reylan25/Cryptics-Legion-Projects
- **Documentation**: Comprehensive guides in `docs/` folder
- **Admin Support**: Contact system administrator for account issues

---

Thank you for using Smart Expense Tracker! We hope this manual helps you effectively manage your finances. For the latest updates and new features, check the project repository regularly.