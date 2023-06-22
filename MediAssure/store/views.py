from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Review
from catagory.models import Catagory
from carts.views import _cart_id
from carts.models import CartItem
from django.db.models import Q
# Create your views here.
from django.core.paginator import Paginator
def store(request,catagory_slug=None):
    catagories=None
    products=None
    if catagory_slug != None:
        catagories=get_object_or_404(Catagory,slug=catagory_slug)
        products=Product.objects.filter(catagory=catagories,is_available=True).order_by('id')
        product_count=products.count()
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')
        product_count=products.count()
        paginator=Paginator(products,4)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)

    context={
    'products':paged_products,
    'product_count':product_count,
    }
    return render(request,'store/store.html',context)
def product_detail(request,catagory_slug,product_slug):
    try:
        single_product=Product.objects.get(catagory__slug=catagory_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        reviews=Review.objects.all()
    except Exception as e:
        raise e
    context={
    'single_product':single_product,
    'in_cart':in_cart,
    'reviews':reviews
    }
    return render(request,'store/product_detail.html',context)
def search(request):
    context={}
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(product_name__icontains=keyword))
            product_count=products.count()
            context={
            'products':products,
            'product_count':product_count,
            }



    return render(request,'store/store.html',context)
def write_review(request):
    if request.method=='POST':
        name=request.POST['name']
        hospital_name=request.POST['hospital_name']
        comment=request.POST['write_review']
        profile_pic=request.FILES.get('image')
        print('write_review',write_review)
        review=Review.objects.create(name=name,hospital_name=hospital_name,comment=comment,profile_pic=profile_pic)
        if review:
            review.save()
        return redirect('home')
    else:
        return render(request,'store/review.html')