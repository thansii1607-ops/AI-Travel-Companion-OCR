import streamlit as st
from PIL import Image

from ocr import extract_text
from document_detector import detect_document_type
from travel_info import extract_travel_info


st.set_page_config(
    page_title="AI Travel Companion",
    page_icon="🌍",
    layout="wide"
)



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

    🏨 Hotel Details

    🍽️ Restaurant Bills

    🗓️ Trip Timeline

    💰 Expense Tracking
    """)

    st.divider()

    st.info(
        "Upload your travel document and let AI organize your journey."
    )




st.markdown(
    '<div class="main-title">🌍 AI Travel Companion</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">✈️ Smart Trip Organizer Powered by OCR & AI</div>',
    unsafe_allow_html=True
)




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




st.markdown(
    '<div class="section-title">📂 Upload Your Travel Documents</div>',
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "🧳 Choose your travel documents",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)



timeline_data = []

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

            if text and text.strip():

                st.success(
                    "✅ OCR successfully extracted text!"
                )

               

                document_type = detect_document_type(text)

                
                lower_text = text.lower()

                restaurant_score = sum([
                    "restaurant" in lower_text,
                    "subtotal" in lower_text,
                    "cgst" in lower_text,
                    "sgst" in lower_text,
                    "grand total" in lower_text,
                    "table no" in lower_text,
                    "payment mode" in lower_text
                ])

                if restaurant_score >= 2:
                    document_type = "Restaurant Bill"

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

               

                travel_info = extract_travel_info(
                    text,
                    document_type
                )

                

                if document_type == "Restaurant Bill":

                    st.markdown(
                        '<div class="section-title">🍽️ Restaurant Bill Details</div>',
                        unsafe_allow_html=True
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            📅 BILL DATE
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

                    with col2:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🕐 TIME
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

                    with col3:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            🧾 BILL NUMBER
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Bill Number",
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
                            💰 SUBTOTAL
                            </div>

                            <div class="info-value">
                            ₹ {travel_info.get(
                                "Subtotal",
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

                    with col6:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            💰 GRAND TOTAL
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

                    col7, col8, col9 = st.columns(3)

                    with col7:

                        st.markdown(
                            f"""
                            <div class="info-card">

                            <div class="info-label">
                            💳 PAYMENT MODE
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Payment Mode",
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
                            ✅ PAYMENT STATUS
                            </div>

                            <div class="info-value">
                            {travel_info.get(
                                "Payment Status",
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
                            📍 LOCATION
                            </div>

                            <div class="info-value">
                            Bengaluru, Karnataka
                            </div>

                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    timeline_data.append({
                        "file": file.name,
                        "document_type": "Restaurant Bill",
                        "date": travel_info.get(
                            "Travel Date",
                            "Not detected"
                        ),
                        "time": travel_info.get(
                            "Travel Time",
                            "Not detected"
                        ),
                        "from": "Restaurant",
                        "to": "Bengaluru"
                    })

                else:

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
                    # COMMON TRAVEL INFORMATION
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

                        c1, c2, c3 = st.columns(3)

                        with c1:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">✈️ FLIGHT NUMBER</div>
                                <div class="info-value">
                                {travel_info.get("Flight Number", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with c2:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">💺 SEAT</div>
                                <div class="info-value">
                                {travel_info.get("Seat", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with c3:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">🚪 GATE</div>
                                <div class="info-value">
                                {travel_info.get("Gate", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    # =================================================
                    # TRAIN
                    # =================================================

                    elif document_type == "Train Ticket":

                        st.markdown(
                            '<div class="section-title">🚆 Train Details</div>',
                            unsafe_allow_html=True
                        )

                        c1, c2, c3 = st.columns(3)

                        with c1:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">🚆 TRAIN NUMBER</div>
                                <div class="info-value">
                                {travel_info.get("Train Number", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with c2:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">🚪 COACH</div>
                                <div class="info-value">
                                {travel_info.get("Coach", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with c3:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">🪑 BERTH</div>
                                <div class="info-value">
                                {travel_info.get("Berth", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    # =================================================
                    # BUS
                    # =================================================

                    elif document_type == "Bus Ticket":

                        st.markdown(
                            '<div class="section-title">🚌 Bus Details</div>',
                            unsafe_allow_html=True
                        )

                        c1, c2, c3 = st.columns(3)

                        with c1:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">🚌 BUS NUMBER</div>
                                <div class="info-value">
                                {travel_info.get("Bus Number", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with c2:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">📍 BOARDING POINT</div>
                                <div class="info-value">
                                {travel_info.get("Boarding Point", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with c3:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">📍 DROP POINT</div>
                                <div class="info-value">
                                {travel_info.get("Drop Point", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    # =================================================
                    # HOTEL
                    # =================================================

                    elif document_type == "Hotel Booking":

                        st.markdown(
                            '<div class="section-title">🏨 Hotel Details</div>',
                            unsafe_allow_html=True
                        )

                        c1, c2, c3 = st.columns(3)

                        with c1:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">🏨 HOTEL</div>
                                <div class="info-value">
                                {travel_info.get("Hotel Name", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with c2:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">🛎️ CHECK-IN</div>
                                <div class="info-value">
                                {travel_info.get("Check-in", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with c3:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">🏁 CHECK-OUT</div>
                                <div class="info-value">
                                {travel_info.get("Check-out", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        c4, c5 = st.columns(2)

                        with c4:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">🛏️ ROOM</div>
                                <div class="info-value">
                                {travel_info.get("Room", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with c5:
                            st.markdown(
                                f"""
                                <div class="info-card">
                                <div class="info-label">💰 HOTEL AMOUNT</div>
                                <div class="info-value">
                                ₹ {travel_info.get("Hotel Amount", "Not detected")}
                                </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    # =================================================
                    # TIMELINE
                    # =================================================

                    timeline_data.append({
                        "file": file.name,
                        "document_type": document_type,
                        "date": travel_info.get(
                            "Travel Date",
                            "Not detected"
                        ),
                        "time": travel_info.get(
                            "Travel Time",
                            "Not detected"
                        ),
                        "from": travel_info.get(
                            "From",
                            "Not detected"
                        ),
                        "to": travel_info.get(
                            "To",
                            "Not detected"
                        )
                    })

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
    Support for English and multiple
    Indian languages.
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
    Organize analyzed documents into
    a digital trip timeline and summary.
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
