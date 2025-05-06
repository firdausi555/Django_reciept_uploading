from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ReceiptFile, Receipt
from .serializers import ReceiptFileSerializer, ReceiptSerializer
from .utils import extract_text_from_pdf, extract_receipt_details
from django.core.files.storage import default_storage
import fitz  # PyMuPDF
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1>Welcome to the Receipt Processing App!</h1>
        <p>Available endpoints:</p>
        <ul>
            <li><a href="/upload">/upload</a> - Upload a receipt</li>
            <li><a href="/validate">/validate</a> - Validate a receipt</li>
            <li><a href="/process">/process</a> - Process a receipt</li>
            <li><a href="/receipts">/receipts</a> - List all receipts</li>
        </ul>
    """)


@api_view(['GET', 'POST'])
def upload_receipt(request):
    if request.method == 'GET':
        return Response({
            "message": "Send a POST request with a PDF file to upload."
        })

    file = request.FILES.get('file')
    if file and file.name.endswith('.pdf'):
        path = default_storage.save(f'receipts/{file.name}', file)
        receipt_file = ReceiptFile.objects.create(file_name=file.name, file_path=path)
        return Response(ReceiptFileSerializer(receipt_file).data)

    return Response({'error': 'Only PDF files allowed or file missing'}, status=400)


@api_view(['POST'])
def validate_receipt(request):
    receipt_id = request.data.get('id')
    try:
        receipt_file = ReceiptFile.objects.get(id=receipt_id)
        doc = fitz.open(receipt_file.file_path.path)
        receipt_file.is_valid = True
        receipt_file.invalid_reason = ''
    except Exception as e:
        receipt_file.is_valid = False
        receipt_file.invalid_reason = str(e)
    receipt_file.save()
    return Response(ReceiptFileSerializer(receipt_file).data)

@api_view(['POST'])
def process_receipt(request):
    receipt_id = request.data.get('id')
    receipt_file = ReceiptFile.objects.get(id=receipt_id)
    if not receipt_file.is_valid:
        return Response({'error': 'File is not valid'}, status=400)

    text = extract_text_from_pdf(receipt_file.file_path.path)
    merchant, total, date = extract_receipt_details(text)

    receipt, _ = Receipt.objects.update_or_create(
        file_path=receipt_file.file_path.path,
        defaults={
            'merchant_name': merchant,
            'total_amount': total,
            'purchased_at': date,
        }
    )
    receipt_file.is_processed = True
    receipt_file.save()
    return Response(ReceiptSerializer(receipt).data)

@api_view(['GET'])
def list_receipts(request):
    receipts = Receipt.objects.all()
    return Response(ReceiptSerializer(receipts, many=True).data)

@api_view(['GET'])
def get_receipt(request, id):
    receipt = Receipt.objects.get(id=id)
    return Response(ReceiptSerializer(receipt).data)
