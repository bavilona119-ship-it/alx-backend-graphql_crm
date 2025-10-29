import requests
from datetime import datetime
from celery import shared_task

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql/"  # adjust if necessary

@shared_task
def generate_crm_report():
    """Weekly CRM report: counts customers, orders, and total revenue."""
    query = """
    query {
      customers {
        id
      }
      orders {
        id
        totalAmount
      }
    }
    """

    try:
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': query})
        data = response.json()

        customers = data['data']['customers']
        orders = data['data']['orders']

        total_customers = len(customers)
        total_orders = len(orders)
        total_revenue = sum([float(order['totalAmount']) for order in orders])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = (
            f"{timestamp} - Report: {total_customers} customers, "
            f"{total_orders} orders, {total_revenue:.2f} revenue\n"
        )

        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(log_message)

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"Error generating report at {datetime.now()}: {str(e)}\n")
