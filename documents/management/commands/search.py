from django.core.management.base import BaseCommand
from ollama import Client
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
        client = Client(host="http://127.0.0.1:11434")
        es = Elasticsearch("http://elasticsearch:9200")

        def embed(text):
            response = client.embeddings(model="mxbai-embed-large", prompt=text)
            return response["embedding"]

        queries = []
        params = {}
        script_scores = []

        if options['title']:
            params['title_embedding'] = embed(options['title'])
            script_scores.append("cosineSimilarity(params.title_embedding, 'title_embedding')")

        if options['author']:
            params['author_embedding'] = embed(options['author'])
            script_scores.append("cosineSimilarity(params.author_embedding, 'author_embedding')")

        if options['carrera']:
            params['carrera_embedding'] = embed(options['carrera'])
            script_scores.append("cosineSimilarity(params.carrera_embedding, 'carrera_embedding')")

        # Si no se especifica ningún campo, usar la query general
        if not script_scores:
            params['query_embedding'] = embed(options['query'])
            script_scores.extend([
                "cosineSimilarity(params.query_embedding, 'title_embedding')",
                "cosineSimilarity(params.query_embedding, 'author_embedding')",
                "cosineSimilarity(params.query_embedding, 'carrera_embedding')"
            ])

        search_body = {
            "size": 5,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": " + ".join([f"(0.5 + 0.5 * {s})" for s in script_scores]),
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
