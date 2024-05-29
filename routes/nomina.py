from fastapi import APIRouter, Response, status, HTTPException
from config.db import conn
from schemas.nomina import nominaEntity, nominasEntity
from models.nomina import Nomina, Producto
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

router = APIRouter()

@router.get('/nomina')
def find_all_nomina():
    return nominasEntity(conn.apiBasesAvanzadas.nomina.find())

@router.post('/nomina')
def create_nomina(nomina: Nomina):
    new_nomina = dict(nomina)  # Convertir el objeto Pydantic a diccionario
    del new_nomina["id"]
    if "productos" in new_nomina:
        if isinstance(new_nomina["productos"], list):
            # Si new_nomina["productos"] es una lista, convierte cada elemento a un diccionario
            new_nomina["productos"] = [dict(producto) for producto in new_nomina["productos"]]
        # Si new_nomina["productos"] es un diccionario, no hace falta convertirlo
    
    # Generar un nuevo id_serial solo si no existe en cada producto
    for producto in new_nomina.get("productos", []):
        if "id_serial" not in producto or producto["id_serial"] is None:
            producto["id_serial"] = str(ObjectId())
    
    print("New Nomina:", new_nomina)  # Imprimir la nueva nómina antes de la inserción

    id = conn.apiBasesAvanzadas.nomina.insert_one(new_nomina).inserted_id

    nomina = conn.apiBasesAvanzadas.nomina.find_one({"_id": id})

    return nominaEntity(nomina)

@router.get('/nomina/{id}')
def find_nomina(id: str):
    return nominaEntity(conn.apiBasesAvanzadas.nomina.find_one({"_id": ObjectId(id)}))

from bson import ObjectId

@router.put('/nomina/{id}')
def update_nomina(id: str, nomina: Nomina):
    updated_nomina = dict(nomina) # Convertir el objeto Pydantic a diccionario
    if "productos" in updated_nomina:
        updated_nomina["productos"] = [dict(producto) for producto in updated_nomina["productos"]]  # Convertir cada producto a diccionario
    conn.apiBasesAvanzadas.nomina.find_one_and_update({"_id": ObjectId(id)}, {"$set": updated_nomina})
    return nominaEntity(conn.apiBasesAvanzadas.nomina.find_one({"_id": ObjectId(id)}))

@router.delete('/nomina/{id}')
def delete_nomina(id: str):
    nominaEntity(conn.apiBasesAvanzadas.nomina.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)

## Rutas para productos:

@router.post('/nomina/{nomina_id}/producto')
def add_producto(nomina_id: str, producto: Producto):
    nomina = conn.apiBasesAvanzadas.nomina.find_one({"_id": ObjectId(nomina_id)})
    if not nomina:
        raise HTTPException(status_code=404, detail="Nomina not found")

    new_producto = producto.dict()  # Convertir el objeto Pydantic a diccionario
    new_producto["id_serial"] = str(ObjectId())  # Generar un id único para el producto
    conn.apiBasesAvanzadas.nomina.update_one(
        {"_id": ObjectId(nomina_id)},
        {"$push": {"productos": new_producto}}
    )

    return new_producto

@router.get('/nomina/{nomina_id}/producto')
def get_productos(nomina_id: str):
    nomina = conn.apiBasesAvanzadas.nomina.find_one({"_id": ObjectId(nomina_id)})
    if not nomina:
        raise HTTPException(status_code=404, detail="Nomina not found")

    return nomina.get("productos", [])

@router.get('/nomina/{nomina_id}/producto/{producto_id}')
def get_producto(nomina_id: str, producto_id: str):
    nomina = conn.apiBasesAvanzadas.nomina.find_one({"_id": ObjectId(nomina_id)})
    if not nomina:
        raise HTTPException(status_code=404, detail="Nomina not found")

    for producto in nomina.get("productos", []):
        if producto["id_serial"] == producto_id:
            return producto

    raise HTTPException(status_code=404, detail="Producto not found")

@router.put('/nomina/{nomina_id}/producto/{producto_id}')
def update_producto(nomina_id: str, producto_id: str, producto: Producto):
    nomina = conn.apiBasesAvanzadas.nomina.find_one({"_id": ObjectId(nomina_id)})
    if not nomina:
        raise HTTPException(status_code=404, detail="Nomina not found")

    productos = nomina.get("productos", [])
    for index, prod in enumerate(productos):
        if prod["id_serial"] == producto_id:
            # Crear un nuevo diccionario actualizando los valores del producto existente
            updated_producto = {**prod, **producto.dict(), "id_serial": producto_id}
            productos[index] = updated_producto
            break
    else:
        raise HTTPException(status_code=404, detail="Producto not found")

    # Actualizar la lista de productos en la base de datos
    conn.apiBasesAvanzadas.nomina.update_one(
        {"_id": ObjectId(nomina_id)},
        {"$set": {"productos": productos}}
    )

    return productos


@router.delete('/nomina/{nomina_id}/producto/{producto_id}')
def delete_producto(nomina_id: str, producto_id: str):
    nomina = conn.apiBasesAvanzadas.nomina.find_one({"_id": ObjectId(nomina_id)})
    if not nomina:
        raise HTTPException(status_code=404, detail="Nomina not found")

    productos = nomina.get("productos", [])
    productos = [prod for prod in productos if prod["id_serial"] != producto_id]

    conn.apiBasesAvanzadas.nomina.update_one(
        {"_id": ObjectId(nomina_id)},
        {"$set": {"productos": productos}}
    )
    return Response(status_code=HTTP_204_NO_CONTENT)

