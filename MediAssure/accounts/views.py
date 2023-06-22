from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from .models import Account
from django.contrib.auth.decorators import login_required

from .forms import UserForm,UserProfileForm



from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

#checkout page
from carts.models import Cart,CartItem
from carts.views import _cart_id

import requests


from .models import UserProfile,Account


from orders.models import Order,OrderProduct
def register(request):
    if request.method=='POST':
        #Taking value
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        #check if password matches
        if password==password2:
            #check dublicate username
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exist!!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email already exist!!')
                    return redirect('register')
                else:
                    #looks good
                    user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                    #accouunt_user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                    user.is_active=False
                    user.save()
                    profile=UserProfile()
                    profile.user_id=user.id
                    profile.profile_picture='default/img_avatar.png'
                    profile.save()

                    accouunt_user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                    accouunt_user.is_active=False
                    accouunt_user.save()






                    current_site=get_current_site(request)
                    mail_subject="Please activate account"
                    message=render_to_string('accounts/account_verification_email.html',{
                    'user':user,
                    'domain':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                    })
                    to_email=email
                    send_email=EmailMessage(mail_subject,message,to=[to_email])
                    send_email.send()


                    #accouunt_user.save()
                    #messages.success(request,'Thank you for registaring with us. We have sent you the verification email to you. Please verify')
                    return redirect('/accounts/login/?command=verification&email='+email)
        else:
            messages.error(request,'password not matching. Try again')
            return redirect('register')

    else:
        return render(request,'accounts/register.html')


def login(request):
     if request.method=='POST':

         username=request.POST['username']
         password=request.POST['password']
         user=auth.authenticate(username=username,password=password)
         if user is not None:
             #for processing checkout page button
             try:
                 cart=Cart.objects.get(cart_id=_cart_id(request))
                 is_cart_item_exist=CartItem.objects.filter(cart=cart).exists()
                 if is_cart_item_exist:
                     cart_item=CartItem.objects.filter(cart=cart)
                     for item in cart_item:
                         item.user=user
                         item.save()
             except:
                 pass
             auth.login(request,user)
             messages.success(request,'Login Successfull!!')
             url=request.META.get('HTTP_REFERER')
             try:
                 query=requests.utils.urlparse(url).query
                 print('query:',query)
                 params=dict(x.split('=') for x in query.split('&'))
                 print('params',params)
                 if 'next' in params:
                     nextpage=params['next']
                     return redirect(nextpage)
             except:
                 return redirect('home')
         else:
            messages.error(request,'username and password is invalid!! ')
            return redirect('login')

     else:
         return render(request,'accounts/login.html')
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request,'Logout Successfull!!')
    return redirect('home')


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'congratulation! your account is activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def dashbord(request):
    order=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    order_count=order.count()
    print('order_count',order_count)
    user_profile=UserProfile.objects.get(user_id=request.user.id)
    context={
    'order_count':order_count,
    'user_profile':user_profile,
    }
    return render(request,'accounts/dashbord.html',context)



def forgetpassword(request):
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__iexact=email)
            current_site=get_current_site(request)
            mail_subject="Please activate account"
            message=render_to_string('accounts/resetpassword_email.html',{
            'user':user,
            'domain':current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,"Reset link  has been sent to you email.")
            return redirect('login')
        else:
            messages.success(request,"Email Does not exist!!.")
            return redirect('forgetpassword')
    else:
        return render(request,'accounts/forgetpassword.html')
def resetpassword(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,'please reset yout passord')
        return redirect('submitpassword')
    else:
        messages.error(request,'link has been expired')
        return redirect('login')



def submitpassword(request):
    if request.method=='POST':
        password=request.POST['password']
        password1=request.POST['password1']
        if password==password1:
            uid=request.session.get('uid')
            user=User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password rested successfully!! Login now')
            return redirect('login')
        else:
            messages.success(request,'Password do not matched')
            return redirect('submitpassword')
    else :
        return render(request,'accounts/resetpassword_page.html')





@login_required(login_url='login')
def my_orders(request):
    order=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    cart_items=CartItem.objects.filter(user=request.user)
    print(cart_items)
    context={
    'order':order,
    'cart_items':cart_items,
    }

    return render(request,'accounts/my_orders.html',context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method=='POST':
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'your Profile has been updated')
            return redirect('edit_profile')

    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
        context={
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile
        }
        return render(request,'accounts/edit_profile.html',context)



@login_required(login_url='login')
def change_password(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        user=User.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            sucess=user.check_password(current_password)
            if sucess:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password has been updated successfully')
                return redirect('change_password')
            else:
                messages.warning(request,'Please Enter Valid Current Password!')
                return redirect('change_password')
        else:
            messages.warning(request,'Password Did Not Matched!')
            return redirect('change_password')

    else:
        return render(request,'accounts/changePassword.html')


@login_required(login_url='login')
def order_details(request,order_id):
    order_details=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)

    sub_total=0
    for i in order_details:
        sub_total+=(i.quantity*i.product_price)
    context={
    'order_details':order_details,
    'order':order,
    'sub_total':sub_total,
    }
    return render(request,'accounts/order_details.html',context)
