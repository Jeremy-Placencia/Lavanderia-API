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

def ver_prendas():
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prendas")
    mostrar = cursor.fetchall()
    if not mostrar:
        raise HTTPException(status_code=404, detail="No hay ninguna prenda agregada")
    cursor.close()
    return mostrar

def crear_prenda(nombre_prenda:str,precio_lavado:int,precio_planchado:int,precio_ambos:int):
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO prendas (nombre_prenda,precio_lavado,precio_planchado,precio_ambos) values (%s,%s,%s,%s)",(nombre_prenda,precio_lavado,precio_planchado,precio_ambos))
    conexion.commit()
    cursor.close()

def ver_prenda_id(id:int):
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prendas WHERE id = %s", (id,))
    prendas = cursor.fetchone()
    if not prendas:
        raise HTTPException(status_code=404, detail="prenda no encontrada")
    cursor.close()
    return prendas

def eliminar_prendas_id(id:int):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM prendas WHERE id = %s", (id,))
    pedidos = cursor.fetchone()
    if pedidos:
        cursor.execute("delete from prendas where id = %s", (id,))
    else:
        raise HTTPException(status_code=404, detail= "Prenda no encontrada")
    conexion.commit()
    cursor.close()

def actualizar_prenda_id(id:int,nombre_prenda:str,precio_lavado:int,precio_planchado:int,precio_ambos:int):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM prendas WHERE id = %s", (id,))
    prenda = cursor.fetchone()
    if prenda:
        cursor.execute("update prendas set nombre_prenda = %s, precio_lavado = %s, precio_planchado = %s, precio_ambos = %s where id = %s",(nombre_prenda,precio_lavado,precio_planchado,precio_ambos,id))
    else:
        raise HTTPException(status_code=404, detail= "Prenda no encontrado")
    conexion.commit()
    cursor.close()