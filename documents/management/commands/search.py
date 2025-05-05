# documents/management/commands/search_docs.py

from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

INDEX_NAME = "urldocuments"



class Command(BaseCommand):
    help = 'Search documents using semantic similarity'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Search query')
        parser.add_argument('--title', type=str, help='Search by title')
        parser.add_argument('--author', type=str, help='Search by author')
        parser.add_argument('--carrera', type=str, help='Search by carrera')

    def handle(self, *args, **options):
        query_text = options['query']
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        es = Elasticsearch("http://elasticsearch:9200")

        queries = []
        params = {}

        # Generar embeddings para cada campo
        if options['title']:
            title_embedding = model.encode(options['title']).tolist()
            queries.append("title")
            params['title_embedding'] = title_embedding

        if options['author']:
            author_embedding = model.encode(options['author']).tolist()
            queries.append("author")
            params['author_embedding'] = author_embedding

        if options['carrera']:
            carrera_embedding = model.encode(options['carrera']).tolist()
            queries.append("carrera")
            params['carrera_embedding'] = carrera_embedding

        # Crear el script de puntuación con comparación por separado para cada campo
        script_scores = []
        if 'title_embedding' in params:
            script_scores.append("cosineSimilarity(params.title_embedding, 'title_embedding')")
        if 'author_embedding' in params:
            script_scores.append("cosineSimilarity(params.author_embedding, 'author_embedding')")
        if 'carrera_embedding' in params:
            script_scores.append("cosineSimilarity(params.carrera_embedding, 'carrera_embedding')")

        # Búsqueda con script_score
        search_body = {
            "size": 5,  # Puedes ajustar el número de resultados
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": " + ".join(script_scores),  # Sumamos todos los script scores
                        "params": params
                    }
                }
            }
        }

        response = es.search(index=INDEX_NAME, body=search_body)
        results = response["hits"]["hits"]

        for hit in results:
            source = hit["_source"]
            score = hit["_score"]
            self.stdout.write(self.style.SUCCESS(f'{score:.3f} → {source["title"]}'))
