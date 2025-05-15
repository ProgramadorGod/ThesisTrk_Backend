#!/bin/bash

echo "🟡 Starting Ollama server in the background..."
ollama serve &

# Esperar unos segundos a que Ollama inicie
sleep 3

# Verificar que el puerto 11434 está abierto (Ollama activo)
if nc -z localhost 11434; then
    echo "✅ Ollama server is running on port 11434"
    ollama pull mxbai-embed-large
    echo "✅ Model mxbai-embed-large pulled successfully"

else
    echo "❌ ERROR: Ollama server did not start properly."
    echo "You may need to start it manually inside the container with: ollama serve"
    exit 1
fi

# Iniciar el servidor de Django
echo "🚀 Starting Django server on port 8000..."
exec python manage.py runserver 0.0.0.0:80
