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
    cursor.execute('''CREATE TABLE IF NOT EXISTS dish (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      price REAL,
                      image_url TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS addition (
                      id INTEGER PRIMARY KEY,
                      name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS "order" (
                      id INTEGER PRIMARY KEY,
                      ticket INTEGER,
                      client TEXT,
                      address TEXT,
                      dish TEXT,
                      addition TEXT)''')
    connection.commit()
    connection.close()

def get_all_dishes():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, name, price, image_url FROM dish')  # Asegúrate de seleccionar el ID
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
    additions = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    connection.close()
    return additions

def add_addition(name):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO addition (name) VALUES (?)', (name,))
    connection.commit()
    connection.close()

def delete_addition(addition_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM addition WHERE id = ?', (addition_id,))
    connection.commit()
    connection.close()

def get_all_orders():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM "order"')
    orders = [{'id': row[0], 'ticket': row[1], 'client': row[2], 'address': row[3], 'dish': row[4], 'addition': row[5]} for row in cursor.fetchall()]
    connection.close()
    return orders

def add_order(ticket, client, address, dish, addition):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO "order" (ticket, client, address, dish, addition) VALUES (?, ?, ?)', (ticket, client, address, dish, addition))
    connection.commit()
    connection.close()

def delete_order(order_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM "order" WHERE id = ?', (order_id,))
    connection.commit()
    connection.close()