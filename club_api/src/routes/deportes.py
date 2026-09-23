from flask import Blueprint, jsonify, request
from ..services import deportes  # Importa el módulo

deportes_bp = Blueprint('deportes', __name__)

@deportes_bp.route('/deportes', methods=['GET'])
def get_deportes():
    # Llamamos a la función a través del módulo 'deportes.'
    lista_deportes = deportes.listar_deportes()

    # Validamos 'lista_deportes' en lugar de 'alumnos'
    if not lista_deportes:
        return '', 204

    return jsonify(lista_deportes)