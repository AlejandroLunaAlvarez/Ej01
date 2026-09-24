from datetime import datetime

# Valida la estructura del JSON, tipos de datos y presencia de campos para la creación de reservas.
def validar_cuerpo_crear_reserva(data):
    mensaje_error = None
    codigo = 200
    es_valido = True

    if not data:
        mensaje_error = "El cuerpo JSON no puede estar vacío"
        codigo = 400
        es_valido = False

    if es_valido:
        campos_requeridos = ['id_socio', 'id_cancha', 'fecha_hora_inicio', 'fecha_hora_fin']
        
        for campo in campos_requeridos:
            if campo not in data:
                mensaje_error = f"El campo '{campo}' es obligatorio"
                codigo = 400
                es_valido = False

        if es_valido and len(data) > len(campos_requeridos):
            mensaje_error = "Se recibieron campos adicionales no permitidos"
            codigo = 400
            es_valido = False

    if es_valido:
        if not isinstance(data['id_socio'], int) or data['id_socio'] <= 0:
            mensaje_error = "El 'id_socio' debe ser un entero positivo"
            codigo = 400
            es_valido = False
        elif not isinstance(data['id_cancha'], int) or data['id_cancha'] <= 0:
            mensaje_error = "El 'id_cancha' debe ser un entero positivo"
            codigo = 400
            es_valido = False

    if es_valido:
        dt_inicio = parsear_fecha_iso(data['fecha_hora_inicio'])
        dt_fin = parsear_fecha_iso(data['fecha_hora_fin'])

        if not dt_inicio or not dt_fin:
            mensaje_error = "Las fechas deben estar en formato ISO 8601 GMT-3 (YYYY-MM-DDTHH:MM:SS.ffffff-03:00)"
            codigo = 400
            es_valido = False

    return mensaje_error, codigo


# Convierte un string en formato ISO 8601 a un objeto datetime.
def parsear_fecha_iso(fecha_str):
    fecha_dt = None
    try:
        fecha_dt = datetime.fromisoformat(fecha_str)
    except Exception:
        fecha_dt = None

    return fecha_dt