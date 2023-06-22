from django.db import models
from catagory.models import Catagory
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    address=models.TextField(max_length=500,blank=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to='photos/product/')
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    def get_url(self):
        return reverse('product_detail',args=[self.catagory.slug,self.slug])
    def __str__(self):
        return self.product_name

class Review(models.Model):
    profile_pic=models.ImageField(upload_to='photos/product/')
    name=models.CharField(max_length=200,unique=True)
    hospital_name=models.CharField(max_length=200,blank=True)
    date=models.DateTimeField(auto_now=True)
    comment=models.TextField(max_length=500,blank=True)
    def __str__(self):
        return self.name


