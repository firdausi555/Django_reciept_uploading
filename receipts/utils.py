import pytesseract
from pdf2image import convert_from_path
import tempfile
import re
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ''
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def extract_receipt_details(text):
    merchant_name = text.splitlines()[0][:255]
    amount_match = re.search(r'\bTotal[:\s]*\$?([\d.,]+)', text, re.IGNORECASE)
    total_amount = float(amount_match.group(1).replace(',', '')) if amount_match else None

    date_match = re.search(r'(\d{2}/\d{2}/\d{4})', text)
    purchased_at = datetime.strptime(date_match.group(1), '%m/%d/%Y') if date_match else None

    return merchant_name, total_amount, purchased_at
