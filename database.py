import sqlite3
import os

DATABASE = os.environ.get('DATABASE_PATH', 'instance/app.db')

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id                  VARCHAR(20) PRIMARY KEY,
    age_group                VARCHAR(10),
    city                     VARCHAR(50),
    city_tier                VARCHAR(10),
    kyc_status               VARCHAR(20),
    account_age_days         INT,
    linked_bank_count        INT,
    avg_monthly_transactions INT,
    avg_transaction_value    DECIMAL(10,2),
    preferred_app            VARCHAR(30),
    preferred_device         VARCHAR(20),
    user_loyalty_score       DOUBLE,
    is_high_risk_user        BOOLEAN
);

CREATE TABLE IF NOT EXISTS merchants (
    merchant_id            VARCHAR(20) PRIMARY KEY,
    merchant_name          VARCHAR(50),
    merchant_category      VARCHAR(50),
    merchant_size          VARCHAR(20),
    city                   VARCHAR(50),
    city_tier              VARCHAR(10),
    avg_daily_transactions INT,
    is_registered          BOOLEAN,
    rating                 DECIMAL(2,1)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id              VARCHAR(20) PRIMARY KEY,
    user_id                     VARCHAR(20),
    receiver_id                 VARCHAR(20),
    receiver_type               VARCHAR(20),
    amount                      DECIMAL(10,2),
    timestamp                   DATETIME,
    date                        DATE,
    hour_of_day                 INT,
    day_of_week                 VARCHAR(10),
    is_weekend                  BOOLEAN,
    is_night_transaction        BOOLEAN,
    time_since_last_txn_min     DOUBLE,
    transaction_type            VARCHAR(30),
    payment_app                 VARCHAR(30),
    device_type                 VARCHAR(20),
    status                      VARCHAR(20),
    user_city_tier              VARCHAR(10),
    user_kyc_status             VARCHAR(20),
    user_avg_monthly_txn        INT,
    user_avg_txn_value          DECIMAL(10,2),
    user_loyalty_score          DOUBLE,
    new_device_flag             BOOLEAN,
    ip_location_mismatch        BOOLEAN,
    failed_attempts_last_24h    INT,
    transaction_velocity        INT,
    amount_deviation_score      DOUBLE,
    is_fraud                    BOOLEAN,
    recurring_payment_flag      BOOLEAN,
    balance_after_transaction   DECIMAL(12,2),
    transaction_frequency_score DOUBLE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
"""


def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn
