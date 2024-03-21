#//////////////////POSTGRESSQL/////////////////////////////////
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv

# from models import Base

# load_dotenv()

# # Obtener variables de entorno
# db_host = os.getenv("DB_HOST")
# db_port = os.getenv("DB_PORT")
# db_name = os.getenv("DB_NAME")
# db_user = os.getenv("DB_USER")
# db_password = os.getenv("DB_PASSWORD")

# # Crear URL de conexión
# db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# # Crear motor de base de datos
# engine = create_engine(db_url)

# # Crear sesión de base de datos
# Session = sessionmaker(bind=engine)
# session = Session()

# # Crear la tabla si no existe
# Base.metadata.create_all(engine)


#//////////////////SQLITE/////////////////////////////////
# import sqlite3

# def initialize_database():
#     connection = sqlite3.connect('database.db')
#     cursor = connection.cursor()

#     # Crear la tabla 'dish' con los atributos 'id' y 'name'
#     cursor.execute('''CREATE TABLE IF NOT EXISTS dish (
#                       id INTEGER PRIMARY KEY,
#                       name TEXT)''')

#     connection.commit()
#     connection.close()


import sqlite3

def initialize_database():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS product (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      description TEXT,
                      price REAL,
                      image_url TEXT,
                      details_url TEXT,
                      details_payload TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservation (
                          id INTEGER PRIMARY KEY,
                          name TEXT,
                          number TEXT,
                          people INTEGER,
                          date TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS dish (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      price REAL,
                      image_url TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS addition (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      price REAL,
                      image_url TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS "order" (
                      id INTEGER PRIMARY KEY,
                      ticket INTEGER,
                      client TEXT,
                      address TEXT,
                      dish TEXT,
                      addition TEXT,
                      status TEXT CHECK(status IN ('preparando', 'en camino', 'entregado')))''')
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM product')
    products = [{'id': row[0], 'name': row[1], 'description': row[2], 'price': row[3], 'image_url': row[4], 'details_url': row[5], 'details_payload': row[6]} for row in cursor.fetchall()]
    connection.close()
    return products

def add_product(name, description, price, image_url, details_url, details_payload):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO product (name, description, price, image_url, details_url, details_payload) VALUES (?, ?, ?, ?, ?, ?)', (name, description, price, image_url, details_url, details_payload))
    connection.commit()
    connection.close()

def delete_product(product_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM product WHERE id = ?', (product_id,))
    connection.commit()
    connection.close()


def get_all_dishes():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM dish')
    dishes = [{'id': row[0], 'name': row[1], 'price': row[2], 'image_url': row[3]} for row in cursor.fetchall()]
    connection.close()
    return dishes

def add_dish(name, price, image_url):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO dish (name, price, image_url) VALUES (?, ?, ?)', (name, price, image_url))
    connection.commit()
    connection.close()

def delete_dish(dish_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM dish WHERE id = ?', (dish_id,))
    connection.commit()
    connection.close()


def get_all_additions():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM addition')
    additions = [{'id': row[0], 'name': row[1], 'price': row[2], 'image_url': row[3]} for row in cursor.fetchall()]
    connection.close()
    return additions

def add_addition(name, price, image_url):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO addition (name, price, image_url) VALUES (?, ?, ?)', (name, price, image_url))
    connection.commit()
    connection.close()

def delete_addition(addition_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM addition WHERE id = ?', (addition_id,))
    connection.commit()
    connection.close()


def get_order_status(ticket_numero):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT status FROM "order" WHERE ticket = ?', (ticket_numero,))
    status = cursor.fetchone()
    connection.close()
    return status[0] if status else None

def get_all_orders_with_status():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM "order"')
    orders = [{'id': row[0], 'ticket': row[1], 'client': row[2], 'address': row[3], 'dish': row[4], 'addition': row[5], 'status': row[6]} for row in cursor.fetchall()]
    connection.close()
    return orders

def add_order(ticket, client, address, dish, addition):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO "order" (ticket, client, address, dish, addition, status) VALUES (?, ?, ?, ?, ?, "preparando")', (ticket, client, address, dish, addition))
    connection.commit()
    connection.close()

def update_order_status(order_id, new_status):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE "order" SET status = ? WHERE id = ?', (new_status, order_id))
    connection.commit()
    connection.close()

def delete_order(order_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM "order" WHERE id = ?', (order_id,))
    connection.commit()
    connection.close()
    
    
def get_all_reservations():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM reservation')
    reservations = [{'id': row[0], 'name': row[1], 'number': row[2], 'people': row[3], 'date': row[4]} for row in cursor.fetchall()]
    connection.close()
    return reservations

def add_reservation(name, number, people, date):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO reservation (name, number, people, date) VALUES (?, ?, ?, ?)', (name, number, people, date))
    connection.commit()
    connection.close()

def delete_reservation(reservation_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM reservation WHERE id = ?', (reservation_id,))
    connection.commit()
    connection.close()