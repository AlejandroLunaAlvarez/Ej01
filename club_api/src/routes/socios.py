from flask import Blueprint, jsonify, request

from ..services.socios import (
    listar_socios_service, 
    crear_socio_service,
    encontrar_socio_por_id,
    actualizar_socio_service
    )

from ..services.paginador import paginar_lista  # Importa la función de paginación

socios_bp = Blueprint('socios', __name__)

@socios_bp.route('/socios', methods=['GET'])
def get_socios():
    nombre = request.args.get("nombre")
    activo = request.args.get("activo")

    if activo is not None:
        try:
            activo = int(activo)
            if activo not in [0, 1]:
                return jsonify({"error": "activo debe ser 0 o 1"}), 400
        except ValueError:
            return jsonify({"error": "activo debe ser un número entero"}), 400
    try:
        socios = listar_socios_service(nombre = nombre, activo = activo)
        socios_paginados = paginar_lista(socios)
        return jsonify({"socios": socios_paginados}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@socios_bp.route('/socios', methods=['POST'])
def crear_socio():
    datos = request.get_json(silent=True)

    if datos is None:
        return jsonify({"error": "El cuerpo de la solicitud debe ser JSON"}), 400

    try:
        socio = crear_socio_service(datos)
        return jsonify(socio), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@socios_bp.route('/socios/<int:id>', methods=['GET'])
def get_socio_por_id(id):
    try:
        socio = encontrar_socio_por_id(id)
        socio_encontrado = next((s for s in socio if s['id'] == id), None)
        if socio_encontrado is None:
            return jsonify({"error": "Socio no encontrado"}), 404
        return jsonify(socio_encontrado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@socios_bp.route('/socios/<int:id>', methods=['PATCH'])
def modificar_socio(id):
    datos = request.get_json(silent=True)
    
    if datos is None:
        return jsonify({"error": "El cuerpo de la solicitud debe ser JSON"}), 400

    try:
        socio = encontrar_socio_por_id(id)
        socio_encontrado = next((s for s in socio if s['id'] == id), None)
        if socio_encontrado is None:
            return jsonify({"error": "Socio no encontrado"}), 404

        # Actualizar los campos del socio con los datos proporcionados
        socio_encontrado.update(datos)
        actualizar_socio_service(
            id,
            nombre=socio_encontrado.get('nombre'),
            apellido=socio_encontrado.get('apellido'),
            email=socio_encontrado.get('email'),
            activo=socio_encontrado.get('activo')
        )
        return jsonify(socio_encontrado), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400