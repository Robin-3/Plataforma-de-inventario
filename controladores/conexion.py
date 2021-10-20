import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fenix.2019@",
        database="inventario"
    )
