
from django.urls import path,include

from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('catagory/<slug:catagory_slug>/',views.store,name='product_by_catagory'),
    path('catagory/<slug:catagory_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('write_review/',views.write_review,name='write_review'),
]
