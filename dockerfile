# Etapa de construcción
FROM python:3.8-slim as builder

WORKDIR /app

# Instalar dependencias de compilación necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev

# Copiar y instalar dependencias
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir rasa[spacy] \
    && python -m spacy download es_core_news_sm

# Etapa final
FROM python:3.8-slim

WORKDIR /app

# Copiar paquetes instalados desde la etapa anterior
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar el resto del código de la aplicación
COPY . /app

# Ejecutar descarga de modelo de forma condicional
RUN python descarga.py
RUN rasa train

# Exponer puertos necesarios
EXPOSE 5005
EXPOSE 5055

# Comando de inicio
CMD ["rasa", "run", "-m", "models", "--enable-api", "--cors", "*", "--debug"]
