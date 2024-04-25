from opensearchpy import OpenSearch

def connect_to_opensearch(region, service, access_key, secret_key, domain_name):
    # Create OpenSearch object with AWS authentication
    os_client = OpenSearch(
        hosts=[{'host': domain_name, 'port': 443}],
        http_auth=(access_key, secret_key),
        use_ssl=True,
        verify_certs=True,
        connection_class="RequestsHttpConnection",
        region=region,
        service=service
    )
    return os_client

# Example usage
region = "your-region"
service = "es"
access_key = "your-access-key"
secret_key = "your-secret-key"
domain_name = "your-opensearch-domain-name"

os_client = connect_to_opensearch(region, service, access_key, secret_key, domain_name)

# Test the connection by retrieving the cluster health
print(os_client.info())
