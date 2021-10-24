import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
<<<<<<< Updated upstream
        password=" ",
=======
        password="1234",
>>>>>>> Stashed changes
        database="inventario"
    )
