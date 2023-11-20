from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__  = 'Usuario'
    
    idUsuario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True, index=True)
    contrasenia = Column(String)    
    telefono = Column(String)
    tipo = Column(Integer)
