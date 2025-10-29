#!/bin/bash
# Script: clean_inactive_customers.sh
# Description: Deletes customers with no orders since a year ago and logs the result.

# Move to project root (update path if needed)
cd "$(dirname "$0")/../.." || exit

# Activate virtual environment if applicable
# source venv/bin/activate

# Run Django shell command to delete inactive customers
deleted_count=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(last_order_date__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the result with timestamp
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo \"[$timestamp] Deleted $deleted_count inactive customers\" >> /tmp/customer_cleanup_log.txt
