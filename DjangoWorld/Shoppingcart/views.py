from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .models import ShoppingCart, ShoppingCartItem, Payment, PaymentItem
from decimal import Decimal

def show_shopping_cart(request):
    user = request.user
    payments = Payment.objects.filter(user=user)
    if request.method == 'POST':
        if 'empty' in request.POST:
            ShoppingCart.objects.get(user=request.user).delete()
            context = {
                'site': 'shopping-cart',
                'shopping_cart_is_empty': True,
                'shopping_cart_items': None,
                'amount': 0,
                'payments': payments,
                'payment_count': len(payments)
            }
            return render(request,'shopping-cart.html', context)
        elif 'pay' in request.POST:
            return redirect('shopping-cart-pay')
    else:
        shopping_cart_is_empty = True
        shopping_cart_items = None
        total = Decimal(0.0)
        if user.is_authenticated:
            shopping_cart = ShoppingCart.objects.filter(user=user).first()
            if shopping_cart:
                shopping_cart_is_empty = False
                shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)
                total = shopping_cart.get_total()
        context = {
            'site': 'shopping-cart',
            'shopping_cart_is_empty': shopping_cart_is_empty,
            'shopping_cart_items': shopping_cart_items,
            'total': total,
            'payments': payments,
            'payment_count': len(payments)
        }
        return render(request, 'shopping-cart.html', context)

@login_required(login_url='/useradmin/login/')
def pay(request):
    user = request.user
    shopping_cart_is_empty = True
    paid = False
    form = None
    items = None
    amount=0.0
    # POST Request
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        form.instance.user = user
        if form.is_valid():
            form.save()
            paid = True
            shopping_cart = ShoppingCart.objects.filter(user=user).first()
            for item in ShoppingCartItem.objects.filter(shopping_cart=shopping_cart):
                form.instance.add_item(item.game, item.quantity)
            ShoppingCart.objects.filter(user=user).first().delete()
        else:
            print(form.errors)
    # GET Request
    else:
        shopping_cart = ShoppingCart.objects.filter(user=user).first()
        if shopping_cart:
            shopping_cart_is_empty = False
            items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)
            form = PaymentForm()
            amount = shopping_cart.get_total()
    context = {
        'site': 'payment',
        'shopping_cart_is_empty': shopping_cart_is_empty,
        'payment_form': form,
        'amount': amount,
        'paid': paid,
        'shopping_cart_items': items
    }
    return render(request, 'pay.html', context)

@login_required(login_url='/useradmin/login/')
def payment_detail(request, pk):
    user = request.user
    payment = Payment.objects.get(pk=pk, user=user)
    payment_items = payment.get_items()
    shopping_cart = ShoppingCart.objects.filter(user=user).first()
    context = {
    "user": user,
    "payment": payment,
    "payment_items": payment_items,
    'shopping_cart': shopping_cart
    }
    return render(request, 'payment_detail.html', context)
