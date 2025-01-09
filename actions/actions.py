from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_out_of_scope") 

        # Revertir el mensaje del usuario que llevó al fallback
        return [UserUtteranceReverted()]


import spacy
import re

# Cargar el modelo de spacy
nlp = spacy.load("es_core_news_sm")

class ActionMultipleQuestions(Action):
    def name(self):
        return "action_multiple_questions"

    def run(self, dispatcher, tracker, domain):
        # Obtener el texto de la última pregunta del usuario
        user_message = tracker.latest_message.get("text")
        
        # Procesar el texto con Spacy
        doc = nlp(user_message)
        
        # Dividir las preguntas (en este caso, por los signos de pregunta)
        preguntas = re.split(r'\?+', user_message)
        
        # Limpiar y eliminar cualquier pregunta vacía
        preguntas = [pregunta.strip() for pregunta in preguntas if pregunta.strip()]
        
        # Respuestas por defecto
        respuestas = []
        
        # Manejo de cada pregunta de acuerdo con el tipo de intención
        for pregunta in preguntas:
            # Lógica de respuestas basada en las intenciones
            if "reporto una licencia" in pregunta.lower():
                respuestas.append("Si deseas reportar la novedad sobre una licencia remunerada o no remunerada, en Midasoft debes ir a 'Mis transacciones' y en 'Solicitudes nómina' seleccionar la opción 'Solicitud de permiso'. Aquí tendrás disponibles los permisos y licencias remuneradas o no remuneradas. Debes justificar la ausencia, seleccionar la licencia correspondiente, ingresar las fechas y adjuntar el documento necesario, esto lo puedes hacer dando clic en examinar. Agregas el documento. Y cuando ya esté adjunto, solo le das clic en aceptar y llegará la novedad a tu líder.")
            elif "tipos de licencias" in pregunta.lower():
                respuestas.append("Los tipos de ausencias disponibles son: licencia por calamidad, licencia de luto, licencia de matrimonio, día de la familia, flex y solvo.")
            elif "Tipos de incapacidad" in pregunta.lower():
                respuestas.append("Los tipos de incapacidad disponibles son: por accidente de trabajo, por enfermedad general, incapacidad de un aprendiz, accidente laboral de un aprendiz, y situación de maternidad o paternidad.")
            # Agrega más condiciones para otros tipos de preguntas
            else:
                respuestas.append("Lo siento, no entendí la pregunta: " + pregunta)

        # Responder con todas las respuestas
        response = "\n\n".join(respuestas)
        dispatcher.utter_message(text=response)

        return []
    

class ActionInitialGreet(Action):
    def name(self) -> str:
        return "action_initial_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        dispatcher.utter_message(text="¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte?")
        return []