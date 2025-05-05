from django.core.management.base import BaseCommand
from documents.models import UrlDocument
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

INDEX_NAME = "urldocuments"


class Command(BaseCommand):
    help = 'Index documents with semantic vectors'

    def handle(self, *args, **kwargs):
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        es = Elasticsearch("http://elasticsearch:9200")

        for doc in UrlDocument.objects.all():
            # Embeddings separados para cada campo
            title_embedding = model.encode(doc.title).tolist()
            author_embedding = model.encode(", ".join(doc.authors)).tolist()
            carrera_embedding = model.encode(doc.carrer.name).tolist()

            document = {
                "title": doc.title,
                "authors": doc.authors,
                "year": doc.year,
                "url": doc.url,
                "carrera": doc.carrer.name,
                "title_embedding": title_embedding,
                "author_embedding": author_embedding,
                "carrera_embedding": carrera_embedding
            }

            response = es.index(index=INDEX_NAME, document=document)
            if response.get('result') in ['created', 'updated']:
                self.stdout.write(self.style.SUCCESS(f'Documento {doc.id} indexado exitosamente'))
            else:
                self.stdout.write(self.style.ERROR(f'Error indexando {doc.id}'))
