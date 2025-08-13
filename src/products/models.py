import uuid
from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    brand = models.CharField(max_length=255)
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductViewMetric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    product_id = models.UUIDField() 
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.product_id} - {self.ip_address} - {self.created_at}"