from flask import request, jsonify, render_template
from app import app, geotree
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
    geotree.session.add(tree)
    geotree.session.commit()
    return jsonify({'message': 'Tree added successfully'}), 201
