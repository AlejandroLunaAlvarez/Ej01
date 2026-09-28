from datetime import datetime, time

# Valida la estructura del JSON, tipos de datos, formato ISO, horario del club y fecha futura para crear reservas
def validar_cuerpo_crear_reserva(data):
    if not data:
        return "El cuerpo JSON no puede estar vacío", 400

    campos_requeridos = ['id_socio', 'id_cancha', 'fecha_hora_inicio', 'fecha_hora_fin']
    for campo in campos_requeridos:
        if campo not in data:
            return f"El campo '{campo}' es obligatorio", 400

    if len(data) > len(campos_requeridos):
        return "Se recibieron campos adicionales no permitidos", 400

    if not isinstance(data['id_socio'], int) or data['id_socio'] <= 0:
        return "El 'id_socio' debe ser un entero positivo", 400

    if not isinstance(data['id_cancha'], int) or data['id_cancha'] <= 0:
        return "El 'id_cancha' debe ser un entero positivo", 400

    dt_inicio = parsear_fecha_iso(data['fecha_hora_inicio'])
    dt_fin = parsear_fecha_iso(data['fecha_hora_fin'])

    if not dt_inicio or not dt_fin:
        return "Las fechas deben estar en formato ISO 8601 GMT-3 (YYYY-MM-DDTHH:MM:SS.ffffff-03:00)", 400

    now = datetime.now(dt_inicio.tzinfo) if dt_inicio.tzinfo else datetime.now()
    if dt_inicio <= now:
        return "La fecha y hora de inicio de la reserva debe ser estrictamente futura", 400

    if dt_inicio.minute != 0 or dt_inicio.second != 0 or dt_fin.minute != 0 or dt_fin.second != 0:
        return "Las reservas deben iniciar y finalizar en horas exactas (ej. 18:00:00)", 400

    if dt_inicio.date() != dt_fin.date():
        return "La reserva no puede cruzar la medianoche", 400

    if dt_inicio.time() < time(8, 0) or dt_fin.time() > time(23, 0):
        return "Las reservas deben estar dentro del horario de atención del club (08:00 a 23:00 hs)", 400

    return None, 200


# Valida que el cuerpo JSON para el cambio de estado contenga únicamente un estado permitido
def validar_cuerpo_cambiar_estado(data):
    if not data:
        return "El cuerpo JSON no puede estar vacío", 400

    if 'estado' not in data:
        return "El campo 'estado' es obligatorio", 400

    if len(data) > 1:
        return "Se recibieron campos adicionales no permitidos", 400

    if not isinstance(data['estado'], str) or data['estado'].lower() not in ['cancelada', 'finalizada']:
        return "El campo 'estado' solo acepta los valores 'cancelada' o 'finalizada'", 400

    return None, 200


# Convierte una cadena en formato ISO 8601 a un objeto datetime
def parsear_fecha_iso(fecha_str):
    try:
        return datetime.fromisoformat(fecha_str)
    except Exception:
        return None