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
Copiar .env.example a un archivo .env y configurar los siguientes valores:

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


## Reservas de canchas

Gestión de reservas de canchas, consulta de disponibilidad, calculo de importe y actualización de estados.

### Endpoints

- Metodos : POST, GET y PUT.

- Endpoint: 
    POST y GET: /reservas
    GET y PUT: /reservas/{id}
    
- Descripción: 
    POST: Crea una nueva reserva
  
    GET: Consulta las reservas existentes o por ID
  
    PUT: Actualiza el estado de una reserva

### Códigos de respuesta

- 201: reserva creada correctamente.

- 200: consulta o actualización realizada correctamente.

- 400: datos de entrada inválidos, socio/cancha inactiva o duración incorrecta.

- 404: reserva inexistente.

- 409: superposición de horarios con otra reserva o bloqueo existente.

### Reglas

- La reserva debe corresponder a un socio activo y una cancha habilitada.
- La `fecha_hora_inicio` debe ser anterior a `fecha_hora_fin`.
- La duración de la reserva debe ser de bloques enteros de 1, 2 o 3 horas.
- No se permiten reservas superpuestas para la misma cancha o el mismo socio.
- No se permite crear una reserva si la cancha posee un bloqueo por mantenimiento en ese horario.
- El importe se calcula automáticamente según la duración y el precio por hora de la cancha.

### Ejemplo de creación

```json
POST /reservas
Content-Type: application/json

{
  "id_socio": 1,
  "id_cancha": 2,
  "fecha_hora_inicio": "2026-11-10T14:00:00-03:00",
  "fecha_hora_fin": "2026-11-10T15:00:00-03:00"
}
Respuesta exitosa:

{
  "id": 1,
  "id_socio": 1,
  "id_cancha": 2,
  "estado": "confirmada",
  "fecha_hora_inicio": "2026-11-10T14:00:00-03:00",
  "fecha_hora_fin": "2026-11-10T15:00:00-03:00",
  "importe": 7500.0
}
```
### Consulta

Se pueden consultar todas las reservas, obtener una por ID o aplicar filtros de búsqueda:

GET /reservas

Reserva por id de la tabla reservas:

GET /reservas/1

si se quiere ver todas las reservas con el id del socio o cancha correspondiente:

GET /reservas?id_cancha=1

GET /reservas?id_socio=2

filtrado por fecha:

GET /reservas?fecha=2026-11-10

Modificación de estado por el id tabla reservas:
PUT /reservas/1/estado
Content-Type: application/json
```json
{
  "estado": "cancelada"
}
```
Aplica lo mismo pero con finalizada:
```json
{
  "estado": "finalizada"
}
```

Si la reserva existe, se actualiza el estado correctamente. Si no existe, la API devuelve 404



### Supuestos
-Las reservas en estado cancelada liberan el horario para nuevas reservas o bloqueos.

-La tarifa final de la reserva se calcula dinámicamente multiplicando las horas por el precio por hora de la cancha.




## Socios

Aquí se podrá consultar toda la info de socios

### Modelo 

|--------------|------------|--------------------------------------------------|
| Campo        | Tipo       | Descipción  				                             |
|--------------|------------|--------------------------------------------------|
|id	           | int        | Identificador único			                         |
|--------------|------------|--------------------------------------------------|
|nombre	       | string     | Nombre del Socio. No puede ser vacío	           |
|--------------|------------|--------------------------------------------------|
|apellido      | string     | Apellido del socio.			                         |
|--------------|------------|--------------------------------------------------|
|email	       | string	    | No puede estar duplicado. Se guarda sin espacios |
|	             |            | en los extremos y en minúsculas.		             |
|--------------|------------|--------------------------------------------------|
|activo	       | int	      | Estado del socio. Valor predeterminado = 1       |
|--------------|------------|--------------------------------------------------|

### Métodos

- GET /socios: Lista los socios paginados.
	
   Parámetros opcionales:
   - nombre: filtra por nombre.
   - activo: filtra por estado de activo.

   Respuesta (200):
   {
    "socios":{
       "_links": { Info del Paginador },
       "data":[{
		"activo": 1,
		"apellido": "Pérez",
		"email": "lucia.perez@email.com",
		"id": 1,
		"nombre": "Lucía"		
	      }]
   }}

- POST /socios: Registra un nuevo socio.
   
   Body:
   {
    "nombre": "Julian",
    "email": "julian@email.com"
   }

   Reglas:
   - "nombre" e "email"  son obligatorios.
   - "email" debe tener un formato válido, se guardará en minúsculas y
     sin espacios a los extremos.
   - El servidor asigna automáticamente "activo" = 1.
   - Si el correo existe se devuelve el error 409.
 
   Respuesta (201):
   {
     "activo": 1,
     "apellido": "Quiroga",
     "email": "facundoquiroga@email.com",
     "id": 1,
     "nombre": "Facundo"
   }

   Errores:
   400/422: Datos faltantes o inválidos.
   409: Email duplicado.

- GET /socios/{id}: Busca a un socio por su id.

   Respuesta (200): Devuelve el socio.
 
   Error (404): No existe ningún socio con ese id.

- PATCH /socios/{id}: Actualiza parcialmente "nombre", "email y/o "apellido".

   Body (todos los campos son opcionales):
   { 
     "activo": 0
   }

   Reglas:
   - Los campos omitidos conservan su valor.
   - Se aplican las mismas validaciones que en el POST
     (nombre vacío no válido, email válido y normalizado).
   - El nuevo correo debe ser único.

   Respuesta (201): Devuelve la información actualizada del socio.

   Errores:
   400/422: Datos inválidos.
   404: El socio no existe.
   409: El email está duplicado.
   
## Paginador

Esta es una función usada para paginar la información recibida de cualquier método.

### Modelo

  "_links": {
    "_first": "http//:127.0.0.1:5000/socios?_limit=10&_offset=0", ## Link del primer resultado
    "_last": "http//:127.0.0.1:5000/socios?_limit=10&_offset=30", ## Link del último resultado
    "_limit": 10, ## Límite de resultados por página, 10 por defecto
    "_next": null, ## Link de la siguiente página, null por defecto
    "_offset": 0, ## Cuantos resultados se salta, 0 por defecto
    "_prev": null, ## Link de la página anterior, null por defecto
    "pagina": 1, ## Página actual, 1 por defecto
    "total_items": (total de resultados)
  }

  Parámetros opcionales:
  - _limit: Es el límite de resultados por página.
  - _offset: Cuantos resultados se saltean antes del primero en pantalla.


## Canchas

Se podrán visualizar el listado de canchas, consultar por una cancha en específico, crear una cancha nueva, actualizar parcialmente una existente y consultar la disponibilidad de canchas.

### Endpoints

- Métodos: GET, POST, PATCH Y DELETE.

- Endpoint: GET y POST: /canchas, GET, PATCH y DELETE: /canchas/{id} y GET: canchas/disponibles.

- Descripción: GET: Consulta todas las canchas existentes o las canchas disponibles o una cancha por id.

  POST: Crea una nueva cancha.
  
  PATCH: Actualiza parcialmente una cancha existente.

  DELETE: Borra una cancha por id.


### Códigos de respuesta

- 200: Consulta o actualización realizada con éxito.

- 201: Creación realizada correctamente.

- 204: Cancha eliminada con éxito, se devuelve una respuesta vacía.

- 400: Datos del cuerpo de la petición incorrectos o inválidos.

- 404: Cancha inexistente.

- 409: La cancha que se quiere eliminar tiene una o varias reservas y/o uno o varios bloqueos.

### Reglas

- El nombre de la cancha no puede quedar vacío después de quitar espacios en sus extremos.

- El deporte que se le asigne a la cancha debe existir.

- El precio debe ser un número entero positivo.

- El deporte asociado no se puede modificar una vez creada la cancha.

- Cambiar el precio no alterará los importes de reservas existentes.

- No se permite eliminar canchas con reservas o bloqueos asignados.

- Al consultar disponibilidad:
  - La `hora_inicio` debe ser anterior a la `hora_final`.
  - El intervalo buscado debe durar máximo 3 horas y no puede atravesar la medianoche ni    estar fuera del horario de atención del club.


### Ejemplo de creación

```json
POST /canchas
Content-Type: application/json

{
  "nombre": "Cancha exterior 1",
  "deporte_id": 1,
  "precio_hora": 1500,
  "techada": false,
  "activa": true
}
Respuesta exitosa:

{
  "id": 1,
  "nombre": "Cancha exterior 1",
  "deporte_id": 1,
  "precio_hora": 1500,
  "techada": false,
  "activa": true
}
```

### Consulta

Se pueden consultar todas las canchas, obtener una por ID o aplicar filtros de búsqueda:

GET /canchas

Cancha por id de la tabla canchas:

GET /canchas/1

Para ver todas las canchas con el id del deporte, con el nombre, si es techada o no o si está activa (también pueden aplicarse a la vez concatenando cada una con &):

GET /canchas?deporte_id=1

GET /canchas?nombre=Cancha exterior 1

GET /canchas?techada=true

GET /canchas?activa=false

Para consultar las canchas disponibles, se pueden aplicar los siguientes filtros:
 - `fecha`, `hora_inicio` y `hora_fin` (obligatorios).
 - `deporte_id` y `techada` (opcionales)

GET /canchas/disponibles?fecha=2026-10-24&hora_inicio=18:00:00&hora_fin=20:00:00

Modificación parcial de la cancha por el id:

PATCH /canchas/1
```json
Content-Type: application/json
{
  "nombre": "Cancha Interior 1",
  "precio_hora": 1000,
  "techada": true,
  "activa": false
}

Si la cancha existe, se actualizan los campos correctamente. Caso contrario, la API devuelve 404

Para eliminar una cancha:

DELETE /canchas/1

Si la cancha del id especificado no tiene ninguna reserva o bloqueo, esta se elimina con éxito y se devuelve un json vacío.
