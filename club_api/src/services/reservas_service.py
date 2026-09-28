from datetime import datetime
from ..repositories import reservas_repository as repo
from ..validators.reservas_validator import parsear_fecha_iso

# Gestiona la lógica de negocio para la creación y validación integral de una reserva
def crear_reserva_service(data):
    socio = repo.obtener_socio_por_id(data['id_socio'])
    if not socio:
        return {"error": "El socio ingresado no existe"}, 400
    if not socio['activo']:
        return {"error": "El socio no se encuentra activo"}, 400

    cancha = repo.obtener_cancha_por_id(data['id_cancha'])
    if not cancha:
        return {"error": "La cancha ingresada no existe"}, 400
    if not cancha['activa']:
        return {"error": "La cancha no se encuentra activa"}, 400

    dt_inicio = parsear_fecha_iso(data['fecha_hora_inicio'])
    dt_fin = parsear_fecha_iso(data['fecha_hora_fin'])

    if dt_fin <= dt_inicio:
        return {"error": "La fecha/hora fin debe ser posterior a la fecha/hora inicio"}, 400

    duracion = dt_fin - dt_inicio
    horas = duracion.total_seconds() / 3600

    if horas not in [1.0, 2.0, 3.0]:
        return {"error": "La duración de la reserva debe ser exactamente de 1, 2 o 3 horas íntegras"}, 400

    superposiciones = repo.buscar_superposiciones(
        data['id_cancha'], data['id_socio'], dt_inicio, dt_fin
    )
    if superposiciones:
        return {"error": "Existe una reserva superpuesta para esa cancha o socio en el horario solicitado"}, 409

    bloqueos = repo.buscar_bloqueos_superpuestos(data['id_cancha'], dt_inicio, dt_fin)
    if bloqueos:
        return {"error": "La cancha se encuentra bloqueada por mantenimiento en el horario solicitado"}, 409

    importe = int(horas * cancha['precio_hora'])
    nuevo_id = repo.crear_reserva(
        data['id_socio'], data['id_cancha'], dt_inicio, dt_fin, importe
    )

    reserva_creada = repo.obtener_reserva_por_id(nuevo_id)
    return reserva_creada, 201


# Obtiene la información detallada de una reserva por su ID
def obtener_reserva_service(reserva_id):
    reserva = repo.obtener_reserva_por_id(reserva_id)
    if not reserva:
        return {"error": "Reserva no encontrada"}, 404
    return reserva, 200


# Retorna el listado paginado de reservas incluyendo los enlaces de navegación HATEOAS
def listar_reservas_service(limit=10, offset=0):
    if limit < 1 or limit > 100:
        limit = 10
    if offset < 0:
        offset = 0

    reservas, total = repo.listar_reservas_paginado(limit, offset)

    base_url = "/club_api/reservas"
    last_offset = max(0, ((total - 1) // limit) * limit) if total > 0 else 0
    prev_offset = max(0, offset - limit) if offset >= limit else None
    next_offset = offset + limit if (offset + limit) < total else None

    links = {
        "_first": f"{base_url}?_limit={limit}&_offset=0",
        "_last": f"{base_url}?_limit={limit}&_offset={last_offset}"
    }

    if prev_offset is not None:
        links["_prev"] = f"{base_url}?_limit={limit}&_offset={prev_offset}"
    if next_offset is not None:
        links["_next"] = f"{base_url}?_limit={limit}&_offset={next_offset}"

    return {
        "reservas": reservas,
        "total": total,
        "_limit": limit,
        "_offset": offset,
        "_links": links
    }, 200


# Procesa la actualización del estado de una reserva verificando sus restricciones
def cambiar_estado_service(reserva_id, data):
    reserva = repo.obtener_reserva_por_id(reserva_id)
    if not reserva:
        return {"error": "Reserva no encontrada"}, 404

    nuevo_estado = data['estado'].lower()
    estado_actual = reserva['estado'].lower()

    if nuevo_estado not in ['cancelada', 'finalizada']:
        return {"error": "El nuevo estado debe ser 'cancelada' o 'finalizada'"}, 400

    if estado_actual != 'confirmada':
        return {"error": f"No se puede modificar una reserva con estado '{estado_actual}'"}, 409

    exito = repo.actualizar_estado_reserva(reserva_id, nuevo_estado)
    if not exito:
        return {"error": "Error al actualizar el estado de la reserva"}, 400

    reserva_actualizada = repo.obtener_reserva_por_id(reserva_id)
    return reserva_actualizada, 200