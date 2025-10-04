import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from models import Country, ExpenseCategory, PaymentMethod, User
from fastapi.testclient import TestClient
from main import app

# Point to the Postgres service in GitHub Actions
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/testdb"

# Create engine & session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override get_db for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Recreate tables and seed base data for each test run."""
    Base.metadata.drop_all(bind=engine)   # ensure clean state
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    # Seed Country
    country = Country(id=1, name="Testland", code="TST")
    db.add(country)

    # Seed Expense Category
    category = ExpenseCategory(id=1, name="Food")
    db.add(category)

    # Seed Payment Method
    payment_method = PaymentMethod(id=1, type="Cash")
    db.add(payment_method)

    # Seed User
    user = User(
        id=1,
        username="testuser",
        first_name="Test",
        last_name="User",
        email="test@example.com",
        password="SecurePass123",   # ⚠️ if your app hashes, replace with hashed
        country_id=1,
        role_id=None,
        is_admin=False,
    )
    db.add(user)

    db.commit()
    db.close()
    yield


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
