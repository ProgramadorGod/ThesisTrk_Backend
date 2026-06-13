import json
from documents.models import UrlDocument

with open('/app/data.json') as f:
    data = json.load(f)

docs = [obj for obj in data if obj['model'] == 'documents.document']
created = 0
errors = 0
for obj in docs:
    f = obj['fields']
    try:
        UrlDocument.objects.get_or_create(
            title=f['title'],
            defaults={
                'carrer_id': f['carrer'],
                'authors': f['authors'],
                'year': f['year'],
                'url': f['url'],
                'is_visible': f['is_visible'],
                'stage_id': f['stage'],
                'progress_percentage': f['progress_percentage'],
                'document_type_id': f['document_type'],
                'visualizations': 0,
                'description': '',
            }
        )
        created += 1
    except Exception as e:
        errors += 1
        if errors <= 3:
            print('Error:', e, f['title'][:50])

print(f'Procesados: {created}/{len(docs)}, Errores: {errors}')
