import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pathlib import Path

# Cargar variables de entorno
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Recuperar configuración
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Crear conexión
cliente = MongoClient(MONGO_URI)
db = cliente[MONGO_DB_NAME]

# Exportamos las colecciones para usarlas en otros archivos
coleccion_tareas = db["tareas"]
coleccion_usuarios = db["usuarios"]