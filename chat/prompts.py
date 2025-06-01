PROMPT_EMBEDDING = """
Tu tarea es transformar una consulta larga y detallada del usuario en una frase corta optimizada para hacer una búsqueda semántica basada en embeddings.

No pongas ninguna palabra que no esté relacionada con el resultado final que esperas encontrar.

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

Ejemplo 3:
Entrada:
"Necesito documentos sobre políticas públicas de educación en Colombia durante la pandemia del COVID-19."
Salida:
políticas públicas educación Colombia pandemia COVID-19

---

Ejemplo 4:
Entrada:
"¿Hay trabajos que mencionen el uso de inteligencia artificial en la agricultura sostenible?"
Salida:
inteligencia artificial agricultura sostenible

---

Ejemplo 5:
Entrada:
"Busco tesis dirigidas por el profesor Carlos Méndez relacionadas con energías renovables."
Salida:
Carlos Méndez energías renovables

---

Ejemplo 6:
Entrada:
"Quiero ver documentos que analicen la brecha de género en carreras STEM en universidades colombianas."
Salida:
brecha de género carreras STEM universidades colombianas

---

Ejemplo 7:
Entrada:
"¿Qué estudiantes han trabajado en proyectos sobre cambio climático y comunidades indígenas?"
Salida:
cambio climático comunidades indígenas

---

Ejemplo 8:
Entrada:
"Investigaciones recientes sobre educación virtual en zonas rurales de Santander."
Salida:
educación virtual zonas rurales Santander

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

PROMPT_INTENCION = """
Analiza el siguiente mensaje del usuario y responde solo con el número de una de las siguientes opciones:

1. El usuario quiere algo específico sobre un tema, una persona, un documento, una tesis, un autor, una carrera, o una búsqueda relacionada con contenido académico o institucional.
2. El usuario no está buscando nada útil: solo está saludando, agradeciendo o haciendo conversación sin contenido útil para búsqueda.

No expliques tu decisión. Responde solo con "1" o "2".

Ejemplos:

Mensaje:
"Quiero ver trabajos de investigación sobre agricultura sostenible en Colombia"
Respuesta:
1

Mensaje:
"¿Quién es Luisa Fernanda Márquez y qué ha investigado?"
Respuesta:
1

Mensaje:
"Conoces alguna alexandra ?"
Respuesta:
1

Mensaje:
"Sabrás de alguna cosa que se haya usado para el wifi en unipaz?"
Respuesta:
1

Mensaje:
"¿Qué documentos hay sobre educación rural en Santander?"
Respuesta:
1

Mensaje:
"Tienes información sobre los trabajos del profesor Carlos Méndez?"
Respuesta:
1

Mensaje:
"Quiero ver proyectos relacionados con cambio climático y comunidades indígenas"
Respuesta:
1

Mensaje:
"Hay tesis que mencionen minería y derechos humanos?"
Respuesta:
1

Mensaje:
"Hola, buenos días"
Respuesta:
2

Mensaje:
"Gracias por tu ayuda"
Respuesta:
2

Mensaje:
"Hola!"
Respuesta:
2

Mensaje:
"Me puedes ayudar con algo?"
Respuesta:
2

---

Mensaje:
"{input}"

Respuesta:
"""
