from sqlalchemy import create_engine, text
from datetime import datetime, date, time
from ..db import ejecutar_consulta, ejecutar_mutacion

def obtener_canchas():
    sql = 'SELECT * FROM canchas'
    return ejecutar_consulta(sql)

def obtener_canchas_filtros(deporte_id: int = None, nombre: str = None,
                            techada: bool = None, activa: bool = None):
    condiciones = []
    datos = {}

    if deporte_id is not None:
        condiciones.append('deporte_id = :deporte_id')
        datos['deporte_id'] = int(deporte_id)

    if nombre is not None:
        condiciones.append('nombre = :nombre')
        datos['nombre'] = nombre

    if techada is not None:
        condiciones.append('techada = :techada')
        datos['techada'] = 1 if techada in (True, 1, '1', 'true', 'True') else 0

    if activa is not None:
        condiciones.append('activa = :activa')
        datos['activa'] = 1 if activa in (True, 1, '1', 'true', 'True') else 0

    sql = 'SELECT * FROM canchas'
    if condiciones:
        sql += ' WHERE ' + ' AND '.join(condiciones)

    return ejecutar_consulta(sql, datos)

def obtener_canchas_activas_libres(fecha_inicio: datetime, fecha_fin: datetime, deporte_id: int = None, techada: bool = None) -> dict:
    condiciones_opcionales = []    
    datos = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    }

    if deporte_id is not None:
        condiciones_opcionales.append('c.deporte_id = :deporte_id')
        datos['deporte_id'] = int(deporte_id)

    if techada is not None:
        condiciones_opcionales.append('c.techada = :techada')
        datos['techada'] = 1 if techada in (True, 1, '1', 'true', 'True') else 0
    
    filtro_opcional = ''
    if condiciones_opcionales:
        filtro_opcional += ' AND ' + ' AND '.join(condiciones_opcionales)

    sql = f"""
        SELECT c.id, c.nombre, c.deporte_id, c.precio_hora, c.techada, c.activa 
        FROM canchas c
        WHERE c.activa = 1 {filtro_opcional}
        AND c.id NOT IN (
            SELECT r.cancha_id
            FROM reservas r
            WHERE r.fecha_hora_inicio < :fecha_fin
                AND r.fecha_hora_fin > :fecha_inicio)
        """

    return ejecutar_consulta(sql, datos)

def insertar_cancha(nombre: str, deporte_id: int, precio_hora: int, techada: bool, activa: bool) -> int:
    sql = """
        INSERT INTO canchas (nombre, deporte_id, precio_hora, techada, activa)
        VALUES (:nombre, :deporte_id, :precio_hora, :techada, :activa)
    """

    datos = {
        'nombre': nombre,
        'deporte_id': deporte_id,
        'precio_hora': precio_hora,
        'techada': techada,
        'activa': activa
    }

    return ejecutar_mutacion(sql, datos)

def obtener_deporte_por_id(deporte_id: int) -> dict:
    sql = 'SELECT id FROM deportes WHERE id=:deporte_id'
    dato = { 'deporte_id': deporte_id }
    filas = ejecutar_consulta(sql, dato)

    return filas[0] if filas else {}

def obtener_cancha_por_id(id_cancha: int) -> dict:
    sql = 'SELECT * FROM canchas WHERE id=:id_cancha'
    dato = { 'id_cancha': id_cancha }
    filas = ejecutar_consulta(sql, dato)

    return filas[0] if filas else {}

def delete_cancha_por_id(id_cancha: int):
    sql = 'DELETE FROM canchas WHERE id=:id_cancha'
    dato = { 'id_cancha': id_cancha }
    ejecutar_mutacion(sql, dato)

def update_parcialmente_cancha(id_cancha: int, nombre: str, precio_hora: int, techada: bool, activa: bool) -> dict:
    condiciones = []
    datos = {}

    if nombre is not None:
        condiciones.append('nombre = :nombre')
        datos['nombre'] = nombre

    if precio_hora is not None:
        condiciones.append('precio_hora = :precio_hora')
        datos['precio_hora'] = int(precio_hora)

    if techada is not None:
        condiciones.append('techada = :techada')
        datos['techada'] = 1 if techada in (True, 1, '1', 'true', 'True') else 0

    if activa is not None:
        condiciones.append('activa = :activa')
        datos['activa'] = 1 if activa in (True, 1, '1', 'true', 'True') else 0

    if condiciones:
        clausula_set = ', '.join(condiciones)
        datos['id_cancha'] = id_cancha
        sql = f"""UPDATE canchas
                SET {clausula_set}
                WHERE id = :id_cancha"""

        ejecutar_mutacion(sql, datos)

    sql = 'SELECT * FROM canchas WHERE id=:id_cancha'
    cancha = ejecutar_consulta(sql, { 'id_cancha': id_cancha })
    return cancha[0]

def obtener_reserva_por_id_cancha(id_cancha: int) -> dict:
    sql = 'SELECT id FROM reservas WHERE cancha_id=:id_cancha'
    dato = { 'id_cancha': id_cancha }

    return ejecutar_consulta(sql, dato)