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
├── 🎯 Main Application
│   └── Cryptics_legion/                          # Main application source
│       ├── src/
│       │   ├── main.py                          # Entry point
│       │   ├── init_db.py                       # DB initialization
│       │   ├── init_admin.py                    # Admin setup
│       │   ├── expense_tracker.db               # SQLite database
│       │   │
│       │   ├── core/                            # Core modules
│       │   │   ├── auth.py                      # Authentication
│       │   │   ├── db.py                        # Database ops
│       │   │   └── theme.py                     # UI theming
│       │   │
│       │   ├── ui/                              # User interface (organized)
│       │   │   ├── auth/                        # Login, Register, Reset
│       │   │   ├── onboarding/                  # Onboarding flow
│       │   │   ├── user/                        # Main features (11 pages)
│       │   │   ├── profile/                     # Profile & settings (4 pages)
│       │   │   ├── admin/                       # Admin tools (11 pages)
│       │   │   └── components/                  # Reusable components
│       │   │
│       │   ├── utils/                           # Business logic
│       │   │   ├── currency.py                  # Currency conversion
│       │   │   ├── statistics.py                # Analytics
│       │   │   └── quickbooks_integration.py    # QB Online integration
│       │   │
│       │   ├── components/                      # UI components
│       │   │   ├── notification.py              # Notifications
│       │   │   ├── enhanced_icons.py            # Icons
│       │   │   └── circular_gauge.py            # Gauges
│       │   │
│       │   ├── assets/                          # App resources
│       │   └── database/                        # DB files
│       │
│       ├── pyproject.toml                       # Python config
│       ├── README.md                            # App documentation
│       └── .gitignore                           # Git excludes
│
├── 📚 Documentation
│   └── docs/                                    # Organized documentation
│       ├── 01_project/                          # Core docs (10 files)
│       ├── 02_admin/                            # Admin guides (8 files)
│       ├── 03_agile/                            # Sprint planning (12 files)
│       ├── 04_features/                         # Features (10 files)
│       ├── 05_quickbooks/                       # QB integration (9 files)
│       ├── 06_reference/                        # References (5 files)
│       ├── 07_assets/                           # Images & PDFs (26 items)
│       └── README.md                            # 📖 Documentation hub
│
├── 🧪 Testing
│   ├── tests/                                   # Automated tests
│   │   ├── test_currency_api.py
│   │   ├── test_notification_persistence.py
│   │   ├── test_onboarding_click.py
│   │   ├── test_onboarding_flow.py
│   │   └── README.md
│   └── Cryptics_legion/test_currency.py        # Additional tests
│
├── 🔧 Utilities
│   ├── scripts/                                 # Admin scripts
│   │   ├── check_accounts.py
│   │   └── README.md
│   └── my_env/                                  # Python virtual environment
│
├── 📋 Configuration
│   ├── pyproject.toml                          # Project config
│   ├── .gitignore                              # Git excludes
│   └── README.md                               # This file
│
└── 📚 Version Control
    └── .git/                                   # Git repository
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

---

## 🗺️ Navigation Guide

### 📖 Starting Points by Role

**👤 For New Users**
→ [docs/README.md](docs/README.md) - Documentation hub
→ [docs/06_reference/USER_MANUAL.md](docs/06_reference/USER_MANUAL.md) - User guide

**👨‍💼 For Admins**
→ [docs/02_admin/ADMIN_QUICK_START.md](docs/02_admin/ADMIN_QUICK_START.md) - 5-minute start
→ [docs/02_admin/ADMIN_NAVIGATION_GUIDE.md](docs/02_admin/ADMIN_NAVIGATION_GUIDE.md) - Interface tour

**👨‍💻 For Developers**
→ [Cryptics_legion/README.md](Cryptics_legion/README.md) - Source code overview
→ [docs/06_reference/UI_FOLDER_ORGANIZATION.md](docs/06_reference/UI_FOLDER_ORGANIZATION.md) - Code structure
→ [docs/01_project/02_ARCHITECTURE.md](docs/01_project/02_ARCHITECTURE.md) - System design

**💰 For QuickBooks Integration**
→ [docs/05_quickbooks/README.md](docs/05_quickbooks/README.md) - QB integration hub
→ [docs/05_quickbooks/QUICKBOOKS_DOCUMENTATION_INDEX.md](docs/05_quickbooks/QUICKBOOKS_DOCUMENTATION_INDEX.md) - Choose your guide

### 🗂️ Where to Find Things

| Need | Location |
|------|----------|
| **Source Code** | `Cryptics_legion/src/` |
| **Tests** | `tests/` |
| **Scripts** | `scripts/` |
| **Documentation** | `docs/` |
| **Application UI** | `Cryptics_legion/src/ui/` |
| **Admin Tools** | `Cryptics_legion/src/ui/admin/` |
| **Database Schema** | `docs/01_project/03_DATA_MODEL.md` |
| **Setup Instructions** | `docs/01_project/05_SETUP_RUN.md` |
| **Troubleshooting** | `docs/06_reference/BUG_DOCUMENTATION.md` |
| **QuickBooks Setup** | `docs/05_quickbooks/` |

### 📚 Documentation Organization

```
docs/
├── 01_project/          Project foundation & architecture
├── 02_admin/            Admin system guides  
├── 03_agile/            Sprint planning & backlog
├── 04_features/         Feature-specific docs
├── 05_quickbooks/       QB integration guides
├── 06_reference/        Quick refs & manuals
└── 07_assets/           Images & supporting files
```

See [docs/README.md](docs/README.md) for complete navigation guide.

---

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
| `FINAL REPORT_INFOASSUR` | Information Assurance Documentation and Final Proj |

---

## 🤝 Team & Contributing

### Team Members

| Role | Member |
|------|--------|
| **Product Lead & Lead Developer** | Reynaldo Reyes (Reylan25) |
| **Data & Integration Engineer** | Carl James Poopalaretnam (Itscrl) |
| **UI/UX & QA Lead** | Roger Regalado (rogxyz-14) |

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


## 🎯 Quick Navigation

### 🚀 Start Here
- **[AGILE_MODEL_OVERVIEW.md](AGILE_MODEL_OVERVIEW.md)** - Overview of Agile methodology used
- **[AGILE_PROJECT_SUMMARY.md](AGILE_PROJECT_SUMMARY.md)** - Complete project summary
- **[PRODUCT_BACKLOG.md](PRODUCT_BACKLOG.md)** - All user stories and backlog items

### 📅 Sprint Documentation
- **[SPRINT_01_FOUNDATION.md](SPRINT_01_FOUNDATION.md)** - Week 1-2: Database & Authentication
- **[SPRINT_02_USER_PROFILE.md](SPRINT_02_USER_PROFILE.md)** - Week 3-4: User Profiles & Onboarding
- **[SPRINT_03_EXPENSE_MANAGEMENT.md](SPRINT_03_EXPENSE_MANAGEMENT.md)** - Week 5-6: Core Expense Features
- **[SPRINT_04_ANALYTICS.md](SPRINT_04_ANALYTICS.md)** - Week 7-8: Statistics & Analytics
- **[SPRINT_05_ADMIN_FOUNDATION.md](SPRINT_05_ADMIN_FOUNDATION.md)** - Week 9-10: Admin System Setup
- **[SPRINT_06_ADMIN_CONFIG.md](SPRINT_06_ADMIN_CONFIG.md)** - Week 11-12: Configuration & Policy
- **[SPRINT_07_ADVANCED_FEATURES.md](SPRINT_07_ADVANCED_FEATURES.md)** - Week 13-14: Advanced Features
- **[SPRINT_08_DEPLOYMENT.md](SPRINT_08_DEPLOYMENT.md)** - Week 15-16: Testing & Deployment

---

## 📖 Documentation Categories

### 🔐 Admin System
Complete documentation for administrative features and configuration tools.

| Document | Description | Status |
|----------|-------------|--------|
| [ADMIN_SYSTEM_DOCUMENTATION.md](ADMIN_SYSTEM_DOCUMENTATION.md) | Complete admin system overview | ✅ Complete |
| [ADMIN_FEATURES_SUMMARY.md](ADMIN_FEATURES_SUMMARY.md) | Admin features at a glance | ✅ Complete |
| [ADMIN_QUICK_START.md](ADMIN_QUICK_START.md) | Getting started with admin | ✅ Complete |
| [ADMIN_ARCHITECTURE.md](ADMIN_ARCHITECTURE.md) | Admin system architecture | ✅ Complete |
| [ADMIN_IMPLEMENTATION_SUMMARY.md](ADMIN_IMPLEMENTATION_SUMMARY.md) | Implementation details | ✅ Complete |
| [ADMIN_TESTING_GUIDE.md](ADMIN_TESTING_GUIDE.md) | Admin testing procedures | ✅ Complete |
| [ADMIN_NAVIGATION_GUIDE.md](ADMIN_NAVIGATION_GUIDE.md) | Navigation structure | ✅ Complete |
| [ADMIN_CONFIGURATION_POLICY_DOCS.md](ADMIN_CONFIGURATION_POLICY_DOCS.md) | Configuration & Policy features | ✅ Complete |

### 💱 Currency & Financial
Documentation for currency exchange and financial features.

| Document | Description | Status |
|----------|-------------|--------|
| [CURRENCY_API_DOCUMENTATION.md](CURRENCY_API_DOCUMENTATION.md) | Currency API complete guide | ✅ Complete |
| [CURRENCY_API_QUICK_START.md](CURRENCY_API_QUICK_START.md) | Quick start for currency API | ✅ Complete |
| [CURRENCY_SYSTEM.md](CURRENCY_SYSTEM.md) | Currency system overview | ✅ Complete |

### 🔒 Security & Authentication
Security features and authentication documentation.

| Document | Description | Status |
|----------|-------------|--------|
| [OTP_PASSWORD_RESET.md](OTP_PASSWORD_RESET.md) | OTP-based password reset | ✅ Complete |
| [PASSCODE_LOCK_FEATURE.md](PASSCODE_LOCK_FEATURE.md) | PIN/Passcode lock security | ✅ Complete |
| [BIOMETRIC_AUTHENTICATION.md](BIOMETRIC_AUTHENTICATION.md) | Future biometric plans | 📋 Planned |
| [GMAIL_SETUP_GUIDE.md](GMAIL_SETUP_GUIDE.md) | Email configuration guide | ✅ Complete |

### 👤 User Features
User-facing features and improvements.

| Document | Description | Status |
|----------|-------------|--------|
| [PERSONAL_DETAILS_IMPROVEMENTS.md](PERSONAL_DETAILS_IMPROVEMENTS.md) | Personal details feature | ✅ Complete |
| [QUICK_START_EMAIL.md](QUICK_START_EMAIL.md) | Email quick start | ✅ Complete |

### 🐛 Bug Tracking
Bug documentation and resolutions.

| Document | Description | Status |
|----------|-------------|--------|
| [BUG_DOCUMENTATION.md](BUG_DOCUMENTATION.md) | Known bugs and fixes | ✅ Complete |

---

## 📊 Project Statistics

### Documentation Metrics
- **Total Documents:** 27 files
- **Total Pages:** 500+ pages (estimated)
- **Word Count:** 100,000+ words
- **Documentation Coverage:** 100%

### Sprint Metrics
- **Total Sprints:** 8 sprints
- **Sprint Duration:** 2 weeks each
- **Total Duration:** 16 weeks (4 months)
- **User Stories Completed:** 47 stories
- **Story Points Delivered:** 364 points
- **Average Velocity:** 45.5 points/sprint

### Code Metrics
- **Files Created:** 50+ files
- **Lines of Code:** 15,000+ lines
- **Code Coverage:** 82%
- **Bug Resolution:** 100% (critical & high)

---

## 🎓 How to Use This Documentation

### For New Team Members
1. Start with [AGILE_MODEL_OVERVIEW.md](AGILE_MODEL_OVERVIEW.md)
2. Read [AGILE_PROJECT_SUMMARY.md](AGILE_PROJECT_SUMMARY.md)
3. Review sprints chronologically (Sprint 1-8)
4. Explore feature-specific docs as needed

### For Developers
1. Review [ADMIN_SYSTEM_DOCUMENTATION.md](ADMIN_SYSTEM_DOCUMENTATION.md)
2. Check [CURRENCY_API_DOCUMENTATION.md](CURRENCY_API_DOCUMENTATION.md)
3. Read implementation summaries
4. Refer to sprint docs for context

### For Project Managers
1. Read [AGILE_PROJECT_SUMMARY.md](AGILE_PROJECT_SUMMARY.md)
2. Review [PRODUCT_BACKLOG.md](PRODUCT_BACKLOG.md)
3. Check sprint retrospectives
4. Monitor [SPRINT_08_DEPLOYMENT.md](SPRINT_08_DEPLOYMENT.md)

### For Stakeholders
1. Start with [AGILE_MODEL_OVERVIEW.md](AGILE_MODEL_OVERVIEW.md)
2. Review feature summaries (ADMIN_FEATURES_SUMMARY.md)
3. Check quick start guides
4. Review sprint demo highlights

---

## 🔍 Document Templates

### Sprint Documentation Template
Each sprint document includes:
- ✅ Sprint Overview
- ✅ User Stories with Acceptance Criteria
- ✅ Sprint Metrics (Velocity, Burndown)
- ✅ Technical Achievements
- ✅ Sprint Demo Highlights
- ✅ Sprint Retrospective
- ✅ Blockers & Resolutions
- ✅ Sprint Handoff

### Feature Documentation Template
Each feature document includes:
- ✅ Feature Overview
- ✅ Implementation Details
- ✅ Database Schema
- ✅ API Documentation
- ✅ Usage Examples
- ✅ Testing Guidelines
- ✅ Troubleshooting

---

## 📝 Documentation Standards

### Format
- **Format:** Markdown (.md)
- **Structure:** Hierarchical headers
- **Code Blocks:** Syntax highlighted
- **Tables:** Formatted consistently
- **Lists:** Organized with checkmarks

### Naming Convention
- `AGILE_*` - Agile methodology docs
- `SPRINT_*` - Sprint-specific docs
- `ADMIN_*` - Admin feature docs
- `CURRENCY_*` - Currency feature docs
- Feature-specific names for others

### Maintenance
- **Updates:** After each sprint
- **Review:** Before sprint retrospective
- **Ownership:** Development team
- **Approval:** Product owner

---

## 🚀 Getting Started Paths

### Path 1: Quick Overview (30 minutes)
1. [AGILE_MODEL_OVERVIEW.md](AGILE_MODEL_OVERVIEW.md) - 10 min
2. [AGILE_PROJECT_SUMMARY.md](AGILE_PROJECT_SUMMARY.md) - 15 min
3. [ADMIN_FEATURES_SUMMARY.md](ADMIN_FEATURES_SUMMARY.md) - 5 min

### Path 2: Developer Onboarding (2 hours)
1. Agile overview - 15 min
2. All sprint docs (Sprint 1-8) - 90 min
3. Technical documentation - 15 min

### Path 3: Comprehensive Study (8 hours)
1. All Agile documentation - 3 hours
2. All sprint documentation - 4 hours
3. All feature documentation - 1 hour

---

## 📞 Support & Contact

### Questions?
- **Technical Issues:** Check BUG_DOCUMENTATION.md
- **Feature Requests:** See PRODUCT_BACKLOG.md
- **Process Questions:** Review AGILE_MODEL_OVERVIEW.md

### Updates
- Documentation updated after each sprint
- Major updates documented in changelog
- Version tracking in Git

---

## 🎯 Key Achievements Documented

### ✅ Completed Features
- Complete user authentication system
- Comprehensive expense tracking
- Advanced statistics & analytics
- Full admin management system
- Configuration & policy tools
- Live currency exchange API
- OTP password reset
- Passcode lock security
- Responsive UI design

### 🚧 In Progress
- Final testing & QA
- Deployment preparation
- User acceptance testing

### 📋 Planned (Backlog)
- Recurring expenses
- Biometric authentication
- Expense splitting
- Advanced analytics
- See PRODUCT_BACKLOG.md for complete list

---

## 📈 Project Progress

```
Sprint 1: ████████░░░░░░░░ 50%  - Foundation Complete
Sprint 2: ████████████░░░░ 75%  - User System Complete
Sprint 3: ████████████████ 100% - Expense Core Complete
Sprint 4: ████████████████ 100% - Analytics Complete
Sprint 5: ████████████████ 100% - Admin Foundation Complete
Sprint 6: ████████████████ 100% - Admin Config Complete
Sprint 7: ████████████████ 100% - Advanced Features Complete
Sprint 8: ██████████████░░ 87%  - Testing & Deployment

Overall Project Progress: ███████████████░ 95%
```

---

## 🏆 Quality Assurance

### Documentation Quality
- ✅ All features documented
- ✅ Clear structure and navigation
- ✅ Code examples included
- ✅ Screenshots where applicable
- ✅ Consistent formatting
- ✅ Regular updates

### Code Quality
- ✅ 82% test coverage
- ✅ 100% code review
- ✅ Zero critical bugs
- ✅ Performance targets met
- ✅ Security audit passed

---

**Last Updated:** December 9, 2025  
**Documentation Version:** 1.0  
**Project Status:** 95% Complete  
**Next Update:** Sprint 8 Completion  

---

*For the most up-to-date information, always refer to the latest version of each document in this folder.*

