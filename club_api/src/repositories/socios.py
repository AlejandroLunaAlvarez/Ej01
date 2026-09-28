from ..db import ejecutar_consulta, ejecutar_mutacion

def buscar_socios(nombre=None, activo=None):
    sql = """
        SELECT *
        FROM socios 
    """

    condiciones = []
    datos = {}

    if nombre is not None:
        condiciones.append("nombre LIKE :nombre")
        datos["nombre"] = nombre
    if activo is not None:
        condiciones.append("activo = :activo")
        datos["activo"] = activo
    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones)
    sql += " ORDER BY id ASC"
    return ejecutar_consulta(sql, datos)

def crear_socio(nombre, apellido, email):
    sql = """
        INSERT INTO socios (
            nombre,
            activo,
            apellido,
            email
        )
        VALUES (
            :nombre,
            1,
            :apellido,
            :email
        )
    """

    datos = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email
    }

    return ejecutar_mutacion(sql, datos)

def buscar_email_existente(email):
    sql = """
        SELECT *
        FROM socios
        WHERE email = :email
    """
    datos = {"email": email}
    return ejecutar_consulta(sql, datos)

def buscar_socio_por_id(id_socio):
    sql = """
        SELECT *
        FROM socios
        WHERE id = :id_socio
    """
    datos = {"id_socio": id_socio}
    return ejecutar_consulta(sql, datos)

def actualizar_socio(id, nombre=None, apellido=None, email=None, activo=None):
    condiciones = []
    datos = {"id": id}

    if nombre is not None:
        condiciones.append("nombre = :nombre")
        datos["nombre"] = nombre
    if apellido is not None:
        condiciones.append("apellido = :apellido")
        datos["apellido"] = apellido
    if email is not None:
        condiciones.append("email = :email")
        datos["email"] = email
    if activo is not None:
        condiciones.append("activo = :activo")
        datos["activo"] = activo

    if not condiciones:
        raise ValueError("No se proporcionaron campos para actualizar")

    sql = f"""
        UPDATE socios
        SET {', '.join(condiciones)}
        WHERE id = :id
    """

    ejecutar_mutacion(sql, datos)