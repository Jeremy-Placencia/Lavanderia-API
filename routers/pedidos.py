from fastapi import APIRouter
from pydantic import BaseModel
from services import pedidos_service
router = APIRouter(prefix="/pedidos", tags=["pedidos"])

class pedido(BaseModel):
    fecha_entrada:str
    fecha_entrega:str
    estado:str
    cliente_id:int


@router.get("/todo-{id}")    
def ver_todo(id:int):
    return pedidos_service.ver_todo_pedido(id)

@router.get("/")
def ver_pedido():
    return pedidos_service.ver_pedidos()

@router.post("/")
def crear_pedido(pedido:pedido):
    pedidos_service.crear_pedido(pedido.fecha_entrada,pedido.fecha_entrega,pedido.estado,
                                 pedido.cliente_id)
    return {"mensaje": "pedido creado", "Datos": pedido}

@router.get("/{id}")
def ver_pedido_id(id:int):
    return pedidos_service.ver_pedido_id(id)

@router.delete("/{id}")
def eliminar_pedido_id(id:int):
    pedidos_service.eliminar_pedido(id)
    return {"mensaje": "Pedido eliminado correctamente", "ID": id}

@router.put("/{id}")
def editar_pedido_id(id:int,estado:str):
    pedidos_service.actualizar_estado_id(id, estado)
    return {"mensaje": "Pedido editado correctamente", "ID": id}