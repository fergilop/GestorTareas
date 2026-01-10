from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos los routers que acabamos de crear
from routers import auth, tareas, listas

app = FastAPI(title="Gestor de Tareas Modular")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AQUI OCURRE LA MAGIA: Unimos las piezas
app.include_router(auth.router)
app.include_router(tareas.router)
app.include_router(listas.router)

@app.get("/")
def home():
    return {"mensaje": "Bienvenido a mi API de Tareas en Docker", "estado": "online"}