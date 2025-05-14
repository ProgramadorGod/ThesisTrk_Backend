from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UrlDocument
from ollama import Client
from django.db.models.signals import pre_save
from django.core.exceptions import ObjectDoesNotExist
from elasticsearch import Elasticsearch

client = Client(host="http://127.0.0.1:11434")
es = Elasticsearch("http://elasticsearch:9200")
INDEX_NAME = "urldocuments"

def embed(text):
    response = client.embeddings(model="mxbai-embed-large", prompt=text)
    return response["embedding"]

@receiver(post_save, sender=UrlDocument)
def index_document(sender, instance, **kwargs):
    title_embedding = embed(instance.title)
    author_embedding = embed(", ".join(instance.authors))
    carrera_embedding = embed(instance.carrer.name)

    document = {
        "id": instance.id,
        "carrera_code": instance.carrer.code,
        "title": instance.title,
        "authors": instance.authors,
        "year": instance.year,
        "url": instance.url,
        "views": instance.visualizations,
        "carrera": instance.carrer.name,
        "title_embedding": title_embedding,
        "author_embedding": author_embedding,
        "carrera_embedding": carrera_embedding
    }

    es.index(index=INDEX_NAME, id=str(instance.id), document=document)

@receiver(post_delete, sender=UrlDocument)
def delete_document(sender, instance, **kwargs):
    es.delete(index=INDEX_NAME, id=str(instance.id), ignore=[404])
