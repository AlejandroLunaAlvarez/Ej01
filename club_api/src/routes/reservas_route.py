from flask import Blueprint, request, jsonify
from src.validators.reservas_validator import validar_cuerpo_crear_reserva
from src.services.reservas_service import (
    crear_reserva_service,
    obtener_reserva_service,
    listar_reservas_service,
    cambiar_estado_service
)

reservas_bp = Blueprint('reservas', __name__)

# POST /club_api/reservas - Registrar reserva
@reservas_bp.route('/reservas', methods=['POST'])
def crear_reserva():
    data = request.get_json(silent=True)

    error_msg, status_code = validar_cuerpo_crear_reserva(data)
    respuesta = {"error": error_msg} if error_msg else None

    if not error_msg:
        respuesta, status_code = crear_reserva_service(data)

    return jsonify(respuesta), status_code


# GET /club_api/reservas/<id> - Obtener una reserva
@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def obtener_reserva(id):
    respuesta, status_code = obtener_reserva_service(id)
    return jsonify(respuesta), status_code


# GET /club_api/reservas - Listar reservas
@reservas_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    respuesta, status_code = listar_reservas_service(limit, offset)
    return jsonify(respuesta), status_code


# PUT /club_api/reservas/<id>/estado - Cambiar estado
@reservas_bp.route('/reservas/<int:id>/estado', methods=['PUT'])
def cambiar_estado_reserva(id):
    data = request.get_json(silent=True)

    respuesta, status_code = cambiar_estado_service(id, data)
    return jsonify(respuesta), status_code