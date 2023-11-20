from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from typing import Annotated
from schemas import UsuarioBase, UsuarioActualizado
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", include_in_schema=False)
async def documentacion():
    return RedirectResponse(url="/docs")

@app.post("/crear_usuario")
async def crear_usuario(usuario: UsuarioBase, db: db_dependency):
    nuevo_usuario = models.Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo, 
        contrasenia=usuario.contrasenia,
        telefono=usuario.telefono,
        tipo=usuario.tipo
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {"respuesta": "Usuario creado correctamente."}


@app.get("/usuario/{id_usuario}")
async def obtener_usuario(id_usuario: int, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return usuario

@app.get("/listar_usuarios")
async def listar_usuarios(db: db_dependency):
    result = db.query(models.Usuario).all()
    return result

@app.patch("/actualizar_usuario/{id_usuario}")
async def actualizar_usuario(id_usuario: int, usuario_actualizado: UsuarioActualizado, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == id_usuario)
    if not usuario.first():
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    usuario.update(usuario_actualizado.model_dump(exclude_unset=True))
    db.commit()
    return {"respuesta": "Usuario actualizado correctamente."}

@app.delete("/eliminar_usuario")
async def eliminar_usuario(id_usuario: int, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.idUsuario == id_usuario)
    if not usuario.first():
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    
    usuario.delete(synchronize_session=False)
    db.commit()
    return {"respuesta": "Usuario eliminado correctamente."}

