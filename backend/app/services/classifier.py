"""Category and Merchant Entity Classifier."""

import re
from typing import Tuple


class MerchantClassifier:
    """Classifies merchant raw text into cleaned merchant name, category, and confidence score."""

    CATEGORY_RULES = {
        "Electronics": ["apple", "amazon", "croma", "reliance digital", "samsung", "best buy", "dell", "lenovo"],
        "Dining & Food": ["swiggy", "zomato", "mcdonalds", "starbucks", "dominos", "kfc", "restaurant", "cafe", "diner"],
        "Groceries": ["blinkit", "zepto", "bigbasket", "walmart", "supermarket", "grocery", "d-mart", "spensers"],
        "Utilities & Bills": ["electric", "water", "gas", "airtel", "jio", "broadband", "power", "utility"],
        "Travel & Transport": ["uber", "ola", "makemytrip", "flight", "airline", "irctc", "railway", "taxi", "petrol", "shell"],
        "Entertainment": ["netflix", "spotify", "bookmyshow", "steam", "playstation", "prime video", "cinema"],
        "Shopping & Apparel": ["zara", "h&m", "myntra", "nike", "adidas", "shopping", "store"],
        "Healthcare": ["pharmacy", "apollo", "hospital", "clinic", "medplus", "doctor"],
    }

    @classmethod
    def classify(cls, raw_merchant: str) -> Tuple[str, str, float]:
        """Returns (clean_merchant, category, confidence_score)."""
        clean = raw_merchant.strip()
        # Remove common transaction prefix noise
        clean = re.sub(r"^(POS|UPI|INF|NEFT|RTGS|IMPS|DEBIT|CREDIT|CARD|TST\*)\s*", "", clean, flags=re.IGNORECASE).strip()
        
        # Extract brand name if present
        lower_clean = clean.lower()

        for category, keywords in cls.CATEGORY_RULES.items():
            for kw in keywords:
                if kw in lower_clean:
                    # Clean merchant title
                    matched_name = kw.title()
                    return clean or matched_name, category, 0.95

        # Fallback category based on simple word heuristic or General Expense
        return clean or "Unknown Merchant", "General & Miscellaneous", 0.75
