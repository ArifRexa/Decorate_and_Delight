from django.urls import path
from .views import *

urlpatterns = [
    path('jewellery/', jewellery_view, name='jewellery'),
    path('jewellery_details/<int:product_id>', jewellery_details_view, name='jewellery_details'),
    path('bedsheet/', bedsheet_view, name='bedsheet'),
    path('bedsheet_details/<int:product_id>', bedsheet_details_view, name='bedsheet_details'),
]
