# Changelog

All notable changes to the Cryptics Legion Azure Cloud Deployment project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


---

## [2026-05-16] - v1.0.0 - Production Deployment Complete

### Added
- `[Carl James Poopalaretnam]` - Deployed complete Azure infrastructure using Azure GUI (Portal)
- `[Carl James Poopalaretnam]` - Created VM and set up Azure Resource Group "cryptics-resource-group" in East Asia region
- `[Carl James Poopalaretnam]` - Deployed application code using SSH/CMD commands on Azure VM
- `[Carl James Poopalaretnam]` - Provisioned App Service Plan "cryptics-app-plan" (B1 tier: 1 vCPU, 1.75 GB RAM)
- `[Carl James Poopalaretnam]` - Created App Service "cryptics-legion-app" with Python 3.11 runtime
- `[Carl James Poopalaretnam]` - Configured Network Security Group with 3 inbound rules (HTTPS 443, HTTP 80, Port 8080)
- `[Carl James Poopalaretnam]` - Implemented HTTPS-only mode for all connections
- `[Carl James Poopalaretnam]` - Set up self-signed SSL/TLS certificates (RSA 2048-bit)
- `[Carl James Poopalaretnam]` - Deployed Nginx reverse proxy for SSL/TLS termination
- `[Carl James Poopalaretnam]` - Configured HTTP → HTTPS redirect rules
- `[Carl James Poopalaretnam]` - Created systemd service for auto-recovery (cryptics-flet.service)
- `[Carl James Poopalaretnam]` - Implemented automatic application restart on crash (RestartSec=10)
- `[Carl James Poopalaretnam]` - Tested and verified all 6 Azure resources deployed successfully
- `[Carl James Poopalaretnam]` - Created comprehensive deployment documentation (deployment/README.md)
- `[Carl James Poopalaretnam]` - Documented troubleshooting guide with 5 common issues and solutions
- `[Carl James Poopalaretnam]` - Set up monitoring and logging infrastructure
- `[Carl James Poopalaretnam]` - Installed and configured Python virtual environment with all dependencies
- `[Carl James Poopalaretnam]` - Created requirements.txt with exact versions of all packages
- `[Carl James Poopalaretnam]` - Tested Flet application end-to-end on deployed infrastructure
- `[Carl James Poopalaretnam]` - Created live deployment verification procedures

### Added - Documentation
- `[Carl James Poopalaretnam]` - Created comprehensive README.md with project overview
- `[Carl James Poopalaretnam]` - Documented prerequisites and quick start guide
- `[Carl James Poopalaretnam]` - Created step-by-step deployment guide 
- `[Carl James Poopalaretnam]` - Added verification procedures for deployment confirmation
- `[Carl James Poopalaretnam]` - Created troubleshooting section covering 5 major issues
- `[Carl James Poopalaretnam]` - Documented maintenance procedures and update processes
- `[Carl James Poopalaretnam]` - Added cost information and optimization strategies
- `[Carl James Poopalaretnam]` - Created live demo script with SSH commands
- `[Carl James Poopalaretnam]` - Created conclusion script for video presentation

### Added - Architecture & Design
- `[Joshua Sario]` - Designed complete system architecture with security zones
- `[Joshua Sario]` - Created professional architecture diagram (architecture_diagram.png)
- `[Joshua Sario]` - Designed security boundary layout (public vs private zones)
- `[Joshua Sario]` - Specified all Azure resources and their connections
- `[Joshua Sario]` - Designed cloud optimization strategy
- `[Joshua Sario]` - Created visual representation of data flow

### Added - Cost Analysis
- `[Roger Regalado]` - Analyzed and documented cost breakdown (cost-estimate.md)
- `[Roger Regalado]` - Calculated monthly cost: $13.14 (B1 tier + no database costs)
- `[Roger Regalado]` - Calculated annual cost: $157.68
- `[Roger Regalado]` - Identified 6 cost optimization strategies
- `[Roger Regalado]` - Compared alternative Azure service tiers
- `[Roger Regalado]` - Created pricing breakdown for each resource
- `[Roger Regalado]` - Documented future cost scaling scenarios
- `[Roger Regalado]` - Added Azure Pricing Calculator screenshot

### Changed
- `[Carl James Poopalaretnam]` - Deployed code via SSH/CMD instead of automated deployment center
- `[Carl James Poopalaretnam]` - Switched from desktop mode to web mode for Flet (avoids GTK library dependency)
- `[Carl James Poopalaretnam]` - Updated startup command from `flet` to `python3 -m flet run` for VM compatibility
- `[Carl James Poopalaretnam]` - Modified Nginx configuration to handle WebSocket upgrades for real-time features
- `[Carl James Poopalaretnam]` - Configured environment variables for all sensitive data (no hardcoded secrets)
- `[Carl James Poopalaretnam]` - Updated App Service to enforce HTTPS-only connections
- `[Carl James Poopalaretnam]` - Switched from manual process to systemd service management

### Fixed
- `[Carl James Poopalaretnam]` - Fixed "libgtk-3.so.0: cannot open shared object file" error by using web mode
- `[Carl James Poopalaretnam]` - Fixed "502 Bad Gateway" error by ensuring Flet process runs continuously
- `[Carl James Poopalaretnam]` - Fixed "bad gateway" issue by implementing systemd auto-restart service
- `[Carl James Poopalaretnam]` - Fixed Nginx upstream connection by configuring localhost:8080 correctly
- `[Carl James Poopalaretnam]` - Fixed missing system libraries (libgstapp-1.0.so.0) by installing Ubuntu packages
- `[Carl James Poopalaretnam]` - Fixed DNS package resolution for Ubuntu 24.04 Noble (t64 variants)
- `[Carl James Poopalaretnam]` - Fixed Python module installation by creating virtual environment
- `[Carl James Poopalaretnam]` - Fixed Flet version conflicts (0.28.3 consistency across all packages)
- `[Carl James Poopalaretnam]` - Fixed SSH authentication by using correct key file path and permissions

---

## [2026-05-15] - v0.9.0 - Pre-Production Testing & Validation

### Added
- `[Carl James Poopalaretnam]` - Set up local testing environment with Flet on port 8080
- `[Carl James Poopalaretnam]` - Created requirements.txt with all Python dependencies
- `[Carl James Poopalaretnam]` - Set up basic Nginx reverse proxy configuration
- `[Carl James Poopalaretnam]` - Generated self-signed SSL certificate for HTTPS testing
- `[Carl James Poopalaretnam]` - Tested application end-to-end functionality
- `[Carl James Poopalaretnam]` - Verified all Azure resources connectivity
- `[Joshua Sario]` - Created detailed architecture design documentation
- `[Roger Regalado]` - Analyzed application cost implications

### Changed
- `[Carl James Poopalaretnam]` - Updated Flet version to 0.28.3 for stability and compatibility
- `[Carl James Poopalaretnam]` - Modified proxy_pass to include HTTP version 1.1 headers for compatibility
- `[Carl James Poopalaretnam]` - Refined NSG rules based on security testing

### Fixed
- `[Carl James Poopalaretnam]` - Fixed port binding issues on Azure VM
- `[Carl James Poopalaretnam]` - Resolved Python module import errors
- `[Carl James Poopalaretnam]` - Corrected Nginx permission issues

---

## [2026-05-14] - v0.8.0 - Infrastructure Design & Planning

### Added
- `[Joshua Sario]` - Designed overall system architecture
- `[Joshua Sario]` - Planned security zone boundaries (public vs private)
- `[Joshua Sario]` - Designed network topology and resource connections
- `[Roger Regalado]` - Initiated cost analysis and estimation
- `[Roger Regalado]` - Planned pricing strategy for B1 tier selection



### Documentation
- `[Carl James Poopalaretnam]` - Created initial project README skeleton
- `[Joshua Sario]` - Started architecture documentation
- `[Roger Regalado]` - Created cost estimation spreadsheet

---

## [2026-05-13] - v0.7.0 - Requirements & Assessment

### Added
- `[Carl James Poopalaretnam]` - Reviewed all 4 project deliverables
- `[Carl James Poopalaretnam]` - Assessed deployment requirements
- `[Joshua Sario]` - Analyzed Azure service options
- `[Roger Regalado]` - Evaluated cost optimization opportunities
- `[Carl James Poopalaretnam]` - Documented technical requirements

### Documentation
- `[Carl James Poopalaretnam]` - Started requirements documentation
- `[Joshua Sario]` - Created architecture planning notes
- `[Roger Regalado]` - Began cost analysis research

---

## Release Notes

### Version 1.0.0 (May 16, 2026)
**Status:** ✅ PRODUCTION READY

**Key Achievements:**
- ✅ All 4 deliverables completed
- ✅ Application live at https://4.240.57.130
- ✅ Cost optimized at $13.14/month
- ✅ Security baseline implemented
- ✅ Complete documentation provided
- ✅ Video presentation recorded
- ✅ 99.95% SLA uptime guarantee
- ✅ Auto-recovery implemented

**Deployed By:** Carl James Poopalaretnam
**Architecture Designed By:** Joshua Sario
**Cost Analysis By:** Roger Regalado

---

## Deployment Timeline

| Date | Milestone | Status | Owner |
|------|-----------|--------|-------|
| May 13 | Requirements Analysis | ✅ Complete | Carl James |
| May 14 | Architecture Design | ✅ Complete | Joshua Sario |
| May 15 | Pre-production Testing | ✅ Complete | Carl James |
| May 16 | Production Deployment | ✅ Complete | Carl James |
| May 16 | Documentation Finalized | ✅ Complete | Carl James |
| May 16 | Video Recording | ✅ Complete | All |
| May 16 | Final Submission | ✅ Complete | All |

---

## Contributor Summary

### Carl James Poopalaretnam - Deployment 
**Role:** Cloud Deployment Lead, Infrastructure Implementation

**Key Contributions:**
- Deployed all Azure infrastructure via Portal GUI
- Deployed application code via SSH/CMD commands
- Set up and configured all 6 Azure resources
- Implemented security and networking
- Created comprehensive deployment documentation
- Troubleshot and fixed all deployment issues
- Tested end-to-end functionality
- Set up monitoring and auto-recovery via systemd
- Created live demo scripts
- Created presentation documentation

**Deployment Methods Used:** Azure Portal GUI + SSH/CMD
**Lines of Code/Config:** 500+ (Nginx config, systemd service, SSH deployment scripts)
**Documentation Created:** 5,000+ words

---

### Joshua Sario - Architect
**Role:** System Architect, Design Lead

**Key Contributions:**
- Designed complete system architecture
- Created professional architecture diagram
- Designed security boundaries and zones
- Specified Azure resource topology
- Planned cloud optimizations
- Created visual data flow diagrams

**Deliverables:** Architecture Diagram (architecture_diagram.png)

---

### Roger Regalado - Finance & Analysis
**Role:** Cost Analyst, Budget Optimization

**Key Contributions:**
- Analyzed and documented cost breakdown
- Identified 6 cost optimization strategies
- Calculated monthly/annual costs
- Compared alternative solutions
- Created pricing strategy
- Documented future scaling costs

**Deliverables:** Cost Estimate Report (cost-estimate.md)

---

## Contact & Support

**Project Head:** Carl James Poopalaretnam
**Architecture:** Joshua Sario
**Cost Analysis:** Roger Regalado

**GitHub:** https://github.com/Reylan25/Cryptics-Legion-Projects
**Live Application:** https://4.240.57.130


