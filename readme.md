# Visión General del Proyecto

Este proyecto consiste en dos microservicios diseñados para procesar archivos CSV que contienen coordenadas geográficas (latitud y longitud), obtener códigos postales utilizando una API externa y almacenar los datos en una base de datos SQLite. La arquitectura garantiza escalabilidad, un manejo adecuado de errores y utiliza Docker para la contenerización, facilitando así el despliegue.

## Visión General de la Arquitectura

El sistema se compone de los siguientes componentes clave:

1. **Servicio 1**: Un microservicio basado en Flask que procesa un archivo CSV que contiene valores de latitud y longitud. Este servicio inserta los datos limpiados en una base de datos SQLite.
2. **Servicio 2**: Un segundo microservicio basado en Flask que recupera estas coordenadas de la base de datos, realiza solicitudes a una API externa de códigos postales y actualiza las entradas con sus respectivos códigos postales.
3. **Base de Datos SQLite**: La base de datos almacena las coordenadas y códigos postales en un formato ligero adecuado para esta tarea.


## Diagrama de Arquitectura

```plaintext
        +------------------+
        |                  |
        |   Servicio 1     |
        | (Sube CSV y DB)  |
        |                  |
        +--------+---------+
                 |
                 | CSV
                 |
        +--------v---------+
        |                  |
        |   SQLite DB      |
        |                  |
        +--------+---------+
                 |
                 |
        +--------v---------+
        |                  |
        |   Servicio 2     |
        | (Obtiene Cód.    |
        |  Postales)       |
        |                  |
        +------------------+
