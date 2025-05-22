from django.urls import path
from .views import ChatWithOllamaView

urlpatterns = [
    path('chat/', ChatWithOllamaView.as_view(), name='chat_with_ollama'),
]
