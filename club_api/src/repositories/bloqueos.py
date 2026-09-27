from ..db import ejecutar_consulta, ejecutar_mutacion


# Busca bloqueos que se superpongan con el horario enviado
def buscar_bloqueos_superpuestos(
    cancha_id,
    fecha,
    hora_inicio,
    hora_fin
):
    sql = """
        SELECT id
        FROM bloqueos
        WHERE cancha_id = :cancha_id
          AND fecha = :fecha
          AND horario_inicio < :hora_fin
          AND horario_fin > :hora_inicio
    """

    datos = {
        "cancha_id": cancha_id,
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin
    }

    return ejecutar_consulta(sql, datos)


# Busca reservas confirmadas que se superpongan con el horario enviado
def buscar_reservas_superpuestas(
    cancha_id,
    fecha_inicio,
    fecha_fin
):
    sql = """
        SELECT id
        FROM reservas
        WHERE estado_id = 1
          AND cancha_id = :cancha_id
          AND fecha_hora_inicio < :fecha_fin
          AND fecha_hora_fin > :fecha_inicio
    """

    datos = {
        "cancha_id": cancha_id,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    }

    return ejecutar_consulta(sql, datos)


# Inserta un nuevo bloqueo
def crear_bloqueo(
    cancha_id,
    fecha,
    hora_inicio,
    hora_fin,
    motivo
):
    sql = """
        INSERT INTO bloqueos (
            cancha_id,
            fecha,
            horario_inicio,
            horario_fin,
            motivo
        )
        VALUES (
            :cancha_id,
            :fecha,
            :hora_inicio,
            :hora_fin,
            :motivo
        )
    """

    datos = {
        "cancha_id": cancha_id,
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "motivo": motivo
    }

    return ejecutar_mutacion(sql, datos)


# Lista los bloqueos aplicando filtros opcionales
def listar_bloqueos(id_cancha=None, fecha=None):
    sql = """
        SELECT
            id,
            cancha_id AS id_cancha,
            fecha,
            CAST(horario_inicio AS CHAR) AS hora_inicio,
            CAST(horario_fin AS CHAR) AS hora_fin,
            motivo
        FROM bloqueos
    """

    condiciones = []
    datos = {}

    if id_cancha is not None:
        condiciones.append("cancha_id = :id_cancha")
        datos["id_cancha"] = id_cancha

    if fecha is not None:
        condiciones.append("fecha = :fecha")
        datos["fecha"] = fecha

    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones)

    sql += " ORDER BY fecha, horario_inicio"

    return ejecutar_consulta(sql, datos)


# Busca un bloqueo por su ID
def obtener_bloqueo_por_id(id_bloqueo):
    sql = """
        SELECT
            id,
            cancha_id AS id_cancha,
            fecha,
            CAST(horario_inicio AS CHAR) AS hora_inicio,
            CAST(horario_fin AS CHAR) AS hora_fin,
            motivo
        FROM bloqueos
        WHERE id = :id_bloqueo
    """

    datos = {
        "id_bloqueo": id_bloqueo
    }

    return ejecutar_consulta(sql, datos)


# Elimina un bloqueo por su ID
def eliminar_bloqueo_por_id(id_bloqueo):
    sql = """
        DELETE FROM bloqueos
        WHERE id = :id_bloqueo
    """

    datos = {
        "id_bloqueo": id_bloqueo
    }

    return ejecutar_mutacion(sql, datos)