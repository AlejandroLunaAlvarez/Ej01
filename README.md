## Integrantes

- Alejandro Luna
- Ignacio Arancibia
- Fabrizio Amado
- Lautaro Quintana
- Kiara Ventura

## Tecnologías y versiones

- Python 3.13
- Flask 3.1.3
- MySQL 8
- SQLAlchemy 2.0.54
- mysql-connector-python 26.7.0
- python-dotenv 1.2.3

Las dependencias de Python se encuentran especificadas en requirements.txt.

## Instalación

Clonar el repositorio:

git clone https://github.com/AlejandroLunaAlvarez/Ej01.git
cd cd ~/Ej01

Crear y activar un entorno virtual:

python3 -m venv venv
source venv/bin/activate

Instalar las dependencias:

pip install -r requirements.txt

## Configuración

### 1. Variables de entorno
Copiar .ev.example a un archivo .env y configurar los siguientes valores:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=CLUB
```
de acuerdo a como tengas configurado MySQL

### 2. Base de datos con MySQL local
Con MySQL 8 corriendo localmente y las variables de entorno configuradas correctamente:

1. Cargar el esquema con los deportes integrados

```
mysql -u "nombre_cargado_en_.env" -p < init_db.sql
```
Esto creara la base de datos llamada CLUB con los deportes precargados.

2. Cargar los datos de prueba ejecutando el siguiente comando:

```
mysql -u "nombre_cargado_en_.env" -p CLUB < init_datos.sql
```

Antes de ejecutar la aplicación, verificar que:

MySQL esté iniciado.
La base de datos CLUB exista.
El usuario utilizado tenga permisos sobre la base de datos.
Las credenciales utilizadas por la aplicación sean correctas.

## Ejecución

Con el entorno virtual activado, ejecutar desde la raíz del proyecto el comando:

```
python -m club_api.app
```

La API quedará disponible en:

http://127.0.0.1:5000

## Deportes

En este apartado se podran ver los deportes indexados en la base de datos.

### Endpoints

- Metodo: GET

-Endpoint:
  GET: /deportes

-Descripcion
  GET: Consulta todos los deportes indexados 

## Bloqueos por mantenimiento

Como extensión opcional se implementó la gestión de bloqueos temporales de canchas por motivos de mantenimiento.

### Endpoints

- Metodos : POST, GET y DELETE. 

- Endpoint: 
    POST y GET: /bloqueos
    DELETE: /bloqueos/{id}
    
- Descripción: 
    POST: Crea el bloqueo de una cancha
    GET: Consulta los bloqueos existentes
    DELETE: Elimina un bloqueo

### Códigos de respuesta

- 201: bloqueo creado correctamente.

- 200: consulta o eliminación realizada correctamente.

- 400: datos de entrada inválidos.

- 404: bloqueo inexistente.

### Reglas

- El bloqueo debe corresponder a una cancha existente.
- La fecha debe ser válida y el inicio debe ser futuro.
- Los horarios deben estar entre las `08:00` y las `23:00`.
- Las horas deben ser exactas, sin minutos distintos de `00`.
- `hora_fin` debe ser posterior a `hora_inicio`.
- Un bloqueo puede durar más de 3 horas.
- No se permiten bloqueos superpuestos para una misma cancha.
- No se permite crear un bloqueo que se superponga con una reserva **confirmada**.
- Las reservas **finalizadas o canceladas** no impiden crear un bloqueo.
- El motivo es obligatorio y no puede estar vacío.
- No se permiten campos adicionales en la solicitud.

### Ejemplo de creación

```http
POST /bloqueos
Content-Type: application/json
```

```json
{
  "id_cancha": 1,
  "fecha": "2026-11-15",
  "hora_inicio": "10:00:00",
  "hora_fin": "12:00:00",
  "motivo": "Mantenimiento"
}
```

Respuesta exitosa:

```json
{
  "id": 1,
  "id_cancha": 1,
  "fecha": "2026-11-15",
  "hora_inicio": "10:00:00",
  "hora_fin": "12:00:00",
  "motivo": "Mantenimiento"
}
```

### Consulta

Se pueden consultar todos los bloqueos o aplicar filtros por cancha y fecha:

```http
GET /bloqueos
GET /bloqueos?id_cancha=1
GET /bloqueos?fecha=2026-11-15
GET /bloqueos?id_cancha=1&fecha=2026-11-15
```

El listado admite paginación mediante `_limit` y `_offset`.

### Eliminación

```http
DELETE /bloqueos/1
```

Si el bloqueo existe, se elimina correctamente. Si no existe, la API devuelve `404`.

### Supuestos

- Los bloqueos representan períodos de mantenimiento de una cancha.
- La eliminación de un bloqueo libera nuevamente ese intervalo.
- Los bloqueos no modifican ni eliminan reservas existentes.
