from main import app, db, User, Expense
from datetime import datetime, timedelta
import random

def populate():
    with app.app_context():
        # Clean up existing data (optional, but good for test consistency)
        db.drop_all() 
        db.create_all()
        print("Database cleared and recreated.")

        categories = ["Food", "Transport", "Subscriptions", "Entertainment", "Health"]
        payment_methods = ["Cash", "Card", "Transfer"]
        
        for i in range(1, 6):
            username = f"User{i}"
            user = User(username=username)
            user.set_password("123")
            db.session.add(user)
            db.session.commit() # Commit to get ID
            
            print(f"Created {username}")
            
            expenses = []
            for j in range(10):
                amount = round(random.uniform(10.0, 5000.0), 2)
                date = datetime.utcnow() - timedelta(days=random.randint(0, 60))
                
                exp = Expense(
                    amount=amount,
                    category=random.choice(categories),
                    user_id=user.id,
                    date=date,
                    comment=f"Expense {j+1} for {username}",
                    payment_method=random.choice(payment_methods)
                )
                expenses.append(exp)
            
            db.session.add_all(expenses)
            db.session.commit()
            print(f"Added 10 expenses for {username}")

if __name__ == "__main__":
    populate()
