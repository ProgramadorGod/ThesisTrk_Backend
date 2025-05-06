# documents/elastic_queries.py

from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

INDEX_NAME = "urldocuments"
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

es = Elasticsearch("http://elasticsearch:9200")

def search_documents(query=None, title=None, author=None, carrera=None, year=None, year_from=None, year_to=None, page=1, size=10):
    params = {}
    script_scores = []
    filters = []

    if title:
        params['title_embedding'] = model.encode(title).tolist()
        script_scores.append("cosineSimilarity(params.title_embedding, 'title_embedding')")

    if author:
        params['author_embedding'] = model.encode(author).tolist()
        script_scores.append("cosineSimilarity(params.author_embedding, 'author_embedding')")


    if carrera:
        if isinstance(carrera, str):
            carrera = [carrera]
        for i, c in enumerate(carrera):
            emb = model.encode(c).tolist()
            params[f'carrera_embedding_{i}'] = emb
            script_scores.append(f"cosineSimilarity(params.carrera_embedding_{i}, 'carrera_embedding')")


    
    if not script_scores and query:
        query_embedding = model.encode(query).tolist()
        params["query_embedding"] = query_embedding
        script_scores.extend([
            "cosineSimilarity(params.query_embedding, 'title_embedding')",
            "cosineSimilarity(params.query_embedding, 'author_embedding')",
            "cosineSimilarity(params.query_embedding, 'carrera_embedding')"
        ])

    if year:
        filters.append({"term": {"year": year}})
    elif year_from or year_to:
        range_filter = {"range": {"year": {}}}
        if year_from:
            range_filter["range"]["year"]["gte"] = str(year_from)
        if year_to:
            range_filter["range"]["year"]["lte"] = str(year_to)
        filters.append(range_filter)

    if not script_scores:
        base_query = {
            "bool": {
                "filter": filters
            }
        } if filters else {"match_all": {}}

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

    return es.search(index=INDEX_NAME, body=search_body)
