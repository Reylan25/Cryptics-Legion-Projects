# Cryptics Legion - Azure Cloud Deployment Project

## 📋 Project Overview

This project demonstrates the deployment of **Cryptics Legion** (Smart Expense Tracker) on Microsoft Azure using enterprise-grade cloud architecture, security best practices, and cost optimization strategies.

**Team Members:**
- Carl James Poopalaretnam (Itscrl) 
- Roger Regalado (rogxyz-14) 
- Joshua Sario

---

## 🎯 Deployment Summary

### Live Application
- **URL:** https://4.240.57.130
- **Status:** ✅ Live and Running
- **Application Type:** Flet-based Expense Tracker (Web)
- **Database:** SQLite (Local)
- **Framework:** Python 3.11 + Flet 0.28.3

### Azure Resources Deployed
| Resource | Type | Purpose |
|----------|------|---------|
| **cryptics-resource-group** | Resource Group | Container for all resources |
| **cryptics-app-plan** | App Service Plan | Compute hosting (B1 Linux) |
| **cryptics-legion-app** | App Service | Web application runtime |
| **cryptics-nsg** | Network Security Group | Firewall rules & access control |
| **cryptics-legion.key** | SSL Certificate | HTTPS encryption (Self-signed) |
| **cryptics-legion.crt** | SSL Certificate | HTTPS encryption (Self-signed) |

---

## 📁 Repository Structure

```
Cryptics-Legion-Azure-Deployment/
├── diagram/
│   └── architecture.png              # Professional Azure architecture diagram
├── deployment/
│   ├── screenshots/
│   └── README.md                     # Detailed deployment instructions
├── report/
│   ├── cost-estimate.md              # Cost analysis & optimization
│
├── CHANGELOG.md                      # Detailed change log
├── README.md                         # This file

```

---

## 🚀 Quick Start - Deploy in 5 Minutes

### Prerequisites
- Azure Portal access (https://portal.azure.com)
- Azure subscription active
- Web browser
- Python 3.11+ installed locally

---

## 🏗️ Architecture Overview

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Internet / Public Users                 │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS (Port 443)
                     ▼
        ┌────────────────────────────┐
        │   Nginx Reverse Proxy      │
        │  (SSL/TLS Termination)     │
        │  VM: 4.240.57.130:443      │
        └────────────┬───────────────┘
                     │ HTTP (Port 8080)
                     ▼
        ┌────────────────────────────┐
        │   Flet Web Application     │
        │  127.0.0.1:8080            │
        │  (Python 3.11)             │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   SQLite Database          │
        │  (Local File-based)        │
        └────────────────────────────┘

Security Boundary:
├─ PUBLIC: Internet → Nginx (443)
└─ PRIVATE: Nginx → Application → Database
```

### Key Features
✅ **HTTPS/TLS Encryption** - All traffic encrypted  
✅ **Network Security** - NSG rules restrict access  
✅ **Horizontal Scaling** - App Service Plan supports scale-out  
✅ **Load Balancing** - Built-in Azure load balancer  
✅ **Auto-restart** - Application auto-recovery enabled  
✅ **Monitoring Ready** - Application Insights compatible  

---

## 📊 Cost Estimate

### Monthly Cost Breakdown
| Resource | Tier | Monthly Cost | Notes |
|----------|------|--------------|-------|
| **App Service Plan** | B1 (Linux) | $13.14 | 1 vCPU, 1.75 GB RAM |
| **Data Transfer** | Egress | $0.05 | First 50 GB free |
| **Storage** | Managed | Included | No extra charges |
| **SSL Certificate** | Self-signed | Free | Let's Encrypt alternative |
| **Network Security** | Basic NSG | Free | Standard rules included |
| **TOTAL** | | **~$13.14/month** | Can scale up as needed |

**Cost Optimization Strategies:**
- ✅ Using B1 tier (cheapest paid tier) instead of Premium
- ✅ Shared infrastructure (no dedicated instances)
- ✅ Local database (SQLite) vs. Azure SQL Database (saves $10-15/month)
- ✅ Self-signed SSL certificate (no Let's Encrypt costs)
- ✅ Auto-shutdown during off-hours (potential 50% savings)

For detailed cost analysis, see [report/cost-estimate.md](report/cost-estimate.md)

---

## 🔐 Security Features

### Authentication & Access Control
- ✅ **Network Security Group** - Restricts inbound traffic to ports 80, 443, 8080
- ✅ **HTTPS/TLS 1.3** - End-to-end encryption
- ✅ **CORS Headers** - Prevents unauthorized cross-origin requests
- ✅ **Input Validation** - SQLi and XSS protection (Flet framework)

### Application Security
- ✅ **bcrypt Password Hashing** - Cost factor 12
- ✅ **OTP Password Reset** - 15-minute expiry
- ✅ **Passcode Protection** - 4-digit PIN lock
- ✅ **Rate Limiting** - Login attempt restrictions

### Infrastructure Security
- ✅ **Firewall Rules** - Azure NSG enforced
- ✅ **No Hardcoded Secrets** - Environment variables used
- ✅ **Auto-HTTPS Redirect** - HTTP → HTTPS
- ✅ **Public IP Isolation** - Limited administrative access

---

## 🎥 Video Presentation

**Video Duration:** 13 minutes  
**Link:** https://youtu.be/tBQIdet-bqM


---

## 🛠️ Maintenance & Monitoring

### Health Checks
```bash
# Check application status
curl https://4.240.57.130

# View application logs
sudo journalctl -u cryptics-flet -f

# Monitor resource usage - Via Azure Portal
# Navigate to: Resource Groups > cryptics-resource-group > cryptics-legion-app > Metrics
```

### Updating the Application
```bash
# Pull latest changes
cd ~/Cryptics-Legion-Projects
git pull origin main

# Restart application
pkill -f "flet run"
cd Cryptics_legion/src
nohup python3 -m flet run --web --host 127.0.0.1 --port 8080 main.py > ~/flet.log 2>&1 &
```

---

## 📚 Documentation

- **[Architecture Diagram](diagram/architecture.png)** - Professional resource diagram
- **[Deployment Guide](deployment/README.md)** - Step-by-step instructions
- **[Cost Report](report/cost-estimate.md)** - Detailed cost analysis
- **[Change Log](CHANGELOG.md)** - Deployment history

---

## 🚨 Troubleshooting

### Application shows "Bad Gateway"
```bash
# Check if Flet is running
sudo ss -tlnp | grep 8080

# Restart application
pkill -f "flet run"
cd ~/Cryptics-Legion-Projects/Cryptics_legion/src
python3 -m flet run --web --host 127.0.0.1 --port 8080 main.py
```

### SSL Certificate warnings
```bash
# Regenerate self-signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/cryptics-legion.key \
  -out /etc/ssl/certs/cryptics-legion.crt \
  -subj "/CN=4.240.57.130"

sudo systemctl restart nginx
```

### Port 8080 already in use
```bash
# Find process using port
sudo lsof -i :8080

# Kill process
sudo kill -9 <PID>

# Or use different port
python3 -m flet run --web --host 127.0.0.1 --port 8081 main.py
```

## 🎓 Academic Credits

- **Course:** Cloud Computing 
- **Institution:** Camarines Sur Polytechnic Colleges
- **Submission Date:** May 16, 2026

**Repository:** https://github.com/Reylan25/Cryptics-Legion-Projects  
**Live App:** https://4.240.57.130  

**Built with ☁️ Azure, 🐍 Python, Flet, SQlite, and 🔒 Security Best Practices**
