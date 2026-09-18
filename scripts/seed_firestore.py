#!/usr/bin/env python3
"""Seed script for initializing Personal Trip & Expense Manager Firestore database."""

from google.cloud import firestore

# CRITICAL: Hardcoded project ID as required by Agent Platform
PROJECT_ID = "qwiklabs-gcp-01-f642bd17f85e"

def seed_database():
    db = firestore.Client(project=PROJECT_ID)
    print(f"Connecting to Firestore for project '{PROJECT_ID}'...")

    # 1. Seed Trips
    trips_data = [
        {
            "trip_id": "paris-2026",
            "name": "Paris Summer Getaway",
            "destination": "Paris, France",
            "status": "past",
            "start_date": "2026-06-10",
            "end_date": "2026-06-18",
            "total_budget": 3500.0,
            "currency": "USD",
        },
        {
            "trip_id": "tokyo-2026",
            "name": "Tokyo Autumn Adventure",
            "destination": "Tokyo, Japan",
            "status": "upcoming",
            "start_date": "2026-10-15",
            "end_date": "2026-10-25",
            "total_budget": 4500.0,
            "currency": "USD",
        },
        {
            "trip_id": "rome-2026",
            "name": "Rome Cultural Tour",
            "destination": "Rome, Italy",
            "status": "upcoming",
            "start_date": "2026-12-01",
            "end_date": "2026-12-08",
            "total_budget": 2800.0,
            "currency": "USD",
        },
    ]

    for trip in trips_data:
        doc_ref = db.collection("trips").document(trip["trip_id"])
        doc_ref.set(trip)
        print(f"Seeded trip: {trip['name']} ({trip['trip_id']})")

    # 2. Seed Expenses for Paris trip
    expenses_data = [
        {
            "expense_id": "exp-001",
            "trip_id": "paris-2026",
            "category": "travel",
            "amount": 850.0,
            "description": "Roundtrip flight JFK to CDG",
            "date": "2026-06-10",
        },
        {
            "expense_id": "exp-002",
            "trip_id": "paris-2026",
            "category": "stay",
            "amount": 1200.0,
            "description": "7 nights Airbnb in Le Marais",
            "date": "2026-06-10",
        },
        {
            "expense_id": "exp-003",
            "trip_id": "paris-2026",
            "category": "tickets",
            "amount": 65.0,
            "description": "Louvre Museum tickets",
            "date": "2026-06-12",
        },
        {
            "expense_id": "exp-004",
            "trip_id": "paris-2026",
            "category": "meals",
            "amount": 340.0,
            "description": "Bistro dinners, bakeries & cafes in Paris",
            "date": "2026-06-15",
        },
        {
            "expense_id": "exp-005",
            "trip_id": "paris-2026",
            "category": "shopping",
            "amount": 180.0,
            "description": "Souvenirs and perfumes at Galeries Lafayette",
            "date": "2026-06-16",
        },
    ]

    for expense in expenses_data:
        doc_ref = db.collection("expenses").document(expense["expense_id"])
        doc_ref.set(expense)
        print(f"Seeded expense: {expense['description']} (${expense['amount']})")

    print("Firestore database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
