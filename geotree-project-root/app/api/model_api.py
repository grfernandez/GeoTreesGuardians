# Load models
import pickle
from flask import Blueprint, jsonify

model_api = Blueprint('model_api', __name__)

# Cargar modelos
#model_especie = pickle.load(open("../models/model_especie.pkl", "rb"))

# Ruta para predecir la especie del árbol
#@model_api.route('/predict', methods=['POST'])
#def predict():
    # Aquí va la lógica de predicción usando el modelo
    #return jsonify({"message": "Predicción realizada"})
