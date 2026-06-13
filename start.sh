#!/bin/bash

echo "🟡 Starting Ollama server in the background..."
ollama serve &

# Esperar activamente hasta 30 segundos a que Ollama levante
echo "⏳ Waiting for Ollama server to respond on port 11434..."
TIMEOUT=30
CONTAINER_PORT=${SERVER_PORT:-8000}
count=0

while ! nc -z localhost 11434; do
    sleep 2
    count=$((count+2))
    if [ $count -ge $TIMEOUT ]; then
        echo "❌ ERROR: Ollama server did not start within $TIMEOUT seconds."
        echo "Continuing anyway to let Django boot..."
        break
    fi
done

if nc -z localhost 11434; then
    echo "✅ Ollama server is running on port 11434"
    echo "📥 Pulling embed model..."
    ollama pull twine/mxbai-embed-xsmall-v1
    echo "✅ Model pulled successfully"
fi

# Iniciar el servidor de Django usando la variable de entorno o el puerto 8000 por defecto
echo "🚀 Starting Django server on port $CONTAINER_PORT..."
exec python manage.py runserver 0.0.0.0:$CONTAINER_PORT
