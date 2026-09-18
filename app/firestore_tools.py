"""Firestore tool definitions for Personal Trip & Expense Manager."""

from typing import Optional
from google.cloud import firestore

# CRITICAL: Hardcoded project ID string literal required for Agent Platform deployment
PROJECT_ID = "qwiklabs-gcp-01-f642bd17f85e"


def _get_db() -> firestore.Client:
    return firestore.Client(project=PROJECT_ID)


def get_trips(status: Optional[str] = None) -> list[dict]:
    """Retrieve trips from Firestore.

    Args:
        status: Optional filter by trip status ('past', 'upcoming', or 'active').

    Returns:
        A list of trip dictionaries with fields like trip_id, name, destination, status, start_date, end_date, total_budget, currency.
    """
    db = _get_db()
    query = db.collection("trips")
    if status:
        query = query.where("status", "==", status.lower())
    
    docs = query.stream()
    return [doc.to_dict() for doc in docs]


def get_trip_expenses(trip_id: str, category: Optional[str] = None) -> list[dict]:
    """Retrieve expenses for a specific trip from Firestore.

    Args:
        trip_id: The ID of the trip (e.g. 'paris-2026').
        category: Optional filter by expense category ('travel', 'stay', 'tickets', 'meals', 'shopping').

    Returns:
        A list of expense dictionaries.
    """
    db = _get_db()
    query = db.collection("expenses").where("trip_id", "==", trip_id)
    if category:
        query = query.where("category", "==", category.lower())
    
    docs = query.stream()
    return [doc.to_dict() for doc in docs]


def get_trip_summary(trip_id: str) -> dict:
    """Calculate expense summary and breakdown by category for a trip.

    Args:
        trip_id: The ID of the trip (e.g. 'paris-2026').

    Returns:
        A dictionary containing trip details, category breakdowns (travel, stay, tickets, meals, shopping), total spent, total budget, and remaining budget.
    """
    db = _get_db()
    trip_doc = db.collection("trips").document(trip_id).get()
    if not trip_doc.exists:
        return {"error": f"Trip '{trip_id}' not found."}
    
    trip = trip_doc.to_dict()
    expenses = get_trip_expenses(trip_id)

    category_totals = {
        "travel": 0.0,
        "stay": 0.0,
        "tickets": 0.0,
        "meals": 0.0,
        "shopping": 0.0,
        "other": 0.0,
    }

    total_spent = 0.0
    for exp in expenses:
        amt = float(exp.get("amount", 0.0))
        cat = exp.get("category", "other").lower()
        if cat in category_totals:
            category_totals[cat] += amt
        else:
            category_totals["other"] += amt
        total_spent += amt

    total_budget = float(trip.get("total_budget", 0.0))
    remaining = total_budget - total_spent

    return {
        "trip_id": trip_id,
        "name": trip.get("name"),
        "destination": trip.get("destination"),
        "status": trip.get("status"),
        "currency": trip.get("currency", "USD"),
        "total_budget": total_budget,
        "total_spent": round(total_spent, 2),
        "remaining_budget": round(remaining, 2),
        "category_breakdown": {k: round(v, 2) for k, v in category_totals.items() if v > 0 or k in ["travel", "stay", "tickets", "meals", "shopping"]},
    }


def add_trip(
    trip_id: str,
    name: str,
    destination: str,
    status: str,
    start_date: str,
    end_date: str,
    total_budget: float,
    currency: str = "USD",
) -> dict:
    """Add or update a trip in Firestore.

    Args:
        trip_id: Unique ID for the trip (e.g. 'tokyo-2026').
        name: Name of the trip (e.g. 'Tokyo Autumn Adventure').
        destination: Destination city/country (e.g. 'Tokyo, Japan').
        status: Status of trip ('past', 'upcoming', or 'active').
        start_date: Start date (YYYY-MM-DD).
        end_date: End date (YYYY-MM-DD).
        total_budget: Total budget allocated for trip.
        currency: Currency code (default 'USD').

    Returns:
        Status dictionary confirming trip creation.
    """
    db = _get_db()
    trip_data = {
        "trip_id": trip_id,
        "name": name,
        "destination": destination,
        "status": status.lower(),
        "start_date": start_date,
        "end_date": end_date,
        "total_budget": float(total_budget),
        "currency": currency,
    }
    db.collection("trips").document(trip_id).set(trip_data)
    return {"status": "success", "message": f"Trip '{name}' saved successfully.", "trip": trip_data}


def log_expense(
    expense_id: str,
    trip_id: str,
    category: str,
    amount: float,
    description: str,
    date: str,
) -> dict:
    """Log a new expense for a trip in Firestore.

    Args:
        expense_id: Unique ID for the expense (e.g. 'exp-101').
        trip_id: ID of the associated trip (e.g. 'paris-2026').
        category: Expense category ('travel', 'stay', 'tickets', 'meals', 'shopping').
        amount: Amount spent.
        description: Description of expense (e.g. 'Dinner at Le Petit Célestin').
        date: Date of expense (YYYY-MM-DD).

    Returns:
        Status dictionary confirming expense logging.
    """
    db = _get_db()
    expense_data = {
        "expense_id": expense_id,
        "trip_id": trip_id,
        "category": category.lower(),
        "amount": float(amount),
        "description": description,
        "date": date,
    }
    db.collection("expenses").document(expense_id).set(expense_data)
    return {"status": "success", "message": f"Expense '{description}' (${amount}) logged successfully.", "expense": expense_data}
