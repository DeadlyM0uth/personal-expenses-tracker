from jinja2 import Environment, PackageLoader, select_autoescape
from flask import Flask

#чтобы запустить введи:
#flask --app ./main.py run

env = Environment(
    loader=PackageLoader("main"),
    autoescape=select_autoescape()
)

app = Flask(__name__)

@app.route("/")
def index():
    return env.get_template("index.html").render()
