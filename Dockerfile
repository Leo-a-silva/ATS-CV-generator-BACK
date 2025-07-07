# Utiliza una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos requeridos
COPY requirements.txt ./
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que utiliza FastAPI
EXPOSE 8000

# Configurar PYTHONPATH
ENV PYTHONPATH="/app/src"

# Comando para iniciar la aplicación # Quitar '--reload' en producción
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]