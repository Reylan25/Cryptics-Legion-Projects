# Cryptics Legion - Azure Cloud Deployment

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Live Deployment](#live-deployment)
3. [Architecture](#architecture)
4. [Prerequisites](#prerequisites)
5. [Quick Start](#quick-start)
6. [Step-by-Step Deployment](#step-by-step-deployment)
7. [Code Deployment via SSH](#code-deployment-via-ssh)
8. [Verification](#verification)
9. [Troubleshooting](#troubleshooting)
10. [Team](#team)

---

## 🎯 Project Overview

**Cryptics Legion** is a Smart Expense Tracker application deployed on Microsoft Azure using enterprise-grade cloud architecture. This project demonstrates best practices in cloud deployment, security, and cost optimization.

**Deployment Method:** Azure Portal GUI + SSH for code deployment

### Key Metrics

| Metric | Value |
|--------|-------|
| **Live URL** | https://4.240.57.130 |
| **Monthly Cost** | $13.14 |

---

## 🌍 Live Deployment

### Access the Application

**Production URL:** https://4.240.57.130

The application is **live and running** on Azure. You can:
- ✅ Log in with demo credentials
- ✅ Add expenses
- ✅ View expense history
- ✅ Track spending by category

### Demo Credentials

```
Username: Demo1234
Password: Demo1234
```

---

## 🏗️ Architecture

### High-Level Overview

```
Internet (HTTPS 443)
    ↓
    ├─→ NSG Firewall (Allow 443, 80, 8080)
    ├─→ Nginx Reverse Proxy (SSL/TLS Termination)
    ├─→ [Behind Security Boundary]
    ├─→ App Service Plan (B1 - 1 vCPU, 1.75GB RAM)
    ├─→ Flet Web Application (Python 3.11)
    └─→ SQLite Database (Local Storage)
```

### Azure Resources

| Resource | Type | Purpose |
|----------|------|---------|
| **cryptics-resource-group** | Resource Group | Container for all resources |
| **cryptics-app-plan** | App Service Plan | Compute (1 vCPU, 1.75 GB RAM) |
| **cryptics-legion-app** | App Service | Web application hosting |
| **cryptics-nsg** | Network Security Group | Firewall rules |
| **SSL Certificates** | Self-signed | HTTPS encryption |
| **SQLite DB** | Local File | Data storage |

### Cloud Optimizations

✅ **99.95% SLA** - Azure uptime guarantee
✅ **Auto-Recovery** - Automatic restart on failure
✅ **Horizontal Scaling** - Add instances as needed
✅ **Cost Optimized** - B1 tier saves $50+/month
✅ **Security First** - Multi-layer protection

---

## 📋 Prerequisites

### Required Software

```bash
# Check what's installed
python3 --version        # Python 3.11+
git --version            # Git 2.0+
ssh -V                   # OpenSSH
```

### Installation (if needed)

#### Windows (PowerShell)
```powershell
# Install Python
winget install Python.Python.3.11

# Install Git
winget install Git.Git
```

#### macOS (Homebrew)
```bash
brew install python@3.11 git
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
```

### Azure Setup

- Navigate to [Azure Portal](https://portal.azure.com)
- Sign in with your Azure account
- Ensure you have an active subscription


### Azure Portal (GUI) + SSH Deployment

The application was deployed using **two methods:**

**Infrastructure Setup (Azure GUI Portal):**
- ✅ Resource Group created via Portal
- ✅ App Service Plan configured via Portal
- ✅ App Service provisioned via Portal
- ✅ Network Security Group configured via Portal
- ✅ HTTPS/SSL enabled via Portal

**Code Deployment (SSH):**
- ✅ Code cloned to VM via SSH
- ✅ Virtual environment created via SSH
- ✅ Dependencies installed via SSH
- ✅ Application running via systemd service
- ✅ Auto-recovery configured via SSH

---

## 📝 Step-by-Step Deployment (Azure Portal)

### Step 1: Create Resource Group

**Purpose:** Container for all Azure resources

**GUI Steps:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "Resource Groups"
3. Click "+ Create"
4. Fill in details:
   - **Name:** cryptics-resource-group
   - **Region:** East Asia
5. Click "Review + Create"
6. Click "Create"

**Verify:**
- Resource group appears in your resource list
- Status shows "Succeeded"

---

### Step 2: Create App Service Plan

**Purpose:** Define compute resources (CPU, RAM, pricing)

**GUI Steps:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "App Service Plans"
3. Click "+ Create"
4. Fill in details:
   - **Resource Group:** cryptics-resource-group
   - **Name:** cryptics-app-plan
   - **Operating System:** Linux
   - **Region:** East Asia
   - **Pricing Plan:** B1 (Basic)
5. Click "Review + Create"
6. Click "Create"

**Configuration Details:**
- **SKU:** B1 (Basic tier - $13.14/month)
- **OS:** Linux (more cost-effective)
- **vCPU:** 1 shared core
- **Memory:** 1.75 GB
- **Instances:** 1

**Verify:**
- Plan appears in your resource group

---

### Step 3: Create App Service

**Purpose:** Runs your Flet web application

**GUI Steps:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Search for "App Services"
3. Click "+ Create"
4. Fill in details:
   - **Resource Group:** cryptics-resource-group
   - **Name:** cryptics-legion-app
   - **Publish:** Code
   - **Operating System:** Linux
   - **App Service Plan:** cryptics-app-plan
   - **Region:** East Asia
5. Click "Review + Create"
6. Click "Create"

**Verify:**
- App Service appears in your resource group
- Status shows "Running"

---

### Step 4: Configure Environment Variables

**Purpose:** Store configuration without hardcoding secrets

**GUI Steps:**
1. Go to your App Service: **cryptics-legion-app**
2. Click **Settings** > **Configuration**
3. Click **+ New application setting**
4. Add these settings:
   - **Name:** WEBSITES_PORT, **Value:** 8080
   - **Name:** EMAIL_ADDRESS, **Value:** your@gmail.com
   - **Name:** EMAIL_PASSWORD, **Value:** your-app-password
   - **Name:** CURRENCY_API_KEY, **Value:** your-api-key
   - **Name:** DEBUG_MODE, **Value:** False
5. Click **Save**

**Verify:**
- All settings appear in the Configuration list

---

### Step 5: Set Startup Command

**Purpose:** Tell Azure how to start your application

**GUI Steps:**
1. Go to your App Service: **cryptics-legion-app**
2. Click **Settings** > **Configuration**
3. Scroll to **General settings**
4. In **Startup command** field, enter:
   ```
   flet run --web --host 127.0.0.1 --port 8080 Cryptics_legion/src/main.py
   ```
5. Click **Save**

---

### Step 6: Deploy Application Code via SSH

**Purpose:** Upload your code to Azure VM using SSH

**SSH Deployment Steps:**

```bash
# 1. SSH into your Azure VM
ssh -i ______.pem _______@_______

# 2. Clone the repository (if not already cloned)
cd ~
git clone https://github.com/Reylan25/Cryptics-Legion-Projects.git
cd Cryptics-Legion-Projects

# 3. Create Python virtual environment
python3 -m venv Cryptics_legion/src/venv

# 4. Activate virtual environment
source Cryptics_legion/src/venv/bin/activate

# 5. Install dependencies
pip install -r Cryptics_legion/requirements.txt
# Or manually:
pip install flet==0.28.3 bcrypt python-dotenv requests

# 6. Run the application (test locally first)
cd Cryptics_legion/src
python3 -m flet run --web --host 127.0.0.1 --port 8080 main.py

# 7. If working, stop the test (Ctrl+C)
# Then run in background:
nohup python3 -m flet run --web --host 127.0.0.1 --port 8080 main.py > ~/flet.log 2>&1 &

# 8. Verify application is running
sudo ss -tlnp | grep 8080
```

**Set Up Auto-Recovery (systemd):**

```bash
# Create systemd service file
sudo tee /etc/systemd/system/cryptics-flet.service > /dev/null <<'EOF'
[Unit]
Description=Cryptics Legion Flet App
After=network.target

[Service]
Type=simple
User=username
WorkingDirectory=/home/username/Cryptics-Legion-Projects/Cryptics_legion/src
Environment="PATH=/home/username/Cryptics-Legion-Projects/Cryptics_legion/src/venv/bin"
ExecStart=/home/username/Cryptics-Legion-Projects/Cryptics_legion/src/venv/bin/python3 -m flet run --web --host 127.0.0.1 --port 8080 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable cryptics-flet
sudo systemctl start cryptics-flet

# Verify it's running
sudo systemctl status cryptics-flet
```

**Verify Deployment:**
```bash
# Check if Flet is running on port 8080
sudo ss -tlnp | grep 8080

# View application logs
sudo journalctl -u cryptics-flet -f

# Test from local machine
curl -I https://4.240.57.130
```

---

### Step 7: Configure Network Security Group

**Purpose:** Firewall rules - control which ports are accessible

**GUI Steps:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Search for **Network Security Groups**
3. Click **+ Create**
4. Fill in details:
   - **Name:** cryptics-nsg
   - **Resource Group:** cryptics-resource-group
   - **Region:** East Asia
5. Click **Create**

**Add Inbound Rules:**

1. Click your NSG > **Inbound security rules** > **+ Add**

**Rule 1 - Allow HTTPS:**
- Name: AllowHTTPS
- Priority: 100
- Direction: Inbound
- Source: Any (*)
- Destination: Any (*)
- Protocol: TCP
- Port: 443
- Action: Allow

**Rule 2 - Allow HTTP:**
- Name: AllowHTTP
- Priority: 101
- Protocol: TCP
- Port: 80
- Action: Allow

**Rule 3 - Allow Port 8080 (Dev):**
- Name: AllowPort8080
- Priority: 102
- Protocol: TCP
- Port: 8080
- Action: Allow

**Verify Rules:**
- All rules appear in the Inbound security rules list

---

### Step 8: Enable HTTPS

**Purpose:** Secure all connections with SSL/TLS encryption

**GUI Steps:**
1. Go to your App Service: **cryptics-legion-app**
2. Click **Settings** > **TLS/SSL settings**
3. Toggle **HTTPS Only** to **ON**
4. Click **Save**

**Add Custom Domain & SSL Certificate:**
1. Go to your App Service > **Custom domains**
2. Click **+ Add custom domain** (optional)
3. Azure automatically provides a managed certificate

**Verify HTTPS:**
- Navigate to https://4.240.57.130
- Should load without security warnings

---

## ✅ Verification

### Check All Resources Created

**Via Azure Portal:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Click **Resource Groups**
3. Click **cryptics-resource-group**
4. View all resources:
   - App Service Plan
   - App Service
   - Network Security Group
   - Storage Account (managed)

### Test Application Health

```bash
# Check app status
curl -I https://4.240.57.130

# Expected output: HTTP/2 200 OK
```

### View Application Logs

**Via SSH (Recommended):**
```bash
# SSH into VM
ssh -i ______.pem _______@_______

# View live logs from systemd
sudo journalctl -u cryptics-flet -f

# Or view application output log
cat ~/flet.log

# Or tail logs in real-time
tail -f ~/flet.log
```

**Via Azure Portal:**
1. Go to your App Service: **cryptics-legion-app**
2. Click **Monitoring** > **Log stream**
3. View live application logs in real-time

---

## 🐛 Troubleshooting

### Issue 1: Application Returns "502 Bad Gateway"

**Symptom:** Browser shows "Bad Gateway" error

**Solution:**

```bash
# Check if Flet is running on the Azure VM
# First, SSH into the VM
ssh -i ______.pem _______@_______

# Check port 8080
sudo ss -tlnp | grep 8080

# If not running, start it
cd ~/Cryptics-Legion-Projects/Cryptics_legion/src
source venv/bin/activate
flet run --web --host 127.0.0.1 --port 8080 main.py

# Or run in background
nohup flet run --web --host 127.0.0.1 --port 8080 main.py > ~/flet.log 2>&1 &
```

### Issue 2: Flet Module Not Found

**Symptom:** Error: "No module named flet"

**Solution:**

```bash
# Install Python dependencies
cd ~/Cryptics-Legion-Projects/Cryptics_legion/src

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install flet==0.28.3 bcrypt python-dotenv requests

# Run application
flet run --web --host 127.0.0.1 --port 8080 main.py
```


### Issue 3: Application Crashes Repeatedly

**Symptom:** App keeps crashing and restarting

**Solution - Set up Auto-Recovery:**

```bash
# SSH into VM
ssh -i ______.pem _______@_______

# Create systemd service
sudo tee /etc/systemd/system/cryptics-flet.service > /dev/null <<'EOF'
[Unit]
Description=Cryptics Legion Flet App
After=network.target

[Service]
Type=simple
User=cryptic
WorkingDirectory=/home/cryptic/Cryptics-Legion-Projects/Cryptics_legion/src
Environment="PATH=/home/cryptic/Cryptics-Legion-Projects/Cryptics_legion/src/venv/bin"
ExecStart=/home/cryptic/Cryptics-Legion-Projects/Cryptics_legion/src/venv/bin/flet run --web --host 127.0.0.1 --port 8080 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable cryptics-flet
sudo systemctl start cryptics-flet

# Check status
sudo systemctl status cryptics-flet
```

---

## 🔧 Maintenance

### Check Application Status

```bash
# Check if app is running on Azure VM
ssh -i ______.pem _______@_______

# Check Flet process
sudo ss -tlnp | grep 8080

# Should show: python3 listening on 127.0.0.1:8080
```

### View Application Logs

```bash
# On Azure VM
cat ~/flet.log

# Or stream live
sudo journalctl -u cryptics-flet -f
```

### Restart Application

```bash
# Via systemd
sudo systemctl restart cryptics-flet

# Or manually
pkill -f "flet run"
cd ~/Cryptics-Legion-Projects/Cryptics_legion/src
nohup flet run --web --host 127.0.0.1 --port 8080 main.py > ~/flet.log 2>&1 &
```

### Update Application

```bash
# Pull latest code
cd ~/Cryptics-Legion-Projects
git pull origin main

# Restart
sudo systemctl restart cryptics-flet
```

### Monitor Resource Usage

**Via SSH (Command Line):**
```bash
# SSH into VM
ssh -i ______.pem _______@_______

# Check CPU and memory usage
top

# Check disk usage
df -h

# Check network connections
sudo ss -tlnp
```

**Via Azure Portal:**
1. Go to your App Service: **cryptics-legion-app**
2. Click **Metrics** to view:
   - CPU Percentage
   - Memory Percentage
   - Request Count
   - Response Time
3. Set time range to view trends

---

## 📊 Cost Information

### Monthly Breakdown

| Resource | Cost |
|----------|------|
| App Service Plan (B1) | $13.14 |
| Data Transfer | $0.00 |
| Database (SQLite) | $0.00 |
| Security (SSL) | $0.00 |
| Monitoring | $0.00 |
| **TOTAL** | **$13.14/month** |

### Cost Optimization Strategy

✅ **Right-Sized Computing** - B1 tier is cheapest paid option
✅ **Local Database** - SQLite saves $15-50/month vs Azure SQL
✅ **Linux OS** - 20% cheaper than Windows
✅ **Free SSL** - Self-signed or Let's Encrypt (no premium)
✅ **Included Monitoring** - Free tier covers this scale

---

## 📚 Additional Resources

- **Architecture Diagram:** [diagram/architecture_diagram.png](../diagram/architecture_diagram.png)
- **Cost Analysis:** [report/cost-estimate.md](../report/cost-estimate.md)
- **Change Log:** [CHANGELOG.md](../CHANGELOG.md)
- **Live Application:** https://4.240.57.130

### Official Documentation

- [Azure CLI Reference](https://docs.microsoft.com/cli/azure/)
- [App Service Documentation](https://docs.microsoft.com/azure/app-service/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [Flet Framework](https://flet.io/)

---

## 👥 Team
- Carl James Poopalaretnam
- Roger Regalado
- Joshua Sario
---


## 🎓 Academic Information

- **Project:** Cryptics Legion - Azure Cloud Deployment
- **Course:** Cloud Computing
- **Submission Date:** May 16, 2026
- **Repository:** https://github.com/Reylan25/Cryptics-Legion-Projects

---

### Quick Commands Reference

```bash
# Verification
curl -I https://4.240.57.130  # Check if app is running

# Application
ssh -i ______.pem _______@_______
sudo systemctl status cryptics-flet
sudo journalctl -u cryptics-flet -f

# Monitoring via Portal
# Resource Groups > cryptics-resource-group > cryptics-legion-app > Metrics
```
