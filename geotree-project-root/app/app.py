from flask import Flask, render_template
from .api.predictspecie import predictspecie_blueprint  # Importar el Blueprint desde predictspecie.py


app = Flask(__name__)

# Registrar el Blueprint de la API de predicción
app.register_blueprint(predictspecie_blueprint, url_prefix='/api')


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/predictspecie')
def predict():
    return render_template('predictspecie.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
