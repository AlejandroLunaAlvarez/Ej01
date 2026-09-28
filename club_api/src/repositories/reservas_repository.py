from ..db import ejecutar_consulta, ejecutar_mutacion

# Consulta un socio y el estado en el que se encuentra
def obtener_socio_por_id(socio_id):
    sql = """
        SELECT id, activo, IF(activo = 1, 'activo', 'inactivo') AS estado_nombre 
        FROM socios 
        WHERE id = :id
    """
    filas = ejecutar_consulta(sql, {"id": socio_id})
    return filas[0] if filas else None


# Consulta una cancha por su ID para verificar su estado de activación y precio por hora
def obtener_cancha_por_id(cancha_id):
    sql = "SELECT id, precio_hora, activa FROM canchas WHERE id = :id"
    filas = ejecutar_consulta(sql, {"id": cancha_id})
    return filas[0] if filas else None


# Comprueba si existen reservas confirmadas que se superpongan en el horario solicitado
def buscar_superposiciones(cancha_id, socio_id, fecha_inicio, fecha_fin):
    sql = """
        SELECT id FROM reservas 
        WHERE estado_id = 1 
          AND (cancha_id = :cancha_id OR socio_id = :socio_id)
          AND NOT (fecha_hora_fin <= :fecha_inicio OR fecha_hora_inicio >= :fecha_fin)
    """
    params = {
        "cancha_id": cancha_id,
        "socio_id": socio_id,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    }
    return ejecutar_consulta(sql, params)


# Comprueba si existen bloqueos por mantenimiento que se superpongan en el horario solicitado
def buscar_bloqueos_superpuestos(cancha_id, fecha_inicio, fecha_fin):
    sql = """
        SELECT id FROM bloqueos 
        WHERE cancha_id = :cancha_id 
          AND fecha = DATE(:fecha_inicio) 
          AND NOT (horario_fin <= TIME(:fecha_inicio) OR horario_inicio >= TIME(:fecha_fin))
    """
    params = {
        "cancha_id": cancha_id,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    }
    return ejecutar_consulta(sql, params)


# Inserta una nueva reserva en la base de datos y retorna su ID generado
def crear_reserva(socio_id, cancha_id, fecha_inicio, fecha_fin, importe, estado_id=1):
    sql = """
        INSERT INTO reservas (socio_id, cancha_id, estado_id, fecha_hora_inicio, fecha_hora_fin, importe) 
        VALUES (:socio_id, :cancha_id, :estado_id, :fecha_inicio, :fecha_fin, :importe)
    """
    params = {
        "socio_id": socio_id,
        "cancha_id": cancha_id,
        "estado_id": estado_id,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "importe": importe
    }
    return ejecutar_mutacion(sql, params)


# Obtiene los detalles completos de una reserva por su ID
def obtener_reserva_por_id(reserva_id):
    sql = """
        SELECT r.id, r.socio_id AS id_socio, r.cancha_id AS id_cancha, 
               er.nombre AS estado, r.fecha_hora_inicio, r.fecha_hora_fin, r.importe
        FROM reservas r
        JOIN estados_reservas er ON r.estado_id = er.id
        WHERE r.id = :id
    """
    filas = ejecutar_consulta(sql, {"id": reserva_id})
    return filas[0] if filas else None


# Consulta el listado de reservas de forma paginada y el total de registros
def listar_reservas_paginado(limit, offset):
    sql_data = """
        SELECT r.id, r.socio_id AS id_socio, r.cancha_id AS id_cancha, 
               er.nombre AS estado, r.fecha_hora_inicio, r.fecha_hora_fin, r.importe
        FROM reservas r
        JOIN estados_reservas er ON r.estado_id = er.id
        ORDER BY r.id ASC
        LIMIT :limit OFFSET :offset
    """
    sql_count = "SELECT COUNT(*) as total FROM reservas"

    res_count = ejecutar_consulta(sql_count)
    total = res_count[0]['total'] if res_count else 0
    reservas = ejecutar_consulta(sql_data, {"limit": limit, "offset": offset})

    return reservas, total


# Actualiza el estado de una reserva existente en la base de datos
def actualizar_estado_reserva(reserva_id, nuevo_estado_nombre):
    sql_get_id = "SELECT id FROM estados_reservas WHERE LOWER(nombre) = :nombre"
    estados = ejecutar_consulta(sql_get_id, {"nombre": nuevo_estado_nombre.lower()})
    exito = False

    if estados:
        estado_id = estados[0]['id']
        sql_update = "UPDATE reservas SET estado_id = :estado_id WHERE id = :id"
        ejecutar_mutacion(sql_update, {"estado_id": estado_id, "id": reserva_id})
        exito = True

    return exito