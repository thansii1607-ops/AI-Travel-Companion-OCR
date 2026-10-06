def detect_document_type(text):

    text = text.lower()

    flight_keywords = [
        "flight",
        "airlines",
        "boarding pass",
        "boarding",
        "pnr",
        "terminal",
        "seat",
        "gate"
    ]

    train_keywords = [
        "railway",
        "railways",
        "train",
        "platform",
        "coach",
        "berth"
    ]

    bus_keywords = [
        "bus",
        "bus ticket",
        "boarding point",
        "drop point",
        "bus number"
    ]

    hotel_keywords = [
        "hotel",
        "check-in",
        "check-out",
        "room",
        "guest",
        "hotel booking"
    ]

    restaurant_keywords = [
        "restaurant",
        "bill",
        "food",
        "total",
        "tax",
        "gst"
    ]

    if any(keyword in text for keyword in flight_keywords):
        return "Flight Ticket"

    elif any(keyword in text for keyword in train_keywords):
        return "Train Ticket"

    elif any(keyword in text for keyword in bus_keywords):
        return "Bus Ticket"

    elif any(keyword in text for keyword in hotel_keywords):
        return "Hotel Booking"

    elif any(keyword in text for keyword in restaurant_keywords):
        return "Restaurant Bill"

    else:
        return "Unknown Document"