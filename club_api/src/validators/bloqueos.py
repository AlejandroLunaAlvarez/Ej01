import re
from datetime import datetime

from ..constants import (
    FORMATO_FECHA,
    TZ_GMT3,
    HORA_MINIMA,
    HORA_MAXIMA,
)


def validar_id_cancha(id_cancha: int):
    if not isinstance(id_cancha, int) or id_cancha <= 0:
        raise ValueError("id_cancha debe ser un número entero positivo")


def validar_hora(hora: str, nombre_campo: str):
    if not isinstance(hora, str):
        raise ValueError(f"{nombre_campo} debe ser un texto")

    formato_hora = r"^(?:[01]\d|2[0-3]):00:00$"

    if not re.match(formato_hora, hora):
        raise ValueError(
            f"{nombre_campo} debe tener formato HH:MM:SS y ser una hora exacta"
        )


def convertir_hora(hora: str):
    return datetime.strptime(hora, "%H:%M:%S").time()


def validar_horario(hora_inicio, hora_fin):
    if hora_inicio < HORA_MINIMA:
        raise ValueError(
            f"hora_inicio no puede ser anterior a {HORA_MINIMA}"
        )

    if hora_fin > HORA_MAXIMA:
        raise ValueError(
            f"hora_fin no puede ser posterior a {HORA_MAXIMA}"
        )

    if hora_fin <= hora_inicio:
        raise ValueError(
            "hora_fin debe ser posterior a hora_inicio"
        )


def validar_fecha(fecha: str):
    if not isinstance(fecha, str):
        raise ValueError("fecha debe ser un texto")

    try:
        fecha_obj = datetime.strptime(
            fecha,
            FORMATO_FECHA
        ).date()
    except ValueError:
        raise ValueError("fecha debe tener formato AAAA-MM-DD")

    return fecha_obj


def validar_inicio_futuro(fecha, hora_inicio):
    ahora = datetime.now(TZ_GMT3)

    inicio_bloqueo = datetime.combine(
        fecha,
        hora_inicio,
        tzinfo=TZ_GMT3
    )

    if inicio_bloqueo <= ahora:
        raise ValueError(
            "El inicio del bloqueo debe ser posterior al horario actual"
        )


def validar_motivo(motivo: str):
    if not isinstance(motivo, str):
        raise ValueError("motivo debe ser un texto")

    if not motivo.strip():
        raise ValueError("motivo no puede estar vacío")


def validar_bloqueo(datos):
    campos_permitidos = {
        "id_cancha",
        "fecha",
        "hora_inicio",
        "hora_fin",
        "motivo",
    }

    for campo in datos:
        if campo not in campos_permitidos:
            raise ValueError(
                f"El campo {campo} no está permitido"
            )

    campos_req = [
        "id_cancha",
        "fecha",
        "hora_inicio",
        "hora_fin",
        "motivo",
    ]

    for campo in campos_req:
        if campo not in datos:
            raise ValueError(
                f"El campo {campo} es requerido"
            )

    validar_id_cancha(datos["id_cancha"])

    validar_hora(datos["hora_inicio"], "hora_inicio")
    validar_hora(datos["hora_fin"], "hora_fin")

    hora_inicio = convertir_hora(datos["hora_inicio"])
    hora_fin = convertir_hora(datos["hora_fin"])

    validar_horario(hora_inicio, hora_fin)

    fecha = validar_fecha(datos["fecha"])

    validar_inicio_futuro(fecha, hora_inicio)

    validar_motivo(datos["motivo"])