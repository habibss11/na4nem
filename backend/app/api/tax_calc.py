import json, os
BASE = os.path.join(os.path.dirname(__file__), "..", "models")
CONST_PATH = os.path.join(BASE, "constants.json")
with open(CONST_PATH, "r", encoding="utf-8") as f:
    CONST = json.load(f)


def calc_usn(revenue: float, expenses: float = 0.0, scheme: str = "6"):
    if scheme == "6":
        tax = revenue * CONST["USN"]["rate_income"]
    else:
        taxable = max(0.0, revenue - expenses)
        tax = taxable * CONST["USN"]["rate_income_minus_expenses"]
    return {"tax": round(tax, 2)}


def calc_ndfl(amount: float):
    rate = CONST["NDFL"]["rate"]
    return {"ndfl": round(amount * rate, 2)}


def calc_insurance(salary_total: float):
    rates = CONST["INSURANCE"]
    total = salary_total * (rates.get("pension", 0) + rates.get("social", 0) + rates.get("medical", 0))
    return {"insurance": round(total, 2)}


def calc_taxes(payload: dict):
    kind = payload.get("kind")
    if kind == "usn":
        return calc_usn(payload.get("revenue", 0.0), payload.get("expenses", 0.0), payload.get("scheme", "6"))
    if kind == "ndfl":
        return calc_ndfl(payload.get("amount", 0.0))
    if kind == "insurance":
        return calc_insurance(payload.get("salary_total", 0.0))
    return {"error": "unknown kind"}
