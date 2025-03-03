import uuid
import requests
from io import BytesIO
from PIL import Image
from .models import ImageProcessingRequest, ProductImage
from concurrent.futures import ThreadPoolExecutor
import logging 
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

def process_images(request_id):
    try:
        request_obj = ImageProcessingRequest.objects.get(request_id=request_id)
        images = ProductImage.objects.filter(request=request_obj)

        def process_image(image):
            input_urls = image.input_urls.split(',')

            for url in input_urls:
                try:
                    response = requests.get(url.strip())
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        img_io = BytesIO()
                        img.save(img_io, format='JPEG', quality=50)

                        filename = f'compressed_{uuid.uuid4().hex}.jpg'
                        compressed_image_file = ContentFile(img_io.getvalue(), name=filename)

                        image.output_image.save(filename, compressed_image_file)  # Store compressed image in DB
                        image.save()
                    else:
                        logger.error(f"Failed to download image from {url}")
                except Exception as e:
                    logger.error(f"Error processing image {url}: {str(e)}")

        # Process images asynchronously
        with ThreadPoolExecutor() as executor:
            executor.map(process_image, images)

        request_obj.status = 'Completed'
        request_obj.save()

        if request_obj.webhook_url:
            requests.post(request_obj.webhook_url, json={'request_id': str(request_id), 'status': 'Completed'})

    except Exception as e:
        logger.error(f"Error in processing images for request {request_id}: {str(e)}")
        request_obj.status = 'Failed'
        request_obj.save()