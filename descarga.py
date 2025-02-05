import os
from sentence_transformers import SentenceTransformer

model_name = "paraphrase-MiniLM-L6-v2"
model_path = os.path.expanduser(f"~/.cache/torch/sentence_transformers/{model_name}")

if not os.path.exists(model_path):
    model = SentenceTransformer(model_name)
    print(f"Modelo '{model_name}' descargado y guardado en {model_path}")
else:
    print(f"Modelo '{model_name}' ya existe en {model_path}")
