from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import Cart,CartItem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
@login_required(login_url='login')
def add_cart(request,product_id):
    product=get_object_or_404(Product,pk=product_id)#get the prodcut
    if request.user.is_authenticated:
        try:
            cart_item=CartItem.objects.get(product=product,user=request.user)
            cart_item.quantity+=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            user=request.user,
            )
            cart_item.save()
        return redirect('carts')

    else:
        try :
            cart=Cart.objects.get(cart_id=_cart_id(request))#get the cart by using cart id from session
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
            cart_id=_cart_id(request)
            )
        cart.save()
        try:
            cart_item=CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity+=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            )
            cart_item.save()
        return redirect('carts')

def remove_cart(request,product_id):
    if request.user.is_authenticated:
        product=get_object_or_404(Product,id=product_id)
        cart_item=CartItem.objects.get(user=request.user,product=product)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        product=get_object_or_404(Product,id=product_id)
        cart_item=CartItem.objects.get(cart=cart,product=product)
    if cart_item.quantity > 1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('carts')
def remove_cart_item(request,product_id):
    if request.user.is_authenticated:
        product=get_object_or_404(Product,id=product_id)
        cart_item=CartItem.objects.get(user=request.user,product=product)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        product=get_object_or_404(Product,id=product_id)
        cart_item=CartItem.objects.get(cart=cart,product=product)

    cart_item.delete()
    return redirect('carts')

def carts(request,total=0,quantity=0,cart_items=None):

    try:
        tax=0
        grand_total=0

        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total=total+(cart_item.product.price*cart_item.quantity)
            quantity=quantity+cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    content={
    'total':total,
    'quantity':quantity,
    'cart_items':cart_items,
    'tax':tax,
    'grand_total':grand_total,

    }
    return render(request,'store/carts.html',content)



@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        '''cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)'''
        for cart_item in cart_items:
            total=total+(cart_item.product.price*cart_item.quantity)
            quantity=quantity+cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    content={
    'total':total,
    'quantity':quantity,
    'cart_items':cart_items,
    'tax':tax,
    'grand_total':grand_total,

    }

    return render(request,'store/checkout.html',content)
