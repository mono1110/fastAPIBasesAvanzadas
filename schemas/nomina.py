def nominaEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "nombre":item["nombre"],
        "apellido":item["apellido"],
        "foto":item["foto"],
        "correo":item["correo"],
        "direccion":item["direccion"],
        "cargo":item["cargo"],
        "salario":item["salario"],
        "productos": item.get("productos", [])  
    }
def nominasEntity(entity) -> list:
    return [nominaEntity(item) for item in entity]
    