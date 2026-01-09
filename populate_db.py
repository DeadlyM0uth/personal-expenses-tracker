from main import app, db, User, Expense
from datetime import datetime, timedelta
import random

def populate():
    """
    Полностью очищает и пересоздаёт базу данных с тестовыми данными.
    Используйте эту функцию для сброса БД в исходное состояние.
    """
    with app.app_context():
        # Clean up existing data (optional, but good for test consistency)
        db.drop_all() 
        db.create_all()
        print("База данных очищена и пересоздана.")

        _create_sample_data()

def populate_if_empty():
    """
    Заполняет базу данных тестовыми данными ТОЛЬКО если она пустая.
    Безопасно вызывать при каждом запуске приложения.
    """
    with app.app_context():
        # Проверяем, есть ли уже пользователи в БД
        user_count = User.query.count()
        
        if user_count == 0:
            print("База данных пустая. Начинаем заполнение тестовыми данными...")
            _create_sample_data()
            print("✓ База данных успешно заполнена!")
        else:
            print(f"База данных уже содержит {user_count} пользователей. Заполнение пропущено.")

def _create_sample_data():
    """
    Внутренняя функция для создания тестовых данных.
    """
    categories = ["еда", "транспорт", "подписки", "развлечения", "здоровье"]
    payment_methods = ["Наличные", "Карта", "Перевод"]
    usernames = ["Иван", "Мария", "Алексей", "Елена", "Дмитрий"]
    
    for i, username in enumerate(usernames, 1):
        user = User(username=username)
        user.set_password("123")
        db.session.add(user)
        db.session.commit() # Commit to get ID
        
        print(f"  → Создан пользователь: {username}")
        
        expenses = []
        for j in range(10):
            amount = round(random.uniform(10.0, 5000.0), 2)
            date = datetime.utcnow() - timedelta(days=random.randint(0, 60))
            
            exp = Expense(
                amount=amount,
                category=random.choice(categories),  # Will be auto-lowercased
                user_id=user.id,
                date=date,
                comment=f"Расход {j+1} для {username}",
                payment_method=random.choice(payment_methods)
            )
            expenses.append(exp)
        
        db.session.add_all(expenses)
        db.session.commit()
        print(f"  → Добавлено 10 расходов для {username}")

if __name__ == "__main__":
    populate()
