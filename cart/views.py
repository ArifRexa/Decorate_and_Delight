from django.shortcuts import render, redirect, get_object_or_404
from store.models import Products
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Create your views here.
from django.http import HttpResponse


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


CustomUser = get_user_model()


def add_cart_view(request, product_id):
    current_user = request.user
    product = Products.objects.get(id=product_id)  # get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            print(cart_items)
            item = CartItem.objects.get(product=product, user=current_user)
            item.quantity += 1
            item.save()

        else:
            try:
                cart = Cart.objects.get(
                    cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=_cart_id(request)
                )
            cart.save()
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                user=current_user
            )
            cart_item.save()
        return redirect('cart')
    else:
        product = Products.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
            cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            cart.save()
    return redirect('cart')


# def add_cart_view(request, product_id):
#     # current_user = request.user
#     product = Products.objects.get(id=product_id)  # get the product
#
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(
#             cart_id=_cart_id(request)
#         )
#         cart.save()
#
#     try:
#         cart_item = CartItem.objects.get(product=product, cart=cart)
#         cart_item.quantity += 1
#         cart_item.save()
#     except CartItem.DoesNotExist:
#         cart_item = CartItem.objects.create(
#             product=product,
#             quantity=1,
#             cart=cart,
#         )
#         cart.save()
#     return redirect('cart')


def cart_view(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        D_charge = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        if total != 0:
            D_charge = 100
        tax = (2 * total) / 100
        grand_total = total + tax + D_charge

    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'D_charge': D_charge
    }
    return render(request, 'cart.html', context)

    # try:
    #     tax = 0
    #     grand_total = 0
    #     D_charge = 0  # Initialize D_charge with a default value
    #
    #     cart = Cart.objects.get(cart_id=_cart_id(request))
    #     cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    #     for cart_item in cart_items:
    #         total += (cart_item.product.price * cart_item.quantity)
    #         quantity += cart_item.quantity
    #     tax = (2 * total) / 100
    #
    #     if total != 0:
    #         D_charge = 100
    #
    #     grand_total = total + tax + D_charge
    # except ObjectDoesNotExist:
    #     pass  # just ignore
    #
    # context = {
    #     'total': total,
    #     'quantity': quantity,
    #     'cart_items': cart_items,
    #     'tax': tax,
    #     'grand_total': grand_total,
    #     'D_charge': D_charge
    # }
    # return render(request, 'cart.html', context)


# Decrease the value of item from the cart
# def remove_cart_view(request, product_id, cart_item_id):
#     product = get_object_or_404(Products, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()
#     except:
#         pass
#     return redirect('cart')
#
#
# # Remove the item from the cart
# def remove_cart_item_view(request, product_id, cart_item_id):
#     product = get_object_or_404(Products, id=product_id)
#
#     if request.user.is_authenticated:
#         cart_item = get_object_or_404(CartItem, product=product, user=request.user, id=cart_item_id)
#     else:
#         cart = get_object_or_404(Cart, cart_id=_cart_id(request))
#         cart_item = get_object_or_404(CartItem, product=product, cart=cart, id=cart_item_id)
#
#     cart_item.delete()
#     return redirect('cart')

# def remove_cart_item_view(request, product_id, cart_item_id):
#     product = get_object_or_404(Products, id=product_id)
#     if request.user.is_authenticated:
#         cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#     else:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
#     cart_item.delete()
#     return redirect('cart')


from django.http import Http404
def remove_cart_view(request, product_id, cart_item_id):
    product = get_object_or_404(Products, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        raise Http404("Cart item does not exist")

    return redirect('cart')


# Remove the item from the cart completely
def remove_cart_item_view(request, product_id, cart_item_id):
    product = get_object_or_404(Products, id=product_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = get_object_or_404(CartItem, product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect('cart')


def checkout_view(request):
    return  render(request, 'checkout.html')
