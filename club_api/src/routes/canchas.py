from flask import Blueprint, jsonify, request
from ..services.canchas import (listar_canchas,
                                  crear_cancha,
                                  buscar_cancha_por_id,
                                  eliminar_cancha_por_id,
                                  modificar_parcialmente_cancha,
                                  listar_canchas_disponibles)

canchas_bp = Blueprint('canchas', __name__)

@canchas_bp.route('/canchas', methods=['GET'])
def get_canchas():
    deporte_id_str = request.args.get("deporte_id")
    deporte_id = int(deporte_id_str) if deporte_id_str else None

    nombre = request.args.get("nombre")

    techada = request.args.get("techada")
    
    activa = request.args.get("activa")

    canchas = listar_canchas(deporte_id, nombre, techada, activa)
    
    if not canchas:
        return '', 204

    return jsonify(canchas)

@canchas_bp.route('/canchas/<id_cancha>', methods=['GET'])
def get_canchas_id(id_cancha):
    id_cancha = int(id_cancha) if id_cancha else None
    cancha = buscar_cancha_por_id(id_cancha)

    if not cancha:
        return jsonify({"error": f"La cancha no fue encontrada, ya que no existe una cancha con id '{id_cancha}'."}), 404
    return jsonify(cancha), 200

@canchas_bp.route('/canchas/<id_cancha>', methods=['PATCH'])
def patch_canchas_id(id_cancha):
    body = request.get_json(silent=True)

    try:
        cancha = modificar_parcialmente_cancha(id_cancha, body)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": str(e)}), 404
    
    if not cancha:
        return '', 204

    return jsonify(cancha), 200

@canchas_bp.route('/canchas', methods=['POST'])
def post_cancha():
    body = request.get_json(silent=True)

    try:
        cancha = crear_cancha(body)
        return jsonify(cancha), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@canchas_bp.route('/canchas/<id_cancha>', methods=['DELETE'])
def delete_cancha(id_cancha):
    try:
        eliminar_cancha_por_id(id_cancha)
        return '', 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except KeyError as e:
        return jsonify({"error": str(e)}), 404

@canchas_bp.route('/canchas/disponibles', methods=['GET'])
def get_canchas_disponibles():
    fecha_str = request.args.get("fecha")

    hora_inicio_str = request.args.get("hora_inicio")
    hora_fin_str = request.args.get("hora_fin")

    deporte_id = request.args.get("deporte_id")
    techada = request.args.get("techada")

    try:
        canchas = listar_canchas_disponibles(fecha_str, hora_inicio_str, hora_fin_str, deporte_id, techada)
        return jsonify(canchas), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


