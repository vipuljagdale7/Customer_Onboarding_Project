from django.urls import path
from .views import create_customer, upload_document, customer_list

urlpatterns = [
    path('create/', create_customer, name='create_customer'),
    path('upload/<int:customer_id>/', upload_document, name='upload_document'),
    path('list/', customer_list, name='customer_list'),
]
