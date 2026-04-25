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
def ver_detalle_pedido():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detalle_pedido")
    mostrar = cursor.fetchall()
    if not mostrar:
        raise HTTPException(status_code=404, detail="No hay ningun detalle de pedido agregado")
    cursor.close()
    return mostrar

def crear_detalle_pedido(pedido_id:int,prenda_id:int,cantidad:int,servicio:str):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prendas WHERE id = %s", (prenda_id,))
    prenda = cursor.fetchone()
    
    if not prenda:
        raise HTTPException(status_code=404, detail="Prenda no encontrada")
    if servicio == "lavado":
        precio = prenda["precio_lavado"]
    elif servicio == "planchado":
        precio = prenda["precio_planchado"]
    elif servicio == "ambos":
        precio = prenda["precio_ambos"]
    else:
        raise HTTPException(status_code=400, detail="Servicio inválido")
    total = precio * cantidad
    cursor.execute("INSERT INTO detalle_pedido (pedido_id,prenda_id,cantidad,servicio,total) values (%s,%s,%s,%s,%s)",(
                    pedido_id,prenda_id,cantidad,servicio,total
    ))
    conexion.commit()
    cursor.close()

def ver_detalle_pedido_id(id:int):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detalle_pedido WHERE id = %s", (id,))
    detalle_pedido = cursor.fetchone()
    if not detalle_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    cursor.close()
    return detalle_pedido

def eliminar_detalle_pedido(id:int):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM detalle_pedido WHERE id = %s", (id,))
    detalle_pedido = cursor.fetchone()
    if detalle_pedido:
        cursor.execute("delete from detalle_pedido where id = %s", (id,))
    else:
        raise HTTPException(status_code=404, detail= "detalle de pedido no encontrado")
    conexion.commit()
    cursor.close()

    