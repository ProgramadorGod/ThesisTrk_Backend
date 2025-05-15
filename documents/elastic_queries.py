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

    # -------------------- FILTROS DIRECTOS --------------------
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

    # Carrera embedding (siempre actúa como el filtro semántico base)
    if carrera:
        if isinstance(carrera, str):
            carrera = [carrera]

        carrera_embeddings = []
        for c in carrera:
            emb = embed(c)
            carrera_embeddings.append(emb)

        for idx, emb in enumerate(carrera_embeddings):
            params[f'carrera_embedding_{idx}'] = emb

        carrera_scores = [
            f"cosineSimilarity(params.carrera_embedding_{idx}, 'carrera_embedding')"
            for idx in range(len(carrera_embeddings))
        ]

        # Carrera es el factor dominante, multiplicamos fuerte
        combined_carrera_score = f"10 * (({' + '.join(carrera_scores)}) / {len(carrera_scores)})"
        script_scores.append(combined_carrera_score)

    # Title embedding
    if title:
        params['title_embedding'] = embed(title)
        script_scores.append("cosineSimilarity(params.title_embedding, 'title_embedding')")

    # Author embedding
    if author:
        params['author_embedding'] = embed(author)
        script_scores.append("cosineSimilarity(params.author_embedding, 'author_embedding')")

    # Fallback: general query embedding si no hay title/author
    if not (title or author) and query:
        params["query_embedding"] = embed(query)
        script_scores.extend([
            "cosineSimilarity(params.query_embedding, 'title_embedding')",
            "cosineSimilarity(params.query_embedding, 'author_embedding')"
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
        # Sumar scores suavemente
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

    # Campos que quieres de vuelta
    search_body["_source"] = [
        "title", "authors", "year", "url", "carrera", "carrera_code", "id", "views"
    ]

    return es.search(index=INDEX_NAME, body=search_body)
