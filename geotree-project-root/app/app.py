from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')
    #return "Hola Mundo Python"
if __name__ == '__main__':
    app.run.run(debug=True, port=5000)
