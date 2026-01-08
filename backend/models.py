from pydantic import BaseModel
from typing import Optional, List

# Modelos de Tareas
class Tarea(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    completada: bool = False

class TareaActualizar(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    completada: Optional[bool] = None

# Modelos de Usuarios
class UsuarioRegistro(BaseModel):
    username: str
    password: str

# El "Hijo" (detalle)
class ItemCompra(BaseModel):
    producto: str
    cantidad: int
    comprado: bool = False

# El "Padre" (Cabecera)
class ListaCompra(BaseModel):
    titulo: str
    items: List[ItemCompra] = []