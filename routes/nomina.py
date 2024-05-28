from fastapi import APIRouter, Response, status
from config.db import conn
from schemas.nomina import nominaEntity,nominasEntity
from models.nomina import Nomina
from config.db import nomina_collection
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

nomina=APIRouter()

@nomina.get('/nomina')
def find_all_nomina():
    return nominasEntity(nomina_collection.find())

@nomina.post('/nomina')
def create_nomina(nomina: Nomina):
    new_nomina=dict(nomina)
    del new_nomina["id"]
    id=nomina_collection.insert_one(new_nomina).inserted_id
    
    nomina=nomina_collection.find_one({"_id":id})
    
    return nominaEntity(nomina)

@nomina.get('/nomina/{id}')
def find_nomina(id:str):
    return nominaEntity(nomina_collection.find_one({"_id":ObjectId(id)}))


@nomina.put('/nomina/{id}')
def update_nomina(id:str,nomina:Nomina):
    nomina_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(nomina)})
    return nominaEntity(nomina_collection.find_one({"_id":ObjectId(id)}))

@nomina.delete('/nomina/{id}')
def delete_nomina(id:str):
    nominaEntity(nomina_collection.find_one_and_delete({"_id":ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)

