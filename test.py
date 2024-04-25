from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

def connect_to_opensearch(region, service, access_key, secret_key, domain_name):
    # Create AWS authentication credentials
    aws_auth = AWS4Auth(access_key, secret_key, region, service)

    # Create the OpenSearch connection
    es = Elasticsearch(
        hosts=[{'host': domain_name, 'port': 443}],
        http_auth=aws_auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    return es

# Example usage
region = "your-region"
service = "es"
access_key = "your-access-key"
secret_key = "your-secret-key"
domain_name = "your-opensearch-domain-name"

es = connect_to_opensearch(region, service, access_key, secret_key, domain_name)

# Test the connection by retrieving the cluster health
print(es.cluster.health())
