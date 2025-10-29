# CRM Celery + Beat Setup Guide

## 🧩 Overview
This guide explains how to configure **Celery** and **Celery Beat** in the CRM Django application.  
The setup enables automatic weekly CRM report generation that summarizes total customers, total orders, and total revenue, with logs stored in `/tmp/crm_report_log.txt`.

---

## ⚙️ Setup Steps

### 1. Install Redis and Dependencies
Install Redis and all required dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
sudo apt install redis-server
redis-server
