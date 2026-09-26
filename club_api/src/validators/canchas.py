from ..repositories.canchas import (obtener_deporte_por_id,
                                         obtener_cancha_por_id,
                                         obtener_reserva_por_id_cancha)

from datetime import datetime
from ..constants import TZ_GMT3

def validar_obligatorios(campo, tipo_campo: str):
    if campo is None:
        raise ValueError(f"El campo {tipo_campo} es obligatorio.")

def validar_nombre(nombre: str) -> str:
    nombre_sin_espacios = nombre.strip()

    if not nombre_sin_espacios:
        raise ValueError("El nombre no puede estar vacío.")

    return nombre_sin_espacios

def validar_deporte(deporte_id: int):    
    deporte = obtener_deporte_por_id(deporte_id)
    if not deporte:
        raise ValueError("El deporte ingresado no existe.")

def validar_precio_hora(precio_hora: int):
    if not type(precio_hora) is int or (type(precio_hora) is int and precio_hora <= 0):
        raise ValueError("El precio por hora debe ser un entero positivo y distinto de 0.")

def validar_id_cancha(id_cancha: int):
    cancha = obtener_cancha_por_id(id_cancha)
    if not cancha:
        raise KeyError(f"La cancha de id: {id_cancha} no existe.")

def revisar_reservas_cancha(id_cancha: int):
    reserva = obtener_reserva_por_id_cancha(id_cancha)
    if reserva:
        raise ValueError(f"La cancha de id: {id_cancha} tiene una o varias reservas.")


def validar_techada(techada: bool) -> bool:
    if techada is None:
        return False
    return techada


def validar_activa(activa: bool) -> bool:
    if activa is None:
        return True
    return activa

def parsear_fecha_iso(fecha):
    try:
        fecha_dt = datetime.fromisoformat(fecha).replace(microsecond=0, tzinfo=TZ_GMT3)
    except ValueError:
        raise ValueError("Formato de fecha u hora inválido.")

    return fecha_dt
