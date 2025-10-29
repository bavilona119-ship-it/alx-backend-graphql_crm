import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message to confirm CRM app is alive.
    Optionally verifies GraphQL hello field.
    """
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # Write heartbeat log (append mode)
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(message + "\n")

    # Optional: GraphQL health check (hello query)
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql", verify=False)
        client = Client(transport=transport, fetch_schema_from_transport=False)
        query = gql("{ hello }")
        response = client.execute(query)
        with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} GraphQL response: {response.get('hello', 'No response')}\n")
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
            log_file.write(f"{timestamp} GraphQL check failed: {e}\n")
