import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models import User, Country, ExpenseCategory, PaymentMethod  # adjust import names to match your models
from passlib.hash import bcrypt

# Use SQLite in-memory DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables and seed initial data."""
    Base.metadata.create_all(bind=engine)

    # --- seed data ---
    session = TestingSessionLocal()

    # Seed countries
    country = Country(id=1, name="United States")
    session.add(country)

    # Seed categories
    category1 = ExpenseCategory(id=1, name="Food")
    category2 = ExpenseCategory(id=2, name="Transport")
    session.add_all([category1, category2])

    # Seed payment methods
    pm1 = PaymentMethod(id=1, name="Cash")
    pm2 = PaymentMethod(id=2, name="Credit Card")
    session.add_all([pm1, pm2])

    # Seed a test user
    user = User(
        id=1,
        email="testuser@example.com",
        password=bcrypt.hash("Secret123!"),  # hash password for login tests
        country_id=1
    )
    session.add(user)

    session.commit()
    session.close()

    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Provide a new database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Override FastAPI's get_db dependency to use the test session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
