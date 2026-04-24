from fastapi import APIRouter
from pydantic import BaseModel
from services import prendas_service
router = APIRouter(prefix="/prendas", tags=["prendas"])

class prenda(BaseModel):
    nombre_prenda:str
    precio_lavado:int
    precio_planchado:int
    precio_ambos:int

@router.get("/")
def ver_prendas():
    return prendas_service.ver_prendas()

@router.post("/")
def crear_prenda(prenda:prenda):
    prendas_service.crear_prenda(prenda.nombre_prenda,prenda.precio_lavado,prenda.precio_planchado,prenda.precio_ambos)
    return {"mensaje": "prenda creada", "Datos": prenda}

@router.get("/{id}")
def ver_prenda_id(id:int):
    return prendas_service.ver_prenda_id(id)

@router.delete("/{id}")
def eliminar_prenda_id(id:int):
    prendas_service.eliminar_prendas_id(id)
    return {"mensaje": "Prenda eliminada correctamente", "ID": id}

@router.put("/{id}")
def editar_prenda_id(id:int,prenda:prenda):
    prendas_service.actualizar_prenda_id(id, prenda.nombre_prenda,prenda.precio_lavado,prenda.precio_planchado,prenda.precio_ambos)
    return {"mensaje": "Prenda editada correctamente", "ID": id}