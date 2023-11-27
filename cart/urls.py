from django.urls import path
from .views import *

urlpatterns = [
    path('add-to-cart/<int:product_id>/', add_cart_view, name='add_cart'),

    path('', cart_view, name='cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', remove_cart_view, name='remove_cart'),
    # path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', remove_cart_item_view, name='remove_cart_item'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', remove_cart_item_view, name='remove_cart_item'),

    path('checkout/', checkout_view, name='checkout'),
    # path('add_cart/<int:product_id>/', add_cart_view, name='add_cart'),
]
