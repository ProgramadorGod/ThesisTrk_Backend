# elastic_client.py

import requests

ELASTIC_URL = 'http://elasticsearch:9200/urldocuments/_search'

def search_in_elastic(index, body):
    url = f"http://elasticsearch:9200/{index}/_search"
    print("Elasticsearch request body:", body)  # Depuración
    response = requests.post(url, json=body)
    response.raise_for_status()
    return response.json()
