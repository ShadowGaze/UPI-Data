from database import init_db
from app import create_app
import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


SEED = """
INSERT INTO users VALUES ('U001','18-25','Mumbai','Tier1','Verified',200,2,30,500.0,'GPay','Mobile',0.8,0);
INSERT INTO merchants VALUES ('M001','ShopMart','Retail','Small','Delhi','Tier1',50,1,4.2);
INSERT INTO transactions VALUES
  ('T001','U001','M001','merchant',250.0,'2024-01-01 10:00','2024-01-01',
   10,'Monday',0,0,5.0,'Purchase','GPay','Mobile','Success',
   'Tier1','Verified',30,500.0,0.8,0,0,0,1,0.5,0,0,5000.0,0.7);
INSERT INTO transactions VALUES
  ('T002','U001','U002','user',100.0,'2024-01-02 22:00','2024-01-02',
   22,'Tuesday',0,1,10.0,'Transfer','PhonePe','Mobile','Success',
   'Tier1','Verified',30,500.0,0.8,1,1,2,3,2.5,1,0,4900.0,0.9);
"""


@pytest.fixture
def client(tmp_path):
    db_path = str(tmp_path / 'test.db')
    os.environ['DATABASE_PATH'] = db_path
    app = create_app()
    app.config['TESTING'] = True
    conn = init_db()
    conn.executescript(SEED)
    conn.commit()
    conn.close()
    with app.test_client() as c:
        yield c
    os.environ.pop('DATABASE_PATH', None)


def test_home(client):
    r = client.get('/')
    assert r.status_code == 200
    assert b'Dashboard' in r.data


def test_transactions_list(client):
    r = client.get('/transactions')
    assert r.status_code == 200
    assert b'T001' in r.data


def test_transactions_search(client):
    r = client.get('/transactions?search=GPay')
    assert r.status_code == 200
    assert b'GPay' in r.data


def test_transactions_fraud_filter(client):
    r = client.get('/transactions?fraud=1')
    assert r.status_code == 200
    assert b'T002' in r.data


def test_transaction_detail(client):
    r = client.get('/transactions/T001')
    assert r.status_code == 200
    assert b'T001' in r.data


def test_transaction_404(client):
    assert client.get('/transactions/XXXX').status_code == 404


def test_users_list(client):
    r = client.get('/users')
    assert r.status_code == 200
    assert b'U001' in r.data


def test_user_search(client):
    r = client.get('/users?search=Mumbai')
    assert r.status_code == 200


def test_user_detail(client):
    r = client.get('/users/U001')
    assert r.status_code == 200
    assert b'U001' in r.data


def test_user_404(client):
    assert client.get('/users/XXXX').status_code == 404


def test_merchants_list(client):
    r = client.get('/merchants')
    assert r.status_code == 200
    assert b'ShopMart' in r.data


def test_merchant_detail(client):
    r = client.get('/merchants/M001')
    assert r.status_code == 200
    assert b'ShopMart' in r.data


def test_merchant_404(client):
    assert client.get('/merchants/XXXX').status_code == 404


def test_404_page(client):
    r = client.get('/nonexistent-route')
    assert r.status_code == 404
    assert b'404' in r.data
