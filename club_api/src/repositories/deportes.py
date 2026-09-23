from sqlalchemy import create_engine, text
from ..constants import DB_URL
from .. import db

motor = create_engine(DB_URL, pool_pre_ping=True)

def obtener_todos_los_deportes() -> list[dict]:
    sql = 'SELECT nombre FROM deportes'

    return db.ejecutar_consulta(sql)
