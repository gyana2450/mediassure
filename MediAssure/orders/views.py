from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Payment,Order,OrderProduct
from store.models import Product
from .forms import OrderForm
from datetime import date
import datetime
from carts.models import CartItem
# Create your views here.
import razorpay
import random
from greatkart.settings import RAZOR_KEY_ID,RAZOR_KEY_SECRET

import json


from store.models import Product


from django.template.loader import render_to_string
from django.core.mail import EmailMessage



from django.template.loader import render_to_string
from django.core.mail import EmailMessage
num=random.uniform(20, 60)
random_num=''.join(str(num).split('.'))
client = razorpay.Client(auth=(RAZOR_KEY_ID,RAZOR_KEY_SECRET))

def order_completed(request):
    try:
        current_user=request.user
        cart_items=CartItem.objects.filter(user=current_user)
        orders=Order.objects.get(user=current_user,is_ordered=False)
        orders.is_ordered=True
        orders.status='completed'
        orders.save()

        payment = Payment.objects.create(user=current_user,payment_id=random_num,payment_method='free',amount_paid=0,status='completed')
        payment.save()
        for cart_item in cart_items:
            mydata = Product.objects.filter(product_name=cart_item.product).values()
            current_stock=mydata[0]['stock']
            update_data = Product.objects.get(product_name=cart_item.product)
            if current_stock<=1:
                update_data.stock=0
            else:
                update_data.stock=current_stock-1
            update_data.save()
            cart_item.delete()
            context={
            'order':orders,
            'payment_id':random_num,
            'payment':payment,
            'cart_items':cart_items,

            }
            print('orders.email',orders.email)
            mail_subject="Appointment booked successfully."
            message=render_to_string('orders/appointment_email_conformation.html',{
            'order':orders,
            'cart_items':cart_items,
            })
            to_email=orders.email
            send_email=EmailMessage(mail_subject,message,to=[to_email,'gyanara07@gmail.com'])
            send_email.send()
            

            return render(request,'orders/order_completed.html',context)
            
                
    #return render(request,'orders/order_completed.html')
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')


def place_order(request):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count <=0:
        return redirect('store')
    grand_total=0
    tax=0
    total=0
    quantity=0
    for cart_item in cart_items:
        total+=(cart_item.product.price*cart_item.quantity)
        quantity+=cart_item.quantity
    tax=(2*total)/100
    grand_total=tax+total
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.pin_code=form.cleaned_data['pin_code']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            #generate order number
            todays_date = date.today()

            yr=int(todays_date.year)
            dt=int(todays_date.day)
            mt=int(todays_date.month)
            d=datetime.date(yr,mt,dt)
            print(d)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+str(data.id)
            data.order_number=order_number
            data.save()
            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)


            currency = 'INR'
            amount = int(order.order_total*100) # Rs. 200

            razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='1'))
            payment_order_id=razorpay_order['id']
            print(razorpay_order)

            context={
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
            'razorpay_merchant_key':RAZOR_KEY_ID,
            'razorpay_order_id':payment_order_id,
            'currency':currency,
            'amount_paid':amount,
            }
            return render(request,'orders/payments.html',context)


    else:
        return redirect('checkout')
