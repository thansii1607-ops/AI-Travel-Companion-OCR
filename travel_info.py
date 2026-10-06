
        import re


# =========================================================
# CLEAN OCR TEXT
# =========================================================

def clean_text(text):
    if not text:
        return ""

    text = str(text)
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("|", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# DATE
# =========================================================

def extract_date(text):
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


# =========================================================
# TIME
# =========================================================

def extract_time(text):
    patterns = [
        r"\b\d{1,2}:\d{2}\s*(?:AM|PM)\b",
        r"\b\d{1,2}:\d{2}\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(0).strip()

    return "Not detected"


# =========================================================
# PASSENGER
# =========================================================

def extract_passenger(text):
    patterns = [
        r"\bpassenger\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,45})",
        r"\bpassenger\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,45})",
        r"\btraveller\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,45})",
        r"\btraveler\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,45})",
        r"\bguest\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,45})",
        r"\bcustomer\s*name\s*[:\-]?\s*([A-Za-z][A-Za-z .]{2,45})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = match.group(1).strip()

            # Stop at common next fields
            value = re.split(
                r"\s+(?:PNR|booking|flight|train|bus|date|seat|time)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            if len(value) >= 3:
                return value.strip()

    return "Not detected"


# =========================================================
# FROM / TO
# =========================================================

def extract_route(text):
    from_place = "Not detected"
    to_place = "Not detected"

    patterns = [
        r"\bfrom\s*[:\-]?\s*([A-Za-z][A-Za-z .]{1,40}?)\s+to\s*[:\-]?\s*([A-Za-z][A-Za-z .]{1,40}?)(?=\s+(?:date|time|flight|train|bus|pnr|seat|booking)\b|$)",

        r"\bfrom\s*[:\-]?\s*([A-Za-z][A-Za-z .]{1,40}?)\s*(?:→|->)\s*([A-Za-z][A-Za-z .]{1,40}?)(?=\s+(?:date|time|flight|train|bus|pnr|seat|booking)\b|$)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            from_place = match.group(1).strip(" :-.,")
            to_place = match.group(2).strip(" :-.,")
            break

    if from_place == "Not detected":
        patterns_from = [
            r"\bdeparture\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})",
            r"\borigin\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})"
        ]

        for pattern in patterns_from:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                from_place = match.group(1).strip()
                break

    if to_place == "Not detected":
        patterns_to = [
            r"\bdestination\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})",
            r"\barrival\s*[:\-]\s*([A-Za-z][A-Za-z .]{2,40})"
        ]

        for pattern in patterns_to:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                to_place = match.group(1).strip()
                break

    return from_place, to_place


# =========================================================
# PNR / BOOKING
# =========================================================

def extract_pnr(text):
    patterns = [
        r"\bPNR\s*(?:NUMBER|NO|#)?\s*[:\-]?\s*([A-Z0-9]{5,15})",
        r"\bBOOKING\s*(?:REFERENCE|REF|ID|NUMBER|NO)?\s*[:\-]?\s*([A-Z0-9]{5,20})",
        r"\bCONFIRMATION\s*(?:NUMBER|NO)?\s*[:\-]?\s*([A-Z0-9]{5,20})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# SEAT
# =========================================================

def extract_seat(text):
    patterns = [
        r"\bSEAT\s*(?:NUMBER|NO|#)?\s*[:\-]?\s*([A-Z0-9]{1,8})",
        r"\bBERTH\s*(?:NUMBER|NO|#)?\s*[:\-]?\s*([A-Z0-9]{1,8})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# GATE
# =========================================================

def extract_gate(text):
    patterns = [
        r"\bGATE\s*(?:NUMBER|NO|#)?\s*[:\-]?\s*([A-Z0-9-]{1,8})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# FLIGHT NUMBER
# =========================================================

def extract_flight_number(text):
    patterns = [
        r"\bFLIGHT\s*(?:NUMBER|NO)?\s*[:\-]?\s*([A-Z]{1,3}\s?\d{2,5})",
        r"\b([A-Z]{2}\s?\d{2,5})\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# TRAIN NUMBER
# =========================================================

def extract_train_number(text):
    patterns = [
        r"\bTRAIN\s*(?:NUMBER|NO)?\s*[:\-]?\s*(\d{4,6})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# COACH
# =========================================================

def extract_coach(text):
    patterns = [
        r"\bCOACH\s*[:\-]?\s*([A-Z0-9]{1,8})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# BERTH
# =========================================================

def extract_berth(text):
    patterns = [
        r"\bBERTH\s*[:\-]?\s*([A-Z0-9]{1,8})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# BUS NUMBER
# =========================================================

def extract_bus_number(text):
    patterns = [
        r"\bBUS\s*(?:NUMBER|NO|#)\s*[:\-]?\s*([A-Z0-9-]{3,15})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# BOARDING POINT
# =========================================================

def extract_boarding_point(text):
    patterns = [
        r"\bBOARDING\s*POINT\s*[:\-]?\s*([A-Za-z0-9 .,&'-]{2,50})",
        r"\bBOARDING\s*[:\-]?\s*([A-Za-z0-9 .,&'-]{2,50})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# DROP POINT
# =========================================================

def extract_drop_point(text):
    patterns = [
        r"\bDROPPING\s*POINT\s*[:\-]?\s*([A-Za-z0-9 .,&'-]{2,50})",
        r"\bDROP\s*POINT\s*[:\-]?\s*([A-Za-z0-9 .,&'-]{2,50})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# HOTEL NAME
# =========================================================

def extract_hotel_name(text):
    patterns = [
        r"\bHOTEL\s*NAME\s*[:\-]?\s*([A-Za-z0-9 .&'-]{2,60})",
        r"\bPROPERTY\s*[:\-]?\s*([A-Za-z0-9 .&'-]{2,60})",
        r"\bRESORT\s*[:\-]?\s*([A-Za-z0-9 .&'-]{2,60})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = match.group(1).strip()

            value = re.split(
                r"\s+(?:room|guest|booking|check|date)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            return value.strip()

    return "Not detected"


# =========================================================
# ROOM
# =========================================================

def extract_room(text):
    patterns = [
        r"\bROOM\s*(?:TYPE|NUMBER|NO)?\s*[:\-]?\s*([A-Za-z0-9 .&'-]{1,40})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# CHECK-IN
# =========================================================

def extract_checkin(text):
    patterns = [
        r"\bCHECK[\s-]*IN\s*[:\-]?\s*(.{3,30})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = match.group(1).strip()

            date_match = re.search(
                r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
                r"\d{1,2}\s+[A-Za-z]+\s+\d{2,4}",
                value
            )

            if date_match:
                return date_match.group(0)

    return "Not detected"


# =========================================================
# CHECK-OUT
# =========================================================

def extract_checkout(text):
    patterns = [
        r"\bCHECK[\s-]*OUT\s*[:\-]?\s*(.{3,30})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = match.group(1).strip()

            date_match = re.search(
                r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
                r"\d{1,2}\s+[A-Za-z]+\s+\d{2,4}",
                value
            )

            if date_match:
                return date_match.group(0)

    return "Not detected"


# =========================================================
# RESTAURANT BILL NUMBER
# =========================================================

def extract_bill_number(text):
    patterns = [
        r"\bBILL\s*(?:NO|NUMBER|#)?\s*[:.]?\s*([A-Z0-9/-]{4,30})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


# =========================================================
# SUBTOTAL
# =========================================================

def extract_subtotal(text):
    patterns = [
        r"\bSUBTOTAL\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).replace(",", "")

    return "Not detected"


# =========================================================
# GST
# =========================================================

def extract_gst(text):
    total = 0.0
    found = False

    patterns = [
        r"\bCGST\s*(?:\([^)]+\))?\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"\bSGST\s*(?:\([^)]+\))?\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"\bGST\s*(?:AMOUNT)?\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for value in matches:
            try:
                total += float(value.replace(",", ""))
                found = True
            except ValueError:
                pass

    if found:
        return f"{total:.2f}"

    return "Not detected"


# =========================================================
# GRAND TOTAL / HOTEL AMOUNT
# =========================================================

def extract_total_amount(text):
    patterns = [
        r"\bGRAND\s*TOTAL\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"\bTOTAL\s*AMOUNT\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)",
        r"\bTOTAL\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).replace(",", "")

    return "Not detected"


# =========================================================
# PAYMENT MODE
# =========================================================

def extract_payment_mode(text):
    patterns = [
        r"\bPAYMENT\s*MODE\s*[:\-]?\s*([A-Za-z ]{2,30})",
        r"\bPAYMENT\s*METHOD\s*[:\-]?\s*([A-Za-z ]{2,30})"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = match.group(1).strip()

            value = re.split(
                r"\s+(?:THANK|VISIT|STATUS)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            return value.strip()

    return "Not detected"


# =========================================================
# PAYMENT STATUS
# =========================================================

def extract_payment_status(text):
    patterns = [
        r"\bPAYMENT\s*STATUS\s*[:\-]?\s*(PAID|UNPAID|PENDING|SUCCESS|FAILED)",
        r"\b(PAID|UNPAID|PENDING|SUCCESS|FAILED)\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).upper()

    return "Not detected"


# =========================================================
# DOCUMENT TYPE FALLBACK
# =========================================================

def detect_local_document_type(text):
    lower = text.lower()

    restaurant_words = [
        "restaurant",
        "subtotal",
        "cgst",
        "sgst",
        "grand total",
        "payment mode",
        "table no",
        "order type"
    ]

    hotel_words = [
        "hotel",
        "check-in",
        "check in",
        "check-out",
        "check out",
        "room",
        "guest"
    ]

    flight_words = [
        "flight",
        "airlines",
        "boarding pass",
        "gate",
        "departure",
        "arrival"
    ]

    train_words = [
        "train",
        "railway",
        "irctc",
        "coach",
        "berth",
        "platform"
    ]

    bus_words = [
        "bus ticket",
        "boarding point",
        "dropping point",
        "bus operator"
    ]

    scores = {
        "Restaurant Bill": sum(x in lower for x in restaurant_words),
        "Hotel Booking": sum(x in lower for x in hotel_words),
        "Flight Ticket": sum(x in lower for x in flight_words),
        "Train Ticket": sum(x in lower for x in train_words),
        "Bus Ticket": sum(x in lower for x in bus_words)
    }

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "Travel Document"

    return best


# =========================================================
# MAIN FUNCTION
# =========================================================

def extract_travel_info(text, document_type=None):

    text = clean_text(text)

    if not text:
        return {
            "Passenger Name": "Not detected",
            "Travel Date": "Not detected",
            "Travel Time": "Not detected",
            "From": "Not detected",
            "To": "Not detected",
            "PNR / Booking Number": "Not detected",
            "Flight Number": "Not detected",
            "Seat": "Not detected",
            "Gate": "Not detected",
            "Boarding Time": "Not detected",
            "Train Number": "Not detected",
            "Coach": "Not detected",
            "Berth": "Not detected",
            "Bus Number": "Not detected",
            "Boarding Point": "Not detected",
            "Drop Point": "Not detected",
            "Hotel Name": "Not detected",
            "Room": "Not detected",
            "Check-in": "Not detected",
            "Check-out": "Not detected",
            "Hotel Amount": "Not detected",
            "Bill Number": "Not detected",
            "Subtotal": "Not detected",
            "GST Amount": "Not detected",
            "Total Amount": "Not detected",
            "Payment Mode": "Not detected",
            "Payment Status": "Not detected"
        }

    if not document_type or document_type == "Unknown":
        document_type = detect_local_document_type(text)

    from_place, to_place = extract_route(text)

    result = {
        "Passenger Name": extract_passenger(text),
        "Travel Date": extract_date(text),
        "Travel Time": extract_time(text),

        "From": from_place,
        "To": to_place,

        "PNR / Booking Number": extract_pnr(text),

        "Flight Number": extract_flight_number(text),
        "Seat": extract_seat(text),
        "Gate": extract_gate(text),
        "Boarding Time": extract_time(text),

        "Train Number": extract_train_number(text),
        "Coach": extract_coach(text),
        "Berth": extract_berth(text),

        "Bus Number": extract_bus_number(text),
        "Boarding Point": extract_boarding_point(text),
        "Drop Point": extract_drop_point(text),

        "Hotel Name": extract_hotel_name(text),
        "Room": extract_room(text),
        "Check-in": extract_checkin(text),
        "Check-out": extract_checkout(text),

        "Hotel Amount": extract_total_amount(text),

        "Bill Number": extract_bill_number(text),
        "Subtotal": extract_subtotal(text),
        "GST Amount": extract_gst(text),
        "Total Amount": extract_total_amount(text),

        "Payment Mode": extract_payment_mode(text),
        "Payment Status": extract_payment_status(text)
    }

    # Restaurant bill should not show travel route
    if document_type == "Restaurant Bill":
        result["From"] = "Not applicable"
        result["To"] = "Not applicable"
        result["Passenger Name"] = "Dine In Guest"

    return result   

            

