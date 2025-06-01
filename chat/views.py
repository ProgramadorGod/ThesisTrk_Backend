import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
from django.conf import settings

from documents.views import search_documents
from .serializers import ChatRequestSerializer
from .prompts import PROMPT_EMBEDDING, PROMPT_INTERPRETA, PROMPT_INTENCION

load_dotenv()  # Carga variables desde .env


def chat_with_openai(messages, temperature=0.7, model="gpt-4o-mini"):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GPT_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


class ChatWithOllamaView(APIView):
    def post(self, request):
        print("📥 [Paso 1] Solicitud POST recibida")

        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_prompt = serializer.validated_data['prompt']
        print(f"📝 Prompt del usuario: {user_prompt}")

        # Paso 1.5: Decidir intención
        intencion_prompt = PROMPT_INTENCION.strip().replace("{input}", user_prompt.strip())
        decision = chat_with_openai([
            {"role": "system", "content": "Devuelve sólo el número 1 o 2 según la intención."},
            {"role": "user", "content": intencion_prompt}
        ], temperature=0.0)

        print(f"🎯 Decisión del modelo: Opción {decision}")

        if decision == "2":
            print("💬 [Modo Chat] Respuesta conversacional")
            chat_answer = chat_with_openai([
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": user_prompt}
            ])
            return Response({
                "modo": "chat",
                "respuesta": chat_answer,
                "busqueda_usada": [],
                "resultados": []
            }, status=status.HTTP_200_OK)

        # Modo búsqueda
        embedding_prompt = PROMPT_EMBEDDING.strip().replace("{input}", user_prompt.strip())
        emb_text = chat_with_openai([
            {"role": "system", "content": "Devuelve consultas optimizadas para una búsqueda."},
            {"role": "user", "content": embedding_prompt}
        ], temperature=0.3)
        print(f"📎 Embedding generado: {emb_text}")

        queries = [line.strip() for line in emb_text.split("\n") if line.strip()]
        all_docs = []

        for q in queries:
            print(f"🔎 Buscando: {q}")
            res = search_documents(query=q, page=1, size=5)
            all_docs.extend(res["hits"]["hits"])

        unique_docs = {}
        for d in all_docs:
            doc_id = d["_id"]
            if doc_id not in unique_docs:
                unique_docs[doc_id] = d["_source"]

        resumen = "\n".join(
            f"- Título: {doc['title']}\n  Autor(es): {', '.join(doc['authors'])}\n  Año: {doc['year']}\n  URL: {doc.get('url', '')}"
            for doc in unique_docs.values()
        )

        interpret_prompt = PROMPT_INTERPRETA.strip() \
            .replace("{consulta}", user_prompt.strip()) \
            .replace("{resultados}", resumen)

        final_answer = chat_with_openai([
            {"role": "system", "content": "Interpreta la consulta del usuario con base en los resultados encontrados."},
            {"role": "user", "content": interpret_prompt}
        ])

        print("✅ Interpretación lista")
        return Response({
            "modo": "busqueda",
            "respuesta": final_answer,
            "busqueda_usada": queries,
            "resultados": list(unique_docs.values())
        }, status=status.HTTP_200_OK)

