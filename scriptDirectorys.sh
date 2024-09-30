#!/bin/bash

# Crear directorios
mkdir -p geotree-project-root/{app/{templates,static/{css,js},api},data,models,docker}

# Crear archivos y agregar contenido

# config.py
cat <<EOL > geotree-project-root/app/config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:admin@db/postgis")
    REDIS_URL = os.getenv("REDIS_URL", "redis://admin:admin@redis:6379/0")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
EOL

# __init__.py
cat <<EOL > geotree-project-root/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
redis_client = FlaskRedis(app)

from app import routes
EOL

# models.py
cat <<EOL > geotree-project-root/app/models.py
from app import db

class Tree(db.Model):
    id = db.Column(db.Integer, primary key=True)
    image_url = db.Column(db.String(255))
    geolocation = db.Column(db.String(255))
    description = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    user = db.Column(db.String(50))
    carbon_volume = db.Column(db.Float)
    species = db.Column(db.String(100))
EOL

# routes.py
cat <<EOL > geotree-project-root/app/routes.py
from flask import request, jsonify, render_template
from app import app, db
from app.models import Tree
from app.api import model_api

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trees', methods=['POST'])
def add_tree():
    data = request.json
    tree = Tree(
        image_url=data['image_url'],
        geolocation=data['geolocation'],
        description=data['description'],
        timestamp=data['timestamp'],
        user=data['user'],
        carbon_volume=data.get('carbon_volume'),
        species=data.get('species')
    )
    db.session.add(tree)
    db.session.commit()
    return jsonify({'message': 'Tree added successfully'}), 201
EOL

# model_api.py
cat <<EOL > geotree-project-root/app/api/model_api.py
import pickle
from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__)

# Load models
model_especie = pickle.load(open("models/model_especie.pkl", "rb"))
model_carbon = pickle.load(open("models/model_carbon.pkl", "rb"))

@api_bp.route('/predict_especie', methods=['POST'])
def predict_especie():
    data = request.json
    prediction = model_especie.predict([data['features']])
    return jsonify({'species': prediction[0]})

@api_bp.route('/predict_carbon', methods=['POST'])
def predict_carbon():
    data = request.json
    prediction = model_carbon.predict([data['features']])
    return jsonify({'carbon_volume': prediction[0]})
EOL

# index.html
cat <<EOL > geotree-project-root/app/templates/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Geo Trees</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
</head>
<body>
    <div id="map"></div>
    <script src="{{ url_for('static', filename='js/loadMaps.js') }}"></script>
    <script src="{{ url_for('static', filename='js/eventMaps.js') }}"></script>
</body>
</html>
EOL

# loadMaps.js
cat <<EOL > geotree-project-root/app/static/js/loadMaps.js
document.addEventListener('DOMContentLoaded', function() {
    var map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
    }).addTo(map);

    fetch('/geojson_data')
        .then(response => response.json())
        .then(data => {
            L.geoJSON(data).addTo(map);
        });
});
EOL

# eventMaps.js
cat <<EOL > geotree-project-root/app/static/js/eventMaps.js
function onMapClick(e) {
    fetch(\`/tree_data?lat=\${e.latlng.lat}&lng=\${e.latlng.lng}\`)
        .then(response => response.json())
        .then(data => {
            // Display the data in a side panel
        });
}

map.on('click', onMapClick);
EOL

# Dockerfile
cat <<EOL > geotree-project-root/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]
EOL

# docker-compose.yml
cat <<EOL > geotree-project-root/docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis
      - kafka

  db:
    image: postgis/postgis:latest
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: geotree-project-root
    ports:
      - "5432:5432"
    volumes:
      - postgis_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    ports:
      - "2181:2181"

volumes:
  postgis_data:
EOL

# .env
cat <<EOL > geotree-project-root/.env
DATABASE_URL=postgresql://admin:admin@db/postgis
REDIS_URL=redis://admin:admin@redis:6379/0
SECRET_KEY=supersecretkey
EOL

# requirements.txt
cat <<EOL > geotree-project-root/requirements.txt
Flask
Flask-SQLAlchemy
Flask-Redis
psycopg2-binary
pandas
numpy
EOL

echo "Estructura de directorios y archivos creada exitosamente."
