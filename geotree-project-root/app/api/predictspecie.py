import os
from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import traceback

# Crear el Blueprint para la API de predicción
predictspecie_blueprint = Blueprint('predictspecie', __name__)

# Cargar el modelo preentrenado
MODEL_PATH = 'identify_trees.h5'
model = load_model(MODEL_PATH)

# Lista de especies de árboles (ajústala con las etiquetas de tu modelo)
species = ['LapachoAmarillo', 'LapachoBlanco', 'LapachoRosado', 'Palmera', 'PaloBorracho']

# Directorio para almacenar imágenes subidas (opcional)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Función para preparar la imagen
def prepare_image(image_path):
    img = load_img(image_path, target_size=(224, 224))  # Cambia el tamaño según tu modelo
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión extra
    img_array /= 255.0  # Normalizar si es necesario
    return img_array

# Ruta de la API de predicción
@predictspecie_blueprint.route('/predictspecie', methods=['POST'])
def predictspecie():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Guardar la imagen temporalmente en el servidor
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Preparar la imagen
        image = prepare_image(file_path)

        # Hacer la predicción
        predictions = model.predict(image)
        predicted_class = np.argmax(predictions, axis=1)[0]
        predicted_species = species[predicted_class]

        # Eliminar la imagen temporal después de predecir
        os.remove(file_path)

        # Retornar el resultado en formato JSON
        return jsonify({'species': predicted_species})
        #return "OK"
    except Exception as e:
        # Capturar detalles del error
        error_message = str(e)
        error_traceback = traceback.format_exc()
        
        return jsonify({
            'error': 'Internal server error',
            'message': error_message,
            'traceback': error_traceback
        }), 500
