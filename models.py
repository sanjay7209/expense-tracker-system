from typing import Text
from database import Base
from sqlalchemy import Column, Integer,String, Boolean, ForeignKey, Date,Time,DateTime,Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship


class BaseEntity:
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    created_by = Column(Integer,nullable=True)
    modified_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    modified_by = Column(Integer,nullable=True)
    status = Column(Integer,nullable=True)
    comments = Column(String,nullable=True)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)

class ExpenseCategory(Base):
    __tablename__ = "expense_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False, unique=True)

class User(Base,BaseEntity):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    last_login_at = Column(TIMESTAMP(timezone=True), nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)

    role = relationship("Role")
    country = relationship("Country")


class Expense(Base,BaseEntity):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("expense_categories.id"), nullable=False)
    payment_method = Column(Integer, ForeignKey("payment_methods.id"), nullable=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)

    user = relationship("User")
    category = relationship("ExpenseCategory")
    # payment_method = relationship("PaymentMethod")



class Budget(Base,BaseEntity):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("expense_categories.id"), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    user = relationship("User")
    category = relationship("ExpenseCategory")