from fastapi import FastAPI
from routes.nomina import router
from routes.producto import producto
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1",
    "null",  # Agrega 'null' para permitir el origen 'null' en algunos navegadores en entorno local
    # Agrega otros orígenes que necesites
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(router)
#app.include_router(producto)
#usando python-mongo5
#conda activate python-mongo5