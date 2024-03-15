from flask import Flask, jsonify, request, render_template
import sett 
import services
# from database import session
# from models import *
import database

app = Flask(__name__)

def initialize_database_once():
    database.initialize_database()

@app.before_request
def before_request_func():
    initialize_database_once()

@app.route('/webhook', methods=['GET'])
def verificar_token():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e,403
    
@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.obtener_Mensaje_whatsapp(message)

        services.administrar_chatbot(text, number, messageId, name)
        return 'enviado'

    except Exception as e:
        return 'no enviado ' + str(e)



@app.route('/dishes', methods=['GET'])
def get_dishes():
    dishes = database.get_all_dishes()
    return jsonify(dishes)

@app.route('/dishes', methods=['POST'])
def add_dish():
    data = request.get_json()
    dish_name = data.get('name')
    dish_price = data.get('price')
    dish_image_url = data.get('image_url')
    
    if dish_name and isinstance(dish_price, (int, float)) and dish_image_url:
        database.add_dish(dish_name, dish_price, dish_image_url)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Debe proporcionar nombre, precio (numérico) y URL de la imagen del plato'}), 400

@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    success = database.delete_dish(dish_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'El plato no existe'}), 404

@app.route('/dish')
def show_dishes():
    dishes = database.get_all_dishes()
    return render_template('dish.html', dishes=dishes)



@app.route('/additions', methods=['GET'])
def get_additions():
    additions = database.get_all_additions()
    return jsonify(additions)

@app.route('/additions', methods=['POST'])
def add_addition():
    data = request.get_json()
    addition_text = data.get('text', '')
    if addition_text:
        database.add_addition(addition_text)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'No se proporcionó un nombre de la adicion'}), 400

@app.route('/additions/<int:addition_id>', methods=['DELETE'])
def delete_addition(addition_id):
    success = database.delete_addition(addition_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'La adicion no existe'}), 404

@app.route('/addition')
def show_additions():
    additions = database.get_all_additions()
    return render_template('addition.html', additions=additions)



@app.route('/orders', methods=['GET'])
def get_orders():
    orders = database.get_all_orders()
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    data = request.get_json()
    ticket = data.get('ticket')
    client = data.get('client')
    address = data.get('address')
    dish = data.get('dish')
    addition = data.get('addition')
    if ticket and client and address and dish and addition:
        database.add_order(ticket, client, address, dish, addition)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'No se proporcionó el cliente la dirección o el ticket'}), 400


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    success = database.delete_order(order_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'El orden no existe'}), 404

@app.route('/order')
def show_orders():
    orders = database.get_all_orders()
    return render_template('order.html', orders=orders)

#//////////////////////////POSTGRESSQL///////////////////////////
# @app.route('/dishes', methods=['GET'])
# def get_dishes():
#     dishes = session.query(Dish).all()
#     return jsonify([dish.name for dish in dishes])

# @app.route('/dishes', methods=['POST'])
# def add_dish():
#     data = request.get_json()
#     dish = data['text']
#     new_dish = Dish(name=dish)
#     session.add(new_dish)
#     session.commit()
#     return jsonify({'success': True})

# @app.route('/dishes/<int:dish_id>', methods=['DELETE'])
# def delete_dish(dish_id):
#     dish = session.query(Dish).filter_by(id=dish_id).first()
#     if dish:
#         session.delete(dish)
#         session.commit()
#         return jsonify({'success': True})
#     else:
#         return jsonify({'success': False, 'error': 'La adición no existe'}), 404

# @app.route('/dish')
# def show_dishes():
#     dishes = session.query(Dish).all()
#     return render_template('dish.html', dishes=dishes)



# @app.route('/additions', methods=['GET'])
# def get_additions():
#     additions = session.query(Addition).all()
#     return jsonify([addition.name for addition in additions])

# @app.route('/additions', methods=['POST'])
# def add_addition():
#     data = request.get_json()
#     addition = data['text']
#     new_addition = Addition(name=addition)
#     session.add(new_addition)
#     session.commit()
#     return jsonify({'success': True})

# @app.route('/additions/<int:addition_id>', methods=['DELETE'])
# def delete_addition(addition_id):
#     addition = session.query(Addition).filter_by(id=addition_id).first()
#     if addition:
#         session.delete(addition)
#         session.commit()
#         return jsonify({'success': True})
#     else:
#         return jsonify({'success': False, 'error': 'La adición no existe'}), 404

# @app.route('/addition')
# def show_additions():
#     additions = session.query(Addition).all()
#     return render_template('addition.html', additions=additions)


# @app.route('/orders', methods=['GET'])
# def get_orders():
#     orders = session.query(Order).all()
#     orders_data = [{'ticket': order.ticket, 'address': order.address, 'client': order.client} for order in orders]
#     return jsonify(orders_data)

# @app.route('/orders', methods=['POST'])
# def add_order():
#     data = request.json  # Obtener los datos JSON del cuerpo del request
#     address = data.get('address')  
#     client = data.get('client')    
    
#     new_order = Order(address=address, client=client)
#     session.add(new_order)
#     session.commit()
    
#     return jsonify({'success': True})

# @app.route('/orders/<int:order_id>', methods=['DELETE'])
# def delete_order(order_id):
#     try:
#         order = session.query(Order).filter_by(ticket=order_id).first()  # Corrige esto para que coincida con el ticket
#         if order:
#             session.delete(order)
#             session.commit()
#             return jsonify({'success': True})
#         else:
#             return jsonify({'success': False, 'error': 'La orden no existe'}), 404
#     except Exception as e:
#         print(f"Error deleting order: {e}")  # Agrega una declaración de impresión para ver el error exacto
#         return jsonify({'success': False, 'error': 'Error al eliminar la orden'}), 500

# @app.route('/order')
# def show_orders():
#     orders = session.query(Order).all()
#     return render_template('order.html', orders=orders)

if __name__ == '__main__':
    app.run()

