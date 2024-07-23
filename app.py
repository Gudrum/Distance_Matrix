from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from log_config import setup_logging
import os
import utils

# Configurar logging
logger = setup_logging()

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

CIUDADES_ECUADOR = [
    "Quito", "Guayaquil", "Cuenca", "Santo Domingo", "Machala",
    "Durán", "Manta", "Portoviejo", "Loja", "Ambato",
    "Riobamba", "Esmeraldas", "Quevedo", "Milagro", "Ibarra",
    "Latacunga", "Babahoyo", "Tulcán", "Azogues", "Otavalo",
    "Santa Elena", "Nueva Loja", "Salinas", "Chone", "Cayambe",
    "Playas", "Zamora", "Macas", "Tena", "Puyo",
    "Puerto Francisco de Orellana", "Yantzaza", "La Troncal", "Jipijapa", "Pedernales",
    "Montecristi", "Pedro Carbo", "Santa Rosa", "El Carmen", "Samborondón"
]

@app.route('/')
def index():
    logger.info("Página principal cargada")
    return render_template('index.html', 
                           cities=CIUDADES_ECUADOR, 
                           google_maps_api_key=os.getenv('GOOGLE_MAPS_API_KEY'))

@app.route('/calculate', methods=['POST'])
def calculate():
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    cities = request.json['cities']

    logger.info(f"Cálculo de ruta solicitado para las ciudades: {cities}")

    if len(cities) < 2:
        logger.warning("Se intentó calcular una ruta con menos de dos ciudades")
        return jsonify({'error': 'Se necesitan al menos dos ciudades'}), 400

    try:
        path, unavailable_cities = utils.nearest_neighbor_algorithm(api_key, cities)
        total_distance, total_time = utils.calculate_total_distance_and_time(api_key, path)

        logger.info(f"Ruta calculada exitosamente: {path}")
        logger.info(f"Distancia total: {total_distance:.2f} km, Tiempo total: {total_time:.2f} horas")

        return jsonify({
            'path': path,
            'total_distance': f"{total_distance:.2f} km",
            'total_time': f"{total_time:.2f} horas",
            'unavailable_cities': unavailable_cities
        })

    except Exception as e:
        logger.error(f"Error al calcular la ruta: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
