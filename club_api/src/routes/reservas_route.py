from flask import Blueprint, request, jsonify
from ..validators.reservas_validator import (
    validar_cuerpo_crear_reserva,
    validar_cuerpo_cambiar_estado
)
from ..services.reservas_service import (
    crear_reserva_service,
    obtener_reserva_service,
    listar_reservas_service,
    cambiar_estado_service
)

reservas_bp = Blueprint('reservas', __name__)

# Endpoint HTTP POST para registrar una nueva reserva
@reservas_bp.route('/reservas', methods=['POST'])
def crear_reserva():
    data = request.get_json(silent=True)
    error_msg, status_code = validar_cuerpo_crear_reserva(data)
    if error_msg:
        return jsonify({"error": error_msg}), status_code

    respuesta, status_code = crear_reserva_service(data)
    return jsonify(respuesta), status_code


# Endpoint HTTP GET para obtener el listado paginado de reservas
@reservas_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    try:
        limit = int(request.args.get('_limit', 10))
    except (ValueError, TypeError):
        limit = 10

    try:
        offset = int(request.args.get('_offset', 0))
    except (ValueError, TypeError):
        offset = 0

    respuesta, status_code = listar_reservas_service(limit, offset)
    return jsonify(respuesta), status_code


# Endpoint HTTP GET para obtener los detalles de una reserva por su ID
@reservas_bp.route('/reservas/<int:reserva_id>', methods=['GET'])
def obtener_reserva(reserva_id):
    respuesta, status_code = obtener_reserva_service(reserva_id)
    return jsonify(respuesta), status_code


# Endpoint HTTP PUT para cambiar el estado de una reserva (cancelar / finalizar)
@reservas_bp.route('/reservas/<int:reserva_id>/estado', methods=['PUT'])
def cambiar_estado(reserva_id):
    data = request.get_json(silent=True)
    error_msg, status_code = validar_cuerpo_cambiar_estado(data)
    if error_msg:
        return jsonify({"error": error_msg}), status_code

    respuesta, status_code = cambiar_estado_service(reserva_id, data)
    return jsonify(respuesta), status_code