import streamlit as st
from PIL import Image
import re

from ocr import extract_text
from document_detector import detect_document_type
from travel_info import extract_travel_info


st.set_page_config(
    page_title="AI Travel Companion",
    page_icon="🌍",
    layout="wide"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #dff4ff 0%, transparent 28%),
        radial-gradient(circle at 90% 20%, #e7e8ff 0%, transparent 30%),
        radial-gradient(circle at 50% 100%, #dff7f1 0%, transparent 35%),
        linear-gradient(135deg, #f4fbff, #eef6fa);
}

.block-container {
    padding-top: 2rem;
}

.main-title {
    text-align: center;
    color: #073b5c;
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #52798c;
    font-size: 18px;
    margin-bottom: 30px;
}

.hero {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.96),
        rgba(231,247,255,0.94)
    );
    padding: 30px;
    border-radius: 24px;
    border: 1px solid #c9e5f2;
    box-shadow: 0 12px 35px rgba(7,59,92,0.10);
    margin-bottom: 25px;
}

.travel-card {
    background: rgba(255,255,255,0.90);
    padding: 24px;
    border-radius: 20px;
    border: 1px solid #d2e7ef;
    box-shadow: 0 8px 25px rgba(7,59,92,0.07);
    margin-bottom: 20px;
}

.section-title {
    color: #073b5c;
    font-size: 25px;
    font-weight: 750;
    margin-bottom: 12px;
}

.document-type {
    background: linear-gradient(135deg, #e5f6ff, #edf5ff);
    padding: 22px;
    border-radius: 18px;
    border-left: 6px solid #298bb5;
    text-align: center;
    color: #075985;
    font-size: 23px;
    font-weight: 750;
    margin: 20px 0;
}

.info-card {
    background: linear-gradient(145deg, #ffffff, #f3faff);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #d3e8f1;
    box-shadow: 0 5px 18px rgba(7,59,92,0.06);
    margin-bottom: 15px;
    min-height: 85px;
}

.info-label {
    color: #628697;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 7px;
}

.info-value {
    color: #073b5c;
    font-size: 18px;
    font-weight: 750;
}

.route-card {
    background: linear-gradient(135deg, #eaf8ff, #f3f9ff);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #c8e5f1;
    text-align: center;
    margin: 15px 0 25px 0;
}

.route-place {
    color: #073b5c;
    font-size: 22px;
    font-weight: 750;
}

.route-arrow {
    color: #298bb5;
    font-size: 28px;
    padding: 0 15px;
}

.feature-card {
    background: rgba(255,255,255,0.90);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #d2e7ef;
    min-height: 150px;
    box-shadow: 0 7px 22px rgba(7,59,92,0.06);
}

.feature-title {
    color: #073b5c;
    font-size: 19px;
    font-weight: 750;
}

.feature-text {
    color: #607d8b;
    font-size: 14px;
    line-height: 1.6;
}

.timeline-card {
    background: linear-gradient(135deg, #ffffff, #f1faff);
    padding: 22px;
    border-radius: 18px;
    border-left: 6px solid #298bb5;
    border-top: 1px solid #d3e8f1;
    border-right: 1px solid #d3e8f1;
    border-bottom: 1px solid #d3e8f1;
    margin-bottom: 15px;
    box-shadow: 0 6px 20px rgba(7,59,92,0.07);
}

.timeline-date {
    color: #298bb5;
    font-size: 15px;
    font-weight: 700;
}

.timeline-title {
    color: #073b5c;
    font-size: 20px;
    font-weight: 750;
    margin-top: 5px;
}

.timeline-info {
    color: #607d8b;
    font-size: 14px;
    margin-top: 5px;
}

.footer {
    text-align: center;
    color: #718d9b;
    font-size: 14px;
    padding: 30px 0 10px 0;
}

.stButton > button {
    background: linear-gradient(135deg, #176b87, #298bb5);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e8f6fc, #f5fbff);
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE & EXPENSE HELPERS
# =====================================================

if "analyzed_documents" not in st.session_state:
    st.session_state.analyzed_documents = {}


def amount_to_number(value):
    if value is None:
        return 0.0

    value = str(value).strip()

    if not value or value.lower() in {
        "not detected",
        "none",
        "n/a",
        "na"
    }:
        return 0.0

    cleaned = value.replace(",", "")
    cleaned = re.sub(r"[^\d.]", "", cleaned)

    if not cleaned:
        return 0.0

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def format_amount(amount):
    return f"₹ {amount:,.2f}"


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:15px;">

    <div style="font-size:55px;">🌍</div>

    <h2 style="color:#073b5c;">
    Travel Companion
    </h2>

    <p style="color:#668594;">
    Your AI-powered travel organizer
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🧠 AI Capabilities")

    st.markdown("""
    ✨ OCR Text Extraction

    🧳 Document Detection

    👤 Passenger Detection

    📅 Date Detection

    🕐 Time Detection

    📍 Route Detection

    🎫 Booking Detection

    ✈️ Flight Details

    💺 Seat Detection

    🚪 Gate Detection

    🗓️ Trip Timeline

    💰 Expense Tracking
    """)

    st.divider()

    st.info(
        "Upload your travel document and let AI organize your journey."
    )


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown(
    '<div class="main-title">🌍 AI Travel Companion</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">✈️ Smart Trip Organizer Powered by OCR & AI</div>',
    unsafe_allow_html=True
)


# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""
<div class="hero">

<h2 style="color:#073b5c;">
🧭 Your Journey, Organized by AI
</h2>

<p style="color:#52798c; font-size:17px;">
Turn your travel documents into a smart digital trip plan.
Upload your tickets, bookings or bills and let AI
extract important information automatically.
</p>

<p style="font-size:19px;">
✈️ Flight &nbsp;&nbsp;
🚆 Train &nbsp;&nbsp;
🚌 Bus &nbsp;&nbsp;
🏨 Hotel &nbsp;&nbsp;
🍽️ Restaurant
</p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# UPLOAD
# =====================================================

st.markdown(
    '<div class="section-title">📂 Upload Your Travel Documents</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "🧳 Choose your travel documents",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if st.session_state.analyzed_documents:

    if st.button(
        "🗑️ Clear Analyzed Documents",
        key="clear_analyzed_documents"
    ):
        st.session_state.analyzed_documents = {}
        st.rerun()


# =====================================================
# DOCUMENT PROCESSING
# =====================================================

if uploaded_files:

    st.success(
        f"🎉 {len(uploaded_files)} document(s) uploaded successfully!"
    )

    for file in uploaded_files:

        st.markdown(
            '<div class="travel-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <h3 style="color:#073b5c;">
            📄 {file.name}
            </h3>
            """,
            unsafe_allow_html=True
        )

        image = Image.open(file)

        st.image(
            image,
            caption="🧳 Travel Document",
            width=600
        )

        analyze = st.button(
            "🔍 Analyze My Document",
            key=f"analyze_{file.name}"
        )

        if analyze:

            with st.spinner(
                "🤖 AI is scanning your document..."
            ):

                text = extract_text(image)

            if text.strip():

                st.success(
                    "✅ OCR successfully extracted text!"
                )

                # =================================================
                # DOCUMENT TYPE
                # =================================================

                document_type = detect_document_type(text)

                st.markdown(
                    f"""
                    <div class="document-type">

                    🧳 DOCUMENT DETECTED

                    <br><br>

                    {document_type}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # =================================================
                # TRAVEL INFORMATION
                # =================================================

                travel_info = extract_travel_info(
                    text,
                    document_type
                )

                # =================================================
                # SAVE ANALYZED DOCUMENT
                # =================================================

                st.session_state.analyzed_documents[file.name] = {
                    "file": file.name,
                    "document_type": document_type,
                    "travel_info": travel_info,
                    "ocr_text": text
                }

                # =================================================
                # JOURNEY DETAILS
                # =================================================

                st.markdown(
                    '<div class="section-title">🗺️ Journey Details</div>',
                    unsafe_allow_html=True
                )

                from_place = travel_info.get(
                    "From",
                    "Not detected"
                )

                to_place = travel_info.get(
                    "To",
                    "Not detected"
                )

                st.markdown(
                    f"""
                    <div class="route-card">

                    <div style="
                    color:#668594;
                    font-size:14px;
                    margin-bottom:12px;
                    ">
                    🧭 TRAVEL ROUTE
                    </div>

                    <span class="route-place">
                    📍 {from_place}
                    </span>

                    <span class="route-arrow">
                    ✈️ ━━━━━ ✈️
                    </span>

                    <span class="route-place">
                    📍 {to_place}
                    </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # =================================================
                # COMMON INFORMATION
                # =================================================

                st.markdown(
                    '<div class="section-title">✈️ Travel Information</div>',
                    unsafe_allow_html=True
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.markdown(
                        f"""
                        <div class="info-card">

                        <div class="info-label">
                        👤 PASSENGER
                        </div>

                        <div class="info-value">
                        {travel_info.get(
                            "Passenger Name",
                            "Not detected"
                        )}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:

                    st.markdown(
                        f"""
                        <div class="info-card">

                        <div class="info-label">
                        📅 TRAVEL DATE
                        </div>

                        <div class="info-value">
                        {travel_info.get(
                            "Travel Date",
                            "Not detected"
                        )}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col3:

                    st.markdown(
                        f"""
                        <div class="info-card">

                        <div class="info-label">
                        🕐 TRAVEL TIME
                        </div>

                        <div class="info-value">
                        {travel_info.get(
                            "Travel Time",
                            "Not detected"
                        )}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                col4, col5, col6 = st.columns(3)

                with col4:

                    st.markdown(
                        f"""
                        <div class="info-card">

                        <div class="info-label">
                        📍 FROM
                        </div>

                        <div class="info-value">
                        {travel_info.get(
                            "From",
                            "Not detected"
                        )}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col5:

                    st.markdown(
                        f"""
                        <div class="info-card">

                        <div class="info-label">
                        📍 TO
                        </div>

                        <div class="info-value">
                        {travel_info.get(
                            "To",
                            "Not detected"
                        )}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col6:

                    st.markdown(
                        f"""
                        <div class="info-card">

                        <div class="info-label">
                        🎫 PNR / BOOKING
                        </div>

                        <div class="info-value">
                        {travel_info.get(
                            "PNR / Booking Number",
                            "Not detected"
                        )}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # =================================================
                # FLIGHT
                # =================================================

                if document_type == "Flight Ticket":

                    st.markdown(
                        '<div class="section-title">✈️ Flight Details</div>',
                        unsafe_allow_html=True
                    )

                    col7, col8, col9 = st.columns(3)

                    with col7:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            ✈️ FLIGHT NUMBER
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Flight Number",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col8:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            💺 SEAT
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Seat",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col9:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🚪 GATE
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Gate",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    col10, col11 = st.columns(2)

                    with col10:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🛫 BOARDING TIME
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Boarding Time",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with col11:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🧳 DOCUMENT
                            </div>

                            <div class="info-value">
                            Flight Boarding Pass
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                # =================================================
                # TRAIN
                # =================================================

                if document_type == "Train Ticket":

                    st.markdown(
                        '<div class="section-title">🚆 Train Details</div>',
                        unsafe_allow_html=True
                    )

                    train_col1, train_col2, train_col3 = st.columns(3)

                    with train_col1:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🚆 TRAIN NUMBER
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Train Number",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with train_col2:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🚪 COACH
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Coach",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with train_col3:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🪑 BERTH
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Berth",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                # =================================================
                # BUS
                # =================================================

                if document_type == "Bus Ticket":

                    st.markdown(
                        '<div class="section-title">🚌 Bus Details</div>',
                        unsafe_allow_html=True
                    )

                    bus_col1, bus_col2, bus_col3 = st.columns(3)

                    with bus_col1:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🚌 BUS NUMBER
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Bus Number",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with bus_col2:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            📍 BOARDING POINT
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Boarding Point",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with bus_col3:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            📍 DROP POINT
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Drop Point",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                # =================================================
                # HOTEL
                # =================================================

                if document_type == "Hotel Booking":

                    st.markdown(
                        '<div class="section-title">🏨 Hotel Details</div>',
                        unsafe_allow_html=True
                    )

                    hotel_col1, hotel_col2, hotel_col3, hotel_col4 = st.columns(4)

                    with hotel_col1:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🏨 HOTEL
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Hotel Name",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with hotel_col2:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🛎️ CHECK-IN
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Check-in",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with hotel_col3:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🏁 CHECK-OUT
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Check-out",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    with hotel_col4:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            💰 HOTEL AMOUNT
                            </div>

                            <div class="info-value">
                            ₹ {travel_info.get(
                                "Hotel Amount",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                # =================================================
                # RESTAURANT
                # =================================================

                if document_type == "Restaurant Bill":

                    st.markdown(
                        '<div class="section-title">🍽️ Expense Details</div>',
                        unsafe_allow_html=True
                    )

                    expense_col1, expense_col2 = st.columns(2)

                    with expense_col1:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            💰 TOTAL AMOUNT
                            </div>

                            <div class="info-value">
                            ₹ {travel_info.get(
                                "Total Amount",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with expense_col2:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🧾 GST
                            </div>

                            <div class="info-value">
                            ₹ {travel_info.get(
                                "GST Amount",
                                "Not detected"
                            )}
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                # =================================================
                # OCR TEXT
                # =================================================

                st.markdown(
                    '<div class="section-title">📝 AI Extracted Text</div>',
                    unsafe_allow_html=True
                )

                st.write(
                    "The following text was recognized from your document:"
                )

                st.code(
                    text,
                    language=None
                )

                with st.expander("🔎 View Raw OCR Text"):

                    st.text_area(
                        "OCR Text",
                        text,
                        height=300,
                        key=f"ocr_{file.name}"
                    )

                st.success(
                    "✨ Your travel document has been successfully analyzed!"
                )

            else:

                st.error(
                    "❌ No readable text found. "
                    "Please upload a clearer image."
                )

        st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# BUILD TIMELINE DATA FROM SESSION STATE
# =====================================================

timeline_data = []

for item in st.session_state.analyzed_documents.values():

    info = item.get("travel_info", {})

    timeline_data.append({
        "file": item.get("file", "Unknown"),
        "document_type": item.get(
            "document_type",
            "Unknown Document"
        ),
        "date": info.get(
            "Travel Date",
            "Not detected"
        ),
        "time": info.get(
            "Travel Time",
            "Not detected"
        ),
        "from": info.get(
            "From",
            "Not detected"
        ),
        "to": info.get(
            "To",
            "Not detected"
        )
    })


# =====================================================
# TRIP TIMELINE
# =====================================================

if timeline_data:

    st.markdown(
        '<div class="section-title">🗓️ Trip Timeline</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Your analyzed travel documents are organized into a simple journey timeline."
    )

    for item in timeline_data:

        st.markdown(
            f"""
            <div class="timeline-card">

            <div class="timeline-date">
            📅 {item["date"]} &nbsp; | &nbsp; 🕐 {item["time"]}
            </div>

            <div class="timeline-title">
            {item["document_type"]}
            </div>

            <div class="timeline-info">
            📄 {item["file"]}
            </div>

            <div class="timeline-info">
            📍 {item["from"]}
            &nbsp;&nbsp; → &nbsp;&nbsp;
            {item["to"]}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# TRAVEL EXPENSE TRACKER
# =====================================================

hotel_total = 0.0
restaurant_total = 0.0
gst_total = 0.0

expense_rows = []

for item in st.session_state.analyzed_documents.values():

    document_type = item.get(
        "document_type",
        "Unknown Document"
    )

    info = item.get(
        "travel_info",
        {}
    )

    file_name = item.get(
        "file",
        "Unknown"
    )

    if document_type == "Hotel Booking":

        amount = amount_to_number(
            info.get(
                "Hotel Amount",
                "Not detected"
            )
        )

        if amount > 0:

            hotel_total += amount

            expense_rows.append({
                "Document": file_name,
                "Type": "Hotel",
                "Amount": amount,
                "GST": 0.0
            })

    elif document_type == "Restaurant Bill":

        amount = amount_to_number(
            info.get(
                "Total Amount",
                "Not detected"
            )
        )

        gst = amount_to_number(
            info.get(
                "GST Amount",
                "Not detected"
            )
        )

        if amount > 0 or gst > 0:

            restaurant_total += amount
            gst_total += gst

            expense_rows.append({
                "Document": file_name,
                "Type": "Restaurant",
                "Amount": amount,
                "GST": gst
            })


total_travel_expense = hotel_total + restaurant_total


if expense_rows:

    st.markdown(
        '<div class="section-title">💰 Travel Expense Summary</div>',
        unsafe_allow_html=True
    )

    st.write(
        "AI automatically collects hotel and restaurant expenses "
        "from your analyzed travel documents."
    )

    expense_col1, expense_col2, expense_col3, expense_col4 = st.columns(4)

    with expense_col1:

        st.markdown(
            f"""
            <div class="info-card">

            <div class="info-label">
            🏨 HOTEL EXPENSE
            </div>

            <div class="info-value">
            {format_amount(hotel_total)}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with expense_col2:

        st.markdown(
            f"""
            <div class="info-card">

            <div class="info-label">
            🍽️ RESTAURANT EXPENSE
            </div>

            <div class="info-value">
            {format_amount(restaurant_total)}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with expense_col3:

        st.markdown(
            f"""
            <div class="info-card">

            <div class="info-label">
            🧾 TOTAL GST
            </div>

            <div class="info-value">
            {format_amount(gst_total)}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with expense_col4:

        st.markdown(
            f"""
            <div class="info-card">

            <div class="info-label">
            💳 TOTAL TRAVEL EXPENSE
            </div>

            <div class="info-value">
            {format_amount(total_travel_expense)}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-title">📊 Expense Breakdown</div>',
        unsafe_allow_html=True
    )

    for row in expense_rows:

        st.markdown(
            f"""
            <div class="timeline-card">

            <div class="timeline-title">
            {row["Type"]} Expense
            </div>

            <div class="timeline-info">
            📄 {row["Document"]}
            </div>

            <div class="timeline-info">
            💰 Amount: {format_amount(row["Amount"])}
            </div>

            <div class="timeline-info">
            🧾 GST: {format_amount(row["GST"])}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# SMART FEATURES
# =====================================================

st.markdown(
    '<div class="section-title">🚀 Smart Travel Features</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="feature-card">

    <div class="feature-title">
    🗓️ Trip Timeline
    </div>

    <p class="feature-text">
    Automatically organize travel dates,
    departure times and journey events.
    </p>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="feature-card">

    <div class="feature-title">
    🧭 Smart Route Detection
    </div>

    <p class="feature-text">
    Extract From and To locations
    from travel documents.
    </p>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown("""
    <div class="feature-card">

    <div class="feature-title">
    💰 Travel Expense Tracker
    </div>

    <p class="feature-text">
    Detect hotel and restaurant bills
    and organize travel expenses.
    </p>

    </div>
    """, unsafe_allow_html=True)


st.write("")


col4, col5, col6 = st.columns(3)

with col4:

    st.markdown("""
    <div class="feature-card">

    <div class="feature-title">
    🌐 Multilingual OCR
    </div>

    <p class="feature-text">
    English OCR is active with multilingual
    OCR support planned for the next phase.
    </p>

    </div>
    """, unsafe_allow_html=True)


with col5:

    st.markdown("""
    <div class="feature-card">

    <div class="feature-title">
    📑 Multiple Documents
    </div>

    <p class="feature-text">
    Upload multiple tickets, bookings
    and bills together.
    </p>

    </div>
    """, unsafe_allow_html=True)


with col6:

    st.markdown("""
    <div class="feature-card">

    <div class="feature-title">
    📥 Trip Summary
    </div>

    <p class="feature-text">
    Organize analyzed documents into a
    digital trip timeline and summary view.
    </p>

    </div>
    """, unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">

🌍 ───────────────────────────────── 🌍

<br><br>

<b>AI Travel Companion</b>

<br>

✈️ Smart Travel • 🧠 Intelligent OCR • 🗺️ Simple Journey Planning

<br><br>

Built with Python • Tesseract OCR • Streamlit

</div>
""", unsafe_allow_html=True)



               

                       
                      

                        

                           
