import re


def detect_document_type(text):
    if not text:
        return "Unknown Document"

    text = text.lower()
    text = re.sub(r"\s+", " ", text)

    bus_keywords = [
        "international bus",
        "bus lines",
        "bus ticket",
        "bus number",
        "boarding point",
        "drop point",
        "ticket number",
        "ticket type",
    ]

    bus_score = sum(1 for keyword in bus_keywords if keyword in text)

   
    if "international bus" in text or "bus lines" in text:
        bus_score += 5

    if "from" in text and "to" in text and "ticket number" in text:
        bus_score += 2


    flight_keywords = [
        "flight",
        "airline",
        "airlines",
        "airport",
        "flight number",
        "terminal",
        "gate",
        "pnr",
        "boarding pass",
    ]

    flight_score = sum(1 for keyword in flight_keywords if keyword in text)


    train_keywords = [
        "railway",
        "railways",
        "train",
        "train number",
        "train no",
        "platform",
        "coach",
        "berth",
        "pnr",
    ]

    train_score = sum(1 for keyword in train_keywords if keyword in text)


    restaurant_keywords = [
        "restaurant",
        "subtotal",
        "grand total",
        "cgst",
        "sgst",
        "gstin",
        "payment mode",
        "order type",
        "table no",
        "dine in",
        "food",
    ]

    restaurant_score = sum(
        1 for keyword in restaurant_keywords if keyword in text
    )

    if "grand total" in text:
        restaurant_score += 3

    if "subtotal" in text:
        restaurant_score += 2

    if "cgst" in text and "sgst" in text:
        restaurant_score += 3

    hotel_keywords = [
        "hotel booking",
        "hotel",
        "check-in",
        "check-out",
        "check in",
        "check out",
        "room",
        "guest",
        "reservation",
        "booking confirmation",
    ]

    hotel_score = sum(1 for keyword in hotel_keywords if keyword in text)

    if restaurant_score >= 3:
        return "Restaurant Bill"

    if bus_score >= 2:
        return "Bus Ticket"

    if train_score >= 2:
        return "Train Ticket"

    if flight_score >= 2:
        return "Flight Ticket"

    if hotel_score >= 2:
        return "Hotel Booking"


    if "bus" in text:
        return "Bus Ticket"

    if "train" in text or "railway" in text:
        return "Train Ticket"

    if "flight" in text or "airline" in text:
        return "Flight Ticket"

    if "hotel" in text or "check-in" in text:
        return "Hotel Booking"

    if "restaurant" in text or "grand total" in text:
        return "Restaurant Bill"

    return "Unknown Document"
