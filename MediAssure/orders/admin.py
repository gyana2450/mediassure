from django.contrib import admin
from .models import Payment,Order,OrderProduct
# Register your models here.
class OrderProdcutInline(admin.TabularInline):
    model=OrderProduct
    readonly_fields=('payment','order_user','product','quantity','product_price','ordered')
    extra=0
class OrderAdmin(admin.ModelAdmin):
    list_dasplay=['order_number','fullname','first_name','last_name','email','phone','status','is_ordered','city','state','created_at']
    list_filter=['status','is_ordered']
    search_fields=['order_number','fullname','first_name','last_name']
    list_per_page=20
    inlines=[OrderProdcutInline]
admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
