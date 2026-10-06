import re


def clean_text(text):
    text = text.replace("|", " ")
    text = text.replace("_", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def find_value(text, patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return "Not detected"


def extract_travel_info(text, document_type="Unknown Document"):

    original_text = text
    text = clean_text(text)

    info = {

        # ==============================
        # COMMON
        # ==============================

        "Passenger Name": "Not detected",
        "Travel Date": "Not detected",
        "Travel Time": "Not detected",
        "From": "Not detected",
        "To": "Not detected",
        "PNR / Booking Number": "Not detected",

        # ==============================
        # FLIGHT
        # ==============================

        "Flight Number": "Not detected",
        "Seat": "Not detected",
        "Gate": "Not detected",
        "Boarding Time": "Not detected",

        # ==============================
        # TRAIN
        # ==============================

        "Train Number": "Not detected",
        "Train Name": "Not detected",
        "Coach": "Not detected",
        "Berth": "Not detected",
        "Platform": "Not detected",

        # ==============================
        # BUS
        # ==============================

        "Bus Number": "Not detected",
        "Boarding Point": "Not detected",
        "Drop Point": "Not detected",
        "Bus Seat": "Not detected",

        # ==============================
        # HOTEL
        # ==============================

        "Hotel Name": "Not detected",
        "Check-in": "Not detected",
        "Check-out": "Not detected",
        "Room Number": "Not detected",
        "Guest Name": "Not detected",
        "Hotel Amount": "Not detected",

        # ==============================
        # RESTAURANT
        # ==============================

        "Restaurant Name": "Not detected",
        "Bill Date": "Not detected",
        "Total Amount": "Not detected",
        "GST Amount": "Not detected"

    }

    # =====================================================
    # PASSENGER / GUEST NAME
    # =====================================================

    passenger_patterns = [

        r"PASSANGER\s+NAME\s*:\s*([A-Z][A-Z ]{2,40}?)(?=\s+(?:DATE|TIME|FLIGHT|SEAT|GATE|BOARDING))",

        r"PASSENGER\s+NAME\s*:\s*([A-Z][A-Z ]{2,40}?)(?=\s+(?:DATE|TIME|FLIGHT|SEAT|GATE|BOARDING))",

        r"PASSANGER\s+NAME\s*[:\-]?\s*\n?\s*([A-Z][A-Z ]{2,40})",

        r"PASSENGER\s+NAME\s*[:\-]?\s*\n?\s*([A-Z][A-Z ]{2,40})",

        r"TRAVELLER\s*[:\-]?\s*([A-Za-z][A-Za-z ]{2,40})",

        r"TRAVELER\s*[:\-]?\s*([A-Za-z][A-Za-z ]{2,40})",

        r"GUEST\s+NAME\s*[:\-]?\s*([A-Za-z][A-Za-z ]{2,40})"
    ]

    for pattern in passenger_patterns:

        match = re.search(
            pattern,
            original_text,
            re.IGNORECASE
        )

        if match:

            name = match.group(1).strip()

            name = re.sub(
                r"\b(DATE|TIME|FLIGHT|SEAT|GATE|BOARDING)\b.*",
                "",
                name,
                flags=re.IGNORECASE
            )

            name = re.sub(
                r"\s+",
                " ",
                name
            ).strip()

            if len(name) >= 3:

                info["Passenger Name"] = name
                info["Guest Name"] = name

                break

    # =====================================================
    # DATE
    # =====================================================

    date_patterns = [

        r"\b\d{1,2}(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\b",

        r"\b\d{1,2}0CT\b",

        r"\b\d{1,2}\s+(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\b",

        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

        r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b",

        r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}\b"
    ]

    for pattern in date_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            detected_date = match.group(0).strip()

            if re.match(
                r"^\d{1,2}0CT$",
                detected_date,
                re.IGNORECASE
            ):

                detected_date = (
                    detected_date[:2] + "OCT"
                )

            info["Travel Date"] = detected_date
            info["Bill Date"] = detected_date

            break

    # =====================================================
    # TIME
    # =====================================================

    time_patterns = [

        r"\b\d{1,2}[:.]\d{2}\s*(?:AM|PM|am|pm)?\b",

        r"\b\d{1,2}\s*(?:AM|PM|am|pm)\b"
    ]

    times = []

    for pattern in time_patterns:

        times.extend(
            re.findall(
                pattern,
                text
            )
        )

    if times:

        info["Travel Time"] = times[0].strip()

    # =====================================================
    # FROM / TO
    # =====================================================

    route_pattern = (
        r"\b([A-Z][A-Z ]{2,30})"
        r"\s*[-–—]\s*"
        r"([A-Z][A-Z ]{2,30})\b"
    )

    route_match = re.search(
        route_pattern,
        original_text
    )

    if route_match:

        info["From"] = route_match.group(1).strip()
        info["To"] = route_match.group(2).strip()

    if info["From"] == "Not detected":

        info["From"] = find_value(
            text,
            [
                r"\bFROM\s*[:\-]\s*([A-Za-z][A-Za-z ]{2,40})"
            ]
        )

    if info["To"] == "Not detected":

        info["To"] = find_value(
            text,
            [
                r"\bTO\s*[:\-]\s*([A-Za-z][A-Za-z ]{2,40})"
            ]
        )

    # =====================================================
    # PNR / BOOKING
    # =====================================================

    pnr_patterns = [

        r"(?:PNR|P\.N\.R)\s*(?:NO|NUMBER|NUM)?\s*[:\-]?\s*([A-Z0-9]{5,15})",

        r"(?:BOOKING\s*(?:ID|NO|NUMBER))\s*[:\-]?\s*([A-Z0-9]{5,20})",

        r"(?:RESERVATION\s*(?:ID|NO|NUMBER))\s*[:\-]?\s*([A-Z0-9]{5,20})"
    ]

    info["PNR / Booking Number"] = find_value(
        text,
        pnr_patterns
    )

    # =====================================================
    # FLIGHT DETAILS
    # =====================================================

    flight_match = re.search(
        r"\bFLIGHT\s*[:\-]?\s*([A-Z]{2,3}\d{2,5})\b",
        original_text,
        re.IGNORECASE
    )

    if flight_match:

        info["Flight Number"] = (
            flight_match.group(1).strip()
        )

    else:

        flight_match = re.search(
            r"\b[A-Z]{2,3}\d{2,5}\b",
            original_text
        )

        if flight_match:

            info["Flight Number"] = (
                flight_match.group(0)
            )

    # =====================================================
    # SEAT
    # =====================================================

    info["Seat"] = find_value(
        original_text,
        [
            r"\bSEAT\s*[:\-]?\s*([A-Z]?\d{1,3}[A-Z]?)"
        ]
    )

    if info["Seat"] == "Not detected":

        seat_match = re.search(
            r"\b\d{1,3}[A-Z]\b",
            original_text
        )

        if seat_match:

            if seat_match.group(0) != "B2":

                info["Seat"] = (
                    seat_match.group(0)
                )

    # =====================================================
    # GATE
    # =====================================================

    info["Gate"] = find_value(
        original_text,
        [
            r"\bGATE\s*[:\-]?\s*([A-Z]?\d{1,3})"
        ]
    )

    # =====================================================
    # BOARDING TIME
    # =====================================================

    info["Boarding Time"] = find_value(
        original_text,
        [
            r"BOARDING\s+TIME\s*[:\-]?\s*(\d{1,2}[:.]\d{2}\s*(?:AM|PM)?)"
        ]
    )

    # =====================================================
    # TRAIN DETAILS
    # =====================================================

    info["Train Number"] = find_value(
        original_text,
        [
            r"(?:TRAIN\s*(?:NO|NUMBER))\s*[:\-]?\s*(\d{4,6})",
            r"\b(\d{5})\b"
        ]
    )

    info["Train Name"] = find_value(
        original_text,
        [
            r"TRAIN\s+NAME\s*[:\-]?\s*([A-Za-z][A-Za-z ]{3,50})"
        ]
    )

    info["Coach"] = find_value(
        original_text,
        [
            r"(?:COACH)\s*[:\-]?\s*([A-Z]{1,3}\d{0,2})"
        ]
    )

    info["Berth"] = find_value(
        original_text,
        [
            r"(?:BERTH|BIRTH)\s*[:\-]?\s*([A-Z]?\d{1,3})"
        ]
    )

    info["Platform"] = find_value(
        original_text,
        [
            r"PLATFORM\s*[:\-]?\s*([A-Z]?\d{1,3})"
        ]
    )

    # =====================================================
    # BUS DETAILS
    # =====================================================

    info["Bus Number"] = find_value(
        original_text,
        [
            r"(?:BUS\s*(?:NO|NUMBER))\s*[:\-]?\s*([A-Z0-9\-]{3,15})"
        ]
    )

    info["Boarding Point"] = find_value(
        original_text,
        [
            r"BOARDING\s+POINT\s*[:\-]?\s*([A-Za-z][A-Za-z ]{2,50})"
        ]
    )

    info["Drop Point"] = find_value(
        original_text,
        [
            r"(?:DROP\s+POINT|DROP)\s*[:\-]?\s*([A-Za-z][A-Za-z ]{2,50})"
        ]
    )

    info["Bus Seat"] = find_value(
        original_text,
        [
            r"(?:SEAT|SEAT\s+NO)\s*[:\-]?\s*([A-Z]?\d{1,3}[A-Z]?)"
        ]
    )

    # =====================================================
    # HOTEL DETAILS
    # =====================================================

    info["Hotel Name"] = find_value(
        original_text,
        [
            r"HOTEL\s*[:\-]?\s*([A-Za-z][A-Za-z0-9 &\-]{2,60})"
        ]
    )

    info["Check-in"] = find_value(
        original_text,
        [
            r"CHECK[\-\s]?IN\s*[:\-]?\s*([A-Za-z0-9,\/\-\s]{3,30})"
        ]
    )

    info["Check-out"] = find_value(
        original_text,
        [
            r"CHECK[\-\s]?OUT\s*[:\-]?\s*([A-Za-z0-9,\/\-\s]{3,30})"
        ]
    )

    info["Room Number"] = find_value(
        original_text,
        [
            r"ROOM\s*(?:NO|NUMBER)?\s*[:\-]?\s*([A-Z]?\d{1,5})"
        ]
    )

    # =====================================================
    # HOTEL AMOUNT
    # =====================================================

    hotel_amount_patterns = [

        r"(?:HOTEL\s+AMOUNT|ROOM\s+CHARGE|ROOM\s+RATE)"
        r"\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)",

        r"(?:TOTAL\s+AMOUNT|TOTAL|GRAND\s+TOTAL)"
        r"\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)"
    ]

    info["Hotel Amount"] = find_value(
        original_text,
        hotel_amount_patterns
    )

    # =====================================================
    # RESTAURANT DETAILS
    # =====================================================

    info["Restaurant Name"] = find_value(
        original_text,
        [
            r"RESTAURANT\s*[:\-]?\s*([A-Za-z][A-Za-z0-9 &\-]{2,60})"
        ]
    )

    # =====================================================
    # TOTAL AMOUNT
    # =====================================================

    total_amount_patterns = [

        r"(?:GRAND\s+TOTAL)"
        r"\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)",

        r"(?:TOTAL\s+AMOUNT)"
        r"\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)",

        r"(?:AMOUNT\s+PAYABLE)"
        r"\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)",

        r"\bTOTAL\b"
        r"\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)"
    ]

    info["Total Amount"] = find_value(
        original_text,
        total_amount_patterns
    )

    # =====================================================
    # GST AMOUNT
    # =====================================================

    gst_patterns = [

        r"GST\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)",

        r"GST\s+AMOUNT\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*"
        r"([0-9,]+(?:\.[0-9]{1,2})?)"
    ]

    info["GST Amount"] = find_value(
        original_text,
        gst_patterns
    )

    # =====================================================
    # CLEAN RESULTS
    # =====================================================

    for key in info:

        if isinstance(info[key], str):

            info[key] = info[key].strip()

            info[key] = re.sub(
                r"\s{2,}",
                " ",
                info[key]
            )

    return info