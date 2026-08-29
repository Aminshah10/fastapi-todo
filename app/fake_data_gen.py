from faker import Faker

from app.users.models import UserModel
from app.tasks.models import TaskModel
from app.auth.models import RefreshTokenModel  # noqa: F401
from app.core.database import SessionLocal

fake = Faker()

def user_seed(db) -> UserModel:
    user = UserModel(username=fake.user_name())
    user.set_password("12345678")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user: {user.username} with userId: {user.id}")
    return user

def task_seeds(db, user: UserModel, count=10):
    for _ in range(count):
        task = TaskModel(
            user_id=user.id,
            title=fake.sentence(nb_words=5),
            description=fake.paragraph(nb_sentences=3),
            is_done=fake.boolean()
        )
        db.add(task)
        db.commit()
    
    print(f"Created {count} tasks for user: {user.username} ID: {user.id}")
        
def main():
    db = SessionLocal()
    try:
        user = user_seed(db)
        task_seeds(db, user)
    finally:
        db.close()
        
if __name__ == "__main__":
    main()