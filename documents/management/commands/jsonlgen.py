# documents/management/commands/generate_jsonl.py

import json
from django.core.management.base import BaseCommand
from documents.models import UrlDocument  # Aquí usamos 'documents' como la app

class Command(BaseCommand):
    help = "Genera un archivo JSONL para fine-tuning desde UrlDocuments"

    def handle(self, *args, **kwargs):
        output_file = "urldocuments.jsonl"
        count = 0

        with open(output_file, "w", encoding="utf-8") as f:
            for doc in UrlDocument.objects.filter(is_visible=True):
                title = doc.title.strip()
                authors = ', '.join(doc.authors) if isinstance(doc.authors, list) else str(doc.authors)
                year = doc.year.strip()

                user_prompt = f"¿Quién escribió '{title}'?"
                assistant_response = f"El autor(es) es/son {authors}, publicado en {year}."

                entry = {
                    "messages": [
                        {"role": "system", "content": "Eres un asistente que conoce una base de datos de documentos académicos."},
                        {"role": "user", "content": user_prompt},
                        {"role": "assistant", "content": assistant_response}
                    ]
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Archivo {output_file} generado con {count} documentos."))
