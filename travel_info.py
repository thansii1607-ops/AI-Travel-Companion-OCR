import re


# =========================================================
# COMMON HELPERS
# =========================================================

NOT_DETECTED = "Not detected"


def clean_text(text):
    if not text:
        return ""

    text = str(text)

    text = text.replace("\r", "\n")
    text = text.replace("|", " ")

    # Keep line structure because some documents
    # have important information on separate lines.
    lines = []

    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()

        if line:
            lines.append(line)

    return "\n".join(lines).strip()


def flat_text(text):
    return re.sub(r"\s+", " ", text).strip()


def clean_value(value):
    if not value:
        return NOT_DETECTED

    value = re.sub(r"\s+", " ", value).strip()
    value = value.strip(" :-.,|")

    return value if value else NOT_DETECTED


# =========================================================
# DATE EXTRACTION
# =========================================================

def extract_all_dates(text):
    patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

        r"\b\d{1,2}\.\d{1,2}\.\d{2,4}\b",

        r"\b\d{1,2}\s+"
        r"(?:Jan|January|Feb|February|Mar|March|Apr|April|May|"
        r"Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|"
        r"Nov|November|Dec|December)"
        r"\s+\d{2,4}\b",

        r"\b(?:Jan|January|Feb|February|Mar|March|Apr|April|May|"
        r"Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|"
        r"Nov|November|Dec|December)"
        r"\s+\d{1,2},?\s+\d{2,4}\b"
    ]

    dates = []

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for value in matches:
            value = value.strip()

            if value not in dates:
                dates.append(value)

    return dates


def extract_date(text):
    dates = extract_all_dates(text)

    if dates:
        return dates[0]

    return NOT_DETECTED


# =========================================================
# TIME EXTRACTION
# =========================================================

def extract_all_times(text):
    patterns = [
        r"\b\d{1,2}:\d{2}\s*(?:AM|PM)\b",
        r"\b\d{1,2}:\d{2}\b"
    ]

    times = []

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for value in matches:
            value = value.strip()

            if value not in times:
                times.append(value)

    return times


def extract_time(text):
    times = extract_all_times(text)

    if times:
        return times[0]

    return NOT_DETECTED


# =========================================================
# PASSENGER NAME
# =========================================================

def extract_passenger(text):
    lines = text.splitlines()

    # Label based extraction
    patterns = [
        r"\bpassenger\s*name\s*[:\-]?\s*(.+)",
        r"\btraveller\s*name\s*[:\-]?\s*(.+)",
        r"\btraveler\s*name\s*[:\-]?\s*(.+)",
        r"\bguest\s*name\s*[:\-]?\s*(.+)",
        r"\bcustomer\s*name\s*[:\-]?\s*(.+)",
        r"\bname\s*[:\-]?\s*(.+)"
    ]

    for line in lines:
        line_clean = clean_value(line)

        for pattern in patterns:
            match = re.search(pattern, line_clean, re.IGNORECASE)

            if match:
                value = clean_value(match.group(1))

                value = re.split(
                    r"\b(?:ticket|fare|issued|from|to|date|time|seat|"
                    r"pnr|booking|flight|train|bus)\b",
                    value,
                    flags=re.IGNORECASE
                )[0]

                if value != NOT_DETECTED and len(value) >= 3:
                    return value

    # -----------------------------------------------------
    # BUS TICKET SPECIAL CASE
    # Example:
    # Name Ticket type Fare base Issued by
    #
    # JULIUS CAESAR MR ONEWAY ADULT
    # -----------------------------------------------------

    for index, line in enumerate(lines):

        if re.search(
            r"\bname\s+ticket\s+type\b",
            line,
            re.IGNORECASE
        ):
            if index + 1 < len(lines):

                candidate = clean_value(lines[index + 1])

                candidate = re.split(
                    r"\b(?:ONEWAY|ONE WAY|ADULT|CHILD|FARE|"
                    r"INTERNATIONAL|BUS)\b",
                    candidate,
                    flags=re.IGNORECASE
                )[0]

                candidate = clean_value(candidate)

                if candidate != NOT_DETECTED:
                    return candidate

    return NOT_DETECTED


# =========================================================
# ROUTE EXTRACTION
# =========================================================

def extract_route(text):
    lines = text.splitlines()

    from_place = NOT_DETECTED
    to_place = NOT_DETECTED

    # -----------------------------------------------------
    # Direct "From X To Y"
    # -----------------------------------------------------

    flat = flat_text(text)

    patterns = [
        r"\bfrom\s*[:\-]?\s*(.+?)\s+\bto\s*[:\-]?\s*(.+?)(?=\s+\bdate\b|\s+\btime\b|\s+\bseat\b|\s+\bticket\b|\s*$)",

        r"\bfrom\s*[:\-]?\s*(.+?)\s+to\s+(.+?)(?=\s+\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\s*$)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            flat,
            re.IGNORECASE
        )

        if match:

            candidate_from = clean_value(match.group(1))
            candidate_to = clean_value(match.group(2))

            if candidate_from != NOT_DETECTED:
                from_place = candidate_from

            if candidate_to != NOT_DETECTED:
                to_place = candidate_to

            break

    # -----------------------------------------------------
    # Separate From / To labels
    # -----------------------------------------------------

    for index, line in enumerate(lines):

        if re.fullmatch(
            r"from\s*:?",
            line.strip(),
            re.IGNORECASE
        ):
            if index + 1 < len(lines):

                candidate = clean_value(lines[index + 1])

                # Do not take a date/time as location
                if not re.fullmatch(
                    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
                    candidate
                ):
                    if not re.search(
                        r"\d{1,2}:\d{2}",
                        candidate
                    ):
                        from_place = candidate

        if re.fullmatch(
            r"to\s*:?",
            line.strip(),
            re.IGNORECASE
        ):
            if index + 1 < len(lines):

                candidate = clean_value(lines[index + 1])

                if not re.fullmatch(
                    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
                    candidate
                ):
                    if not re.search(
                        r"\d{1,2}:\d{2}",
                        candidate
                    ):
                        to_place = candidate

    # -----------------------------------------------------
    # Bus / travel document special case
    #
    # From Date Time Seat Ticket number
    # Rome, Italy 13-04-2016 12:30 3A 00017558273
    # To
    # Paris, France 14-04-2016 10:30
    # -----------------------------------------------------

    for index, line in enumerate(lines):

        if re.search(
            r"\bfrom\b.*\bdate\b.*\btime\b.*\bseat\b.*\bticket\b",
            line,
            re.IGNORECASE
        ):

            if index + 1 < len(lines):

                next_line = clean_value(lines[index + 1])

                date_match = re.search(
                    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
                    next_line
                )

                time_match = re.search(
                    r"\d{1,2}:\d{2}",
                    next_line
                )

                if date_match and time_match:

                    location = next_line[:date_match.start()].strip()

                    location = clean_value(location)

                    if location:
                        from_place = location

    # -----------------------------------------------------
    # Find "To" followed by location
    # -----------------------------------------------------

    for index, line in enumerate(lines):

        if line.strip().lower() == "to":

            if index + 1 < len(lines):

                next_line = clean_value(lines[index + 1])

                # Remove date/time from location line
                next_line = re.split(
                    r"\s+\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
                    next_line
                )[0]

                next_line = re.split(
                    r"\s+\d{1,2}:\d{2}",
                    next_line
                )[0]

                next_line = clean_value(next_line)

                if next_line:
                    to_place = next_line

    # -----------------------------------------------------
    # Departure / destination fallback
    # -----------------------------------------------------

    if from_place == NOT_DETECTED:

        patterns_from = [
            r"\bdeparture\s*[:\-]\s*(.+)",
            r"\borigin\s*[:\-]\s*(.+)"
        ]

        for pattern in patterns_from:

            match = re.search(
                pattern,
                flat,
                re.IGNORECASE
            )

            if match:
                from_place = clean_value(match.group(1))
                break

    if to_place == NOT_DETECTED:

        patterns_to = [
            r"\bdestination\s*[:\-]\s*(.+)",
            r"\barrival\s*[:\-]\s*(.+)"
        ]

        for pattern in patterns_to:

            match = re.search(
                pattern,
                flat,
                re.IGNORECASE
            )

            if match:
                to_place = clean_value(match.group(1))
                break

    return from_place, to_place


# =========================================================
# PNR / BOOKING NUMBER
# =========================================================

def extract_pnr(text):

    patterns = [
        r"\bPNR\s*(?:NUMBER|NO|#)?\s*[:\-]?\s*([A-Z0-9]{5,20})",

        r"\bBOOKING\s*(?:REFERENCE|REF|ID|NUMBER|NO)?"
        r"\s*[:\-]?\s*([A-Z0-9]{5,20})",

        r"\bCONFIRMATION\s*(?:NUMBER|NO)?"
        r"\s*[:\-]?\s*([A-Z0-9]{5,20})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return NOT_DETECTED


# =========================================================
# TICKET NUMBER
# =========================================================

def extract_ticket_number(text):

    patterns = [
        r"\bTICKET\s*(?:NUMBER|NO|#)?\s*[:\-]?\s*([A-Z0-9-]{5,25})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return NOT_DETECTED


# =========================================================
# SEAT
# =========================================================

def extract_seat(text):

    patterns = [
        r"\bSEAT\s*(?:NUMBER|NO|#)?\s*[:\-]?\s*([A-Z0-9-]{1,10})",

        r"\bSEAT\s+([A-Z0-9-]{1,10})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    # Bus special case
    # Example: 12:30 3A 00017558273

    lines = text.splitlines()

    for line in lines:

        if re.search(
            r"\bseat\b.*\bticket\b",
            line,
            re.IGNORECASE
        ):
            next_index = lines.index(line) + 1

            if next_index < len(lines):

                next_line = lines[next_index]

                match = re.search(
                    r"\b\d{1,2}:\d{2}\s+([A-Z]?\d{1,3})\s+\d{5,}",
                    next_line,
                    re.IGNORECASE
                )

                if match:
                    return match.group(1)

    return NOT_DETECTED


# =========================================================
# GATE
# =========================================================

def extract_gate(text):

    pattern = (
        r"\bGATE\s*(?:NUMBER|NO|#)?"
        r"\s*[:\-]?\s*([A-Z0-9-]{1,10})"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return NOT_DETECTED


# =========================================================
# FLIGHT NUMBER
# =========================================================

def extract_flight_number(text):

    patterns = [
        r"\bFLIGHT\s*(?:NUMBER|NO)?\s*[:\-]?"
        r"\s*([A-Z]{1,3}\s?\d{2,5})",

        r"\b([A-Z]{2}\s?\d{2,5})\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            value = match.group(1).strip()

            # Avoid treating random text as flight number
            if re.search(r"\d", value):
                return value

    return NOT_DETECTED


# =========================================================
# TRAIN NUMBER
# =========================================================

def extract_train_number(text):

    patterns = [
        r"\bTRAIN\s*(?:NUMBER|NO)?"
        r"\s*[:\-]?\s*(\d{4,6})",

        r"\bTRAIN\s+(\d{4,6})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return NOT_DETECTED


# =========================================================
# COACH
# =========================================================

def extract_coach(text):

    pattern = (
        r"\bCOACH\s*(?:NUMBER|NO)?"
        r"\s*[:\-]?\s*([A-Z0-9]{1,8})"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return NOT_DETECTED


# =========================================================
# BERTH
# =========================================================

def extract_berth(text):

    pattern = (
        r"\bBERTH\s*(?:NUMBER|NO)?"
        r"\s*[:\-]?\s*([A-Z0-9]{1,8})"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return NOT_DETECTED


# =========================================================
# BUS NUMBER
# =========================================================

def extract_bus_number(text):

    patterns = [
        r"\bBUS\s*(?:NUMBER|NO|#)"
        r"\s*[:\-]?\s*([A-Z0-9-]{2,20})",

        r"\bBUS\s+([A-Z0-9-]{2,20})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return NOT_DETECTED


# =========================================================
# BOARDING POINT
# =========================================================

def extract_boarding_point(text):

    patterns = [
        r"\bBOARDING\s*POINT\s*[:\-]?\s*(.+)",
        r"\bBOARDING\s*[:\-]?\s*(.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            flat_text(text),
            re.IGNORECASE
        )

        if match:

            value = clean_value(match.group(1))

            value = re.split(
                r"\b(?:date|time|seat|ticket|drop|destination)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            return clean_value(value)

    return NOT_DETECTED


# =========================================================
# DROP POINT
# =========================================================

def extract_drop_point(text):

    patterns = [
        r"\bDROPPING\s*POINT\s*[:\-]?\s*(.+)",
        r"\bDROP\s*POINT\s*[:\-]?\s*(.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            flat_text(text),
            re.IGNORECASE
        )

        if match:

            value = clean_value(match.group(1))

            value = re.split(
                r"\b(?:date|time|seat|ticket)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            return clean_value(value)

    return NOT_DETECTED


# =========================================================
# HOTEL NAME
# =========================================================

def extract_hotel_name(text):

    lines = text.splitlines()

    patterns = [
        r"\bHOTEL\s*NAME\s*[:\-]?\s*(.+)",
        r"\bPROPERTY\s*[:\-]?\s*(.+)",
        r"\bRESORT\s*[:\-]?\s*(.+)"
    ]

    for line in lines:

        for pattern in patterns:

            match = re.search(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:

                value = clean_value(match.group(1))

                value = re.split(
                    r"\b(?:room|guest|booking|check|date)\b",
                    value,
                    flags=re.IGNORECASE
                )[0]

                return clean_value(value)

    return NOT_DETECTED


# =========================================================
# ROOM
# =========================================================

def extract_room(text):

    patterns = [
        r"\bROOM\s*(?:NUMBER|NO|TYPE)?"
        r"\s*[:\-]?\s*([A-Za-z0-9 .&'-]{1,40})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(match.group(1))

            value = re.split(
                r"\b(?:guest|booking|check|date)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            return clean_value(value)

    return NOT_DETECTED


# =========================================================
# CHECK-IN
# =========================================================

def extract_checkin(text):

    patterns = [
        r"\bCHECK[\s-]*IN\s*[:\-]?\s*(.{1,50})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1)

            dates = extract_all_dates(value)

            if dates:
                return dates[0]

    return NOT_DETECTED


# =========================================================
# CHECK-OUT
# =========================================================

def extract_checkout(text):

    patterns = [
        r"\bCHECK[\s-]*OUT\s*[:\-]?\s*(.{1,50})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1)

            dates = extract_all_dates(value)

            if dates:
                return dates[0]

    return NOT_DETECTED


# =========================================================
# BILL NUMBER
# =========================================================

def extract_bill_number(text):

    patterns = [
        r"\bBILL\s*(?:NO|NUMBER|#)"
        r"\s*[:.i\-]?\s*([A-Z0-9][A-Z0-9/-]{3,30})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            # Remove OCR artifacts
            value = value.lstrip("iI|:")

            return value

    return NOT_DETECTED


# =========================================================
# AMOUNT CLEANING
# =========================================================

def clean_amount(value):

    if not value:
        return NOT_DETECTED

    value = value.strip()

    # OCR can convert ₹ into %
    value = value.replace("₹", "")
    value = value.replace("Rs.", "")
    value = value.replace("Rs", "")
    value = value.replace("INR", "")

    # Remove spaces
    value = value.replace(" ", "")

    # Remove commas
    value = value.replace(",", "")

    # Remove accidental % before amount
    value = re.sub(r"^%+", "", value)

    # If OCR gives something like 7149.00,
    # do not modify automatically because it may be a
    # legitimate amount.

    match = re.search(
        r"\d+(?:\.\d{1,2})?",
        value
    )

    if match:
        try:
            number = float(match.group(0))
            return f"{number:.2f}"
        except ValueError:
            pass

    return NOT_DETECTED


# =========================================================
# SUBTOTAL
# =========================================================

def extract_subtotal(text):

    patterns = [
        r"\bSUBTOTAL\s*[:\-]?\s*(?:₹|Rs\.?|INR|%)?\s*"
        r"(\d[\d,]*(?:\.\d{1,2})?)",

        r"\bSUB\s*TOTAL\s*[:\-]?\s*(?:₹|Rs\.?|INR|%)?\s*"
        r"(\d[\d,]*(?:\.\d{1,2})?)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return clean_amount(match.group(1))

    return NOT_DETECTED


# =========================================================
# GST
# =========================================================

def extract_gst(text):

    cgst = None
    sgst = None
    gst_total = None

    cgst_pattern = (
        r"\bCGST\s*(?:\([^)]+\))?\s*"
        r"[:\-]?\s*(?:₹|Rs\.?|INR|%)?\s*"
        r"(\d[\d,]*(?:\.\d{1,2})?)"
    )

    sgst_pattern = (
        r"\bSGST\s*(?:\([^)]+\))?\s*"
        r"[:\-]?\s*(?:₹|Rs\.?|INR|%)?\s*"
        r"(\d[\d,]*(?:\.\d{1,2})?)"
    )

    gst_pattern = (
        r"\bGST\s*(?:AMOUNT)?\s*"
        r"[:\-]?\s*(?:₹|Rs\.?|INR|%)?\s*"
        r"(\d[\d,]*(?:\.\d{1,2})?)"
    )

    match = re.search(
        cgst_pattern,
        text,
        re.IGNORECASE
    )

    if match:
        try:
            cgst = float(
                clean_amount(match.group(1))
            )
        except (ValueError, TypeError):
            cgst = None

    match = re.search(
        sgst_pattern,
        text,
        re.IGNORECASE
    )

    if match:
        try:
            sgst = float(
                clean_amount(match.group(1))
            )
        except (ValueError, TypeError):
            sgst = None

    if cgst is not None and sgst is not None:

        gst_total = cgst + sgst

        return (
            f"{gst_total:.2f} "
            f"(CGST {cgst:.2f} + SGST {sgst:.2f})"
        )

    match = re.search(
        gst_pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return clean_amount(match.group(1))

    return NOT_DETECTED


# =========================================================
# GRAND TOTAL
# =========================================================

def extract_total_amount(text):

    patterns = [
        r"\bGRAND\s*TOTAL\s*[:\-]?\s*"
        r"(?:₹|Rs\.?|INR|%)?\s*"
        r"(\d[\d,]*(?:\.\d{1,2})?)",

        r"\bTOTAL\s*AMOUNT\s*[:\-]?\s*"
        r"(?:₹|Rs\.?|INR|%)?\s*"
        r"(\d[\d,]*(?:\.\d{1,2})?)",

        r"\bTOTAL\s*[:\-]?\s*"
        r"(?:₹|Rs\.?|INR|%)?\s*"
        r"(\d[\d,]*(?:\.\d{1,2})?)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return clean_amount(match.group(1))

    return NOT_DETECTED


# =========================================================
# PAYMENT MODE
# =========================================================

def extract_payment_mode(text):

    patterns = [
        r"\bPAYMENT\s*MODE\s*[:\-]?\s*(.+)",
        r"\bPAYMENT\s*METHOD\s*[:\-]?\s*(.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            flat_text(text),
            re.IGNORECASE
        )

        if match:

            value = clean_value(match.group(1))

            value = re.split(
                r"\b(?:THANK|VISIT|STATUS|PAYMENT)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            return clean_value(value)

    return NOT_DETECTED


# =========================================================
# PAYMENT STATUS
# =========================================================

def extract_payment_status(text):

    patterns = [
        r"\bPAYMENT\s*STATUS\s*[:\-]?\s*"
        r"(PAID|UNPAID|PENDING|SUCCESS|FAILED)",

        r"\b(PAID|UNPAID|PENDING|SUCCESS|FAILED)\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).upper()

    return NOT_DETECTED


# =========================================================
# ORDER TYPE
# =========================================================

def extract_order_type(text):

    pattern = (
        r"\bORDER\s*TYPE\s*[:\-]?\s*"
        r"(DINE\s*IN|TAKE\s*AWAY|TAKEAWAY|DELIVERY|"
        r"DELIVERED|PICKUP)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip().upper()

    return NOT_DETECTED


# =========================================================
# TABLE NUMBER
# =========================================================

def extract_table_number(text):

    pattern = (
        r"\bTABLE\s*(?:NO|NUMBER|#)?"
        r"\s*[:\-]?\s*([A-Z0-9-]{1,10})"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return NOT_DETECTED


# =========================================================
# RESTAURANT NAME
# =========================================================

def extract_restaurant_name(text):

    lines = text.splitlines()

    # -----------------------------------------------------
    # Explicit restaurant name
    # -----------------------------------------------------

    patterns = [
        r"\bRESTAURANT\s*NAME\s*[:\-]?\s*(.+)",
        r"\bRESTAURANT\s*[:\-]?\s*(.+)"
    ]

    for line in lines:

        for pattern in patterns:

            match = re.search(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:

                value = clean_value(match.group(1))

                value = re.split(
                    r"\b(?:address|bill|date|time|gstin)\b",
                    value,
                    flags=re.IGNORECASE
                )[0]

                if value != NOT_DETECTED:
                    return value

    # -----------------------------------------------------
    # Sample OCR:
    #
    # YOUR RESTAURANT
    #
    # GOOD FOOD. GREAT
    # MEMORIES.
    # -----------------------------------------------------

    for index, line in enumerate(lines):

        if re.search(
            r"\bYOUR\s+RESTAURANT\b",
            line,
            re.IGNORECASE
        ):
            return "YOUR RESTAURANT"

    # Generic restaurant heading
    for line in lines[:10]:

        candidate = clean_value(line)

        if (
            candidate != NOT_DETECTED
            and "restaurant" in candidate.lower()
            and "address" not in candidate.lower()
        ):
            return candidate

    return NOT_DETECTED


# =========================================================
# RESTAURANT ADDRESS
# =========================================================

def extract_restaurant_address(text):

    lines = text.splitlines()

    for index, line in enumerate(lines):

        if re.search(
            r"restaurant\s+address",
            line,
            re.IGNORECASE
        ):

            if index + 1 < len(lines):

                address = clean_value(
                    lines[index + 1]
                )

                return address

    return NOT_DETECTED


# =========================================================
# DOCUMENT TYPE FALLBACK
# =========================================================

def detect_local_document_type(text):

    lower = flat_text(text).lower()

    scores = {
        "Restaurant Bill": 0,
        "Hotel Booking": 0,
        "Flight Ticket": 0,
        "Train Ticket": 0,
        "Bus Ticket": 0
    }

    # -----------------------------------------------------
    # RESTAURANT
    # -----------------------------------------------------

    restaurant_words = [
        "restaurant",
        "subtotal",
        "cgst",
        "sgst",
        "grand total",
        "payment mode",
        "order type",
        "table no",
        "gstin",
        "dine in"
    ]

    for word in restaurant_words:
        if word in lower:
            scores["Restaurant Bill"] += 1

    # -----------------------------------------------------
    # BUS
    # -----------------------------------------------------

    bus_words = [
        "international bus",
        "bus lines",
        "bus ticket",
        "bus number",
        "boarding point",
        "drop point",
        "ticket number"
    ]

    for word in bus_words:
        if word in lower:
            scores["Bus Ticket"] += 1

    # Very strong bus indicator
    if "international bus" in lower:
        scores["Bus Ticket"] += 5

    if "bus lines" in lower:
        scores["Bus Ticket"] += 5

    # -----------------------------------------------------
    # TRAIN
    # -----------------------------------------------------

    train_words = [
        "railway",
        "railways",
        "train",
        "train number",
        "platform",
        "coach",
        "berth",
        "irctc"
    ]

    for word in train_words:
        if word in lower:
            scores["Train Ticket"] += 1

    # -----------------------------------------------------
    # FLIGHT
    # -----------------------------------------------------

    flight_words = [
        "flight",
        "airline",
        "airlines",
        "airport",
        "terminal",
        "gate",
        "pnr"
    ]

    for word in flight_words:
        if word in lower:
            scores["Flight Ticket"] += 1

    # Boarding pass alone should NOT decide flight.
    # Many bus tickets also use "boarding pass".
    if "boarding pass" in lower and "bus" not in lower:
        scores["Flight Ticket"] += 2

    # -----------------------------------------------------
    # HOTEL
    # -----------------------------------------------------

    hotel_words = [
        "hotel booking",
        "hotel",
        "check-in",
        "check in",
        "check-out",
        "check out",
        "room",
        "reservation",
        "guest"
    ]

    for word in hotel_words:
        if word in lower:
            scores["Hotel Booking"] += 1

    # -----------------------------------------------------
    # STRONG PRIORITY
    # -----------------------------------------------------

    if "international bus" in lower or "bus lines" in lower:
        return "Bus Ticket"

    if (
        "grand total" in lower
        and "subtotal" in lower
        and "cgst" in lower
        and "sgst" in lower
    ):
        return "Restaurant Bill"

    # -----------------------------------------------------
    # BEST SCORE
    # -----------------------------------------------------

    best_type = max(
        scores,
        key=scores.get
    )

    if scores[best_type] >= 2:
        return best_type

    return "Travel Document"


# =========================================================
# MAIN FUNCTION
# =========================================================

def extract_travel_info(text, document_type=None):

    text = clean_text(text)

    # -----------------------------------------------------
    # ALWAYS RETURN SAME DICTIONARY STRUCTURE
    # This prevents app.py .get() errors.
    # -----------------------------------------------------

    result = {
        "Passenger Name": NOT_DETECTED,

        "Travel Date": NOT_DETECTED,
        "Travel Time": NOT_DETECTED,

        "From": NOT_DETECTED,
        "To": NOT_DETECTED,

        "PNR / Booking Number": NOT_DETECTED,

        "Flight Number": NOT_DETECTED,
        "Seat": NOT_DETECTED,
        "Gate": NOT_DETECTED,
        "Boarding Time": NOT_DETECTED,

        "Train Number": NOT_DETECTED,
        "Coach": NOT_DETECTED,
        "Berth": NOT_DETECTED,

        "Bus Number": NOT_DETECTED,
        "Boarding Point": NOT_DETECTED,
        "Drop Point": NOT_DETECTED,

        "Hotel Name": NOT_DETECTED,
        "Room": NOT_DETECTED,
        "Check-in": NOT_DETECTED,
        "Check-out": NOT_DETECTED,
        "Hotel Amount": NOT_DETECTED,

        "Bill Number": NOT_DETECTED,
        "Subtotal": NOT_DETECTED,
        "GST Amount": NOT_DETECTED,
        "Total Amount": NOT_DETECTED,

        "Payment Mode": NOT_DETECTED,
        "Payment Status": NOT_DETECTED,

        "Order Type": NOT_DETECTED,
        "Table Number": NOT_DETECTED,

        "Restaurant Name": NOT_DETECTED,
        "Restaurant Address": NOT_DETECTED
    }

    if not text:
        return result

    # -----------------------------------------------------
    # DOCUMENT TYPE
    # -----------------------------------------------------

    detected_type = detect_local_document_type(text)

    supplied_type = document_type or ""

    # If supplied detector says Flight but OCR strongly
    # indicates Bus, correct it locally.
    if detected_type != "Travel Document":
        document_type = detected_type
    else:
        document_type = supplied_type

    # -----------------------------------------------------
    # COMMON EXTRACTION
    # -----------------------------------------------------

    dates = extract_all_dates(text)
    times = extract_all_times(text)

    result["Passenger Name"] = extract_passenger(text)

    if dates:
        result["Travel Date"] = dates[0]

    if times:
        result["Travel Time"] = times[0]

    from_place, to_place = extract_route(text)

    result["From"] = from_place
    result["To"] = to_place

    result["PNR / Booking Number"] = extract_pnr(text)

    # -----------------------------------------------------
    # FLIGHT
    # -----------------------------------------------------

    result["Flight Number"] = extract_flight_number(text)
    result["Seat"] = extract_seat(text)
    result["Gate"] = extract_gate(text)

    if times:
        result["Boarding Time"] = times[0]

    # -----------------------------------------------------
    # TRAIN
    # -----------------------------------------------------

    result["Train Number"] = extract_train_number(text)
    result["Coach"] = extract_coach(text)
    result["Berth"] = extract_berth(text)

    # -----------------------------------------------------
    # BUS
    # -----------------------------------------------------

    result["Bus Number"] = extract_bus_number(text)
    result["Boarding Point"] = extract_boarding_point(text)
    result["Drop Point"] = extract_drop_point(text)

    # -----------------------------------------------------
    # BUS SPECIAL EXTRACTION
    # -----------------------------------------------------

    if document_type == "Bus Ticket":

        lines = text.splitlines()

        # Find line:
        # From Date Time Seat Ticket number
        for index, line in enumerate(lines):

            if re.search(
                r"\bfrom\b.*\bdate\b.*\btime\b.*\bseat\b.*\bticket\b",
                line,
                re.IGNORECASE
            ):

                if index + 1 < len(lines):

                    data_line = lines[index + 1]

                    date_match = re.search(
                        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
                        data_line
                    )

                    time_match = re.search(
                        r"\d{1,2}:\d{2}",
                        data_line
                    )

                    if date_match:
                        result["Travel Date"] = date_match.group(0)

                    if time_match:
                        result["Travel Time"] = time_match.group(0)

                    # Location before date
                    if date_match:

                        location = data_line[
                            :date_match.start()
                        ]

                        location = clean_value(location)

                        if location:
                            result["From"] = location

                    # Seat
                    if time_match:

                        after_time = data_line[
                            time_match.end():
                        ]

                        seat_match = re.search(
                            r"\b([A-Z]?\d{1,3})\b",
                            after_time
                        )

                        if seat_match:
                            result["Seat"] = (
                                seat_match.group(1)
                            )

                    # Ticket number
                    ticket_match = re.search(
                        r"\b\d{7,20}\b",
                        data_line
                    )

                    if ticket_match:
                        result["PNR / Booking Number"] = (
                            ticket_match.group(0)
                        )

        # -------------------------------------------------
        # Arrival data
        # -------------------------------------------------

        for index, line in enumerate(lines):

            if line.strip().lower() == "to":

                if index + 1 < len(lines):

                    arrival_line = lines[index + 1]

                    arrival_date = re.search(
                        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
                        arrival_line
                    )

                    arrival_time = re.search(
                        r"\d{1,2}:\d{2}",
                        arrival_line
                    )

                    if arrival_date:

                        result["Check-out"] = (
                            arrival_date.group(0)
                        )

                    if arrival_time:

                        # Arrival time is kept separately
                        # in the dictionary if app.py supports it.
                        result["Drop Point"] = re.split(
                            r"\s+\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
                            arrival_line
                        )[0].strip()

    # -----------------------------------------------------
    # HOTEL
    # -----------------------------------------------------

    result["Hotel Name"] = extract_hotel_name(text)
    result["Room"] = extract_room(text)
    result["Check-in"] = extract_checkin(text)
    result["Check-out"] = extract_checkout(text)
    result["Hotel Amount"] = extract_total_amount(text)

    # -----------------------------------------------------
    # RESTAURANT
    # -----------------------------------------------------

    result["Restaurant Name"] = extract_restaurant_name(text)

    result["Restaurant Address"] = (
        extract_restaurant_address(text)
    )

    result["Bill Number"] = extract_bill_number(text)

    result["Subtotal"] = extract_subtotal(text)

    result["GST Amount"] = extract_gst(text)

    result["Total Amount"] = extract_total_amount(text)

    result["Payment Mode"] = extract_payment_mode(text)

    result["Payment Status"] = extract_payment_status(text)

    result["Order Type"] = extract_order_type(text)

    result["Table Number"] = extract_table_number(text)

    # -----------------------------------------------------
    # RESTAURANT DOCUMENT
    # -----------------------------------------------------

    if document_type == "Restaurant Bill":

        result["From"] = "Not applicable"
        result["To"] = "Not applicable"

        # Don't treat restaurant customer as passenger
        result["Passenger Name"] = "Dine In Guest"

        result["Travel Date"] = (
            dates[0] if dates else NOT_DETECTED
        )

        result["Travel Time"] = (
            times[0] if times else NOT_DETECTED
        )

    # -----------------------------------------------------
    # FINAL SAFETY
    # Make sure every value is never None.
    # -----------------------------------------------------

    for key in result:

        if result[key] is None:
            result[key] = NOT_DETECTED

        elif not isinstance(result[key], str):
            result[key] = str(result[key])

    return result

