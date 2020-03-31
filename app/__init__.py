from flask import Flask
from app.controllers import blueprints
from flask import render_template

app = Flask(__name__, template_folder='../templates')

for blueprint in blueprints:
    app.register_blueprint(blueprint)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')