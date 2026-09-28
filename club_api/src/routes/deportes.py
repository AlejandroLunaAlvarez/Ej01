from flask import Blueprint, jsonify, request
from ..services import deportes 

deportes_bp = Blueprint('deportes', __name__)

@deportes_bp.route('/deportes', methods=['GET'])
def get_deportes():
    
    lista_deportes = deportes.listar_deportes()

    if not lista_deportes:
        return '', 204

    return jsonify(lista_deportes)