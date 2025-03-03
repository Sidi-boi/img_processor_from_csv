from django.urls import path
from .views import upload_csv, get_status

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('status/<uuid:request_id>/', get_status, name='status_api'),
]
