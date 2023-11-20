from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    contrasenia: str
    telefono: str
    tipo: int

class UsuarioActualizado(BaseModel):
    nombre: str = None
    correo: str = None
    contrasenia: str = None
    telefono: str = None
    tipo: int = None