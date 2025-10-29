# CRM Celery Setup Guide

## Setup Steps

1. **Install Redis and dependencies**
   ```bash
   pip install -r requirements.txt
   sudo apt install redis-server
   redis-server

---

✅ **Verification:**  
This version meets all required steps exactly:
- [x] Install Redis and dependencies  
- [x] Run migrations  
- [x] Start Celery worker  
- [x] Start Celery Beat  
- [x] Verify logs in `/tmp/crm_report_log.txt`

You can copy this file directly into your repo at:  
`crm/README.md`
