from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager
from models import db, User, Expense

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

# --- USER ENDPOINTS ---

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400
    
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=data["username"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if data.get("username"):
        # check uniqueness if changing username
        if data["username"] != user.username and User.query.filter_by(username=data["username"]).first():
             return jsonify({"error": "Username already exists"}), 400
        user.username = data["username"]
    if data.get("password"):
         user.set_password(data["password"])
    
    db.session.commit()
    return jsonify(user.to_dict())

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

# --- EXPENSE ENDPOINTS ---

@app.route("/api/expenses", methods=["POST"])
def create_expense():
    data = request.get_json()
    required = ["amount", "category", "user_id"]
    if not data or any(k not in data for k in required):
        return jsonify({"error": "Missing required fields (amount, category, user_id)"}), 400

    # Optional: verify user exists
    if not User.query.get(data["user_id"]):
         return jsonify({"error": "User not found"}), 404

    from datetime import datetime
    date_val = datetime.utcnow()
    if data.get("date"):
        try:
             date_val = datetime.fromisoformat(data["date"])
        except ValueError:
             return jsonify({"error": "Invalid date format (use ISO)"}), 400

    expense = Expense(
        amount=data["amount"],
        category=data["category"],
        user_id=data["user_id"],
        date=date_val,
        comment=data.get("comment"),
        payment_method=data.get("payment_method")
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify(expense.to_dict()), 201

@app.route("/api/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    return jsonify(expense.to_dict())

@app.route("/api/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    data = request.get_json()
    
    if "amount" in data: expense.amount = data["amount"]
    if "category" in data: expense.category = data["category"]
    if "comment" in data: expense.comment = data["comment"]
    if "payment_method" in data: expense.payment_method = data["payment_method"]
    if "date" in data:
         try:
             expense.date = datetime.fromisoformat(data["date"])
         except ValueError:
             return jsonify({"error": "Invalid date format"}), 400
             
    db.session.commit()
    return jsonify(expense.to_dict())

@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted"}), 200

@app.route("/api/users/<int:user_id>/expenses", methods=["GET"])
def get_user_expenses(user_id):
    user = User.query.get_or_404(user_id)
    expenses = Expense.query.filter_by(user_id=user.id).all()
    return jsonify([e.to_dict() for e in expenses])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
