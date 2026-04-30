import os

DATABASE = os.environ.get('DATABASE_PATH', 'instance/app.db')
DATA_DIR = os.environ.get('DATA_DIR', 'data')
