from typing import Optional
from pydantic import BaseModel

class Producto(BaseModel):
    id_serial: Optional[str] = None
    nombre: str
    categoria: str
    imagen: str
    modelo: str
    serie: str
    marca: str
    fabricante: str


class Nomina(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellido: str
    foto: str
    correo: str
    direccion: str
    cargo: str
    salario: float
    productos: Optional[list[Producto]] = None





