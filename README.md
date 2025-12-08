# Cryptics Labs - Smart Expense Tracker

A cross-platform personal expense tracking application built with Python Flet framework, designed to provide transparent financial insights with local-first privacy and real-time currency support.

🎯 Project Overview

Cryptics Labs is a desktop and mobile expense tracker that helps users manage their finances efficiently without cloud dependency or subscription requirements. The system provides multi-account support, real-time currency conversion, and intelligent expense categorization.

Key Characteristics
- **Local-First**: Completely offline with SQLite database
- **Multi-Currency**: 10 currency support with real-time exchange rates
- **Privacy-Focused**: All data stored locally, no cloud required
- **Cross-Platform**: Works on Windows, macOS, Linux, iOS, Android, Web
- **Secure**: bcrypt password hashing, OTP password reset, passcode protection

---

## 🚀 Features

### Core Features
✅ User authentication with secure password hashing  
✅ Multi-account management with custom colors and types  
✅ Real-time expense tracking with category suggestions  
✅ 10-currency support with live exchange rates  
✅ Advanced statistics and spending analytics  
✅ Personal details management with validation  

### Security Features
✅ bcrypt password hashing (cost factor 12)  
✅ Email-based OTP password reset (15-min expiry)  
✅ Passcode PIN protection (4 digits)  
✅ Rate limiting on login attempts
✅ Strong Password required  

### Account & Expense Management
✅ Multiple account types (Cash, Savings, Credit Card, E-Wallet, etc.)  
✅ Account balances with currency conversion  
✅ Expense categorization with 200+ brand recognition  
✅ Expense search and filtering by date/category  
✅ Account sorting and primary account selection  

### Analytics & Insights
✅ Monthly spending trends and statistics  
✅ Category-wise expense breakdown  
✅ Circular gauge visualizations  
✅ Account balance summaries  
✅ Real-time calculations and reporting  

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Python Flet (Flutter-based) |
| **Language** | Python 3.9+ |
| **Database** | SQLite3 (Local) |
| **Password Hashing** | bcrypt |
| **Currency API** | Fixer.io / ExchangeRate-API |
| **Email Service** | Gmail SMTP |
| **Testing** | pytest |
| **Dependency Management** | Poetry / UV |

---

## 📁 Project Structure

```
Cryptics-Legion-Projects/
├── Cryptics_legion/
│   ├── main.py                    # Application entry point
│   ├── init_db.py                 # Database initialization
│   ├── pyproject.toml             # Project configuration
│   ├── src/
│   │   ├── core/
│   │   │   ├── auth.py            # Authentication logic
│   │   │   ├── db.py              # Database connection
│   │   │   └── theme.py           # Theme configuration
│   │   ├── ui/                    # All UI pages
│   │   │   ├── login_page.py
│   │   │   ├── home_page.py
│   │   │   ├── Expenses.py
│   │   │   ├── statistics_page.py
│   │   │   └── [13+ other pages...]
│   │   ├── components/            # Reusable UI components
│   │   │   ├── bottom_nav.py
│   │   │   ├── circular_gauge.py
│   │   │   └── [other components...]
│   │   ├── utils/                 # Business logic
│   │   │   ├── currency_exchange.py
│   │   │   ├── statistics.py
│   │   │   ├── brand_recognition.py
│   │   │   └── otp.py
│   │   ├── database/
│   │   │   └── expense_tracker.db
│   │   └── storage/               # Cache and temp files
│   └── assets/                    # Images and icons
├── docs/                          # Comprehensive documentation
│   ├── 00_PROJECT_OVERVIEW.md
│   ├── 01_FEATURES_SCOPE.md
│   ├── 02_ARCHITECTURE.md
│   ├── 03_DATA_MODEL.md
│   ├── 04_EMERGING_TECH.md
│   ├── 05_SETUP_RUN.md
│   ├── 06_TESTING.md
│   ├── 07_TEAM_ROLES.md
│   ├── 08_RISKS_CONSTRAINTS.md
│   ├── 09_INDIVIDUAL_REFLECTION.md
│   ├── DATABASE_SCHEMA_ACTUAL.md
│   └── [more docs...]
├── README.md                      # This file
└── .gitignore
```

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/Reylan25/Cryptics-Legion-Projects.git
cd Cryptics-Legion-Projects/Cryptics_legion
```

**2. Create virtual environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

**3. Install dependencies**
```bash
# Using UV (fastest)
uv sync

# OR using Poetry
poetry install

# OR using pip
pip install flet==0.28.3 bcrypt python-dotenv requests
```

**4. Initialize database**
```bash
python src/init_db.py
```

**5. Run the application**
```bash
python src/main.py
```

### Demo User Credentials

| Role | Username | Password |
|------|----------|----------|
| User | demo | demo123 |
| (Create new account) | Any name | min 8 chars |

### Environment Configuration

Create a `.env` file in `Cryptics_legion/` directory:

```env
# Email Configuration (for OTP password reset)
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Currency API (optional)
CURRENCY_API_KEY=your-fixer-io-key

# App Configuration
DEBUG_MODE=False
LOG_LEVEL=INFO
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_auth.py

# Verbose output
pytest -v
```

**Test Coverage**: 73% (target: 80%)

---

## 💾 Database Management

### Initialize Database
```bash
python src/init_db.py
```

### Database Schema

**4 Core Tables:**
- `users` - User accounts with personal details
- `expenses` - Individual expense records
- `accounts` - Multiple financial accounts
- `password_reset_otps` - OTP tokens for password reset

See `docs/DATABASE_SCHEMA_ACTUAL.md` for full schema details.

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

| Document | Description |
|----------|-------------|
| `00_PROJECT_OVERVIEW.md` | Project vision and objectives |
| `01_FEATURES_SCOPE.md` | Feature matrix and roadmap |
| `02_ARCHITECTURE.md` | System design and components |
| `03_DATA_MODEL.md` | Database ERD and schemas |
| `04_EMERGING_TECH.md` | Technology choices and rationale |
| `05_SETUP_RUN.md` | Installation and setup guide |
| `06_TESTING.md` | Testing strategy and coverage |
| `07_TEAM_ROLES.md` | Team structure and ownership |
| `08_RISKS_CONSTRAINTS.md` | Risk assessment and roadmap |
| `09_INDIVIDUAL_REFLECTION.md` | Team reflections |
| `DATABASE_SCHEMA_ACTUAL.md` | Detailed database schema |

---

## 🤝 Team & Contributing

### Team Members

| Role | Member |
|------|--------|
| **Product Lead & Lead Developer** | Reynaldo Reyes (Reylan25) |
| **Data & Integration Engineer** | Itscrl |
| **UI/UX & QA Lead** | rogxyz-14 |

### Contributing Guidelines

1. Create feature branch: `git checkout -b feature/YourFeature`
2. Make changes with clear commit messages
3. Run tests: `pytest --cov`
4. Update documentation
5. Create Pull Request with description
6. Code review and approval
7. Merge to main

**Code Standards:**
- Follow PEP 8 (Black formatter)
- Type hints recommended
- Google-style docstrings
- WCAG 2.1 accessibility compliance
- Test coverage minimum 70%

---

## 🔒 Security

### Authentication
- Bcrypt password hashing with cost factor 12
- OTP-based password reset (15-minute expiry)
- Passcode PIN protection for app lock
- Session tokens with timeout

### Data Protection
- All data stored locally in SQLite
- No cloud transmission by default
- Passwords hashed before storage
- Encrypted OTP tokens

### Best Practices
- Rate limiting on login attempts
- Secure HTTPS for API calls
- Input validation and sanitization
- No hardcoded credentials

See `docs/04_EMERGING_TECH.md` for security details.

---

## 🚀 Roadmap

### v0.2.0 (Current)
✅ Multi-currency support  
✅ Statistics and analytics  
✅ Passcode protection  
✅ Real-time exchange rates  

### v0.3.0 (Planned)
🔄 iOS/Android mobile apps  
🔄 Recurring expenses  
🔄 Budget alerts  

### v0.4.0 (Future)
🔄 Cloud backup and sync  
🔄 Machine learning categorization  
🔄 Advanced reporting  

### v0.5.0+
🔄 Biometric authentication  
🔄 Team expense sharing  
🔄 Advanced security features  

---


## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👥 Authors & Acknowledgments

**Reynaldo Reyes (Reylan25)** - Product vision, Flet architecture, emerging technology integration

**Carl James Poopalaretnam(Itscrl)** - Data infrastructure, database optimization, storage solutions, documentation

**Roger Regalado(rogxyz-14)** - UI/UX design, accessibility, quality assurance

### Open Source Dependencies
- **Flet**: Flutter for Python - https://flet.dev
- **bcrypt**: Secure password hashing
- **SQLite3**: Local database engine
- **requests**: HTTP client library

---

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check documentation in `docs/` folder
- Review code comments and docstrings

---

**Built with 🐍 Python and Flet for transparent, private financial management**

**Current Version**: v0.2.0  
**Last Updated**: December 9, 2025  

