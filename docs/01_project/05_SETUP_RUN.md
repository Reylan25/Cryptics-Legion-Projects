# Setup & Installation Guide

## Prerequisites

### System Requirements
- **Python**: 3.9 or higher
- **OS**: Windows, macOS, Linux, iOS, or Android
- **RAM**: 512MB minimum (2GB recommended)
- **Storage**: 500MB for app + dependencies
- **Internet**: Required for initial setup and exchange rate APIs

### Required Software
- Git (for cloning repository)
- Python package manager: `pip`, `uv`, or `poetry`

---

## Installation Methods

### **Option 1: Using UV (Recommended - Fastest)**

#### 1.1 Install UV
```bash
# Windows
pip install uv

# macOS/Linux
brew install uv
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 1.2 Clone Repository
```bash
git clone https://github.com/Reylan25/Cryptics-Legion-Projects.git
cd Cryptics-Legion-Projects/Cryptics_legion
```

#### 1.3 Install Dependencies
```bash
uv sync
```

#### 1.4 Run Application
```bash
# Desktop app
uv run flet run

# Web app
uv run flet run --web

# Mobile (after setup)
flet build apk -v  # Android
flet build ipa -v  # iOS
```

---

### **Option 2: Using Poetry**

#### 2.1 Install Poetry
```bash
# Windows (using pipx or pip)
pip install poetry

# macOS
brew install poetry

# Linux
curl -sSL https://install.python-poetry.org | python3 -
```

#### 2.2 Clone Repository
```bash
git clone https://github.com/Reylan25/Cryptics-Legion-Projects.git
cd Cryptics-Legion-Projects/Cryptics_legion
```

#### 2.3 Install Dependencies
```bash
poetry install
```

#### 2.4 Run Application
```bash
# Desktop app
poetry run flet run

# Web app
poetry run flet run --web
```

---

### **Option 3: Using PIP (Traditional)**

#### 3.1 Clone Repository
```bash
git clone https://github.com/Reylan25/Cryptics-Legion-Projects.git
cd Cryptics-Legion-Projects/Cryptics_legion
```

#### 3.2 Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3.3 Install Dependencies
```bash
pip install -r requirements.txt
# or directly from pyproject.toml
pip install flet==0.28.3 bcrypt requests
```

#### 3.4 Run Application
```bash
cd src
python main.py

# Or using Flet CLI
flet run
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Exchange Rate API (Optional, uses free tier by default)
EXCHANGE_RATE_API_KEY=your_api_key_here

# Email Configuration (for OTP password reset)
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_PASSWORD=your_app_password_here
# Note: Use Gmail App Password, not your actual password
# Generate at: myaccount.google.com/apppasswords

# Database
DATABASE_PATH=storage/cryptics_legion.db

# App Configuration
APP_VERSION=0.2.0
DEBUG_MODE=false
```

### Setup Gmail for OTP (Optional)

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication if not already enabled
3. Go to **App passwords** section
4. Create an app password for "Mail" and "Windows Computer"
5. Copy the 16-character password
6. Set `GMAIL_PASSWORD` in `.env`

---

## Project Structure

```
Cryptics_legion/
├── pyproject.toml           # Project metadata & dependencies
├── README.md                # Original setup guide
├── src/
│   ├── main.py             # Application entry point
│   ├── init_db.py          # Database initialization
│   │
│   ├── core/               # Core business logic
│   │   ├── auth.py         # Authentication (login, register)
│   │   ├── db.py           # Database operations
│   │   └── theme.py        # UI theming
│   │
│   ├── ui/                 # User interface pages
│   │   ├── login_page.py           # Login screen
│   │   ├── register_page.py        # Registration
│   │   ├── home_page.py            # Dashboard
│   │   ├── Expenses.py             # Expense management
│   │   ├── statistics_page.py      # Analytics & charts
│   │   ├── account_settings_page.py # Account management
│   │   ├── personal_details.py     # User profile
│   │   ├── passcode_lock_page.py   # Security feature
│   │   └── [other pages...]
│   │
│   ├── utils/              # Utility functions
│   │   ├── currency.py     # Currency formatting
│   │   ├── statistics.py   # Analytics functions
│   │   ├── otp.py          # OTP generation
│   │   ├── brand_recognition.py  # Payment detection
│   │   └── currency_exchange.py  # Exchange rate API
│   │
│   ├── components/         # Reusable UI components
│   │   ├── bottom_nav.py
│   │   ├── circular_gauge.py
│   │   └── expense_item.py
│   │
│   ├── assets/             # Images, fonts, icons
│   └── storage/            # Data storage
│       ├── data/           # Cache files
│       └── temp/           # Temporary files
│
├── test_currency.py        # Currency module tests
├── check_accounts.py       # Database utility script
└── docs/                   # Documentation (this folder)
```

---

## First Run Setup

### Step 1: Initialize Database
The app automatically creates the database on first run:
```bash
python src/init_db.py
```

This creates:
- `storage/cryptics_legion.db` - Main database
- Tables: users, accounts, expenses, password_reset_otps

### Step 2: Create Test User (Optional)
```python
# Edit src/init_db.py to create test user
# Or register through the app UI
```

### Step 3: Verify Installation
```bash
# Test imports
python -c "import flet; print('✓ Flet installed')"
python -c "import bcrypt; print('✓ bcrypt installed')"
python -c "from src.core import db; print('✓ Database accessible')"
```

---

## Building for Different Platforms

### Windows Desktop
```bash
flet build windows -v
# Output: build/windows/cryptics-legion-0.2.0.exe
```

### macOS Desktop
```bash
flet build macos -v
# Output: build/macos/cryptics-legion-0.2.0.app
```

### Linux Desktop
```bash
flet build linux -v
# Output: build/linux/cryptics-legion-0.2.0
```

### Android APK
```bash
# Requires Android SDK
flet build apk -v
# Output: build/app/outputs/apk/release/app-release.apk
```

### iOS IPA
```bash
# Requires Xcode (macOS only)
flet build ipa -v
# Output: build/app/outputs/ipa/app-release.ipa
```

### Web (Progressive Web App)
```bash
flet build web -v
# Output: build/web/
# Deploy to any web server
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'flet'`
**Solution**: Reinstall dependencies
```bash
pip install --upgrade flet bcrypt requests
```

### Issue: Database locked error
**Solution**: Close all instances of the app, delete `storage/` and restart
```bash
rm -rf storage/
python src/init_db.py
```

### Issue: Exchange rates not loading
**Solution**: Check internet connection and API status
```bash
# Manually test API
curl https://api.exchangerate-api.com/v4/latest/USD
```

### Issue: Email OTP not sending
**Solution**: Verify Gmail credentials in `.env`
```bash
# Test SMTP connection
python -c "import smtplib; s = smtplib.SMTP_SSL('smtp.gmail.com', 465); print('✓ Connected')"
```

### Issue: Port already in use (web)
**Solution**: Use different port
```bash
flet run --web --port 8001
```

---

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
```bash
# Edit files in src/
vim src/ui/home_page.py
```

### 3. Test Locally
```bash
uv run flet run
```

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add new currency support"
```

### 5. Push & Create PR
```bash
git push origin feature/your-feature-name
# Create pull request on GitHub
```

---

## Performance Optimization

### Development Tips
- Use `uv` for fastest dependency resolution
- Run with `--profile` flag to identify bottlenecks
- Clear `.flet_build/` cache if experiencing build issues

### Production Optimization
- Build with `--release` flag
- Minify CSS/JS for web builds
- Preload large datasets on app startup
- Cache API responses locally

---

## System Requirements by Platform

| Platform | CPU | RAM | Storage | Notes |
|----------|-----|-----|---------|-------|
| Windows | x64 | 512MB | 100MB | Windows 7+ |
| macOS | Intel/M1 | 1GB | 100MB | 10.11+ |
| Linux | x64 | 512MB | 100MB | Ubuntu 18.04+, Fedora 28+, etc. |
| iOS | A10+ | 2GB | 150MB | iOS 12+ |
| Android | ARMv7/ARMv8 | 2GB | 150MB | Android 6.0+ |

