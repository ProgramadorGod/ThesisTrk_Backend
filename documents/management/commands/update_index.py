# management/commands/update_indexed_docs.py
from django.core.management.base import BaseCommand
from documents.models import UrlDocument
from elasticsearch import Elasticsearch

INDEX_NAME = "urldocuments"

class Command(BaseCommand):
    help = 'Actualiza solo los documentos ya indexados con nuevos campos'

    def handle(self, *args, **kwargs):
        es = Elasticsearch("http://elasticsearch:9200")

        for doc in UrlDocument.objects.all():
            if es.exists(index=INDEX_NAME, id=str(doc.id)):
                update_doc = {
                    "doc": {
                        
                        "views": doc.visualizations,
                    }
                }
                es.update(index=INDEX_NAME, id=str(doc.id), body=update_doc)
                self.stdout.write(self.style.SUCCESS(f"Documento {doc.id} actualizado"))
            else:
                self.stdout.write(self.style.WARNING(f"Documento {doc.id} no estaba indexado"))
