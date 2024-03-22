import requests
import sett
import json
import time
import database
from flask import jsonify
import sqlite3
import uuid

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message:
        text = 'Mensaje no reconocido'  # More descriptive error message
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'Mensaje no procesado'  # More descriptive error message

    return text

def send_catalog_message(number, template_name):
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "template": {
            "name": template_name,
            "language": "es"
        },
        "message_id": str(uuid.uuid4())  # Add a unique message ID
    }
    return json.dumps(data)

def send_whatsapp_message(data):
    whatsapp_token = sett.whatsapp_token
    whatsapp_url = sett.whatsapp_url
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {whatsapp_token}'}

    try:
        response = requests.post(whatsapp_url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        print("Response from send_whatsapp_message:", response.text)  # Add this line
        return response.json()  # Assuming the response is JSON (check API documentation)
    except requests.exceptions.RequestException as e:
        print(f"Error enviando mensaje por WhatsApp: {e}")
        return {'error': 'Error al enviar mensaje', 'status_code': 500}

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {whatsapp_token}'}
        print("Se envía:", data)
        response = requests.post(whatsapp_url, headers=headers, data=data)
        print("Estado de la respuesta:", response.status_code)
        if response.status_code == 200:
            # Assuming successful response based on the API documentation
            return 'Mensaje enviado', 200
        else:
            print("Error al enviar mensaje:", response.text)
            # Consider adding more specific error handling based on response code
            return 'Error al enviar mensaje', response.status_code
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 'Error interno', 500
    
def text_Message(number, text):
    data = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {
            "body": text
        }
    })
    return data

def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "btn" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

estado = ""
direccion =  ""
nombre = ""
plato = ""
adicion = ""

def administrar_chatbot(text,number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ",text)
    markRead = markRead_Message(messageId)
    list.append(markRead)
    global estado
    global direccion
    global nombre
    global plato
    global adicion
    
    if "hola" in text or "sí, por favor." in text:
        body = "¡Hola! 👋 Bienvenido al Restaurante Prueba. ¿Cómo puedo ayudarte hoy?"
        footer = "Restaurante Prueba"
        options = ["📋 Menú", "📅 Reservacion", "⏱️ Estado mi Pedido"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
        
    elif "menú" in text:
        data = send_catalog_message(number, "menu")
        response = send_whatsapp_message(data)
        # Check for errors in the response (assuming JSON format)
        if 'error' in response:
            print(f"Error al enviar catálogo: {response['error']}")
            user_message = 'Error al mostrar el menú. Intenta nuevamente más tarde.'
            response = text_Message(number, user_message)
            list.append(response)
                
    elif any(dish['name'].lower() == text.lower() for dish in get_dishes()): 
        plato = text  
        body = f"Pediste {plato}😋, ¿estás segur@ que quieres realizar este pedido?"
        footer = "Restaurante prueba"
        options = ["✅ Si.", "❌ No, gracias."]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3", messageId)
        list.append(replyButtonData)

    elif any(addition['name'].lower() == text.lower() for addition in get_addition()):
        adicion = text
        body = f"¿Como deseas recibir tu pedido📋?"
        footer = "Restaurante prueba"
        options = ["Recoger en Sitio 🏬", "Domicilio 🏡"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed5", messageId)
        list.append(replyButtonData)
        estado = "entrega"
    
    elif estado == "entrega" and "recoger en sitio" in text:
        body = "Ok, lo esperamos en 10 minutos⏱, ¿Necesitas ayuda con algo más hoy?"
        footer = "Restaurante prueba"
        options = ["✅ Sí, por favor.", "❌ No, gracias."]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed6", messageId)
        list.append(replyButtonData)
        estado = ""
        
    elif estado == "entrega" or "no, corregir." in text:
        textMessage = text_Message(number,"Ok😊, Ingresa la dirección de entrega: ")
        enviar_Mensaje_whatsapp(textMessage)
        estado = "esperando_direccion"

    elif estado == "esperando_direccion":
        direccion = text
        textMessage = text_Message(number, "Ingresa tu nombre😄: ")
        enviar_Mensaje_whatsapp(textMessage)
        estado = "esperando_nombre"
    
    elif estado == "esperando_nombre":
        nombre = text
        body = f"Confirmas que tu dirección de entrega es {direccion} y tu nombre es {nombre}"
        footer = "Restaurante prueba"
        options = ["✅ Confirmar", "❌ No, corregir."]
        estado = ""
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed7", messageId)
        list.append(replyButtonData)
    
    elif "confirmar" in text:
        textMessage = text_Message(number, "Espera un momento el numero del ticket..")
        enviar_Mensaje_whatsapp(textMessage)
        
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT MAX(ticket) FROM "order"')
        last_ticket = cursor.fetchone()[0]
        if last_ticket is None:
            last_ticket = 0
            
        ticket = last_ticket + 1
        client = nombre
        address = direccion
        dish = plato
        addition = adicion
        print(f"Ticket: {ticket}, Cliente: {client}, Dirección: {address}, Plato: {dish}, Adición: {addition}")
        if ticket and client and address and dish and addition:
            database.add_order(ticket, client, address, dish, addition)
            time.sleep(2)
            body = f"Tu pedido se ha realizado con exito✅. El numero de ticket de tu pedido es: '{ticket}'. ¿Necesitas ayuda con algo más hoy?"
            footer = "Restaurante prueba"
            options = ["✅ Sí, por favor.", "❌ No, gracias."]
            replyButtonData = buttonReply_Message(number, options, body, footer, "sed8", messageId)
            list.append(replyButtonData)
        else:
            return jsonify({'success': False, 'error': 'No se proporcionó el cliente o la dirección'}), 400
    
    elif "reservacion" in text.lower():
        textMessage = text_Message(number,"Para realizar una reservación, por favor visita el siguiente enlace: https://frill-innovative-durian.glitch.me/reservation")
        print(number)
        enviar_Mensaje_whatsapp(textMessage)
    
    elif "estado mi pedido" in text:
        textMessage = text_Message(number,"Ingresa el numero de tu ticket:")
        enviar_Mensaje_whatsapp(textMessage)
        estado = "esperando_ticket"
        
    elif estado == "esperando_ticket":
        estado = ""
        if text.isdigit():
            ticket_numero = int(text)
            status = database.get_order_status(ticket_numero)
            if status:
                textMessage = text_Message(number, f"El estado del pedido es: {status}")
                enviar_Mensaje_whatsapp(textMessage)
                textMessage = text_Message(number, f"Si necesitas ayuda, escríbeme 'hola' o elige una de las opciones que te ofrezco.")
                enviar_Mensaje_whatsapp(textMessage)
            else:
                textMessage = text_Message(number, "El número de ticket ingresado no existe. Por favor, inténtalo nuevamente.")
                enviar_Mensaje_whatsapp(textMessage)
                estado = "esperando_ticket"
        else:
            textMessage = text_Message(number, "Por favor, ingresa un número de ticket válido.")
            enviar_Mensaje_whatsapp(textMessage)
            estado = "esperando_ticket"
        
    elif "no, gracias." in text:
        textMessage = text_Message(number,"Hasta pronto!😊. Escribe 'hola' si necesitas ayuda")
        list.append(textMessage)
            
    else:
        data = text_Message(number,"Lo siento, no entendí lo que dijiste😔. Si necesitas algo, escribe 'hola' o elige una de las opciones ofrecidas.")
        list.append(data)

    for item in list:
        enviar_Mensaje_whatsapp(item)        


def get_dishes():
    url = 'http://localhost:5000/dishes'
    response = requests.get(url)
    if response.status_code == 200:
        dishes = response.json()
        print(f"Opciones recuperadas: {dishes}")
        return dishes  # Retorna toda la información del plato
    else:
        print(f"Error al obtener opciones: {response.status_code}")
        return []
    
def get_addition():
    url = 'http://localhost:5000/additions'
    response = requests.get(url)
    if response.status_code == 200:
        additions = response.json()
        print(f"Opciones recuperadas: {additions}")
        return additions
    else:
        print(f"Error al obtener opciones: {response.status_code}")
        return []