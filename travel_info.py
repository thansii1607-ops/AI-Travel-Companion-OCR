import re


# ---------------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------------

def clean_text(text):
    """Clean OCR text without removing useful information."""

    if not text:
        return ""

    text = str(text)

    # Replace common OCR separators
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("|", " ")

    # Remove excessive spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------------------------------
# GENERIC FIELD EXTRACTION
# ---------------------------------------------------------

def extract_field(text, patterns):
    """Extract a field using multiple OCR-friendly patterns."""

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = match.group(1).strip()

            # Clean unwanted trailing characters
            value = re.sub(r"\s{2,}", " ", value)
            value = value.strip(" :-.,|")

            if value:
                return value

    return "Not detected"


# ---------------------------------------------------------
# PASSENGER / CUSTOMER / GUEST
# ---------------------------------------------------------

def extract_passenger(text):
    """Extract passenger, customer or guest name."""

    patterns = [
        r"\bpassenger\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,50}?)(?=\s+(?:pnr|booking|flight|train|bus|date|seat)\b|$)",
        r"\bpassenger\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,50}?)(?=\s+(?:pnr|booking|flight|train|bus|date|seat)\b|$)",
        r"\btravell?er\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,50}?)(?=\s+(?:pnr|booking|flight|train|bus|date|seat)\b|$)",
        r"\bguest\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,50}?)(?=\s+(?:room|hotel|booking|date)\b|$)",
        r"\bcustomer\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,50}?)(?=\s+(?:bill|amount|total|date)\b|$)"
    ]

    return extract_field(text, patterns)


# ---------------------------------------------------------
# DATE
# ---------------------------------------------------------

def extract_date(text):
    """Extract travel / booking / bill date."""

    patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

        r"\b\d{1,2}\s+"
        r"(?:Jan|January|Feb|February|Mar|March|Apr|April|May|"
        r"Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|"
        r"Nov|November|Dec|December)"
        r"\s+\d{2,4}\b",

        r"\b(?:Jan|January|Feb|February|Mar|March|Apr|April|May|"
        r"Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|"
        r"Nov|November|Dec|December)"
        r"\s+\d{1,2},?\s+\d{2,4}\b",

        r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0).strip()

    return "Not detected"


# ---------------------------------------------------------
# TIME
# ---------------------------------------------------------

def extract_time(text):
    """Extract travel time."""

    patterns = [
        r"\b\d{1,2}:\d{2}\s*(?:AM|PM)\b",
        r"\b\d{1,2}:\d{2}\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0).strip()

    return "Not detected"


# ---------------------------------------------------------
# FROM / TO
# ---------------------------------------------------------

def extract_route(text):
    """Extract departure and destination."""

    # Example:
    # From Chennai To Bangalore
    patterns = [
        r"\bfrom\s*[:\-]?\s*([A-Za-z][A-Za-z .]{1,40}?)\s+to\s*[:\-]?\s*([A-Za-z][A-Za-z .]{1,40}?)(?=\s+(?:date|time|flight|train|bus|pnr|seat|booking)\b|$)",

        # Example:
        # Chennai -> Bangalore
        r"\b([A-Za-z][A-Za-z .]{1,35}?)\s*(?:->|→)\s*([A-Za-z][A-Za-z .]{1,35}?)(?=\s+(?:date|time|flight|train|bus|pnr|seat|booking)\b|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            from_place = match.group(1).strip(" :-.,")
            to_place = match.group(2).strip(" :-.,")

            if from_place and to_place:
                return {
                    "from": from_place,
                    "to": to_place
                }

    # Individual FROM / TO fields
    from_patterns = [
        r"\bfrom\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})",
        r"\bdeparture\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})",
        r"\borigin\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})"
    ]

    to_patterns = [
        r"\bto\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})",
        r"\bdestination\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})",
        r"\barrival\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})"
    ]

    from_place = extract_field(text, from_patterns)
    to_place = extract_field(text, to_patterns)

    return {
        "from": from_place,
        "to": to_place
    }


# ---------------------------------------------------------
# PNR
# ---------------------------------------------------------

def extract_pnr(text):
    """Extract PNR / booking reference."""

    patterns = [
        r"\bpnr\s*(?:number|no|#)?\s*[:\-]?\s*([A-Z0-9]{5,15})",
        r"\bbooking\s*(?:reference|ref|id)?\s*[:\-]?\s*([A-Z0-9]{5,15})",
        r"\bconfirmation\s*(?:number|no)?\s*[:\-]?\s*([A-Z0-9]{5,15})"
    ]

    return extract_field(text, patterns)


# ---------------------------------------------------------
# SEAT
# ---------------------------------------------------------

def extract_seat(text):
    """Extract seat number."""

    patterns = [
        r"\bseat\s*(?:number|no|#)?\s*[:\-]?\s*([A-Z0-9]{1,6})",
        r"\bberth\s*(?:number|no|#)?\s*[:\-]?\s*([A-Z0-9]{1,6})"
    ]

    return extract_field(text, patterns)


# ---------------------------------------------------------
# FLIGHT NUMBER
# ---------------------------------------------------------

def extract_flight_number(text):
    """Extract airline flight number."""

    patterns = [
        r"\bflight\s*(?:number|no)?\s*[:\-]?\s*([A-Z]{1,3}\s?\d{2,5})",
        r"\b([A-Z]{2}\s?\d{2,5})\b"
    ]

    return extract_field(text, patterns)


# ---------------------------------------------------------
# TRAIN NUMBER
# ---------------------------------------------------------

def extract_train_number(text):
    """Extract train number."""

    patterns = [
        r"\btrain\s*(?:number|no)?\s*[:\-]?\s*(\d{4,6})",
        r"\btrain\s*[:\-]?\s*([A-Za-z0-9 -]{3,40})"
    ]

    return extract_field(text, patterns)


# ---------------------------------------------------------
# BUS DETAILS
# ---------------------------------------------------------

def extract_bus_details(text):
    """Extract bus operator / bus number."""

    operator_patterns = [
        r"\bbus\s*(?:operator|name)\s*[:\-]?\s*([A-Za-z0-9 .&'-]{2,50})",
        r"\boperator\s*[:\-]?\s*([A-Za-z0-9 .&'-]{2,50})"
    ]

    number_patterns = [
        r"\bbus\s*(?:number|no|#)\s*[:\-]?\s*([A-Z0-9-]{3,15})"
    ]

    return {
        "operator": extract_field(text, operator_patterns),
        "number": extract_field(text, number_patterns)
    }


# ---------------------------------------------------------
# HOTEL DETAILS
# ---------------------------------------------------------

def extract_hotel_details(text):
    """Extract hotel and room information."""

    hotel_patterns = [
        r"\bhotel\s*(?:name)?\s*[:\-]?\s*([A-Za-z0-9 .&'-]{2,60})(?=\s+(?:room|check|date|guest|booking)\b|$)",
        r"\bproperty\s*[:\-]?\s*([A-Za-z0-9 .&'-]{2,60})(?=\s+(?:room|check|date|guest|booking)\b|$)",
        r"\bresort\s*[:\-]?\s*([A-Za-z0-9 .&'-]{2,60})(?=\s+(?:room|check|date|guest|booking)\b|$)"
    ]

    room_patterns = [
        r"\broom\s*(?:type|number|no)?\s*[:\-]?\s*([A-Za-z0-9 .&'-]{1,40})",
        r"\broom\s*[:\-]?\s*([A-Za-z0-9 .&'-]{1,40})"
    ]

    return {
        "hotel_name": extract_field(text, hotel_patterns),
        "room": extract_field(text, room_patterns)
    }


# ---------------------------------------------------------
# AMOUNT
# ---------------------------------------------------------

def extract_amount(text):
    """Extract total / fare / bill amount."""

    patterns = [
        r"\bgrand\s*total\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"\btotal\s*amount\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"\btotal\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"\bamount\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"\b(?:fare|price)\s*[:\-]?\s*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"(?:₹|rs\.?|inr)\s*([\d,]+(?:\.\d{1,2})?)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            amount = match.group(1).replace(",", "")
            return amount

    return "Not detected"


# ---------------------------------------------------------
# DOCUMENT TYPE
# ---------------------------------------------------------

def detect_document_type(text):
    """Detect the type of travel document."""

    text_lower = text.lower()

    scores = {
        "Flight Ticket": 0,
        "Train Ticket": 0,
        "Bus Ticket": 0,
        "Hotel Booking": 0,
        "Restaurant Bill": 0
    }

    # Flight
    flight_words = [
        "flight",
        "airlines",
        "airways",
        "boarding pass",
        "departure",
        "arrival",
        "gate",
        "flight number"
    ]

    for word in flight_words:
        if word in text_lower:
            scores["Flight Ticket"] += 1

    # Train
    train_words = [
        "train",
        "railway",
        "irctc",
        "coach",
        "berth",
        "platform",
        "train number"
    ]

    for word in train_words:
        if word in text_lower:
            scores["Train Ticket"] += 1

    # Bus
    bus_words = [
        "bus ticket",
        "bus number",
        "boarding point",
        "dropping point",
        "bus operator"
    ]

    for word in bus_words:
        if word in text_lower:
            scores["Bus Ticket"] += 1

    # Hotel
    hotel_words = [
        "hotel",
        "room",
        "check-in",
        "check in",
        "check-out",
        "check out",
        "guest",
        "reservation"
    ]

    for word in hotel_words:
        if word in text_lower:
            scores["Hotel Booking"] += 1

    # Restaurant
    restaurant_words = [
        "restaurant",
        "food",
        "tax",
        "gst",
        "subtotal",
        "bill",
        "table",
        "waiter"
    ]

    for word in restaurant_words:
        if word in text_lower:
            scores["Restaurant Bill"] += 1

    detected_type = max(scores, key=scores.get)

    if scores[detected_type] == 0:
        return "Travel Document"

    return detected_type


# ---------------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------------

def extract_travel_info(text, document_type=None):
    """
    Main travel information extraction function.

    Compatible with:
        extract_travel_info(text)
    and:
        extract_travel_info(text, document_type)
    """

    text = clean_text(text)

    if not text:
        return {
            "document_type": document_type or "Travel Document",
            "passenger": "Not detected",
            "travel_date": "Not detected",
            "travel_time": "Not detected",
            "from": "Not detected",
            "to": "Not detected",
            "pnr": "Not detected",
            "seat": "Not detected",
            "flight_number": "Not detected",
            "train_number": "Not detected",
            "bus_operator": "Not detected",
            "bus_number": "Not detected",
            "hotel_name": "Not detected",
            "room": "Not detected",
            "amount": "Not detected"
        }

    # Use document type from app.py if provided
    if not document_type:
        document_type = detect_document_type(text)

    route = extract_route(text)
    hotel = extract_hotel_details(text)
    bus = extract_bus_details(text)

    return {
        "document_type": document_type,
        "passenger": extract_passenger(text),
        "travel_date": extract_date(text),
        "travel_time": extract_time(text),

        "from": route["from"],
        "to": route["to"],

        "pnr": extract_pnr(text),
        "seat": extract_seat(text),

        "flight_number": extract_flight_number(text),
        "train_number": extract_train_number(text),

        "bus_operator": bus["operator"],
        "bus_number": bus["number"],

        "hotel_name": hotel["hotel_name"],
        "room": hotel["room"],

        "amount": extract_amount(text)
    }


    
 
