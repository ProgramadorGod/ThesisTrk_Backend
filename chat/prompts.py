PROMPT_EMBEDDING = """

Tu tarea es transformar una consulta larga y detallada del usuario en una frase corta optimizada para hacer una búsqueda semántica basada en embeddings.


Evita repetir palabras o ideas en las distintas consultas. Cada línea debe ser una consulta distinta, directa y concreta.

Ejemplo 1:
Entrada:
"Estoy buscando estudios que analicen cómo afecta la conectividad limitada al rendimiento escolar en zonas rurales de América Latina."

Salida:
conectividad limitada rendimiento escolar zonas rurales América Latina

---

Ejemplo 2:
Entrada:
"¿Quién es Jennifer Alexandra Liévano y qué trabajos hizo en ingeniería informática?"

Salida:
Jennifer Alexandra Liévano


---

Entrada:
{input}

Salida:

"""



PROMPT_INTERPRETA = """
Eres un asistente académico experto en interpretar resultados de búsqueda documental.

Has recibido esta petición original del usuario:
"{consulta}"

Se realizó una búsqueda y se encontraron los siguientes documentos:

{resultados}

Tu tarea es analizar los resultados y responder de forma clara y detallada al usuario, considerando:

1. ¿Alguno de los documentos coincide con el título exacto o muy similar al que se busca?
2. ¿Alguno de los documentos tiene un autor o autores coincidentes o relevantes para la búsqueda?
3. ¿Los documentos están relacionados con el área o carrera mencionada o inferida en la petición?
4. Si hay coincidencias claras, menciónalas indicando título, autor(es), año y área.
5. Si no hay coincidencias relevantes, indícalo claramente.
6. Explica brevemente por qué los documentos encontrados son o no útiles para la consulta.

Responde en un lenguaje sencillo para el usuario final.

---

Respuesta:
"""
