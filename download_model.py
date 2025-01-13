from transformers import T5ForConditionalGeneration, T5Tokenizer

# Cargar el modelo y el tokenizador desde Hugging Face
model_name = "google/flan-t5-base"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Guardar el modelo localmente
model.save_pretrained('./flan-t5-base')
tokenizer.save_pretrained('./flan-t5-base')
