CATEGORY_RULES = {
    "Groceries": ["walmart", "target", "costco", "kroger", "whole foods", "trader joe"],
    "Dining": ["restaurant", "coffee", "starbucks", "chipotle", "doordash", "uber eats"],
    "Transportation": ["uber", "lyft", "shell", "chevron", "exxon", "gas", "fuel"],
    "Housing": ["rent", "mortgage", "apartment", "hoa"],
    "Utilities": ["electric", "water", "internet", "utility", "verizon", "att", "t-mobile"],
    "Entertainment": ["netflix", "spotify", "hulu", "movie", "ticketmaster"],
    "Shopping": ["amazon", "best buy", "nike", "apple", "store purchase"],
    "Healthcare": ["pharmacy", "doctor", "clinic", "hospital", "cvs", "walgreens"],
    "Income": ["payroll", "salary", "deposit", "direct dep", "refund", "bonus"],
}


def categorize_transaction(description: str, amount: float) -> str:
    text = description.lower().strip()

    if amount > 0:
        for keyword in CATEGORY_RULES["Income"]:
            if keyword in text:
                return "Income"
        return "Income"

    for category, keywords in CATEGORY_RULES.items():
        if category == "Income":
            continue
        for keyword in keywords:
            if keyword in text:
                return category

    return "Other"
