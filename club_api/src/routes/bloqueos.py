from flask import Blueprint, jsonify, request

from ..services.bloqueos import (
    crear_bloqueo_service,
    listar_bloqueos_service,
    eliminar_bloqueo_service
)

bloqueos_bp = Blueprint('bloqueos', __name__)

@bloqueos_bp.route("/bloqueos", methods=["POST"])

def crear_bloqueo():
    datos = request.get_json(silent=True)

    if datos is None:
        return jsonify({"error": "El cuerpo de la solicitud debe ser JSON"}), 400

    try:
        bloqueo = crear_bloqueo_service(datos)
        return jsonify(bloqueo), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bloqueos_bp.route("/bloqueos", methods=["GET"])
def listar_bloqueos():
    id_cancha = request.args.get("id_cancha")
    fecha = request.args.get("fecha")

    if id_cancha is not None:
        try:
            id_cancha = int(id_cancha)
        except ValueError:
            return jsonify({
                "error": "id_cancha debe ser un número entero"
            }), 400

    try:
        bloqueos = listar_bloqueos_service(
            id_cancha=id_cancha,
            fecha=fecha
        )

        return jsonify({
            "bloqueos": bloqueos
        }), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 400

@bloqueos_bp.route("/bloqueos/<int:id>", methods=["DELETE"])
def eliminar_bloqueo(id):
    try:
        eliminar_bloqueo_service(id)

        return jsonify({
            "mensaje": "Bloqueo eliminado correctamente"
        }), 200

    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 404