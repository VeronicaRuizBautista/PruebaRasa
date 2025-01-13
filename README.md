# 🚀 **Documentación para el Chatbot Rasa con Flan-t5-base**  

## 📋 **Requisitos previos**
Antes de empezar, asegúrate de tener lo siguiente:

- Microsoft Visual C++ Build Tools
- Python3.8
- PostgreSQL
- setuptools==58.0.4

---

## 🛠️ **Pasos para configurar y ejecutar el chatbot**

### 1️⃣ **Crear y activar un entorno virtual**
```bash
python3.8 -m venv venv
.\venv\Scripts\activate
```

### 2️⃣ **Instalar dependencias necesarias**
Ejecuta los siguientes comandos para instalar los paquetes requeridos:

```bash
pip install psycopg2-binary==2.9.3
pip install fire==0.4.0
pip install transformers torch
pip install datasets accelerate
pip install fuzzywuzzy
pip install rasa[transformers]
```

### 3️⃣ **Descargar el modelo necesario**
Ejecuta el script para descargar el modelo requerido por el chatbot:

```bash
python download_model.py
```

### 4️⃣ **Iniciar el servidor de acciones**
Este comando ejecuta el servidor que manejará las acciones personalizadas del chatbot:

```bash
rasa run actions
```

### 5️⃣ **Iniciar el servidor del chatbot**
Finalmente, entrena e inicia el chatbot con los siguientes comandos:

```bash
rasa train
rasa shell
```
