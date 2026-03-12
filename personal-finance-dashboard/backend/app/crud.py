from collections import defaultdict
from sqlalchemy import select
from .models import Transaction


def get_all_transactions(db):
    return db.execute(select(Transaction).order_by(Transaction.date.desc(), Transaction.id.desc())).scalars().all()


def get_summary(db):
    transactions = get_all_transactions(db)
    income = round(sum(t.amount for t in transactions if t.amount > 0), 2)
    spending = round(abs(sum(t.amount for t in transactions if t.amount < 0)), 2)
    net = round(income - spending, 2)
    return {
        "income": income,
        "spending": spending,
        "net": net,
        "transaction_count": len(transactions),
    }


def get_category_breakdown(db):
    totals = defaultdict(float)
    for t in get_all_transactions(db):
        if t.amount < 0:
            totals[t.category] += abs(t.amount)
    return [
        {"category": category, "amount": round(amount, 2)}
        for category, amount in sorted(totals.items(), key=lambda item: item[1], reverse=True)
    ]


def get_monthly_trends(db):
    monthly = defaultdict(lambda: {"income": 0.0, "spending": 0.0})

    for t in get_all_transactions(db):
        month_key = t.date.strftime("%Y-%m")
        if t.amount > 0:
            monthly[month_key]["income"] += t.amount
        else:
            monthly[month_key]["spending"] += abs(t.amount)

    return [
        {
            "month": month,
            "income": round(values["income"], 2),
            "spending": round(values["spending"], 2),
        }
        for month, values in sorted(monthly.items())
    ]
