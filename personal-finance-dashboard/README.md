# Personal Finance Dashboard

A full-stack web app that lets users upload bank transaction CSVs, automatically categorize spending, and visualize budget trends over time.

**Tech stack:** React, FastAPI, SQLite, SQLAlchemy, Recharts

## Why this project exists

Most bank exports are hard to analyze quickly. This project turns raw CSV transaction data into a simple dashboard that helps users answer three useful questions fast:

- Where is my money going?
- How are my monthly spending patterns changing?
- Which transactions should I review more closely?

It is designed to show practical software engineering skills across the full stack: file handling, API development, database design, data cleaning, business logic, testing, and frontend data visualization.

## Features

- Upload bank CSV files through the UI
- Normalize transaction rows into a SQLite database
- Auto-categorize transactions using rule-based keyword matching
- View total spending, income, and net cash flow
- See spending by category in a bar chart
- See monthly income vs spending trends in a line chart
- Browse imported transactions in a searchable table
- Run API tests with pytest

## Project structure

```text
personal-finance-dashboard/
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
├── sample-data/
│   └── sample_bank_transactions.csv
├── .gitignore
├── LICENSE
└── README.md
```

## Demo workflow

1. Start the FastAPI backend
2. Start the React frontend
3. Upload the sample CSV in `sample-data/sample_bank_transactions.csv`
4. Review dashboard metrics and charts

## Backend setup

### 1) Create and activate a virtual environment

**macOS / Linux**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the API server

```bash
uvicorn app.main:app --reload
```

The backend runs at `http://127.0.0.1:8000`.

Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## Frontend setup

### 1) Install dependencies

```bash
cd frontend
npm install
```

### 2) Start the frontend

```bash
npm run dev
```

The frontend runs at `http://127.0.0.1:5173` by default.

## CSV format

The importer accepts CSVs with columns similar to these bank export patterns:

- `date`, `description`, `amount`
- `transaction_date`, `merchant`, `amount`
- `posted_date`, `details`, `debit`, `credit`

The app normalizes those fields into:

- `date`
- `description`
- `amount`

### Notes on amounts

- Negative values are treated as spending
- Positive values are treated as income
- If `debit` and `credit` columns exist, the app converts them into a single signed amount

## Running tests

```bash
cd backend
pytest
```

## API endpoints

- `POST /upload` — upload and import a CSV
- `GET /summary` — total income, spending, and net cash flow
- `GET /category-breakdown` — spending totals by category
- `GET /monthly-trends` — monthly income and spending trend data
- `GET /transactions` — list transactions
- `DELETE /transactions` — clear all imported transactions

## Resume-ready engineering highlights

- Full-stack architecture with a React frontend, FastAPI backend, and SQLite persistence layer
- CSV parsing and normalization logic that handles different bank export formats
- Rule-based categorization engine for turning raw descriptions into useful financial insights
- Dashboard visualizations for category-level and time-series analysis
- Automated backend tests for upload and analytics endpoints

## Ideas for future improvements

- User authentication and per-user data isolation
- Editable categories and custom categorization rules
- Budget alerts and monthly spending targets
- Plaid integration for direct bank sync
- Docker support and cloud deployment
- Export charts and reports as PDF

## License

This project is licensed under the MIT License.
