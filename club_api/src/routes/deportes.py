from flask import Blueprint, jsonify, request
from ..services import deportes  # Importa el módulo
from ..services.paginador import paginar_lista  # Importa la función de paginación

deportes_bp = Blueprint('deportes', __name__)

@deportes_bp.route('/deportes', methods=['GET'])
def get_deportes():
    # Llamamos a la función a través del módulo 'deportes.'
    lista_deportes = deportes.listar_deportes()
    deportes_paginados = paginar_lista(lista_deportes)

    # Validamos 'lista_deportes' en lugar de 'alumnos'
    if not lista_deportes:
        return '', 204

    return jsonify(deportes_paginados)