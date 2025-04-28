# documents/management/commands/index_documents.py

from django.core.management.base import BaseCommand
from documents.models import UrlDocument
import requests

class Command(BaseCommand):
    help = 'Index documents into Elasticsearch'

    def handle(self, *args, **kwargs):
        es_url = 'http://elasticsearch:9200'
        index_name = 'urldocuments'

        for doc in UrlDocument.objects.all():
            document = {
                'title': doc.title,
                'author': doc.authors,
                'year': doc.year,
                'url': doc.url,
            }
            response = requests.post(f'{es_url}/{index_name}/_doc', json=document)

            if response.status_code not in [200, 201]:
                self.stdout.write(self.style.ERROR(f'Error indexing {doc.id}: {response.text}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Indexed document {doc.id}'))
