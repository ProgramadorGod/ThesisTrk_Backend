from elasticsearch import Elasticsearch
from ollama import Client

INDEX_NAME = "urldocuments"
client = Client(host="http://127.0.0.1:11434")

def embed(text):
    response = client.embeddings(model="mxbai-embed-large", prompt=text)
    return response["embedding"]

es = Elasticsearch("http://elasticsearch:9200")

def search_documents(query=None, title=None, author=None, carrera=None, year=None, year_from=None, year_to=None, page=1, size=10):
    params = {}
    script_scores = []
    filters = []

    # -------------------- FILTROS --------------------
    if year:
        filters.append({"term": {"year": year}})
    elif year_from or year_to:
        range_filter = {"range": {"year": {}}}
        if year_from:
            range_filter["range"]["year"]["gte"] = str(year_from)
        if year_to:
            range_filter["range"]["year"]["lte"] = str(year_to)
        filters.append(range_filter)

    # -------------------- EMBEDDINGS --------------------
    # Title embedding
    if title:
        params['title_embedding'] = embed(title)
        script_scores.append("cosineSimilarity(params.title_embedding, 'title_embedding')")

    # Author embedding
    if author:
        params['author_embedding'] = embed(author)
        script_scores.append("cosineSimilarity(params.author_embedding, 'author_embedding')")

    # Carrera embedding (soporta múltiples carreras)
    if carrera:
        if isinstance(carrera, str):
            carrera = [carrera]
        combined_carrera_embedding = embed(" ".join(carrera))
        params['carrera_embedding'] = combined_carrera_embedding
        script_scores.append("cosineSimilarity(params.carrera_embedding, 'carrera_embedding')")

    # General query embedding (si no hay específicos)
    if not script_scores and query:
        params["query_embedding"] = embed(query)
        script_scores.extend([
            "cosineSimilarity(params.query_embedding, 'title_embedding')",
            "cosineSimilarity(params.query_embedding, 'author_embedding')",
            "cosineSimilarity(params.query_embedding, 'carrera_embedding')"
        ])

    # -------------------- QUERY BODY --------------------
    if not script_scores:
        base_query = {"bool": {"filter": filters}} if filters else {"match_all": {}}
        search_body = {
            "from": (page - 1) * size,
            "size": size,
            "query": base_query
        }
    else:
        safe_score = " + ".join([f"(0.5 + 0.5 * {s})" for s in script_scores])
        search_body = {
            "from": (page - 1) * size,
            "size": size,
            "query": {
                "script_score": {
                    "query": {
                        "bool": {
                            "filter": filters
                        }
                    },
                    "script": {
                        "source": safe_score,
                        "params": params
                    }
                }
            }
        }

    search_body["_source"] = [
        "title", "authors", "year", "url", "carrera", "carrera_code", "id", "views"
    ]

    return es.search(index=INDEX_NAME, body=search_body)
