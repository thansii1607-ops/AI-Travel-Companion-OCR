import re


def clean_text(text):
    """Clean OCR extracted text."""
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_date(text):
    """Extract date from OCR text."""

    patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b",
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0)

    return "Not detected"


def extract_amount(text):
    """Extract amount from bill or booking document."""

    patterns = [
        r"(?:total|amount|grand total|fare|price)\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"(?:₹|Rs\.?|INR)\s*([\d,]+(?:\.\d{1,2})?)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

    return "Not detected"


def extract_passenger(text):
    """Extract passenger / customer name."""

    patterns = [
        r"(?:passenger\s*name|passenger|traveller|traveler)\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,40})",
        r"(?:customer\s*name|customer)\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,40})",
        r"(?:guest\s*name|guest)\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,40})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


def extract_route(text):
    """Extract From and To locations."""

    patterns = [
        r"from\s*[:\-]?\s*([A-Za-z .]{2,40})\s+(?:to|->|→)\s*([A-Za-z .]{2,40})",
        r"([A-Za-z .]{2,40})\s*(?:->|→)\s*([A-Za-z .]{2,40})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return {
                "from": match.group(1).strip(),
                "to": match.group(2).strip()
            }

    return {
        "from": "Not detected",
        "to": "Not detected"
    }


def detect_transport_type(text):
    """Detect flight, train or bus document."""

    text_lower = text.lower()

    flight_keywords = [
        "flight",
        "airlines",
        "airways",
        "boarding pass",
        "departure",
        "arrival",
        "gate",
        "pnr"
    ]

    train_keywords = [
        "train",
        "railway",
        "irctc",
        "coach",
        "berth",
        "platform",
        "pnr"
    ]

    bus_keywords = [
        "bus",
        "bus ticket",
        "boarding point",
        "dropping point",
        "seat number"
    ]

    flight_score = sum(
        keyword in text_lower for keyword in flight_keywords
    )

    train_score = sum(
        keyword in text_lower for keyword in train_keywords
    )

    bus_score = sum(
        keyword in text_lower for keyword in bus_keywords
    )

    scores = {
        "Flight": flight_score,
        "Train": train_score,
        "Bus": bus_score
    }

    detected_type = max(scores, key=scores.get)

    if scores[detected_type] == 0:
        return "Travel Document"

    return detected_type


def extract_hotel_details(text):
    """Extract hotel booking information."""

    hotel_name = "Not detected"
    room = "Not detected"

    hotel_patterns = [
        r"(?:hotel|property|resort)\s*[:\-]?\s*([A-Za-z0-9 .&'-]{3,50})"
    ]

    room_patterns = [
        r"(?:room|room type)\s*[:\-]?\s*([A-Za-z0-9 .&'-]{2,40})"
    ]

    for pattern in hotel_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            hotel_name = match.group(1).strip()
            break

    for pattern in room_patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            room = match.group(1).strip()
            break

    return {
        "hotel_name": hotel_name,
        "room": room
    }


def extract_travel_info(text):
    """
    Main function to extract travel information.
    """

    text = clean_text(text)

    route = extract_route(text)
    hotel = extract_hotel_details(text)

    travel_info = {
        "document_type": detect_transport_type(text),
        "passenger": extract_passenger(text),
        "travel_date": extract_date(text),
        "from": route["from"],
        "to": route["to"],
        "hotel_name": hotel["hotel_name"],
        "room": hotel["room"],
        "amount": extract_amount(text)
    }

    return travel_info
