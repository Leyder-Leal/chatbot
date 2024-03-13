from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from models import Base

load_dotenv()

# Obtener variables de entorno
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Crear URL de conexión
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Crear motor de base de datos
engine = create_engine(db_url)

# Crear sesión de base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Crear la tabla si no existe
Base.metadata.create_all(engine)