import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from models import Countries, Categories, PaymentMethods, Users
from fastapi.testclient import TestClient
from main import app
from passlib.hash import bcrypt

# Use the DATABASE_URL from env (Postgres in CI), fallback to sqlite in dev
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/testdb"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Create tables fresh for tests and seed initial data.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    # Seed Countries
    country = Countries(id=1, name="Testland")
    db.add(country)

    # Seed Categories
    category = Categories(id=1, name="Food")
    db.add(category)

    # Seed Payment Methods
    payment_method = PaymentMethods(id=1, name="Cash")
    db.add(payment_method)

    # Seed Default User
    user = Users(
        id=1,
        username="seeduser",
        first_name="Seed",
        last_name="User",
        email="seed@example.com",
        password=bcrypt.hash("SecurePass123"),  # hashed password
        country_id=1,
        is_admin=False
    )
    db.add(user)

    db.commit()
    db.close()

    yield

    # Teardown
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    """
    Provide a TestClient for API tests.
    """
    with TestClient(app) as c:
        yield c
