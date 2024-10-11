

# Documentación de la API
=====================================

## Índice

* [Usuario](#usuario)
* [Ingreso](#ingreso)
* [Colaborador](#colaborador)
* [PagoColaborador](#pagocolaborador)
* [ObligacionFiscal](#obligacionfiscal)
* [ActionLog](#actionlog)


## Usuario
### Rutas

* `POST /auth/signup/` - Crear una nueva cuenta de usuario
* `GET /auth/user/update/` - Actualizar información del usuario
* `GET /auth/user/account-data/` - Obtener datos de la cuenta del usuario
* `POST /auth/password/reset/` - Solicitar un restablecimiento de contraseña
* `POST /auth/password/reset/confirm/` - Confirmar un restablecimiento de contraseña
* `POST /auth/login/` - Iniciar sesión en el sistema
* `POST /auth/logout/` - Cerrar sesión del sistema
* ~~`GET /auth/user/` - Obtener detalles del usuario~~ (Endpoint desactualizado, usar **GET /auth/user/account-data/**)
* `POST /auth/password/change/` - Cambiar la contraseña del usuario
* `POST /auth/2fa-login/` - Iniciar sesión con autenticación de dos factores
* `POST /auth/2fa-verify/` - Verificar código de autenticación de dos factores

## Ingreso
### Rutas

* `GET /ingresos/<int:usuario_id>/` - Listar todos los ingresos de un usuario
* `GET /ingresos-totales/<int:usuario_id>/` - Obtener el total de ingresos de un usuario
* `GET /ingresos-de-un-mes/<int:usuario_id>/<int:mes>/<int:anio>/` - Obtener los ingresos de un usuario por mes y año
* `GET /ingresos-de-un-anio/<int:usuario_id>/<int:anio>/` - Obtener los ingresos de un usuario por año
* `GET /ingreso-total-en-un-mes/<int:usuario_id>/<int:mes>/<int:anio>/` - Obtener el total de ingresos de un usuario por mes y año
* `GET /ingreso-total-en-un-anio/<int:usuario_id>/<int:anio>/` - Obtener el total de ingresos de un usuario por año
* `POST /ingresos/` - Crear un nuevo ingreso

## Colaborador
### Rutas

* `GET /api/colaboradores/` - Listar todos los colaboradores
* `POST /api/colaboradores/` - Crear un nuevo colaborador
* `GET /api/colaboradores/{id}/` - Obtener un colaborador por ID
* `PUT /api/colaboradores/{id}/` - Actualizar un colaborador
* `DELETE /api/colaboradores/{id}/` - Eliminar un colaborador

## PagoColaborador
### Rutas

* `GET /api/pagos-colaboradores/` - Listar todos los pagos de colaboradores
* `POST /api/pagos-colaboradores/` - Crear un nuevo pago de colaborador
* `GET /api/pagos-colaboradores/{id}/` - Obtener un pago de colaborador por ID
* `PUT /api/pagos-colaboradores/{id}/` - Actualizar un pago de colaborador
* `DELETE /api/pagos-colaboradores/{id}/` - Eliminar un pago de colaborador

## ObligacionFiscal
### Rutas

* `GET /api/obligaciones-fiscales/` - Listar todas las obligaciones fiscales
* `POST /api/obligaciones-fiscales/` - Crear una nueva obligación fiscal
* `GET /api/obligaciones-fiscales/{id}/` - Obtener una obligación fiscal por ID
* `PUT /api/obligaciones-fiscales/{id}/` - Actualizar una obligación fiscal
* `DELETE /api/obligaciones-fiscales/{id}/` - Eliminar una obligación fiscal
* `POST /api/actualizacion-estados/{id}/` - Actualizar el estado de una obligación fiscal

## ActionLog
### Rutas

* `GET /api/action-logs/` - Listar todos los registros de acción
* `POST /api/action-logs/` - Crear un nuevo registro de acción
* `GET /api/action-logs/{id}/` - Obtener un registro de acción por ID
* `PUT /api/action-logs/{id}/` - Actualizar un registro de acción
* `DELETE /api/action-logs/{id}/` - Eliminar un registro de acción



# API Documentation
=====================================

## Index

* [Usuario](#usuario)
* [Ingreso](#ingreso)
* [Colaborador](#colaborador)
* [PagoColaborador](#pagocolaborador)
* [ObligacionFiscal](#obligacionfiscal)
* [ActionLog](#actionlog)

## Usuario
### Routes

* `POST /auth/signup/` - Create a new user account
* `GET /auth/user/update/` - Update user information
* `GET /auth/user/account-data/` - Get user account data
* `POST /auth/password/reset/` - Request a password reset
* `POST /auth/password/reset/confirm/` - Confirm a password reset
* `POST /auth/login/` - Login to the system
* `POST /auth/logout/` - Logout of the system
* ~~`GET /auth/user/` - Get user details~~ (Endpoint not ready for use, use **GET /auth/user/account-data/** instead)
* `POST /auth/password/change/` - Change user password
* `POST /auth/2fa-login/` - Login with two-factor authentication
* `POST /auth/2fa-verify/` - Verify two-factor authentication code

## Ingreso
### Routes

* `GET /ingresos/<int:usuario_id>/` - List all ingresos for a user
* `GET /ingresos-totales/<int:usuario_id>/` - Get total ingresos for a user
* `GET /ingresos-de-un-mes/<int:usuario_id>/<int:mes>/<int:anio>/` - Get ingresos for a user by month and year
* `GET /ingresos-de-un-anio/<int:usuario_id>/<int:anio>/` - Get ingresos for a user by year
* `GET /ingreso-total-en-un-mes/<int:usuario_id>/<int:mes>/<int:anio>/` - Get total ingresos for a user by month and year
* `GET /ingreso-total-en-un-anio/<int:usuario_id>/<int:anio>/` - Get total ingresos for a user by year
* `POST /ingresos/` - Create a new ingreso

## Colaborador
### Routes

* `GET /api/colaboradores/` - List all collaborators
* `POST /api/colaboradores/` - Create a new collaborator
* `GET /api/colaboradores/{id}/` - Get a collaborator by ID
* `PUT /api/colaboradores/{id}/` - Update a collaborator
* `DELETE /api/colaboradores/{id}/` - Delete a collaborator

## PagoColaborador
### Routes

* `GET /api/pagos-colaboradores/` - List all collaborator payments
* `POST /api/pagos-colaboradores/` - Create a new collaborator payment
* `GET /api/pagos-colaboradores/{id}/` - Get a collaborator payment by ID
* `PUT /api/pagos-colaboradores/{id}/` - Update a collaborator payment
* `DELETE /api/pagos-colaboradores/{id}/` - Delete a collaborator payment

## ObligacionFiscal
### Routes

* `GET /api/obligaciones-fiscales/` - List all fiscal obligations
* `POST /api/obligaciones-fiscales/` - Create a new fiscal obligation
* `GET /api/obligaciones-fiscales/{id}/` - Get a fiscal obligation by ID
* `PUT /api/obligaciones-fiscales/{id}/` - Update a fiscal obligation
* `DELETE /api/obligaciones-fiscales/{id}/` - Delete a fiscal obligation
* `POST /api/actualizacion-estados/{id}/` - Update the state of a fiscal obligation

## ActionLog
### Routes

* `GET /api/action-logs/` - List all action logs
* `POST /api/action-logs/` - Create a new action log
* `GET /api/action-logs/{id}/` - Get an action log by ID
* `PUT /api/action-logs/{id}/` - Update an action log
* `DELETE /api/action-logs/{id}/` - Delete an action log