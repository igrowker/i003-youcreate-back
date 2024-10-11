# **YouCreate**
================

## Descripción del Proyecto
---------------------------

YouCreate es un proyecto de aplicación web diseñado para permitir a los usuarios crear y gestionar contenido de manera fácil y segura.


## Requisitos Previos
----------------------

* Python 3.x
* Dependencias especificadas en `requirements.txt`
* Base de datos PostgreSQL

## Instalación
--------------

1. Clona el repositorio: `git clone https://github.com/[usuario]/YouCreate.git`
2. Cambia al directorio del proyecto: `cd YouCreate`
3. Instala las dependencias: `pip install -r requirements.txt`
4. Configura la base de datos: `python manage.py migrate`


## Ejecución local
-------------

1. Ejecuta el servidor de desarrollo: `python manage.py runserver`
2. Accede a la aplicación en `http://localhost:8000`


## Estructura del Proyecto
---------------------------

* `site_app`: Aplicación principal del proyecto
* `proyecto`: Configuración del proyecto
* `settings.py`: Archivo de configuración del proyecto
* `requirements.txt`: Dependencias del proyecto
* `Usuario`: Aplicación para la gestión de usuarios
* `Ingreso`: Aplicación para el ingreso de ingresos
* `ObligacionFiscal`: Aplicación para la generación de obligaciones fiscales
* `Colaborador`: Aplicación para la gestión de colaboradores del usuario
* `PagoColaborador`: Aplicación para la gestión de pagos a colaboradores/campañas
* `ActionLog`: Aplicación para la gestión de registros de acciones criticas del usuario

## Funcionalidades
------------------

* Autenticación y autorización de usuarios
* Gestión de contenido
* Integración con Google para el inicio de sesión

## Contribución
--------------

Si deseas contribuir al proyecto, por favor sigue los siguientes pasos:

1. Crea una rama para tu característica o corrección de bug
2. Realiza los cambios necesarios
3. Crea un pull request para revisar tus cambios

## Licencia
------------
