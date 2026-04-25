from fastapi import APIRouter
from pydantic import BaseModel
from services import detalle_pedido_service
router = APIRouter(prefix="/detalle_pedido", tags=["detalle_pedido"])

class detalle_pedido(BaseModel):
    pedido_id:int
    prenda_id:int
    cantidad:int
    servicio:str
    

@router.get("/")
def ver_pedido():
    return detalle_pedido_service.ver_detalle_pedido()

@router.post("/")
def crear_pedido(detalle_pedido:detalle_pedido):
    detalle_pedido_service.crear_detalle_pedido(detalle_pedido.pedido_id,
    detalle_pedido.prenda_id,detalle_pedido.cantidad,detalle_pedido.servicio)
    return {"mensaje": "detalle del pedido creado", "Datos": detalle_pedido}

@router.get("/{id}")
def ver_detalle_pedido_id(id:int):
    return detalle_pedido_service.ver_detalle_pedido_id(id)

@router.delete("/{id}")
def eliminar_detalle_pedido_id(id:int):
    detalle_pedido_service.eliminar_detalle_pedido(id)
    return {"mensaje": "detalle del pedido eliminado correctamente", "ID": id}