from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User

#чтобы запустить введи:
#flask --app ./main.py run

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key' # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
