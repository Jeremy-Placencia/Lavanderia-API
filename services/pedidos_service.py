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