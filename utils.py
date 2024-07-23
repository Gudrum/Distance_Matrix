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
