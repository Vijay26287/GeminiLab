"""Real-time Currency Conversion Tool for Personal Trip Manager (from Public APIs)."""

import json
import os
import urllib.parse
import urllib.request


def convert_currency(amount: float, from_currency: str, to_currency: str = "USD") -> dict:
    """Convert an amount from one travel currency to another using real-time foreign exchange rates.

    Args:
        amount: The monetary amount to convert (e.g. 85.50).
        from_currency: 3-letter currency code converting from (e.g. 'EUR', 'JPY', 'GBP').
        to_currency: 3-letter currency code converting to (default 'USD').

    Returns:
        A dictionary containing original_amount, from_currency, converted_amount, to_currency, and exchange_rate.
    """
    from_curr = from_currency.strip().upper()
    to_curr = to_currency.strip().upper()
    
    if from_curr == to_curr:
        return {
            "status": "success",
            "original_amount": amount,
            "from_currency": from_curr,
            "converted_amount": round(amount, 2),
            "to_currency": to_curr,
            "rate": 1.0,
        }

    # Reads optional API key from environment variable if configured
    api_key = os.getenv("CURRENCY_API_KEY") or os.getenv("EXCHANGE_RATE_API_KEY")

    try:
        if api_key:
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_curr}/{to_curr}/{amount}"
            req = urllib.request.Request(url, headers={"User-Agent": "PersonalTripManager/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                converted = float(data.get("conversion_result", amount))
                rate = float(data.get("conversion_rate", 1.0))
        else:
            # Free public API (Frankfurter Exchange Rates API)
            url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_curr}&to={to_curr}"
            req = urllib.request.Request(url, headers={"User-Agent": "PersonalTripManager/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                rates = data.get("rates", {})
                converted = float(rates.get(to_curr, amount))
                rate = round(converted / amount, 4) if amount > 0 else 1.0

        return {
            "status": "success",
            "original_amount": amount,
            "from_currency": from_curr,
            "converted_amount": round(converted, 2),
            "to_currency": to_curr,
            "rate": rate,
        }

    except Exception as e:
        return {
            "error": f"Failed to convert currency from {from_curr} to {to_curr}: {str(e)}"
        }
