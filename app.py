from fastapi import FastAPI
from routes.nomina import nomina
from routes.producto import producto

app = FastAPI()

app.include_router(nomina)
app.include_router(producto)
