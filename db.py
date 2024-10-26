from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime 
from sqlalchemy import CheckConstraint

# Initialize SQLAlchemy
db = SQLAlchemy()

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(255), unique=True, nullable=False)  # unique user ID
    password = db.Column(db.Text, nullable=False)  # hashed password

# Transaction model
# class Transaction(db.Model):
    # __tablename__ = 'transactions'
    # id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.String(255), db.ForeignKey('users.user_id'))  # foreign key to users
    # type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    # amount = db.Column(db.Numeric(10, 2), nullable=False)  # amount in decimal format
    # description = db.Column(db.Text)  # description/notes of the transaction
    # date = db.Column(db.DateTime, default=db.func.current_timestamp())  # date and time of transaction

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Wallet(db.Model):
    __tablename__ = 'wallet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    balance = db.Column(db.Float, nullable=False)  # Total balance


# class Wallet(db.Model):
#     __tablename__ = 'wallet'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     type = db.Column(db.String(10), nullable=False)
#     category = db.Column(db.String(50), nullable=False)
#     payment_method = db.Column(db.String(50), nullable=False)
#     notes = db.Column(db.String(255))
#     date = db.Column(db.DateTime, default=db.func.current_timestamp())
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

#     __table_args__ = (
#         CheckConstraint("type IN ('income', 'expense')", name="check_wallet_type"),
#     )