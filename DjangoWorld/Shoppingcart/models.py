from sqlite3 import Timestamp
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.db import models
from Games.models import Comment, Game

# Create your models here.

class ShoppingCart(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def add_item(user, game, quantity=1):
        shopping_cart = ShoppingCart.objects.filter(user=user).first()
        if shopping_cart:
            item = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart, game=game).first()
        else:
            shopping_cart = ShoppingCart.objects.create(user=user)
            item=None
        if item:
            item.quantity=item.quantity+quantity
            item.save()
        else:
            ShoppingCartItem.objects.create(
                                            quantity=quantity,
                                            shopping_cart=shopping_cart,
                                            game=game
                                            )
    def get_number_of_items(self):
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        count = 0
        for item in shopping_cart_items:
            count += item.quantity
        return count

    def get_total(self):
        total = Decimal(0.0)
        shopping_cart_items= ShoppingCartItem.objects.filter(shopping_cart=self)
        for item in shopping_cart_items:
            total += item.game.price * item.quantity
        return total

    def get_items(self):
        return ShoppingCartItem.objects.filter(shopping_cart=self)


class ShoppingCartItem(models.Model):
    quantity = models.IntegerField(default=1)
    shopping_cart = models.ForeignKey(ShoppingCart,on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def amount(self):
        return self.game.price*self.quantity

class Payment(models.Model):
    credit_card_number = models.CharField(max_length=19)
    expiry_date = models.CharField(max_length=7)
    # amount = models.DecimalField(decimal_places=2,max_digits=10)
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def amount(self):
        total = 0.0
        for item in self.get_items():
            total += item.game.price * item.quantity
        return total

    def add_item(self, game, quantity=1):
        item = PaymentItem.objects.filter(payment=self, game=game).first()
        if item:
            item.quantity = item.quantity + quantity
            item.quantity.save()
        else:
            PaymentItem.objects.create(
                                       quantity=quantity,
                                       game=game,
                                       payment=self
                                       )
    def get_items(self):
        return PaymentItem.objects.filter(payment=self)

    def get_number_of_items(self):
        return self.get_items().count()

class PaymentItem(models.Model):
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
