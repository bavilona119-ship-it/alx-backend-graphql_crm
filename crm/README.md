# CRM Celery Setup Guide

## Setup Steps

1. **Install Redis and dependencies**
   ```bash
   pip install -r requirements.txt
   sudo apt install redis-server
   redis-server

 python manage.py migrate
celery -A crm worker -l info
celery -A crm beat -l infocat 
/tmp/crm_report_log.txt

