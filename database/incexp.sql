-- Drop tables if they exist
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS wallet CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    user_id VARCHAR(50) UNIQUE NOT NULL,  -- Email ID used as user_id
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create wallet table with balance column
CREATE TABLE wallet (
    id SERIAL PRIMARY KEY,  
    user_id INT REFERENCES users(id) ON DELETE CASCADE,  -- Foreign key referencing users
    balance FLOAT NOT NULL,  -- Renamed from amount to balance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table for income and expenses
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,  -- Foreign key referencing users
    amount NUMERIC(10, 2) NOT NULL,  -- Amount for each transaction
    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),  -- Type of transaction
    category VARCHAR(50) NOT NULL,  -- Category of income/expense
    payment_method VARCHAR(50) NOT NULL,  -- Payment method used
    notes VARCHAR(255),  -- Optional notes field
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date of transaction
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date when the record was created
);

-- Join query to view wallet along with usernames
SELECT 
    wallet.*, 
    users.username 
FROM 
    wallet 
JOIN 
    users 
ON 
    wallet.user_id = users.id;

-- Query to view all users
SELECT * FROM users;

-- Query to view all wallets (user balances)
SELECT * FROM wallet;

-- Query to view all transactions (income/expenses)
SELECT * FROM transactions;
