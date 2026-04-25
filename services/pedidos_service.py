import mysql.connector
from fastapi import HTTPException
from dotenv import load_dotenv
import os
load_dotenv()

conexion = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

def ver_pedidos():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos")
    mostrar = cursor.fetchall()
    if not mostrar:
        raise HTTPException(status_code=404, detail="No hay ningun pedido agregado")
    cursor.close()
    return mostrar

def crear_pedido(fecha_entrada:str,fecha_entrega:str,estado:str,cliente_id:int):
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO pedidos (fecha_entrada, fecha_entrega, estado, cliente_id) VALUES (%s, %s, %s, %s)",
                   (fecha_entrada,fecha_entrega,estado,cliente_id))
    conexion.commit()
    cursor.close()

def ver_pedido_id(id:int):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
    pedidos = cursor.fetchone()
    if not pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    cursor.close()
    return pedidos

def eliminar_pedido(id:int):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
    pedidos = cursor.fetchone()
    if pedidos:
        cursor.execute("delete from pedidos where id = %s", (id,))
    else:
        raise HTTPException(status_code=404, detail= "Pedido no encontrado")
    conexion.commit()
    cursor.close()

def actualizar_estado_id(id:int,estado:str):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
    pedido = cursor.fetchone()
    if pedido:
        cursor.execute("update pedidos set estado = %s",(estado,))
    else:
        raise HTTPException(status_code=404, detail= "Pedido no encontrado")
    conexion.commit()
    cursor.close()

def ver_todo_pedido(id:int):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT clientes.nombre, pedidos.fecha_entrega, pedidos.estado, prendas.nombre_prenda, detalle_pedido.cantidad,detalle_pedido.servicio,detalle_pedido.total FROM detalle_pedido JOIN prendas ON detalle_pedido.prenda_id = prendas.id JOIN pedidos ON detalle_pedido.pedido_id = pedidos.id JOIN clientes ON pedidos.cliente_id = clientes.id WHERE detalle_pedido.pedido_id = %s",(id,))
    mostrar = cursor.fetchall()
    total_general = sum(fila["total"] for fila in mostrar)
    if not mostrar:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    cursor.close()
    return {
    "pedido_id": id,
    "cliente": mostrar[0]["nombre"],
    "fecha_entrega": mostrar[0]["fecha_entrega"],
    "estado": mostrar[0]["estado"],
    "prendas": [{"nombre_prenda": p["nombre_prenda"], "cantidad": p["cantidad"], "servicio": p["servicio"], "total": p["total"]} for p in mostrar],
    "total_general": total_general
}