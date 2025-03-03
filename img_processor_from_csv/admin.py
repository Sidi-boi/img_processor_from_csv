from django.contrib import admin
from .models import ImageProcessingRequest, ProductImage


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'serial_number', 'output_image')
    
admin.site.register(ImageProcessingRequest)
admin.site.register(ProductImage)
