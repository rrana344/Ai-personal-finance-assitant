import re
from pathlib import Path


def extract_receipt_data(path: Path) -> dict:
    text = ""
    try:
        from PIL import Image
        import pytesseract

        text = pytesseract.image_to_string(Image.open(path))
    except Exception:
        text = "OCR engine unavailable. Enter details manually."

    amount = _extract_amount(text)
    category = _detect_category(text)
    return {"raw_text": text, "amount": amount, "category": category, "type": "expense"}


def _extract_amount(text: str) -> float | None:
    matches = re.findall(r"(?:total|amount|paid)?\s*(?:rs\.?|inr|\$)?\s*(\d+(?:\.\d{1,2})?)", text, flags=re.I)
    values = [float(match) for match in matches]
    return max(values) if values else None


def _detect_category(text: str) -> str:
    lowered = text.lower()
    mapping = {
        "Food": ["restaurant", "cafe", "grocery", "food"],
        "Travel": ["uber", "flight", "hotel", "train", "taxi"],
        "Bills": ["electric", "internet", "mobile", "utility"],
        "Shopping": ["store", "mall", "amazon", "shopping"],
        "Health": ["pharmacy", "clinic", "hospital"],
    }
    for category, keywords in mapping.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "Bills"
