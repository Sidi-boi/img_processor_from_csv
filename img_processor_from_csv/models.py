from django.db import models
import uuid

class ImageProcessingRequest(models.Model):
    request_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, default='Pending')
    webhook_url = models.URLField(null=True, blank=True)

class ProductImage(models.Model):
    request = models.ForeignKey(ImageProcessingRequest, on_delete=models.CASCADE)
    serial_number = models.IntegerField()
    product_name = models.CharField(max_length=255)
    input_urls = models.TextField()
    output_image = models.ImageField(upload_to='compressed_images/', blank=True, null=True)  
