#!/usr/bin/env python3
"""
send_order_reminders.py
Queries the GraphQL API for orders within the last 7 days
and logs each order's ID and customer email.
"""

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# Configure GraphQL transport
transport = RequestsHTTPTransport(url=GRAPHQL_ENDPOINT, verify=False)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Compute date range
today = datetime.now()
week_ago = today - timedelta(days=7)

# GraphQL query to get recent orders
query = gql(f"""
{{
  orders(orderDate_Gte: "{week_ago.date()}", orderDate_Lte: "{today.date()}") {{
    id
    customer {{
      email
    }}
  }}
}}
""")

try:
    result = client.execute(query)
    orders = result.get("orders", [])

    # Prepare log file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = "/tmp/order_reminders_log.txt"

    with open(log_path, "a") as log_file:
        for order in orders:
            order_id = order.get("id")
            email = order.get("customer", {}).get("email")
            log_file.write(f"[{timestamp}] Reminder for Order ID {order_id} - Email: {email}\n")

    print("Order reminders processed!")

except Exception as e:
    print(f"Error processing reminders: {e}")
