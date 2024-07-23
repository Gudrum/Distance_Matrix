# Proyecto Vecino mas Cercano

Este proyecto es una aplicación web que utiliza el algoritmo del vecino más cercano para calcular la ruta óptima entre ciudades en Ecuador. La aplicación muestra las distancias y tiempos estimados entre las ciudades seleccionadas y representa la ruta en un mapa utilizando la API de Google Maps.

## Contenidos

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Funcionamiento del Algoritmo del Vecino Más Cercano](#funcionamiento-del-algoritmo-del-vecino-más-cercano)
- [Uso](#uso)
- [Problemas Conocidos](#problemas-conocidos)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

## Descripción

La aplicación permite a los usuarios seleccionar varias ciudades de Ecuador y calcular la ruta óptima que conecta todas las ciudades seleccionadas utilizando el algoritmo del vecino más cercano. La ruta calculada y sus detalles se muestran en un mapa interactivo y en una lista de resultados.

## Requisitos

- Python 3.x
- Flask
- Google Maps API Key
- Paquetes adicionales listados en `requirements.txt`

## Instalación

1. Clonar el repositorio:

    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```

2. Crear y activar un entorno virtual:

    ```bash
    python -m venv env
    source env/bin/activate  # En Windows: env\Scripts\activate
    ```

3. Instalar las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Crear un archivo `.env` en el directorio raíz del proyecto y añadir tu clave de la API de Google Maps:

    ```env
    GOOGLE_MAPS_API_KEY=TU_API_KEY
    ```

## Ejecución

1. Iniciar la aplicación Flask:

    ```bash
    flask run
    ```

2. Abrir un navegador web y navegar a `http://127.0.0.1:5000`.

## Estructura del Proyecto

```plaintext
algoritmo-vecino-mas-cercano/
│
├── app.py                   # Archivo principal de la aplicación Flask
├── utils.py                 # Funciones utilitarias y lógica del algoritmo
├── templates/
│   └── index.html           # Plantilla HTML para la interfaz de usuario
├── static/
│   └── css/
│       └── style.css        # Estilos CSS para la interfaz de usuario
├── log_config.py            # Configuración del logging
├── requirements.txt         # Lista de dependencias
└── .env                     # Archivo para la clave de la API de Google Maps
```

## Funcionamiento del Algoritmo del Vecino Más Cercano

El algoritmo del vecino más cercano es una heurística para resolver el problema del viajante (TSP). La idea principal es comenzar en una ciudad de inicio, luego seleccionar iterativamente la ciudad más cercana que no haya sido visitada, y repetir este proceso hasta que todas las ciudades hayan sido visitadas.

### Detalles del Algoritmo

1. **Inicialización**: Comienza en una ciudad de inicio y marca todas las demás ciudades como no visitadas.
2. **Búsqueda de Vecino Más Cercano**:
    - Para la ciudad actual, encuentra la ciudad no visitada más cercana.
    - Añade esta ciudad a la ruta y márcala como visitada.
3. **Repetición**: Repite el proceso anterior hasta que todas las ciudades hayan sido visitadas.
4. **Retorno**: Devuelve a la ciudad de inicio (opcional, dependiendo del problema).

### Implementación en `utils.py`

```python
import googlemaps
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def nearest_neighbor_algorithm(api_key, cities):
    gmaps = googlemaps.Client(key=api_key)
    unvisited = cities[1:]
    path = [cities[0]]
    unavailable_cities = []

    logger.info(f"Iniciando algoritmo del vecino más cercano con las ciudades: {cities}")

    while unvisited:
        current = path[-1]
        next_city = None
        min_distance = float('inf')

        for city in unvisited:
            try:
                result = gmaps.distance_matrix(current, city)['rows'][0]['elements'][0]
                if 'distance' in result:
                    distance = result['distance']['value']
                    if distance < min_distance:
                        min_distance = distance
                        next_city = city
                else:
                    unavailable_cities.append(city)
                    logger.warning(f"No se encontró información de distancia para {city}")
            except KeyError:
                unavailable_cities.append(city)
                logger.warning(f"No se encontró información de distancia para {city}")

        if next_city:
            path.append(next_city)
            unvisited.remove(next_city)
            logger.info(f"Añadida {next_city} a la ruta")
        else:
            break

    logger.info(f"Ruta final calculada: {path}")
    return path, unavailable_cities

def calculate_total_distance_and_time(api_key, path):
    gmaps = googlemaps.Client(key=api_key)
    total_distance = 0
    total_time = 0

    logger.info(f"Calculando distancia y tiempo total para la ruta: {path}")

    for i in range(len(path) - 1):
        result = gmaps.distance_matrix(path[i], path[i+1])['rows'][0]['elements'][0]
        distance = result['distance']['value'] / 1000  # Convert to km
        time = result['duration']['value'] / 3600  # Convert to hours
        total_distance += distance
        total_time += time
        logger.info(f"De {path[i]} a {path[i+1]}: {distance:.2f} km, {time:.2f} horas")

    logger.info(f"Distancia total: {total_distance:.2f} km, Tiempo total: {total_time:.2f} horas")
    return total_distance, total_time
```

## Uso

1. **Seleccionar Ciudades**: En la interfaz de usuario, seleccione las ciudades que desea visitar marcando las casillas de verificación correspondientes.
2. **Calcular Ruta**: Haga clic en el botón "Calcular Ruta".
3. **Ver Resultados**: La ruta óptima se mostrará en el mapa junto con la distancia total y el tiempo estimado de viaje.

## Problemas Conocidos

- Algunas rutas pueden no estar disponibles en la API de Google Maps, lo que resulta en un mensaje de error o en ciudades no disponibles.
- La precisión de la ruta puede verse afectada por la disponibilidad de datos de tráfico y rutas de la API de Google Maps.

## Contribuciones

Las contribuciones son bienvenidas. Para contribuir, por favor siga estos pasos:

1. Haga un fork del repositorio.
2. Cree una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realice sus cambios y haga commit (`git commit -am 'Añadir nueva característica'`).
4. Haga push a la rama (`git push origin feature/nueva-caracteristica`).
5. Cree un nuevo Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Vea el archivo `LICENSE` para más detalles.