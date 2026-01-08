from fastapi import APIRouter, HTTPException, Depends
from models import ListaCompra
from database import coleccion_listas
from routers.auth import obtener_usuario_actual

router = APIRouter()

# 1. CREAR UNA LISTA COMPLETA (Cabecera + Líneas iniciales)
@router.post("/listas")
async def crear_lista(lista: ListaCompra, usuario: dict = Depends(obtener_usuario_actual)):
    # Verificamos si ya existe una lista con ese nombre para este usuario
    if coleccion_listas.find_one({"titulo": lista.titulo, "usuario": usuario["username"]}):
        raise HTTPException(status_code=400, detail="Ya tienes una lista con este nombre")
    
    # Convertimos el modelo Pydantic a diccionario
    nueva_lista = lista.dict()
    
    # Añadimos el dueño de la lista (para que no las vea todo el mundo)
    nueva_lista["usuario"] = usuario["username"]
    
    coleccion_listas.insert_one(nueva_lista)
    return {"mensaje": "Lista de compra creada con éxito"}

# 2. LEER MIS LISTAS
@router.get("/listas")
async def obtener_listas(usuario: dict = Depends(obtener_usuario_actual)):
    # Buscamos solo las listas que pertenecen al usuario conectado
    # Ocultamos el _id para evitar errores de conversión por ahora
    mis_listas = list(coleccion_listas.find({"usuario": usuario["username"]}, {"_id": 0}))
    return mis_listas

@router.delete("/listas")
async def eliminar_lista(titulo: str, usuario: dict = Depends(obtener_usuario_actual)):
    # Buscamos la lista que coincida en título y usuario
    resultado = coleccion_listas.delete_one({"titulo": titulo, "usuario": usuario["username"]})
    
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    return {"mensaje": "Lista eliminada"}

# RUTA 3: ACTUALIZAR UNA LISTA COMPLETA
@router.put("/listas/{titulo_original}")
async def actualizar_lista(titulo_original: str, lista_nueva: ListaCompra, usuario: dict = Depends(obtener_usuario_actual)):
    # Buscamos la lista original para asegurar que existe y es del usuario
    filtro = {"titulo": titulo_original, "usuario": usuario["username"]}
    
    # Convertimos los datos nuevos a diccionario
    datos_nuevos = lista_nueva.dict()
    datos_nuevos["usuario"] = usuario["username"] # Aseguramos que el dueño sigue siendo el mismo

    # La magia de Mongo: Reemplazamos todo el documento
    resultado = coleccion_listas.replace_one(filtro, datos_nuevos)

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lista no encontrada")
    
    return {"mensaje": "Lista actualizada correctamente"}