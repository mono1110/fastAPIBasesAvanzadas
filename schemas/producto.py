def productoEntity(item) -> dict:
    return {
        "id_serial":item["id_serial"],
        "nombre":item["nombre"],
        "categoria":item["categoria"],
        "imagen":item["imagen"],
        "modelo":item["modelo"],
        "serie":item["serie"],
        "marca":item["marca"],
        "fabricante":item["fabricante"],
        "id_empleado":item["id_empleado"]
    }
    