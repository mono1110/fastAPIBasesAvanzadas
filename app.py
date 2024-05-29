from fastapi import FastAPI
from routes.nomina import router
from routes.producto import producto

app = FastAPI()

app.include_router(router)
#app.include_router(producto)
#usando python-mongo5
#conda activate python-mongo5