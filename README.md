# globant_ch
Aquí tienes el archivo README.md en formato Markdown:

---

# Globant Coding Challenge

Este proyecto es un proof-of-concept (PoC) para un proyecto de migración de datos a gran escala en Globant. El reto se divide en dos desafíos principales:

## Desafío #1 – Migración de Datos y Servicio API

- **Migración de Datos:**
  - Migrar datos históricos desde archivos CSV a una nueva base de datos SQL.
  - Archivos CSV involucrados:
    - **hired_employees.csv:** Registros de contratación de empleados.
    - **departments.csv:** Información de los departamentos.
    - **jobs.csv:** Información de los cargos o puestos.

- **Servicio REST API:**
  - Recibir transacciones nuevas, permitiendo inserciones en lote (entre 1 y 1000 filas por solicitud).
  - Validar cada transacción conforme a las reglas definidas en el diccionario de datos.
  - Registrar las transacciones que no cumplan con las reglas (todos los campos son obligatorios).
  - Soportar la inserción de datos para múltiples tablas en una única solicitud.

- **Funciones de Respaldo y Restauración:**
  - Realizar respaldos de cada tabla en el sistema de archivos en formato AVRO.
  - Restaurar una tabla a partir de su respaldo.

- **Consideraciones Adicionales:**
  - Publicar el código en GitHub, con actualizaciones frecuentes para evidenciar el proceso de desarrollo.
  - Opcionalmente: crear un Dockerfile para el despliegue, considerar aspectos de seguridad en el servicio API e integrar herramientas cloud.

## Esquema de la Base de Datos

La base de datos SQL se estructura en tres tablas principales:

- **departments:** Contiene el identificador y el nombre del departamento.
- **jobs:** Contiene el identificador y el nombre del cargo o puesto.
- **hired_employees:** Registra los datos de contratación de los empleados, incluyendo fecha y hora de contratación, y referencias (foreign keys) a `departments` y `jobs`.

Consulte el script SQL incluido para ver los detalles exactos del esquema.

## Desafío #2 – Exploración de Datos y Endpoints de Métricas

- **Endpoints de Métricas:**
  - **Métricas Trimestrales de Contratación:** Número de empleados contratados en 2021 para cada cargo y departamento, dividido por trimestre. El resultado se ordena alfabéticamente por departamento y cargo.
  - **Desempeño de Contratación por Departamento:** Listado de departamentos que contrataron más empleados que la media de 2021, mostrando el id, el nombre del departamento y el total de contrataciones, ordenado de mayor a menor según el número de contrataciones.

- **Opcional:** Generar reportes visuales para cada métrica utilizando la herramienta de visualización de su preferencia.

## Herramientas y Tecnologías

- **Lenguajes de Programación:** Python, Java, Go o Scala.
- **Base de Datos:** Sistema SQL (ejemplo: MySQL, PostgreSQL, etc.).
- **Formatos de Datos:** CSV para entrada de datos; AVRO para los respaldos.
- **Despliegue:** Contenerización con Docker.
- **Control de Versiones:** Git (repositorio en GitHub).

## Instalación y Ejecución del Proyecto

1. **Clonar el Repositorio:**
   ```bash
   git clone https://github.com/tuusuario/globant-challenge.git
   cd globant-challenge
   ```

2. **Construir la Imagen Docker (si se usa Docker):**
   ```bash
   docker build -t globant-challenge .
   ```

3. **Ejecutar el Contenedor:**
   ```bash
   docker run -p 8000:8000 globant-challenge
   ```

4. **Uso del API:**
   - installdb: se ejecuta manualmente
   - Realizar respaldo: `POST /backup`

   - DEpartments  Get all: `GET /departments`

   - Departments Get by id : `GET /departments/{id}`

   - Departments create: `POST /departments`

   - Departments update: `PUT /departments/{id}`

   - Departments delete: `DELETE /departments/{id}`
   
   - Jobs Get all: `GET /jobs`

   - Jobs Get by id : `GET /jobs/{id}`

   - Jobs create: `POST /jobs`

   - Jobs update: `PUT /jobs/{id}`

   - Jobs delete: `DELETE /jobs/{id}`

   - Employees  Get all: `GET /employees`

   - Employees Get by id : `GET /employees/{id}`

   - Employees create: `POST /employees`

   - Employees update: `PUT /employees/{id}`

   - Employees delete: `DELETE /employees/{id}`
   
   - Reportes: `GET /hiring-report`

   - Reportes: `GET /top-hiring-departments`

## Consideraciones de Seguridad

- Implementar mecanismos de autenticación y autorización en los endpoints del API.
- Validar rigurosamente los datos para evitar la inserción de transacciones no conformes.
- Registrar todas las transacciones que no cumplan con las reglas para fines de auditoría.

## Flujo de Trabajo con Git

- Utilice Git para el control de versiones siguiendo una estrategia de ramas para gestionar nuevas características y correcciones.
- Realice commits frecuentes con mensajes claros y descriptivos para documentar el progreso del desarrollo.

## Mejoras Futuras

- Ampliar la integración de fuentes de datos y mecanismos de validación.
- Mejorar las funciones de respaldo y restauración con mayor granularidad.
- Integrar herramientas avanzadas de análisis y visualización para reportes completos.

## Licencia

Especifique los términos de la licencia bajo la cual se distribuye este proyecto.

---

Este archivo README.md proporciona una visión general del proyecto, instrucciones para la instalación y despliegue, y detalla tanto los desafíos abordados como las tecnologías utilizadas. ¿Necesitas alguna modificación adicional o información complementaria?
