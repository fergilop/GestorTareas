from fastapi import APIRouter, HTTPException, Depends
from models import Tarea, TareaActualizar
from database import coleccion_tareas
# Importamos la función de seguridad desde auth (que crearemos en el paso 5)
from routers.auth import obtener_usuario_actual 

router = APIRouter()

# RUTA 1: LEER TODAS
@router.get("/tareas")
async def obtener_todas_las_tareas():
    tareas = list(coleccion_tareas.find({}, {"_id": 0}))
    return tareas

# RUTA 2: CREAR
@router.post("/tareas")
async def crear_tarea(tarea: Tarea, usuario: dict = Depends(obtener_usuario_actual)):
    if coleccion_tareas.find_one({"titulo": tarea.titulo}):
        raise HTTPException(status_code=400, detail="La tarea ya existe")
    nueva_tarea = tarea.dict()
    coleccion_tareas.insert_one(nueva_tarea)
    return {"mensaje": "Tarea creada", "id": str(nueva_tarea["_id"])}

# RUTA 3: ELIMINAR
@router.delete("/tareas/eliminar")
async def eliminar_tarea(titulo: str, usuario: dict = Depends(obtener_usuario_actual)):
    resultado = coleccion_tareas.delete_one({"titulo": titulo})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"mensaje": f"Tarea eliminada por {usuario['username']}"}

# RUTA 4: ACTUALIZAR
@router.put("/tareas/{titulo_original}")
async def actualizar_tarea(titulo_original: str, tarea: TareaActualizar, usuario: dict = Depends(obtener_usuario_actual)):
    datos = {k: v for k, v in tarea.dict().items() if v is not None}
    resultado = coleccion_tareas.update_one({"titulo": titulo_original}, {"$set": datos})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"mensaje": "Tarea actualizada"}