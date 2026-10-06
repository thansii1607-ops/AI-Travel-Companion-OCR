# AI Travel Companion – Smart Trip Organizer Using OCR

## Overview

AI Travel Companion is an OCR-based travel document organizer that extracts important information from travel documents and displays it in a simple dashboard.

## Live Demo

https://ai-travel-companion-ocr.streamlit.app/

## Features

- Upload multiple travel documents
- OCR-based text extraction
- Automatic document detection
- Flight ticket information extraction
- Train ticket information extraction
- Bus ticket information extraction
- Hotel booking and room details
- Restaurant bill and expense extraction
- Trip timeline organization
- Travel expense information

## Supported Documents

- Flight Tickets
- Train Tickets
- Bus Tickets
- Hotel Bookings
- Hotel / Room Bills
- Restaurant Bills

## Technologies

- Python
- Streamlit
- Tesseract OCR
- Pytesseract
- Pillow
- Regular Expressions

## Project Structure

```text
AI-Travel-Companion-OCR
│
├── app.py
├── ocr.py
├── document_detector.py
├── travel_info.py
├── requirements.txt
└── README.md

Upload Document
      ↓
OCR Text Extraction
      ↓
Document Detection
      ↓
Information Extraction
      ↓
Trip Timeline
      ↓
Expense Information

##Future Enhancements

-Multilingual OCR
-AI itinerary generation
-Automatic expense summary
-PDF trip report
-Travel reminders
-Map integration

## Conclusion

AI Travel Companion simplifies travel management by using OCR to extract and organize important information from travel documents. It provides a convenient way to manage tickets, bookings, bills, travel timelines, and expenses in one place.
