from django.db import models

class ReceiptFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='receipts/')
    is_valid = models.BooleanField(default=False)
    invalid_reason = models.TextField(blank=True, null=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Receipt(models.Model):
    purchased_at = models.DateTimeField(null=True, blank=True)
    merchant_name = models.CharField(max_length=255, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    file_path = models.FilePathField(path='media/receipts', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
