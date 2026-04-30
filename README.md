# PayGuard — UPI Payment Fraud Analysis

A Flask web application for exploring and analysing UPI digital payment transactions, user profiles, and merchant data with built-in fraud detection insights.

***

## Features

- Browse and search transactions, users, and merchants
- Detailed profile pages with linked data across all three entities
- Fraud signal indicators — new device, IP mismatch, failed attempts, velocity
- Analysis dashboard with Matplotlib charts
- Pagination and filtering on all list pages
- Custom error pages (404, 500)

***

## Tech Stack

- **Backend:** Python, Flask, SQLite3
- **Templates:** Jinja2
- **Charts:** Matplotlib (server-side PNG)
- **Server:** Gunicorn (production)

***

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd fraud_app
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows:**
```powershell
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add data files

Place the CSV files inside the `data/` folder:

```
data/
├── transactions.csv
├── users.csv
└── merchants.csv
```

### 5. Load data into the database

```bash
python load_data.py
```

This creates `instance/app.db` and imports the data. Safe to run multiple times — skips if data is already loaded.

### 6. Run the app

```bash
python run.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

***

## Running Tests

```bash
pytest tests/ -v
```

***

## Deployment on Render

1. Push your code including the `data/` folder to GitHub
2. Create a new **Web Service** on [render.com](https://render.com)
3. Connect your repository and set:

| Field | Value |
|-------|-------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python load_data.py && gunicorn run:app` |

4. Deploy — the database is built automatically from the CSV files on first boot.

**Live URL:** `https://your-app-name.onrender.com`

***

## Project Structure

```
UPI/
├── run.py
├── config.py
├── database.py
├── load_data.py
├── charts.py
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── controllers/
│   ├── templates/
│   └── static/
├── data/
├── instance/
├── tests/
├── requirements.txt
├── Procfile
└── runtime.txt
```

***

## Environment

- Python 3.11+
- Flask 3.1.0+