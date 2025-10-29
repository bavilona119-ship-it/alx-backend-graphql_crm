 Step	Description
1	Install Redis and project dependencies
2	Apply Django database migrations
3	Start the Celery worker (celery -A crm worker -l info)
4	Start Celery Beat (celery -A crm beat -l info)
5	Verify generated logs at /tmp/crm_report_log.txt
