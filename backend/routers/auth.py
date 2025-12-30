import os 
from fastapi import Query

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Importamos configuración y modelos
from database import coleccion_usuarios, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models import UsuarioRegistro

router = APIRouter()

# Configuración de Seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- FUNCIONES AUXILIARES ---
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Esta función se usa en otros archivos, por eso es importante
async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"username": username}

# --- RUTAS ---
@router.post("/registrar")
async def registrar_usuario(usuario: UsuarioRegistro, admin_key: str = Query(..., description="Clave maestra para registrarse")):
    
    # 1. Recuperar la clave secreta del entorno
    secret_on_server = os.getenv("REGISTRATION_KEY")
    
    # 2. Comprobar si coincide
    if secret_on_server and admin_key != secret_on_server:
        raise HTTPException(status_code=403, detail="No tienes permiso para registrar usuarios. Clave incorrecta.")
    
    # 3. Si no hay clave configurada en el servidor, o si coincide, procedemos
    if coleccion_usuarios.find_one({"username": usuario.username}):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    hashed_password = get_password_hash(usuario.password)
    coleccion_usuarios.insert_one({"username": usuario.username, "password": hashed_password})
    
    return {"mensaje": "Usuario creado con éxito"}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = coleccion_usuarios.find_one({"username": form_data.username})
    if not user_db or not verify_password(form_data.password, user_db["password"]):
        raise HTTPException(status_code=401, detail="Login fallido")
    token = create_access_token(data={"sub": user_db["username"]})
    return {"access_token": token, "token_type": "bearer"}