from django.contrib import admin
from .models import Product,Review
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=['product_name','slug','price','stock','catagory']
class ReviewAdmin(admin.ModelAdmin):
    list_display=['name','date']
admin.site.register(Product,ProductAdmin)
admin.site.register(Review,ReviewAdmin)
