from django.core.management.base import BaseCommand
from documents.models import UrlDocument
from django.core.serializers.json import DjangoJSONEncoder
import json

# IDs con año inválido
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        ids = [410, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 497, 498, 500, 507, 508, 509, 510, 514, 515, 1364, 2620, 2785, 3057, 4173, 4191]

        # Obtener datos
        docs = UrlDocument.objects.filter(id__in=ids).select_related('carrer')  # prefetch carrera

        # Formatear en JSON
        output = [
            {
                "id": doc.id,
                "title": doc.title,
                "carrera": doc.carrer.name if doc.carrer else None,
                "year": doc.year
            }
            for doc in docs
        ]

        # Mostrar como JSON bonito
        print(json.dumps(output, cls=DjangoJSONEncoder, indent=2, ensure_ascii=False))
