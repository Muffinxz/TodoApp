from sqlalchemy import  create_engine, text
from sqlalchemy.pool import StaticPool
from TodoApp.models import Todos
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from ..routers.Auth import bcrypt_context
from ..models import Users

from ..main import app
from TodoApp.routers import todos

import pytest
from ..database import Base


SQLALCHEMY_DATABASE_URL="sqlite:///./testdb.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
from pathlib import Path

print("cwd:", Path.cwd())
print("engine url:", engine.url)
print("engine database:", engine.url.database)
print("absolute db path:", Path(engine.url.database).resolve())

client = TestClient(app)

TestingSessionLocal=sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username" : 'AchrafC', 'id' : 1, 'user_role': 'admin'}

@pytest.fixture
def test_todo():
    todo=Todos(
        title='Learn to code',
        description="Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1,
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user= Users(
        username='achraf',
        email='codingwithAchraf',
        first_name='Achraf',
        last_name='Chak',
        hashed_password= bcrypt_context.hash("testpass"),
        role='admin',
        phone_number='(111)-111-1111',
    )
    db =TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()