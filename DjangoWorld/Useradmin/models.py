from datetime import date, datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from Shoppingcart.models import ShoppingCart

class MyUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def count_shopping_cart_items(self):
        count = 0
        if self.is_authenticated:
            shopping_carts = ShoppingCart.objects.filter(user=self)
            if shopping_carts:
                shopping_cart = shopping_carts.first()
                count = shopping_cart.get_number_of_items()
        return count

    def get_shopping_cart(self):
        shopping_cart=None
        shopping_carts = ShoppingCart.objects.filter(user=self)
        if shopping_carts:
            shopping_cart = shopping_carts.first()
        return shopping_cart

    def can_delete(self):
        return self.is_superuser or self.is_staff

    def can_edit(self):
        return self.is_superuser or self.is_staff

    def __str__(self):
        return self.username
