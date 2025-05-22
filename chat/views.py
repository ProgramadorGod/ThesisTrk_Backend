import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from documents.views import search_documents
from .serializers import ChatRequestSerializer
from .prompts import PROMPT_EMBEDDING, PROMPT_INTERPRETA

OLLAMA_URL = "http://100.98.13.124:11434"

class ChatWithOllamaView(APIView):
    def post(self, request):
        print("📥 [Paso 1] Solicitud POST recibida")

        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print("❌ Error de validación de datos")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_prompt = serializer.validated_data['prompt']
        print(f"🔍 Prompt del usuario: {user_prompt}")

        embedding_prompts = [
            PROMPT_EMBEDDING.strip().replace("{input}", user_prompt.strip()),
        ]

        all_docs = []
        all_queries = []

        try:
            for idx, emb_prompt in enumerate(embedding_prompts):
                print(f"🧠 [Paso 2] Generando embedding #{idx + 1}...")

                emb_payload = {
                    "model": "phi4-mini",
                    "prompt": emb_prompt,
                    "stream": False,
                    "options": {"temperature": 0.3}
                }
                emb_resp = requests.post(f"{OLLAMA_URL}/v1/completions", json=emb_payload)
                emb_resp.raise_for_status()
                emb_text = emb_resp.json().get("choices", [{}])[0].get("text", "").strip()

                print(f"✅ Embedding #{idx + 1} generado:")
                print(emb_text)

                query_lines = [line.strip() for line in emb_text.split("\n") if line.strip()]

                for line in query_lines:
                    print(f"🔎 Buscando documentos con: '{line}'")
                    all_queries.append(line)
                    search_res = search_documents(query=line, page=1, size=5)
                    docs = search_res["hits"]["hits"]
                    print(f"📄 Documentos encontrados: {len(docs)}")
                    all_docs.extend(docs)

            print("📦 [Paso 3] Filtrando documentos únicos por ID...")
            unique_docs = {}
            for d in all_docs:
                doc_id = d["_id"]
                if doc_id not in unique_docs:
                    unique_docs[doc_id] = d["_source"]
            print(f"✅ Total únicos: {len(unique_docs)}")

            print("📝 [Paso 4] Preparando prompt para interpretación final...")
            resumen_resultados = "\n".join(
                f"- Título: {doc['title']}\n  Autor(es): {', '.join(doc['authors'])}\n  Año: {doc['year']}\n  URL: {doc.get('url', '')}"
                for doc in unique_docs.values()
            )

            interpret_prompt = PROMPT_INTERPRETA.strip() \
                .replace("{consulta}", user_prompt.strip()) \
                .replace("{resultados}", resumen_resultados)

            print("🗣️ [Paso 5] Enviando prompt de interpretación al modelo...")

            interpret_payload = {
                "model": "phi4-mini",
                "prompt": interpret_prompt,
                "stream": False,
                "options": {"temperature": 0.7}
            }

            interpret_response = requests.post(f"{OLLAMA_URL}/v1/completions", json=interpret_payload)
            interpret_response.raise_for_status()
            final_answer = interpret_response.json().get("choices", [{}])[0].get("text", "").strip()

            print("✅ Interpretación completada")
            return Response({
                "modo": "chat",
                "respuesta": final_answer,
                "busqueda_usada": all_queries,
                "resultados": list(unique_docs.values())
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red: {str(e)}")
            return Response({"error": f"Error de red: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



