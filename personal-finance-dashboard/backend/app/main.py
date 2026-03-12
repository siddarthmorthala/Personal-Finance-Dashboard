import csv
import io
from datetime import datetime
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .categorizer import categorize_transaction
from .crud import get_all_transactions, get_category_breakdown, get_monthly_trends, get_summary
from .database import Base, engine, get_db
from .models import Transaction
from .schemas import TransactionOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATE_COLUMNS = ["date", "transaction_date", "posted_date"]
DESCRIPTION_COLUMNS = ["description", "merchant", "details", "memo"]
AMOUNT_COLUMNS = ["amount"]
DEBIT_COLUMNS = ["debit"]
CREDIT_COLUMNS = ["credit"]
DATE_FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]


def normalize_columns(row: dict) -> dict:
    return {str(k).strip().lower(): str(v).strip() for k, v in row.items()}


def parse_date(value: str):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Unsupported date format: {value}")


def get_first_present(row: dict, possible_columns: list[str]) -> str | None:
    for col in possible_columns:
        if col in row and row[col] != "":
            return row[col]
    return None


def parse_amount(row: dict) -> float:
    amount_value = get_first_present(row, AMOUNT_COLUMNS)
    if amount_value is not None:
        return float(amount_value.replace(",", ""))

    debit_value = get_first_present(row, DEBIT_COLUMNS)
    credit_value = get_first_present(row, CREDIT_COLUMNS)

    debit = float(debit_value.replace(",", "")) if debit_value else 0.0
    credit = float(credit_value.replace(",", "")) if credit_value else 0.0

    if debit == 0.0 and credit == 0.0:
        raise ValueError("Could not determine transaction amount")

    return credit - debit


@app.get("/")
def health_check():
    return {"message": "Personal Finance Dashboard API is running"}


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = await file.read()

    try:
        decoded = content.decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(decoded))
        imported_count = 0

        for raw_row in reader:
            row = normalize_columns(raw_row)
            date_value = get_first_present(row, DATE_COLUMNS)
            description_value = get_first_present(row, DESCRIPTION_COLUMNS)

            if not date_value or not description_value:
                continue

            amount = parse_amount(row)
            parsed_date = parse_date(date_value)
            category = categorize_transaction(description_value, amount)

            transaction = Transaction(
                date=parsed_date,
                description=description_value,
                amount=amount,
                category=category,
            )
            db.add(transaction)
            imported_count += 1

        db.commit()
        return {"message": "CSV imported successfully", "imported_count": imported_count}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to process CSV: {exc}") from exc


@app.get("/summary")
def summary(db: Session = Depends(get_db)):
    return get_summary(db)


@app.get("/category-breakdown")
def category_breakdown(db: Session = Depends(get_db)):
    return get_category_breakdown(db)


@app.get("/monthly-trends")
def monthly_trends(db: Session = Depends(get_db)):
    return get_monthly_trends(db)


@app.get("/transactions", response_model=list[TransactionOut])
def transactions(db: Session = Depends(get_db)):
    return get_all_transactions(db)


@app.delete("/transactions")
def delete_transactions(db: Session = Depends(get_db)):
    deleted = db.query(Transaction).delete()
    db.commit()
    return {"message": "Transactions cleared", "deleted_count": deleted}
