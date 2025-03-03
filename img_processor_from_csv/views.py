import csv
from concurrent.futures import ThreadPoolExecutor
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse
from .models import ImageProcessingRequest, ProductImage
from .utils import process_images 
import logging
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_csv(request):
    logger.info("Received a CSV upload request.")

    csv_file = request.FILES.get('file')
    webhook_url = request.data.get('webhook_url')

    if not csv_file:
        logger.error("No file uploaded.")
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    # Create request entry in DB with "Pending" status
    request_obj = ImageProcessingRequest.objects.create(webhook_url=webhook_url)
    logger.info(f"Created new ImageProcessingRequest with ID {request_obj.request_id}")

    try:
        # Read CSV and store entries in DB
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        next(reader) 

        for row in reader:
            serial_number, product_name, input_urls = row[:3]
            ProductImage.objects.create(
                request=request_obj,
                serial_number=int(serial_number),
                product_name=product_name,
                input_urls=input_urls
            )
            logger.info(f"Stored product: {product_name} (Serial: {serial_number}) with images.")

        # Start image processing asynchronously
        logger.info(f"Starting async image processing for request {request_obj.request_id}")
        ThreadPoolExecutor().submit(process_images, request_obj.request_id)

        # Return request ID instantly
        logger.info(f"Returning request ID {request_obj.request_id} to client.")
        return JsonResponse({'request_id': str(request_obj.request_id)})

    except Exception as e:
        # If any error occurs, update status to "Failed"
        request_obj.status = "Failed"
        request_obj.save()
        logger.error(f"Error processing request {request_obj.request_id}: {str(e)}")
        return JsonResponse({'error': 'Failed to process CSV'}, status=500)

@api_view(['GET'])
def get_status(request_id):
    logger.info(f"Checking status for request ID: {request_id}")

    request_obj = get_object_or_404(ImageProcessingRequest, request_id=request_id)

    if request_obj.status == "Completed":
        logger.info(f"Request ID {request_id} has completed processing.")
        return JsonResponse({'request_id': str(request_id), 'status': 'Completed'})
    else:
        logger.info(f"Request ID {request_id} is still processing.")
        return JsonResponse({'request_id': str(request_id), 'status': 'In Process'})

