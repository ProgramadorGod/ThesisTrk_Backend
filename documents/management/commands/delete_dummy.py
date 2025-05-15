from django.core.management.base import BaseCommand
from documents.models import UrlDocument

class Command(BaseCommand):
    help = 'Elimina documentos con título "TÍTULO" y URL vacía o nula.'

    def handle(self, *args, **kwargs):
        documents_to_delete = UrlDocument.objects.filter(title="")
        documents_to_delete = UrlDocument.objects.filter(title="TÍTULO")
        count = documents_to_delete.count()

        if count == 0:
            self.stdout.write("✅ No se encontraron documentos con título 'TÍTULO' y URL vacía.")
        else:
            documents_to_delete.delete()
            self.stdout.write(f"🗑️ Se eliminaron {count} documentos con título 'TÍTULO' y URL vacía.")
