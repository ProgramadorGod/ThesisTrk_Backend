from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch

class Command(BaseCommand):
    help = 'Borrar el índice de Elasticsearch para los documentos'

    def handle(self, *args, **kwargs):
        es = Elasticsearch("http://elasticsearch:9200")
        index_name = "urldocuments"  # O el nombre del índice que estás usando

        # Verificar si el índice existe
        if es.indices.exists(index=index_name):
            # Borrar el índice
            es.indices.delete(index=index_name)
            self.stdout.write(self.style.SUCCESS(f'Índice "{index_name}" eliminado correctamente.'))
        else:
            self.stdout.write(self.style.WARNING(f'El índice "{index_name}" no existe.'))
