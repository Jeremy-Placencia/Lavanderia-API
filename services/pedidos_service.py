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
    cursor.close()
    return mostrar

def crear_pedido(fecha_entrada:str, fecha_entrega:str, estado:str, cliente_id:int):
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO pedidos (fecha_entrada, fecha_entrega, estado, cliente_id) VALUES (%s, %s, %s, %s)",
                   (fecha_entrada, fecha_entrega, estado, cliente_id))
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    return nuevo_id

def ver_pedido_id(id:int):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
    pedido = cursor.fetchone()
    cursor.close()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

def eliminar_pedido(id:int):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
    pedido = cursor.fetchone()
    if not pedido:
        cursor.close()
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    cursor.execute("DELETE FROM detalle_pedido WHERE pedido_id = %s", (id,))
    cursor.execute("DELETE FROM pedidos WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()

def actualizar_estado_id(id:int, estado:str):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
    pedido = cursor.fetchone()
    if not pedido:
        cursor.close()
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (estado, id))
    conexion.commit()
    cursor.close()

def ver_todo_pedido(id:int):
    cursor = conexion.cursor(dictionary=True)
    
    cursor.execute("SELECT pedidos.id, clientes.nombre, pedidos.fecha_entrega, pedidos.estado FROM pedidos JOIN clientes ON pedidos.cliente_id = clientes.id WHERE pedidos.id = %s", (id,))
    pedido = cursor.fetchone()
    if not pedido:
        cursor.close()
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    cursor.execute("""
        SELECT prendas.nombre_prenda, detalle_pedido.cantidad,
        detalle_pedido.servicio, detalle_pedido.total
        FROM detalle_pedido
        JOIN prendas ON detalle_pedido.prenda_id = prendas.id
        WHERE detalle_pedido.pedido_id = %s
    """, (id,))
    detalles = cursor.fetchall()
    cursor.close()
    
    return {
        "pedido_id": id,
        "cliente": pedido["nombre"],
        "fecha_entrega": str(pedido["fecha_entrega"]),
        "estado": pedido["estado"],
        "prendas": detalles if detalles else [{"mensaje": "Sin prendas agregadas"}],
        "total_general": sum(d["total"] for d in detalles)
    }

def ver_pedidos_por_estado(estado: str):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT pedidos.id, clientes.nombre, clientes.telefono,
        pedidos.fecha_entrega, pedidos.estado
        FROM pedidos
        JOIN clientes ON pedidos.cliente_id = clientes.id
        WHERE pedidos.estado = %s
    """, (estado,))
    resultado = cursor.fetchall()
    cursor.close()
    return resultado