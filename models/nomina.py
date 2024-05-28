from typing import Optional
from pydantic import BaseModel

class Nomina(BaseModel):
    id: Optional[str] = None
    nombre: str
    apellido: str
    foto: str
    correo: str
    direccion: str
    cargo: str
    salario: float





