from typing import List
from hashlib import pbkdf2_hmac
from math import ceil

SALT = b'Al cesar lo que es del cesar'

def CifrarContrasena(contrasena: str) -> str:
    return pbkdf2_hmac('sha256', contrasena.encode('utf-8'), SALT, 100000).hex()

def ListaATabla(lista: list, numero_columnas: int) -> List[list]:
    return [lista[sublista*numero_columnas:(sublista+1)*numero_columnas] for sublista in range(ceil(len(lista)/numero_columnas))] # if len(lista) > 0 else [[]]
