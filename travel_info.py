import re


def clean_text(text):
    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)

    return text.strip()


def flat_text(text):
    return re.sub(r"\s+", " ", text).strip()


def clean_value(value):
    if not value:
        return "Not detected"

    value = re.sub(r"\s+", " ", value)
    value = value.strip(" :.-")

    return value if value else "Not detected"


def extract_date(text):

    labeled_patterns = [
        r"\b(?:bill\s*)?date\s*[:\-]?\s*(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"\b(?:bill\s*)?date\s*[:\-]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    ]

    for pattern in labeled_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return clean_value(match.group(1))

    patterns = [
        r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return clean_value(match.group(0))

    return "Not detected"


def extract_all_dates(text):

    patterns = [
        r"\b\d{1,2}-\d{1,2}-\d{2,4}\b",
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\b"
    ]

    dates = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for date in matches:

            if date not in dates:
                dates.append(date)

    return dates


def extract_time(text):

    patterns = [
        r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b",
        r"\b(?:[01]?\d|2[0-3])\.[0-5]\d\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(0).replace(".", ":")

    return "Not detected"


def extract_passenger_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


    for i, line in enumerate(lines):

        if re.fullmatch(
            r"name",
            line,
            re.IGNORECASE
        ):

            if i + 1 < len(lines):

                value = clean_value(
                    lines[i + 1]
                )

    
                if value.lower() not in [
                    "ticket type",
                    "fare base",
                    "issued by",
                    "from",
                    "to",
                    "date",
                    "time",
                    "seat",
                    "ticket number",
                    "number"
                ]:

                   
                    if not re.search(
                        r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}",
                        value
                    ):

                      
                        if re.search(
                            r"[A-Za-z]{2,}",
                            value
                        ):

                           
                            value = re.split(
                                r"\b(?:oneway|adult|ticket|type|fare|issued|from|to|date|time|seat|number)\b",
                                value,
                                maxsplit=1,
                                flags=re.IGNORECASE
                            )[0]

                            value = clean_value(value)

                            if value != "Not detected":
                                return value

  

    patterns = [

        r"\bPASSENGER\s*NAME\s*[:\-]\s*"
        r"([A-Za-z][A-Za-z .'-]{2,60})",

        r"\bPASSENGER\s*[:\-]\s*"
        r"([A-Za-z][A-Za-z .'-]{2,60})",

        r"\bNAME\s*[:\-]\s*"
        r"([A-Za-z][A-Za-z .'-]{2,60})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(
                match.group(1)
            )

            value = re.split(
                r"\b(?:ticket\s*type|fare\s*base|issued\s*by|from|to|date|time|seat|ticket|number)\b",
                value,
                maxsplit=1,
                flags=re.IGNORECASE
            )[0]

            value = clean_value(value)

            if value.lower() not in [
                "ticket type",
                "fare base",
                "issued by",
                "customer name",
                "dine in guest",
                "number",
                "numbe"
            ]:

                if value != "Not detected":
                    return value

    return "Not detected"


def extract_route(text):

    from_place = "Not detected"
    to_place = "Not detected"

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


    for i, line in enumerate(lines):

        if re.search(
            r"\bfrom\b",
            line,
            re.IGNORECASE
        ):

            if i + 1 < len(lines):

                next_line = lines[i + 1].strip()

                date_match = re.search(
                    r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
                    next_line
                )

                if date_match:

                    possible_from = next_line[
                        :date_match.start()
                    ].strip()

                    if possible_from:

                        from_place = clean_value(
                            possible_from
                        )

            # Same-line fallback
            match = re.search(
                r"\bfrom\b\s+(.+?)\s+\d{1,2}[-/]\d{1,2}[-/]\d{2,4}",
                line,
                re.IGNORECASE
            )

            if match:

                from_place = clean_value(
                    match.group(1)
                )

  

    for i, line in enumerate(lines):

        if re.fullmatch(
            r"to",
            line,
            re.IGNORECASE
        ):

            if i + 1 < len(lines):

                possible_to = lines[i + 1].strip()

                possible_to = re.split(
                    r"\s+\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b",
                    possible_to
                )[0]

                if possible_to:

                    to_place = clean_value(
                        possible_to
                    )

        else:

            match = re.search(
                r"\bto\b\s+(.+?)\s+\d{1,2}[-/]\d{1,2}[-/]\d{2,4}",
                line,
                re.IGNORECASE
            )

            if match:

                to_place = clean_value(
                    match.group(1)
                )



    if from_place == "Not detected":

        pattern = (
            r"\bfrom\s*[:\-]?\s*"
            r"([A-Za-z][A-Za-z ,.'-]{2,60})"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(
                match.group(1)
            )

            value = re.split(
                r"\b(?:date|time|seat|ticket|number)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            if value:
                from_place = clean_value(value)

  

    if to_place == "Not detected":

        pattern = (
            r"\bto\s*[:\-]?\s*"
            r"([A-Za-z][A-Za-z ,.'-]{2,60})"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(
                match.group(1)
            )

            value = re.split(
                r"\b(?:date|time|seat|ticket|number)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            if value:
                to_place = clean_value(value)

    return from_place, to_place


def extract_pnr(text):

    patterns = [

        r"\bPNR\s*(?:NO|NUMBER)?\s*[:#.\-]?\s*([A-Z0-9]{5,20})",

        r"\bBOOKING\s*(?:ID|NO|NUMBER|REFERENCE)"
        r"\s*[:#.\-]?\s*([A-Z0-9/-]{5,25})",

        r"\bBOOKING\s*REFERENCE"
        r"\s*[:#.\-]?\s*([A-Z0-9/-]{5,25})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(
                match.group(1)
            )

            if value.lower() not in [
                "number",
                "numbe",
                "no",
                "name",
                "seat",
                "ticket"
            ]:

                return value

    return "Not detected"


def extract_ticket_number(text):

    patterns = [

        r"\bTICKET\s*(?:NO|NUMBER|NUMBE)?"
        r"\s*[:#.\-]?\s*([A-Z0-9/-]{5,30})",

        r"\bTICKET\s+NUMBE"
        r"\s*[:#.\-]?\s*([A-Z0-9/-]{5,30})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(
                match.group(1)
            )

            if value.lower() not in [
                "number",
                "numbe",
                "seat",
                "name"
            ]:

                return value

    return "Not detected"



def extract_seat(text):

    patterns = [

        r"\bSEAT\s*(?:NO|NUMBER)?"
        r"\s*[:#.\-]?\s*([A-Z]?\d{1,3}[A-Z]?)",

        r"\bSEAT\s+([A-Z]?\d{1,3}[A-Z]?)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return clean_value(
                match.group(1)
            )

    return "Not detected"


def extract_gate(text):

    pattern = (
        r"\bGATE\s*(?:NO|NUMBER)?"
        r"\s*[:#.\-]?\s*([A-Z]?\d{1,4})"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        return clean_value(
            match.group(1)
        )

    return "Not detected"


def extract_flight_number(text):

    patterns = [

        r"\bFLIGHT\s*(?:NO|NUMBER)?"
        r"\s*[:#.\-]?\s*([A-Z]{1,3}\s?\d{1,5})",

        r"\b([A-Z]{2}\s?\d{2,5})\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(
                match.group(1)
            )

            if not value.isdigit():
                return value

    return "Not detected"


def extract_boarding_time(text):

    patterns = [

        r"\bBOARDING\s*TIME\s*[:\-]?\s*"
        r"((?:[01]?\d|2[0-3]):[0-5]\d)",

        r"\bBOARDING\s*[:\-]?\s*"
        r"((?:[01]?\d|2[0-3]):[0-5]\d)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return "Not detected"


def extract_train_number(text):

    patterns = [

        r"\bTRAIN\s*(?:NO|NUMBER)?"
        r"\s*[:#.\-]?\s*(\d{4,6})",

        r"\b(\d{5})\s+[A-Za-z][A-Za-z ]+"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return clean_value(
                match.group(1)
            )

    return "Not detected"


def extract_coach(text):

    patterns = [

        r"\bCOACH\s*[:#.\-]?\s*([A-Z]{1,3}\d{0,3})",

        r"\b([A-Z]{1,2}\d{1,3})\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(
                match.group(1)
            )

            if len(value) <= 6:
                return value

    return "Not detected"


def extract_berth(text):

    patterns = [

        r"\bBERTH\s*(?:NO|NUMBER)?"
        r"\s*[:#.\-]?\s*([A-Z]?\d{1,3})",

        r"\bBERTH\s*[:#.\-]?\s*([A-Z]?\d{1,3})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return clean_value(
                match.group(1)
            )

    return "Not detected"


def extract_bus_number(text):

    patterns = [

        r"\bBUS\s*(?:NO|NUMBER)?"
        r"\s*[:#.\-]?\s*([A-Z0-9/-]{2,20})",

        r"\bBUS\s*ID\s*[:#.\-]?"
        r"\s*([A-Z0-9/-]{2,20})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(
                match.group(1)
            )

            if value.lower() not in [
                "ticket",
                "lines",
                "pass",
                "number"
            ]:

                return value

    return "Not detected"


# =========================================================
# HOTEL NAME
# =========================================================

def extract_hotel_name(text):

    patterns = [

        r"\bHOTEL\s*(?:NAME)?"
        r"\s*[:\-]?\s*([A-Za-z0-9 &'.,-]{3,80})",

        r"\b([A-Z][A-Z &'-]{3,50})\s+HOTEL\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return clean_value(
                match.group(1)
            )

    return "Not detected"


# =========================================================
# CHECK-IN
# =========================================================

def extract_check_in(text):

    pattern = (
        r"\bCHECK[- ]?IN\s*[:\-]?"
        r"\s*(.*?)(?=\n|CHECK[- ]?OUT|$)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        return clean_value(
            match.group(1)
        )

    return "Not detected"


# =========================================================
# CHECK-OUT
# =========================================================

def extract_check_out(text):

    pattern = (
        r"\bCHECK[- ]?OUT\s*[:\-]?"
        r"\s*(.*?)(?=\n|$)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        return clean_value(
            match.group(1)
        )

    return "Not detected"


# =========================================================
# RESTAURANT BILL NUMBER
# =========================================================

def extract_bill_number(text):

    for line in text.splitlines():

        patterns = [

            r"\bBILL\s*(?:NO|NUMBER|#)"
            r"\s*[\.:]?\s*(?:[iIl]\s+)?"
            r"([A-Z][A-Z0-9/-]{3,30})",

            r"\bBILL\s*[:\-]?\s*"
            r"(?:NO|NUMBER|#)?"
            r"\s*[\.:]?\s*(?:[iIl]\s+)?"
            r"([A-Z][A-Z0-9/-]{3,30})"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:

                value = match.group(1).strip()

                value = re.sub(
                    r"^[iIl]\s+",
                    "",
                    value
                )

                return value

    return "Not detected"


# =========================================================
# MONEY
# =========================================================

def extract_amount(text, label):

    pattern = (
        rf"{label}\s*[:\-]?"
        rf"\s*[₹Rs.\s]*"
        rf"([0-9][0-9,]*"
        rf"(?:\.[0-9]{{1,2}})?)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:

        return "₹ " + match.group(1).replace(
            ",",
            ""
        )

    return "Not detected"


def extract_subtotal(text):

    return extract_amount(
        text,
        r"\bSUBTOTAL\b"
    )


def extract_grand_total(text):

    patterns = [

        r"\bGRAND\s*TOTAL\s*[:\-]?"
        r"\s*[₹Rs.\s]*"
        r"([0-9][0-9,]*(?:\.[0-9]{1,2})?)",

        r"\bTOTAL\s*[:\-]?"
        r"\s*[₹Rs.\s]*"
        r"([0-9][0-9,]*(?:\.[0-9]{1,2})?)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return "₹ " + match.group(
                1
            ).replace(",", "")

    return "Not detected"


# =========================================================
# GST
# =========================================================

def extract_gst(text):

    cgst = None
    sgst = None

    cgst_match = re.search(
        r"\bCGST.*?[₹Rs.\s]*"
        r"([0-9][0-9,]*(?:\.[0-9]{1,2})?)",
        text,
        re.IGNORECASE
    )

    sgst_match = re.search(
        r"\bSGST.*?[₹Rs.\s]*"
        r"([0-9][0-9,]*(?:\.[0-9]{1,2})?)",
        text,
        re.IGNORECASE
    )

    if cgst_match:

        cgst = cgst_match.group(1).replace(
            ",",
            ""
        )

    if sgst_match:

        sgst = sgst_match.group(1).replace(
            ",",
            ""
        )

    if cgst and sgst:

        try:

            total = float(cgst) + float(sgst)

            return (
                f"₹ {total:.2f} "
                f"(CGST {float(cgst):.2f} "
                f"+ SGST {float(sgst):.2f})"
            )

        except:
            return "Not detected"

    if cgst:
        return f"₹ {cgst}"

    if sgst:
        return f"₹ {sgst}"

    return "Not detected"


# =========================================================
# PAYMENT MODE
# =========================================================

def extract_payment_mode(text):

    patterns = [

        r"\bPAYMENT\s*MODE\s*[:\-]?\s*([A-Za-z ]+)",

        r"\bPAYMENT\s*METHOD\s*[:\-]?\s*([A-Za-z ]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = clean_value(
                match.group(1)
            )

            value = re.split(
                r"\b(?:payment|status|total|thank|visit)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            return clean_value(value)

    methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Cash on Delivery",
        "Cash",
        "Net Banking",
        "Google Pay",
        "PhonePe",
        "Paytm"
    ]

    for method in methods:

        if method.lower() in text.lower():
            return method

    return "Not detected"


# =========================================================
# PAYMENT STATUS
# =========================================================

def extract_payment_status(text):

    patterns = [

        r"\bPAYMENT\s*STATUS\s*[:\-]?\s*([A-Za-z]+)",

        r"\bSTATUS\s*[:\-]?\s*(PAID|UNPAID|PENDING|SUCCESS|FAILED)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return clean_value(
                match.group(1)
            ).upper()

    if re.search(
        r"\bPAID\b",
        text,
        re.IGNORECASE
    ):
        return "PAID"

    if re.search(
        r"\bPENDING\b",
        text,
        re.IGNORECASE
    ):
        return "PENDING"

    if re.search(
        r"\bFAILED\b",
        text,
        re.IGNORECASE
    ):
        return "FAILED"

    if re.search(
        r"\bSUCCESS\b",
        text,
        re.IGNORECASE
    ):
        return "SUCCESS"

    return "Not detected"


# =========================================================
# RESTAURANT LOCATION
# =========================================================

def extract_location(text):

    pattern = (
        r"\b([A-Z][A-Za-z]+,\s*"
        r"[A-Z][A-Za-z]+)"
        r"(?:\s+\d{6})?"
    )

    matches = re.findall(
        pattern,
        text
    )

    for value in matches:

        if value.lower() not in [
            "your restaurant",
            "customer name"
        ]:

            return clean_value(value)

    return "Not detected"


# =========================================================
# RESTAURANT NAME
# =========================================================

def extract_restaurant_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines:

        if "your restaurant" in line.lower():
            return "Your Restaurant"

    return "Not detected"


# =========================================================
# MAIN EXTRACTION
# =========================================================

def extract_travel_info(text, document_type):

    text = clean_text(text)

    result = {

        "Travel Date": "Not detected",
        "Travel Time": "Not detected",

        "From": "Not detected",
        "To": "Not detected",

        "Passenger Name": "Not detected",

        "PNR / Booking Number":
            "Not detected",

        # Flight
        "Flight Number": "Not detected",
        "Seat": "Not detected",
        "Gate": "Not detected",
        "Boarding Time": "Not detected",

        # Train
        "Train Number": "Not detected",
        "Coach": "Not detected",
        "Berth": "Not detected",

        # Bus
        "Bus Number": "Not detected",
        "Boarding Point": "Not detected",
        "Drop Point": "Not detected",

        # Hotel
        "Hotel Name": "Not detected",
        "Check-in": "Not detected",
        "Check-out": "Not detected",

        # Restaurant
        "Restaurant Name": "Not detected",
        "Bill Number": "Not detected",
        "Subtotal": "Not detected",
        "GST Amount": "Not detected",
        "Total Amount": "Not detected",
        "Payment Mode": "Not detected",
        "Payment Status": "Not detected",
        "Location": "Not detected"
    }

    # =====================================================
    # COMMON
    # =====================================================

    result["Travel Date"] = extract_date(text)

    result["Travel Time"] = extract_time(text)

    from_place, to_place = extract_route(text)

    result["From"] = from_place
    result["To"] = to_place

    result["Passenger Name"] = (
        extract_passenger_name(text)
    )

    result["PNR / Booking Number"] = (
        extract_pnr(text)
    )

    # =====================================================
    # FLIGHT
    # =====================================================

    if document_type == "Flight Ticket":

        result["Flight Number"] = (
            extract_flight_number(text)
        )

        result["Seat"] = extract_seat(text)

        result["Gate"] = extract_gate(text)

        result["Boarding Time"] = (
            extract_boarding_time(text)
        )

    # =====================================================
    # TRAIN
    # =====================================================

    elif document_type == "Train Ticket":

        result["Train Number"] = (
            extract_train_number(text)
        )

        result["Coach"] = extract_coach(text)

        result["Berth"] = extract_berth(text)

    # =====================================================
    # BUS
    # =====================================================

    elif document_type == "Bus Ticket":

        result["Bus Number"] = (
            extract_bus_number(text)
        )

        # From = Boarding Point
        if result["From"] != "Not detected":

            result["Boarding Point"] = (
                result["From"]
            )

        # To = Drop Point
        if result["To"] != "Not detected":

            result["Drop Point"] = (
                result["To"]
            )

        # Ticket number as booking reference
        ticket_number = (
            extract_ticket_number(text)
        )

        if (
            result["PNR / Booking Number"]
            == "Not detected"
        ):

            result["PNR / Booking Number"] = (
                ticket_number
            )

    # =====================================================
    # HOTEL
    # =====================================================

    elif document_type == "Hotel Booking":

        result["Hotel Name"] = (
            extract_hotel_name(text)
        )

        result["Check-in"] = (
            extract_check_in(text)
        )

        result["Check-out"] = (
            extract_check_out(text)
        )

    # =====================================================
    # RESTAURANT
    # =====================================================

    elif document_type == "Restaurant Bill":

        result["Travel Date"] = (
            extract_date(text)
        )

        result["Travel Time"] = (
            extract_time(text)
        )

        result["Restaurant Name"] = (
            extract_restaurant_name(text)
        )

        result["Bill Number"] = (
            extract_bill_number(text)
        )

        result["Subtotal"] = (
            extract_subtotal(text)
        )

        result["GST Amount"] = (
            extract_gst(text)
        )

        result["Total Amount"] = (
            extract_grand_total(text)
        )

        result["Payment Mode"] = (
            extract_payment_mode(text)
        )

        result["Payment Status"] = (
            extract_payment_status(text)
        )

        result["Location"] = (
            extract_location(text)
        )

        # Restaurant location as destination
        if result["To"] == "Not detected":

            result["To"] = (
                result["Location"]
            )

    else:

        result["Travel Date"] = (
            extract_date(text)
        )

        result["Travel Time"] = (
            extract_time(text)
        )

    return result

