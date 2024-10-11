import os
import json
import logging
from logging.handlers import SocketHandler

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.basicConfig(level=logging.INFO)
# Crear un logger
logger = logging.getLogger('logs-geotree')
logger.setLevel(logging.INFO)

# Configuración para enviar logs a Logstash (vía TCP)
logstash_host = 'logstash'
logstash_port = 50000

# Clase para formatear logs en JSON
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'message': record.getMessage(),
            'levelname': record.levelname,
            'asctime': self.formatTime(record, self.datefmt),
            'name': record.name,
        }
        return json.dumps(log_obj)

# Añadir un manejador para enviar logs a Logstash vía TCP
try:
    # Crear el handler de Logstash (vía TCP)
    logstash_handler = SocketHandler(logstash_host, logstash_port)
    
    # Usar el formateador JSON
    logstash_handler.setFormatter(JSONFormatter())

    # Añadir el handler al logger
    logger.addHandler(logstash_handler)
    
    logger.info("Logstash handler configurado correctamente")
except Exception as e:
    logger.error(f"Error configurando Logstash handler: {str(e)}")

# Función para crear los directorios de logs si no existen
def create_log_directory(log_folder):
    try:
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
    except Exception as e:
        logging.error(f"Error creando el directorio de logs: {str(e)}")
        raise

# Función para registrar los logs de drift
def log_drift(feature, predicted_species, confidence, p_value, drift_detected, log_folder='uploads/logs'):
    try:
        # Crear directorio de logs si no existe
        create_log_directory(log_folder)
        
        # Crear un log en formato JSON
        drift_log = {
            'feature': feature,
            'predicted_species': predicted_species,
            'confidence': float(confidence),  # Convertir float32 a float
            'p_value': float(p_value),        # Convertir float32 a float
            'drift_detected': bool(drift_detected),  # Convertir bool_ a bool
        }

        # Enviar el log a Logstash
        #logger.info("test")
        #logger.info(json.dumps(drift_log))   # Pasar el diccionario directamente
        logger.info(drift_log.json)

        # Ruta del archivo de log
        log_file_path = os.path.join(log_folder, 'drift_log.json')
        
        # Guardar el log en un archivo JSON
        with open(log_file_path, 'a') as log_file:
            json.dump(drift_log, log_file)
            log_file.write('\n')

        
    except Exception as e:
        logging.error(f"Error registrando información de drift: {str(e)}")
        raise
