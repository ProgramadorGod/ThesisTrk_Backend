from django.core.management.base import BaseCommand
from documents.models import UrlDocument
from ollama import Client
from elasticsearch import Elasticsearch

INDEX_NAME = "urldocuments"
#client = Client(host="http://127.0.0.1:11434")
client = Client(host="http://172.17.0.1:11434")

class Command(BaseCommand):
    help = 'Index documents with semantic vectors'

    def handle(self, *args, **kwargs):
        es = Elasticsearch("http://elasticsearch:9200")

        def embed(text):
            response = client.embeddings(model="twine/mxbai-embed-xsmall-v1", prompt=text)
            return response["embedding"]

        for doc in UrlDocument.objects.all():
            title_embedding = embed(doc.title)
            author_embedding = embed(", ".join(doc.authors))
            carrera_embedding = embed(doc.carrer.name)

            document = {
                "id": doc.id,
                "title": doc.title,
                "views": doc.visualizations,
                "authors": doc.authors,
                "year": doc.year,
                "url": doc.url,
                "carrera": doc.carrer.name,
                "carrera_code": doc.carrer.code,
                "title_embedding": title_embedding,
                "author_embedding": author_embedding,
                "carrera_embedding": carrera_embedding
            }

            response = es.index(index=INDEX_NAME, id=str(doc.id), document=document)
            if response.get('result') in ['created', 'updated']:
                self.stdout.write(self.style.SUCCESS(f'Documento {doc.id} indexado exitosamente'))
            else:
                self.stdout.write(self.style.ERROR(f'Error indexando {doc.id}'))
