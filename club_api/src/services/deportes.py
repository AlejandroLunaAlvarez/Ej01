import logging
from ..repositories import deportes

logger = logging.getLogger(__name__)


def construir_deportes(deportes: dict) -> dict:
    """Deportes"""
    return {
        'nombre':   deportes['nombre']
    }

def listar_deportes() -> list[dict]:
    """Retorna todos los deportes."""
    return [construir_deportes(a) for a in deportes.obtener_todos_los_deportes()]