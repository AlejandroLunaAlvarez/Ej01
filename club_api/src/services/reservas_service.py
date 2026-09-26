from datetime import datetime
from ..repositories import reservas_repository as repo
from ..validators.reservas_validator import parsear_fecha_iso

def crear_reserva_service(data):
    # 1. Verificar si existe el socio y si está activo
    socio = repo.obtener_socio_por_id(data['id_socio'])
    if not socio:
        return {"error": "El socio ingresado no existe"}, 400
    if socio['estado_nombre'].lower() != 'activo':
        return {"error": "El socio no se encuentra activo"}, 400

    # 2. Verificar si existe la cancha y si está activa
    cancha = repo.obtener_cancha_por_id(data['id_cancha'])
    if not cancha:
        return {"error": "La cancha ingresada no existe"}, 400
    if not cancha['activa']:
        return {"error": "La cancha no se encuentra activa para reservas"}, 400

    # 3. Validar rango de fechas y calcular horas
    dt_inicio = parsear_fecha_iso(data['fecha_hora_inicio'])
    dt_fin = parsear_fecha_iso(data['fecha_hora_fin'])

    if dt_fin <= dt_inicio:
        return {"error": "La fecha/hora fin debe ser posterior a la fecha/hora inicio"}, 400

    duracion = dt_fin - dt_inicio
    horas = duracion.total_seconds() / 3600

    if horas not in [1.0, 2.0, 3.0]:
        return {"error": "La duración de la reserva debe ser exactamente de 1, 2 o 3 horas integras"}, 400

    # 4. Validar superposiciones
    superposiciones = repo.buscar_superposiciones(
        data['id_cancha'], data['id_socio'], dt_inicio, dt_fin
    )
    if superposiciones:
        return {"error": "Existe una reserva superpuesta para esa cancha o socio en el horario solicitado"}, 409

    # 5. Calcular importe e insertar
    importe = int(horas * cancha['precio_hora'])
    nuevo_id = repo.crear_reserva(
        data['id_socio'], data['id_cancha'], dt_inicio, dt_fin, importe
    )

    reserva_creada = repo.obtener_reserva_por_id(nuevo_id)
    return reserva_creada, 201


def obtener_reserva_service(reserva_id):
    reserva = repo.obtener_reserva_por_id(reserva_id)
    if not reserva:
        return {"error": "Reserva no encontrada"}, 404
    return reserva, 200


def listar_reservas_service(limit=10, offset=0):
    reservas, total = repo.listar_reservas_paginado(limit, offset)
    return {"reservas": reservas, "total": total, "limit": limit, "offset": offset}, 200


def cambiar_estado_service(reserva_id, data):
    if not data or 'estado' not in data:
        return {"error": "El campo 'estado' es obligatorio"}, 400

    nuevo_estado = data['estado']
    exito = repo.actualizar_estado_reserva(reserva_id, nuevo_estado)

    if not exito:
        return {"error": "No se pudo actualizar el estado. Estado no válido o reserva inexistente"}, 400

    reserva_actualizada = repo.obtener_reserva_por_id(reserva_id)
    return reserva_actualizada, 200