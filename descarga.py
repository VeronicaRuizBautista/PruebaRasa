from sentence_transformers import SentenceTransformer

model_name = "distilbert-base-nli-stsb-mean-tokens"
model = SentenceTransformer(model_name)
print(f"Modelo '{model_name}' cargado exitosamente.")
