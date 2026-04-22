from fastapi import APIRouter
from pydantic import BaseModel
from services import cliente_service
router = APIRouter(prefix="/clientes", tags=["clientes"])

class cliente(BaseModel):
    nombre:str
    telefono:str

@router.get("/")
def ver_clientes():
    return cliente_service.get_all_clientes()

@router.post("/")
def agregar_cliente(cliente:cliente):
    cliente_service.post_cliente(cliente.nombre, cliente.telefono)
    return {"mensaje": "cliente agregado correctamente", "Datos": cliente}

@router.get("/{id}")
def ver_clientes_id(id:int):
    return cliente_service.buscar_clientes_id(id)

@router.delete("/{id}")
def eliminar_cliente_id(id:int):
    cliente_service.eliminar_cliente_id(id)
    return {"mensaje": "cliente eliminado correctamente", "ID":id}

@router.put("/{id}")
def actualizar_cliente_id(id:int,cliente:cliente):
    cliente_service.actualizar_cliente_id(id,cliente.nombre,cliente.telefono)
    return {"mensaje": "usuario acutualizado correctamente", "Datos": cliente}