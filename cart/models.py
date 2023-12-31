from django.db import models
from store.models import Products
# from accounts.models import CustomUser
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def _str_(self):
        return self.cart_id


class CartItem(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def _self_(self):
        return self.product
