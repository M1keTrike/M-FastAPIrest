# Proyecto FastAPI REST

Este proyecto utiliza FastAPI para construir una API REST. A continuación se describen los pasos para configurar el entorno virtual y ejecutar el proyecto.

## Requisitos

- **Python 3.8+**
- **Git**

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/M1keTrike/M-FastAPIrest.git
   cd M-FastAPIrest

Crea un entorno virtual. Asegúrate de estar en el directorio raíz del proyecto antes de ejecutar este comando:


python -m venv .venv
Activa el entorno virtual:

En Windows:


.venv\Scripts\activate

En macOS/Linux:

source .venv/bin/activate
Instala las dependencias:


pip install -r requirements.txt
Ejecución
Después de instalar las dependencias, puedes ejecutar el proyecto con el siguiente comando:


uvicorn main:app --reload
Esto iniciará el servidor en modo de recarga automática (ideal para desarrollo).

Notas
Si necesitas agregar nuevas dependencias, instálalas en el entorno virtual activo y luego guarda las dependencias en requirements.txt:


pip freeze > requirements.txt
Recuerda desactivar el entorno virtual cuando termines de trabajar con:



Este archivo `README.md` proporciona instrucciones detalladas para que los usuarios puedan clonar el repositorio, configurar el entorno virtual,