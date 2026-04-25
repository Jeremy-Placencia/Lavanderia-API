from fastapi import APIRouter
from pydantic import BaseModel
from services import pedidos_service
router = APIRouter(prefix="/pedidos", tags=["pedidos"])

class pedido(BaseModel):
    fecha_entrada:str
    fecha_entrega:str
    estado:str
    cliente_id:int

class EstadoUpdate(BaseModel):
    estado: str

@router.get("/")
def ver_pedido():
    return pedidos_service.ver_pedidos()

@router.get("/listos")
def ver_pedidos_listos():
    return pedidos_service.ver_pedidos_por_estado("listo")

@router.get("/todo-{id}")    
def ver_todo(id:int):
    return pedidos_service.ver_todo_pedido(id)

@router.get("/{id}")
def ver_pedido_id(id:int):
    return pedidos_service.ver_pedido_id(id)

@router.post("/")
def crear_pedido(pedido:pedido):
    nuevo_id = pedidos_service.crear_pedido(pedido.fecha_entrada, pedido.fecha_entrega, pedido.estado, pedido.cliente_id)
    return {"id": nuevo_id}

@router.delete("/{id}")
def eliminar_pedido_id(id:int):
    pedidos_service.eliminar_pedido(id)
    return {"mensaje": "Pedido eliminado correctamente", "ID": id}

@router.put("/{id}")
def editar_pedido_id(id:int, body: EstadoUpdate):
    pedidos_service.actualizar_estado_id(id, body.estado)
    return {"mensaje": "Estado actualizado", "ID": id}
