from datetime import datetime

from ..repositories import bloqueos as repo
from ..repositories.canchas import obtener_cancha_por_id

from ..validators.bloqueos import (
    validar_bloqueo,
    validar_fecha,
    convertir_hora
)

from ..constants import TZ_GMT3


def crear_bloqueo_service(data):
    validar_bloqueo(data)

    cancha = obtener_cancha_por_id(data["id_cancha"])

    if not cancha:
        raise ValueError(
            f"La cancha con id '{data['id_cancha']}' no existe"
        )

    fecha = datetime.strptime(
        data["fecha"],
        "%Y-%m-%d"
    ).date()

    hora_inicio = convertir_hora(data["hora_inicio"])
    hora_fin = convertir_hora(data["hora_fin"])

    bloqueos_superpuestos = repo.buscar_bloqueos_superpuestos(
        data["id_cancha"],
        fecha,
        hora_inicio,
        hora_fin
    )

    if bloqueos_superpuestos:
        raise ValueError(
            "Ya existe un bloqueo que se superpone con el horario indicado"
        )

    fecha_hora_inicio = datetime.combine(
        fecha,
        hora_inicio,
        tzinfo=TZ_GMT3
    )

    fecha_hora_fin = datetime.combine(
        fecha,
        hora_fin,
        tzinfo=TZ_GMT3
    )

    reservas_superpuestas = repo.buscar_reservas_superpuestas(
        data["id_cancha"],
        fecha_hora_inicio,
        fecha_hora_fin
    )

    if reservas_superpuestas:
        raise ValueError(
            "Existe una reserva confirmada que se superpone con el horario indicado"
        )

    nuevo_id = repo.crear_bloqueo(
        data["id_cancha"],
        fecha,
        hora_inicio,
        hora_fin,
        data["motivo"]
    )

    return {
        "id": nuevo_id,
        "id_cancha": data["id_cancha"],
        "fecha": data["fecha"],
        "hora_inicio": data["hora_inicio"],
        "hora_fin": data["hora_fin"],
        "motivo": data["motivo"]
    }


def listar_bloqueos_service(id_cancha=None, fecha=None):

    if fecha is not None:
        validar_fecha(fecha)

    return repo.listar_bloqueos(
        id_cancha,
        fecha
    )


def eliminar_bloqueo_service(id_bloqueo):
    bloqueo = repo.obtener_bloqueo_por_id(id_bloqueo)

    if not bloqueo:
        raise ValueError("El bloqueo no existe")

    repo.eliminar_bloqueo_por_id(id_bloqueo)