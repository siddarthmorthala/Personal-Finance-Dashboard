import io
import os
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_finance.db"

from app.main import app  # noqa: E402
from app.database import Base, engine  # noqa: E402

client = TestClient(app)


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_finance.db"):
        os.remove("test_finance.db")


def test_upload_and_summary_flow():
    client.delete("/transactions")

    csv_content = """date,description,amount
2026-01-01,Payroll Deposit,2500
2026-01-02,Starbucks,-8.50
2026-01-03,Amazon Purchase,-45.00
2026-02-01,Rent Payment,-1200
"""
    files = {"file": ("transactions.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}

    upload_response = client.post("/upload", files=files)
    assert upload_response.status_code == 200
    assert upload_response.json()["imported_count"] == 4

    summary_response = client.get("/summary")
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary["income"] == 2500.0
    assert summary["spending"] == 1253.5
    assert summary["transaction_count"] == 4

    category_response = client.get("/category-breakdown")
    assert category_response.status_code == 200
    categories = category_response.json()
    assert any(item["category"] == "Housing" for item in categories)

    transactions_response = client.get("/transactions")
    assert transactions_response.status_code == 200
    assert len(transactions_response.json()) == 4
