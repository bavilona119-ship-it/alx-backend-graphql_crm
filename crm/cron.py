import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    """
    Executes GraphQL mutation to update low-stock products (<10)
    and logs the updated product names and stock levels.
    """
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_path = "/tmp/low_stock_updates_log.txt"

    try:
        # Setup GraphQL client
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
        client = Client(transport=transport, fetch_schema_from_transport=False)

        # Define mutation
        mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                message
                updatedProducts {
                    id
                    name
                    stock
                }
            }
        }
        """)

        # Execute mutation
        result = client.execute(mutation)
        updated = result["updateLowStockProducts"]["updatedProducts"]

        # Log each updated product
        with open(log_path, "a") as log_file:
            log_file.write(f"\n[{timestamp}] Low-stock update executed.\n")
            if updated:
                for p in updated:
                    log_file.write(f" - {p['name']}: new stock = {p['stock']}\n")
            else:
                log_file.write("No low-stock products found.\n")

    except Exception as e:
        with open(log_path, "a") as log_file:
            log_file.write(f"[{timestamp}] Error executing update_low_stock: {e}\n")
