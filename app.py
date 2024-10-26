from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import db, User, Wallet, Transaction  # Import db, User, and Wallet models
from datetime import datetime 
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = 'your_secret_key'  # Use a strong secret key

# Initialize the database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        # Validate user
        user = User.query.filter_by(user_id=user_id).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user_id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        user_id = request.form['user_id']
        password = request.form['password']

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Add user to the database
        user = User(username=username, user_id=user_id, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully', 'success')
        except Exception:
            db.session.rollback()
            flash('User ID already exists', 'danger')

    return redirect(url_for('login'))

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(user_id=session['user_id']).first()

    if user is None:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

    username = user.username

    # Fetch user's wallet balance
    wallet = Wallet.query.filter_by(user_id=user.id).first()
    total_balance = wallet.balance if wallet else 0  # Fetch the balance

    # Fetch user's transactions from the Transaction table
    transactions = Transaction.query.filter_by(user_id=user.id).all()

    # Initialize total income and expense
    total_income = 0
    total_expense = 0

    # Calculate total income and expense
    for transaction in transactions:
        if transaction.type == 'income':
            total_income += transaction.amount
        elif transaction.type == 'expense':
            total_expense += transaction.amount

    return render_template('dashboard.html', 
                           username=username, 
                           transactions=transactions, 
                           balance=total_balance,
                           income=total_income,  # Pass total income to template
                           expense=total_expense)  # Pass total expense to template
    
@app.route('/add_income', methods=['POST'])
def add_income():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Convert the amount to float
    amount = float(request.form['income_amount'])
    category = request.form['income_category']
    payment_method = request.form['income_payment_method']
    notes = request.form['income_notes']
    income_date = request.form['income_date']
    income_date = datetime.fromisoformat(income_date)
    type = 'income'

    # Get user_id based on session
    user = User.query.filter_by(user_id=session['user_id']).first()

    # Add income transaction to the Transaction table
    transaction = Transaction(
        user_id=user.id, 
        amount=amount,  # Store the income amount as positive
        type=type,
        category=category,
        payment_method=payment_method,
        notes=notes,
        date=income_date,  # Use user-provided date
        created_at=datetime.utcnow() 
    )

    # Update the user's wallet balance
    wallet = Wallet.query.filter_by(user_id=user.id).first()
    if wallet:
        wallet.balance += amount  # Add income to the balance
    else:
        wallet = Wallet(user_id=user.id, balance=amount)
        db.session.add(wallet)

    db.session.add(transaction)
    db.session.commit()
    flash('Income added successfully!', 'success')

    return redirect(url_for('dashboard'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Convert the amount to float
    amount = float(request.form['expense_amount'])
    category = request.form['expense_category']
    payment_method = request.form['expense_payment_method']
    notes = request.form['expense_notes']
    expense_date = request.form['expense_date']
    expense_date = datetime.fromisoformat(expense_date)
    type = 'expense'

    # Get user_id based on session
    user = User.query.filter_by(user_id=session['user_id']).first()

    # Add expense transaction to the Transaction table
    transaction = Transaction(
        user_id=user.id,  
        amount=amount,  # Store the expense amount as positive
        type=type,
        category=category,
        payment_method=payment_method,
        notes=notes,
        date=expense_date,  # Use user-provided date
        created_at=datetime.utcnow() 
    )

    # Update the user's wallet balance
    wallet = Wallet.query.filter_by(user_id=user.id).first()
    if wallet:
        wallet.balance -= amount  # Subtract expense from the balance
    else:
        wallet = Wallet(user_id=user.id, balance=-amount)
        db.session.add(wallet)

    db.session.add(transaction)
    db.session.commit()
    flash('Expense added successfully!', 'success')

    return redirect(url_for('dashboard'))

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Fetch the transaction to delete
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        flash('Transaction not found', 'danger')
        return redirect(url_for('dashboard'))

    # Get user and wallet info
    user = User.query.filter_by(user_id=session['user_id']).first()
    wallet = Wallet.query.filter_by(user_id=user.id).first()

    # Update the wallet balance based on transaction type
    if transaction.type == 'income':
        wallet.balance -= float(transaction.amount)  # Remove income from balance
    elif transaction.type == 'expense':
        wallet.balance += float(transaction.amount)  # Add expense back to balance

    # Delete the transaction
    db.session.delete(transaction)
    db.session.commit()

    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
