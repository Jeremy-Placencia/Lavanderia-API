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

def get_all_clientes():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("select * from clientes")
    clientes = cursor.fetchall()
    if not clientes:
        raise HTTPException(status_code=404, detail="No hay ningun cliente agregado")
    cursor.close()
    return clientes

def post_cliente(nombre: str, telefono: str):
    telefono = formatear_telefono(telefono)
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO clientes (nombre, telefono) VALUES (%s, %s)", (nombre, telefono))
    conexion.commit()
    cursor.close()

def formatear_telefono(telefono: str):
    telefono = telefono.replace("-", "")  # quita guiones si ya los tiene
    if len(telefono) != 10:
        raise HTTPException(status_code=400, detail="El número debe tener exactamente 10 dígitos")
    return f"{telefono[:3]}-{telefono[3:6]}-{telefono[6:]}"

def buscar_clientes_id(id:int):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cursor.close()
    return cliente

def eliminar_cliente_id(id:int):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    if cliente:
        cursor.execute("delete from clientes where id = %s", (id,))
    else:
        raise HTTPException(status_code=404, detail= "Cliente no encontrado")
    conexion.commit()
    cursor.close()

def actualizar_cliente_id(id:int,nombre:str,telefono:str):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    cliente = cursor.fetchone()
    if cliente:
        cursor.execute("update clientes set nombre = %s, telefono = %s where id = %s",(nombre,telefono,id))
    else:
        raise HTTPException(status_code=404, detail= "Cliente no encontrado")
    conexion.commit()
    cursor.close()
    