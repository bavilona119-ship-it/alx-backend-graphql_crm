#!/bin/bash
# Deletes customers with no orders in the past year and logs the action.

cd "$(dirname "$0")/../.." || exit

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

timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$timestamp] Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
