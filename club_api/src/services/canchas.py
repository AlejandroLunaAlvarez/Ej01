from ..repositories.canchas import (obtener_canchas_filtros,
                                         obtener_canchas,
                                         insertar_cancha,
                                         obtener_cancha_por_id,
                                         delete_cancha_por_id,
                                         update_parcialmente_cancha,
                                         obtener_canchas_activas_libres)

from ..validators.canchas import (validar_nombre,
                                    validar_deporte,
                                    validar_precio_hora,
                                    validar_id_cancha,
                                    revisar_reservas_cancha,
                                    validar_techada,
                                    validar_activa,
                                    validar_obligatorios,
                                    parsear_fecha_iso)

from ..constants import TZ_GMT3, HORA_MAXIMA, HORA_MINIMA, DURACION_MAXIMA_RESERVA

from datetime import datetime

def construir_cancha_dto(cancha: dict) -> dict:
    return {
        'nombre':   cancha['nombre'],
        'deporte_id':   cancha['deporte_id'],
        'precio_hora':   cancha['precio_hora'],
        'techada':   cancha['techada'],
        'activa':   cancha['activa'],
    }

def listar_canchas(deporte_id: int = None, nombre: str = None, techada: bool = None, activa: bool = None) -> list[dict]:
    if deporte_id is None and nombre is None and techada is None and activa is None:
        return [construir_cancha_dto(cancha) for cancha in obtener_canchas()]

    return [construir_cancha_dto(cancha) for cancha in obtener_canchas_filtros(deporte_id, nombre, techada, activa)]

    

def crear_cancha(body: dict) -> dict:
    validar_obligatorios(body.get('nombre'), 'nombre')
    nombre = validar_nombre(body.get('nombre'))

    deporte_id = body.get('deporte_id')
    validar_obligatorios(deporte_id, 'deporte')
    validar_deporte(deporte_id)

    precio_hora = body.get('precio_hora')
    validar_obligatorios(precio_hora, 'precio por hora')
    validar_precio_hora(precio_hora)

    techada = validar_techada(body.get('techada'))

    activa = validar_activa(body.get('activa'))

    insertar_cancha(
        nombre,
        deporte_id,
        precio_hora,
        techada,
        activa)

    return construir_cancha_dto({
        'nombre': nombre,
        'deporte_id': deporte_id,
        'precio_hora': precio_hora,
        'techada': techada,
        'activa': activa,
    })

def buscar_cancha_por_id(id_cancha: int) -> dict:
    cancha = obtener_cancha_por_id(id_cancha)

    if not cancha:
        return {}

    return construir_cancha_dto(cancha)

def eliminar_cancha_por_id(id_cancha: int):
    validar_id_cancha(id_cancha)
    revisar_reservas_cancha(id_cancha)
    delete_cancha_por_id(id_cancha)

def modificar_parcialmente_cancha(id_cancha: int, body: dict) -> dict:
    validar_id_cancha(id_cancha)

    nombre = body.get('nombre')
    if nombre is not None:
        nombre = validar_nombre(nombre)

    precio_hora = body.get('precio_hora')
    if precio_hora is not None:
        validar_precio_hora(precio_hora)

    techada = body.get('techada')

    activa = body.get('activa')

    cancha = update_parcialmente_cancha(
        id_cancha, nombre, precio_hora, techada, activa)
    return construir_cancha_dto(cancha)

def listar_canchas_disponibles(fecha_str: str, hora_inicio_str: str, hora_fin_str: str, deporte_id: int = None, techada: bool = None) -> dict:
    if not fecha_str or not hora_inicio_str or not hora_fin_str:
        raise ValueError("Los parámetros fecha, hora de inicio y hora fin son obligatorios.")

    fecha_inicio_str = f"{fecha_str}T{hora_inicio_str}"
    fecha_fin_str = f"{fecha_str}T{hora_fin_str}"

    fecha_inicio = parsear_fecha_iso(fecha_inicio_str)
    fecha_fin = parsear_fecha_iso(fecha_fin_str)

    if fecha_inicio >= fecha_fin:
        raise ValueError("La hora de inicio debe ser estrictamente menor a la de fin.")

    if fecha_inicio.time() < HORA_MINIMA or fecha_fin.time() > HORA_MAXIMA:
        raise ValueError("El intervalo de reserva debe estar dentro de la hora de atención del club (08:00-23:00).")

    duracion = fecha_fin - fecha_inicio
    if duracion > DURACION_MAXIMA_RESERVA:
        raise ValueError("El intervalo de reserva debe durar máximo 3 horas.")
    
    if fecha_inicio <= datetime.now(TZ_GMT3):
        raise ValueError("El intervalo de reserva debe ser posterior a la hora actual.")

    return obtener_canchas_activas_libres(fecha_inicio, fecha_fin, deporte_id, techada)