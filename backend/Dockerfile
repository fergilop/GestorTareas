# Usamos una versión ligera de Python
FROM python:3.13-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos las dependencias del sistema necesarias (si las hubiera)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de librerías e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código del backend
COPY . .

# Render asigna un puerto dinámico mediante la variable $PORT. 
# Usamos un shell script corto para que uvicorn lo lea correctamente.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}