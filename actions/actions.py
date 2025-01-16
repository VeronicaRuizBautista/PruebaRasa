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


import re
from sentence_transformers import SentenceTransformer, util
class ActionProcesarPreguntas(Action):
    def name(self) -> Text:
        return "action_multiple_questions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Preguntas del usuario
        mensaje_usuario = tracker.latest_message.get('text', "").lower()  # Convertir a minúsculas
        preguntas_usuario = re.split(r'[¿?;.\n]+', mensaje_usuario)
        preguntas_usuario = [pregunta.strip() for pregunta in preguntas_usuario if pregunta.strip()]

        # Respuestas predefinidas
        respuestas_dict = {
            "enviar requerimiento": "Para enviar un requerimiento, accede al CRM de Solver, haz clic en Gestión Helpdesk, luego en Enviar nuevo requerimiento y llena los campos necesarios.",
            "clasificacion ergonomica": "En clasificación puedes seleccionar elementos como base para dos monitores, laptop o reposapiés.",
            "seguimiento requerimiento": "Puedes hacer un seguimiento revisando el estado de tu caso: abierto, sin asignar o cerrado.",
            "solvo id": "Así como tienes una cédula de ciudadanía que te identifica frente al estado, en Solvo también tenemos algo llamado Solvo ID. Este será una serial que te identificará dentro de la empresa como un empleado o un solver. Si quieres conocer cuál es tu Solvo ID, puedes ingresar a Midasoft y en la esquina superior derecha debajo de tu cédula vas a encontrar este número.",
            "seguridad social": "Si deseas ver dónde está la información respecto a tu seguridad social, ingresa a Midasoft y en 'Mis Datos', dándole clic a 'Información Seguridad Social', vas a poder encontrar todo lo relacionado con tu pensión, tu ARL y tu EPS. Si deseas ver dónde están tus cesantías, puedes regresar y donde dice 'Fondo de Cesantías' encontrarás el dato que necesitas.",
            "reporto una licencia": "Si deseas reportar la novedad sobre una licencia remunerada o no remunerada, en Midasoft debes ir a 'Mis transacciones' y en 'Solicitudes nómina' seleccionar la opción 'Solicitud de permiso'. Aquí tendrás disponibles los permisos y licencias remuneradas o no remuneradas. Debes justificar la ausencia, seleccionar la licencia correspondiente, ingresar las fechas y adjuntar el documento necesario, esto lo puedes hacer dando clic en examinar. Agregas el documento. Y cuando ya esté adjunto, solo le das clic en aceptar y llegará la novedad a tu líder.",
            "tipos de licencias": "Los tipos de ausencias disponibles son: licencia por calamidad, licencia de luto, licencia de matrimonio, día de la familia, flex y solvo.",
            "tipos de incapacidad": "Los tipos de incapacidad disponibles son: por accidente de trabajo, por enfermedad general, incapacidad de un aprendiz, accidente laboral de un aprendiz, y situación de maternidad o paternidad.",
            "cita psicologica": "Para pedir una cita de acompañamiento psicológico, ve a 'Mis transacciones', luego a 'Seguridad y salud en el trabajo' y selecciona 'Solicitud de citas'. Escoge el tipo de cita, tu ciudad, la sede y la fecha de programación.",
            "cita psicologica gratis": "Tienes derecho a cuatro citas gratuitas con la profesional. Después de esas, deberás asumir el costo con una tarifa diferencial.",
            "disponibilidad citas psicologicas": "Las citas se agendan semanalmente. Si no hay disponibilidad, revisa más tarde y permanece pendiente de nuevas aperturas.",
            "montar requerimiento": "Para montar un nuevo requerimiento, ve al CRM, haz clic en Gestión Helpdesk y selecciona 'Enviar nuevo requerimiento'. Agrega un asunto, selecciona un ítem y completa los detalles. No olvides guardar tu solicitud.",
            "descargar comprobante": "Para descargar tu comprobante de pago, entra a Midasoft, busca tu nómina y descárgala en formato PDF.",
            "informacion comprobante": "El comprobante incluye tu Solvo ID, tu nombre, salario mensual, cargo, cuenta bancaria, conceptos de pago y deducciones, además del valor neto a pagar.",
            "deducciones comprobante": "Las deducciones reflejadas incluyen aportes a salud, pensión u otros conceptos aplicables según tu nómina.",
            "valor neto": "El valor neto a pagar es el monto que finalmente se te deposita después de aplicar todas las deducciones.",
            "revisar comprobante": "Para revisar tu comprobante de pago, ve a 'Mis certificaciones' y haz clic en 'Comprobante de nómina'. Selecciona el periodo que deseas consultar.",
            "enviar comprobante correo": "Puedes enviar tu comprobante a tu correo seleccionando el periodo y haciendo clic en 'Enviar al correo electrónico'.",
            "periodo comprobante": "En 'Mis certificaciones', selecciona el periodo que deseas consultar. Por ejemplo, el primer pago de mayo, y luego descarga o envía el comprobante."
        }

        # Modelo de embeddings
        model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

        # Convertir preguntas y respuestas en embeddings
        preguntas_embeddings = model.encode(preguntas_usuario)
        respuestas_keys = list(respuestas_dict.keys())
        respuestas_embeddings = model.encode(respuestas_keys)

        # Calcular similitud entre preguntas y respuestas
        similitudes = util.pytorch_cos_sim(preguntas_embeddings, respuestas_embeddings)

        # Procesar preguntas y seleccionar la mejor respuesta
        respuestas = []
        for i, pregunta in enumerate(preguntas_usuario):
            max_similitud = similitudes[i].max().item()
            mejor_respuesta_idx = similitudes[i].argmax().item()

            # Umbral mínimo para considerar una respuesta válida
            umbral_similitud = 0.5
            if max_similitud >= umbral_similitud:
                mejor_respuesta = respuestas_dict[respuestas_keys[mejor_respuesta_idx]]
                respuestas.append(f"Pregunta: {pregunta}\nRespuesta: {mejor_respuesta}")
            else:
                respuestas.append(f"Pregunta: {pregunta}\nRespuesta: Lo siento, no tengo información sobre esto en este momento.")

        # Responder al usuario
        dispatcher.utter_message("\n\n".join(respuestas))
        return []



# import spacy
# import re

# # Cargar el modelo de Spacy
# nlp = spacy.load("es_core_news_sm")

# class ActionMultipleQuestions(Action):
#     def name(self):
#         return "action_multiple_questions"

#     def run(self, dispatcher, tracker, domain):
#         # Obtener el texto de la última pregunta del usuario
#         user_message = tracker.latest_message.get("text")
        
#         # Procesar el texto con Spacy
#         doc = nlp(user_message)
        
#         # Dividir las preguntas (en este caso, por los signos de pregunta)
#         preguntas = re.split(r'\?+', user_message)
        
#         # Limpiar y eliminar cualquier pregunta vacía
#         preguntas = [pregunta.strip() for pregunta in preguntas if pregunta.strip()]
        
#         # Diccionario de respuestas
#         respuestas_dict = {
#             "enviar requerimiento": "Para enviar un requerimiento, accede al CRM de Solver, haz clic en Gestión Helpdesk, luego en Enviar nuevo requerimiento y llena los campos necesarios.",
#             "clasificacion ergonomica": "En clasificación puedes seleccionar elementos como base para dos monitores, laptop o reposapiés.",
#             "seguimiento requerimiento": "Puedes hacer un seguimiento revisando el estado de tu caso: abierto, sin asignar o cerrado.",
#             "solvo id": "Así como tienes una cédula de ciudadanía que te identifica frente al estado, en Solvo también tenemos algo llamado Solvo ID. Este será una serial que te identificará dentro de la empresa como un empleado o un solver. Si quieres conocer cuál es tu Solvo ID, puedes ingresar a Midasoft y en la esquina superior derecha debajo de tu cédula vas a encontrar este número.",
#             "seguridad social": "Si deseas ver dónde está la información respecto a tu seguridad social, ingresa a Midasoft y en 'Mis Datos', dándole clic a 'Información Seguridad Social', vas a poder encontrar todo lo relacionado con tu pensión, tu ARL y tu EPS. Si deseas ver dónde están tus cesantías, puedes regresar y donde dice 'Fondo de Cesantías' encontrarás el dato que necesitas.",
#             "reporto una licencia": "Si deseas reportar la novedad sobre una licencia remunerada o no remunerada, en Midasoft debes ir a 'Mis transacciones' y en 'Solicitudes nómina' seleccionar la opción 'Solicitud de permiso'. Aquí tendrás disponibles los permisos y licencias remuneradas o no remuneradas. Debes justificar la ausencia, seleccionar la licencia correspondiente, ingresar las fechas y adjuntar el documento necesario, esto lo puedes hacer dando clic en examinar. Agregas el documento. Y cuando ya esté adjunto, solo le das clic en aceptar y llegará la novedad a tu líder.",
#             "tipos de licencias": "Los tipos de ausencias disponibles son: licencia por calamidad, licencia de luto, licencia de matrimonio, día de la familia, flex y solvo.",
#             "tipos de incapacidad": "Los tipos de incapacidad disponibles son: por accidente de trabajo, por enfermedad general, incapacidad de un aprendiz, accidente laboral de un aprendiz, y situación de maternidad o paternidad.",
#             "cita psicologica": "Para pedir una cita de acompañamiento psicológico, ve a 'Mis transacciones', luego a 'Seguridad y salud en el trabajo' y selecciona 'Solicitud de citas'. Escoge el tipo de cita, tu ciudad, la sede y la fecha de programación.",
#             "cita psicologica gratis": "Tienes derecho a cuatro citas gratuitas con la profesional. Después de esas, deberás asumir el costo con una tarifa diferencial.",
#             "disponibilidad citas psicologicas": "Las citas se agendan semanalmente. Si no hay disponibilidad, revisa más tarde y permanece pendiente de nuevas aperturas.",
#             "montar requerimiento": "Para montar un nuevo requerimiento, ve al CRM, haz clic en Gestión Helpdesk y selecciona 'Enviar nuevo requerimiento'. Agrega un asunto, selecciona un ítem y completa los detalles. No olvides guardar tu solicitud.",
#             "descargar comprobante": "Para descargar tu comprobante de pago, entra a Midasoft, busca tu nómina y descárgala en formato PDF.",
#             "informacion comprobante": "El comprobante incluye tu Solvo ID, tu nombre, salario mensual, cargo, cuenta bancaria, conceptos de pago y deducciones, además del valor neto a pagar.",
#             "deducciones comprobante": "Las deducciones reflejadas incluyen aportes a salud, pensión u otros conceptos aplicables según tu nómina.",
#             "valor neto": "El valor neto a pagar es el monto que finalmente se te deposita después de aplicar todas las deducciones.",
#             "revisar comprobante": "Para revisar tu comprobante de pago, ve a 'Mis certificaciones' y haz clic en 'Comprobante de nómina'. Selecciona el periodo que deseas consultar.",
#             "enviar comprobante correo": "Puedes enviar tu comprobante a tu correo seleccionando el periodo y haciendo clic en 'Enviar al correo electrónico'.",
#             "periodo comprobante": "En 'Mis certificaciones', selecciona el periodo que deseas consultar. Por ejemplo, el primer pago de mayo, y luego descarga o envía el comprobante."
#         }
                
#         # Respuestas por defecto
#         respuesta = []
                
#         # Manejo de cada pregunta
#         for pregunta in preguntas:
#             pregunta_normalizada = pregunta.strip().lower()
#             respuesta_encontrada = False  # Bandera para saber si se encontró respuesta
            
#             for clave, valor in respuestas_dict.items():
#                 if clave.lower() in pregunta_normalizada:
#                     respuesta.append(valor)
#                     respuesta_encontrada = True
#                     continue
            
#             if not respuesta_encontrada:
#                 respuesta.append(f"Lo siento, no entendí la pregunta: {pregunta}")


#         # Responder con todas las respuestas
#         response = "\n\n".join(respuesta)
#         dispatcher.utter_message(text=response)

#         return []

class ActionSendAutoMessage(Action):
    def name(self) -> str:
        return "action_send_auto_message"

    async def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        # Enviar el mensaje automático
        dispatcher.utter_message(text="Si necesitas más ayuda, no dudes en preguntar.")
        return []