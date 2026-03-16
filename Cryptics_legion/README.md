# 📦 Cryptics Legion

Main application source code for the Smart Expense Tracker.

## 📁 Folder Structure

```
Cryptics_legion/
├── src/                           # Application source code
│   ├── main.py                   # Application entry point
│   ├── init_db.py                # Database initialization
│   ├── init_admin.py             # Admin account setup
│   ├── expense_tracker.db        # SQLite database
│   │
│   ├── core/                     # Core modules
│   │   ├── auth.py              # Authentication logic
│   │   ├── db.py                # Database operations
│   │   └── theme.py             # UI theming
│   │
│   ├── ui/                       # User interface pages (organized by category)
│   │   ├── auth/                # Login, Register, Password Reset
│   │   ├── onboarding/          # Onboarding wizard
│   │   ├── user/                # Main user features
│   │   ├── profile/             # User profile & settings
│   │   ├── admin/               # Admin management tools
│   │   └── components/          # Reusable components
│   │
│   ├── utils/                    # Utility modules
│   │   ├── currency.py          # Currency operations
│   │   ├── statistics.py        # Analytics & charts
│   │   └── quickbooks_integration.py  # QB integration
│   │
│   ├── components/               # UI components
│   │   ├── notification.py      # Notification system
│   │   ├── enhanced_icons.py    # Icon components
│   │   └── circular_gauge.py    # Gauge component
│   │
│   ├── assets/                   # Application assets
│   │   └── (icons, images, etc.)
│   │
│   └── database/                 # Database files
│       └── expense_tracker.db   # Main database
│
├── pyproject.toml                # Python project config
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🚀 Running the Application

```bash
# Navigate to project root
cd Cryptics-Legion-Projects

# Activate virtual environment (if using venv)
my_env\Scripts\activate

# or for PowerShell
my_env\Scripts\Activate.ps1

# Run the application
python Cryptics_legion/src/main.py
```

## 📖 Key Files

### Entry Point
- **main.py** - Application entry point with navigation logic

### Database
- **init_db.py** - Initialize database schema
- **init_admin.py** - Create default admin account
- **core/db.py** - Database operations and queries

### Modules
- **core/auth.py** - User authentication
- **core/theme.py** - UI theming system
- **utils/currency.py** - Currency conversion
- **utils/statistics.py** - Analytics and charts
- **utils/quickbooks_integration.py** - QB Online integration

## 🔐 Admin Account

Default admin credentials (auto-created on first run):
- **Username:** ADMIN
- **Password:** ADMIN256

⚠️ **Change these credentials in production!**

## 📚 Related Documentation

- **Project Setup:** [../../docs/01_project/05_SETUP_RUN.md](../../docs/01_project/05_SETUP_RUN.md)
- **Architecture:** [../../docs/01_project/02_ARCHITECTURE.md](../../docs/01_project/02_ARCHITECTURE.md)
- **UI Organization:** [../../docs/06_reference/UI_FOLDER_ORGANIZATION.md](../../docs/06_reference/UI_FOLDER_ORGANIZATION.md)
- **QuickBooks:** [../../docs/05_quickbooks/README.md](../../docs/05_quickbooks/README.md)

---

*Smart Expense Tracker - Main Application Source Code*
