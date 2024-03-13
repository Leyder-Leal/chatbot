from flask import Flask, jsonify, request, render_template
import sett 
import services
from database import session
from models import *

app = Flask(__name__)

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
    dishes = session.query(Dish).all()
    return jsonify([dish.name for dish in dishes])

@app.route('/dishes', methods=['POST'])
def add_dish():
    data = request.get_json()
    dish = data['text']
    new_dish = Dish(name=dish)
    session.add(new_dish)
    session.commit()
    return jsonify({'success': True})

@app.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    dish = session.query(Dish).filter_by(id=dish_id).first()
    if dish:
        session.delete(dish)
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'La adición no existe'}), 404

@app.route('/dish')
def show_dishes():
    dishes = session.query(Dish).all()
    return render_template('dish.html', dishes=dishes)



@app.route('/additions', methods=['GET'])
def get_additions():
    additions = session.query(Addition).all()
    return jsonify([addition.name for addition in additions])

@app.route('/additions', methods=['POST'])
def add_addition():
    data = request.get_json()
    addition = data['text']
    new_addition = Addition(name=addition)
    session.add(new_addition)
    session.commit()
    return jsonify({'success': True})

@app.route('/additions/<int:addition_id>', methods=['DELETE'])
def delete_addition(addition_id):
    addition = session.query(Addition).filter_by(id=addition_id).first()
    if addition:
        session.delete(addition)
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'La adición no existe'}), 404

@app.route('/addition')
def show_additions():
    additions = session.query(Addition).all()
    return render_template('addition.html', additions=additions)


# @app.route('/orders', methods=['GET'])
# def get_orders():
#     orders = session.query(Order).all()
#     return jsonify([order.ticket for order in orders])

# @app.route('/orders', methods=['POST'])
# def add_order():
#     data = request.get_json()
#     order = data['text']
#     new_order = Order(name=order)
#     session.add(new_order)
#     session.commit()
#     return jsonify({'success': True})

# @app.route('/orders/<int:order_id>', methods=['DELETE'])
# def delete_order(order_id):
#     order = session.query(Order).filter_by(id=order_id).first()
#     if order:
#         session.delete(order)
#         session.commit()
#         return jsonify({'success': True})
#     else:
#         return jsonify({'success': False, 'error': 'La adición no existe'}), 404

# @app.route('/order')
# def show_orders():
#     orders = session.query(Order).all()
#     return render_template('order.html', orders=orders)

if __name__ == '__main__':
    app.run()

