from rasa_sdk import Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5ForConditionalGeneration, T5Tokenizer
import json
from fuzzywuzzy import process

class ActionGenerateResponse(Action):

    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained('google/flan-t5-base')
        self.model = T5ForConditionalGeneration.from_pretrained('google/flan-t5-base')

        # Cargar los datos desde el archivo JSON
        self.datos = self.cargar_datos()

    def cargar_datos(self):
        """Cargar los datos desde un archivo JSON."""
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(f"Datos cargados: {data}")  # Verificar que los datos se cargan correctamente
                return data
        except Exception as e:
            print(f"Error al cargar el archivo JSON: {e}")
            return {}

    def name(self) -> str:
        """Nombre de la acción personalizada."""
        return "action_generate_response"

    from typing import List
    async def run(self, dispatcher: CollectingDispatcher, tracker, domain) -> List[EventType]:
        user_question = tracker.latest_message.get('text').lower()

        # Verificar que la pregunta está siendo tomada correctamente
        print(f"Pregunta recibida: {user_question}")

        # Buscar la respuesta en los datos cargados
        respuesta = self.datos.get(user_question, "Lo siento, no tengo una respuesta para eso.")

        # Imprimir la respuesta que se encuentra o no
        print(f"Respuesta encontrada: {respuesta}")

        # Generar respuesta con Flan-T5
        input_text = f"Pregunta: {user_question} Datos: {respuesta} Respuesta:"
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
        
        outputs = self.model.generate(**inputs, max_length=100, num_return_sequences=1)
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Enviar respuesta al usuario
        dispatcher.utter_message(text=generated_text)

        return []
