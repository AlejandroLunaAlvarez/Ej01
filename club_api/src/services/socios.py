from ..repositories import socios

def listar_socios_service(nombre=None, activo=None):
    return socios.buscar_socios(nombre, activo)

def crear_socio_service(data):
    if "nombre" not in data or "apellido" not in data or "email" not in data:
        raise ValueError("Faltan campos obligatorios: nombre, apellido, email")

    if "email" in data and "@" not in data["email"]:
        raise ValueError("El email proporcionado no es válido")

    email = data["email"].strip().lower()

    email_existente = socios.buscar_email_existente(email=data["email"])
    if email_existente:
        raise ValueError("Ya existe un socio con el email proporcionado")

    nuevo_id = socios.crear_socio(
        data["nombre"],
        data["apellido"],
        email
    )

    return {
        "id": nuevo_id,
        "activo": 1,  
        "nombre": data["nombre"],
        "apellido": data["apellido"],
        "email": email
    }
def encontrar_socio_por_id(id_socio):
    socio = socios.buscar_socio_por_id(id_socio)
    if not socio:
        raise ValueError("Socio no encontrado")
    return socio

def actualizar_socio_service(id, nombre=None, apellido=None, email=None, activo=None):
    if email is not None and "@" not in email:
        raise ValueError("El email proporcionado no es válido")

    if email is not None:
        email_existente = socios.buscar_email_existente(email=email)
        if email_existente and email_existente[0]['id'] != id:
            raise ValueError("Ya existe un socio con el email proporcionado")

    socios.actualizar_socio(id, nombre, apellido, email, activo)