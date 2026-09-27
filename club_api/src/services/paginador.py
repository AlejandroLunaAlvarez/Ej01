from flask import request
from urllib.parse import urlencode
import math


def paginar_lista(lista, serializer=None):
    # Parámetros _limit y _offset (validados)
    _limit = request.args.get("_limit", 10, type=int)
    _offset = request.args.get("_offset", 0, type=int)

    # _limit: debe ser mayor a 1 y menor que 100
    if _limit <= 1 or _limit >= 100:
        _limit = 10

    # _offset: debe ser un entero mayor o igual a 0
    if _offset < 0:
        _offset = 0
        
    # Paginación de una lista normal
    total = len(lista)
    items = lista[_offset:_offset + _limit]

    if serializer:
        items = [serializer(item) for item in items]

    total_pages = math.ceil(total / _limit) if total else 0
    pagina_actual = (_offset // _limit) + 1

    def enlace(offset):
        params = {
            "_limit": _limit,
            "_offset": offset
        }
        return f"{request.base_url}?{urlencode(params)}"

    return {
        "data" : items,
        "_links": {
            "_limit": _limit,
            "_offset": _offset,
            "pagina": pagina_actual,
            "total_items": total,
            "_first": enlace(0) if total_pages > 0 else None,
            "_prev": enlace(max(0, _offset - _limit)) if pagina_actual > 1 else None,
            "_next": enlace(_offset + _limit)
            if pagina_actual < total_pages else None,
            "_last": enlace((total_pages - 1) * _limit)
            if total_pages > 0 else None
        }
    }