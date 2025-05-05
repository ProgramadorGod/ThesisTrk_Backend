# documents/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UrlDocument
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "urldocuments"

@receiver(post_save, sender=UrlDocument)
def index_document(sender, instance, **kwargs):
    title_embedding = model.encode(instance.title).tolist()
    author_embedding = model.encode(", ".join(instance.authors)).tolist()
    carrera_embedding = model.encode(instance.carrer.name).tolist()

    document = {
        "title": instance.title,
        "authors": instance.authors,
        "year": instance.year,
        "url": instance.url,
        "carrera": instance.carrer.name,
        "title_embedding": title_embedding,
        "author_embedding": author_embedding,
        "carrera_embedding": carrera_embedding
    }

    es.index(index=INDEX_NAME, id=str(instance.id), document=document)

@receiver(post_delete, sender=UrlDocument)
def delete_document(sender, instance, **kwargs):
    es.delete(index=INDEX_NAME, id=str(instance.id), ignore=[404])
