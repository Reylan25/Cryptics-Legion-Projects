# System Architecture

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     CRYPTICS LEGION APP                         │
│                    (Flet Desktop/Mobile)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
        ┌──────────▼──────────┐  ┌──────▼───────────┐
        │  UI/PRESENTATION    │  │  BUSINESS LOGIC  │
        │     LAYER (Flet)    │  │    (Python)      │
        └────────────┬────────┘  └────────┬─────────┘
                     │                    │
        ┌────────────┴────────────────────┴──────────┐
        │                                             │
        │  ┌────────────────────────────────────┐   │
        │  │  CORE MODULES                      │   │
        │  ├────────────────────────────────────┤   │
        │  │ • auth.py    (Authentication)      │   │
        │  │ • db.py      (Database Access)     │   │
        │  │ • theme.py   (UI Theming)          │   │
        │  └────────────────────────────────────┘   │
        │                                             │
        │  ┌────────────────────────────────────┐   │
        │  │  UTILITIES                         │   │
        │  ├────────────────────────────────────┤   │
        │  │ • currency.py (Conversion Logic)   │   │
        │  │ • statistics.py (Analytics)        │   │
        │  │ • otp.py (Password Reset)          │   │
        │  └────────────────────────────────────┘   │
        │                                             │
        └────────────┬─────────────────────────────┘
                     │
        ┌────────────▼────────────┐
        │  DATA ACCESS LAYER      │
        │  (db.py - SQLite ORM)   │
        └────────────┬────────────┘
                     │
        ┌────────────▼─────────────────┐
        │   SQLite Database            │
        │  ┌────────────────────────┐  │
        │  │ Users                  │  │
        │  │ Accounts               │  │
        │  │ Expenses               │  │
        │  │ Password Reset OTPs    │  │
        │  └────────────────────────┘  │
        └────────────┬─────────────────┘
                     │
        ┌────────────▼──────────────────────┐
        │  EXTERNAL INTEGRATIONS            │
        ├──────────────────────────────────┤
        │ • Fixer.io / ExchangeRate-API    │
        │   (Currency Exchange Rates)      │
        └──────────────────────────────────┘
```

---

## Component Breakdown

### **1. UI Layer (Flet)**
- **login_page.py** - User authentication interface
- **register_page.py** - New user registration
- **home_page.py** - Dashboard with balance & recent expenses
- **Expenses.py** - Main expense list and management
- **statistics_page.py** - Charts and analytics
- **account_settings_page.py** - Account management
- **profile_page.py** - User profile management
- **personal_details.py** - User information editing
- **passcode_lock_page.py** - Security feature
- **currency_selection_page.py** - Currency preference
- **exchange_rates_page.py** - Real-time rate viewer

### **2. Core Logic Layer**
- **auth.py** - User authentication, password hashing, OTP verification
- **db.py** - SQLite database operations and ORM
- **theme.py** - Centralized UI theming and color management

### **3. Utilities Layer**
- **currency.py** - Currency formatting and conversion
- **statistics.py** - Expense analysis and chart generation
- **otp.py** - One-time password generation and email delivery

### **4. Data Layer**
- **SQLite Database** - Persistent storage of all application data
- **File System** - Cache for exchange rates, temporary files

---

## Data Flow Architecture

```
User Input (UI)
    ↓
Flet Event Handler
    ↓
Business Logic (Python)
    ↓
Data Access Layer (db.py)
    ↓
SQLite Database
    ↓
Response back to UI (Update Display)
```

---

## Key Architectural Decisions

### **1. Flet for Cross-Platform UI**
- ✅ Single codebase for Windows, macOS, Linux, iOS, Android
- ✅ Python-native development (no separate Swift/Kotlin)
- ✅ Fast iteration and prototyping

### **2. SQLite for Local Storage**
- ✅ No server required (offline-first)
- ✅ Built-in Python support
- ✅ Lightweight and portable
- ✅ Suitable for single-user applications

### **3. Modular Architecture**
- ✅ Separation of concerns (UI, Logic, Data)
- ✅ Easy to test and maintain
- ✅ Scalable for feature additions

### **4. External API Integration**
- ✅ Fixer.io / ExchangeRate-API for real-time exchange rates
- ✅ Gmail API for OTP delivery
- ✅ Configurable API keys via environment variables

---

## Deployment Targets

| Platform | Build Method | Status |
|----------|-------------|--------|
| **Windows** | `flet build windows -v` | ✅ |
| **macOS** | `flet build macos -v` | ✅ |
| **Linux** | `flet build linux -v` | ✅ |
| **iOS** | `flet build ipa -v` | ✅ |
| **Android** | `flet build apk -v` | ✅ |
| **Web** | `flet run --web` | ✅ |

