from django.urls import path
from . import views
urlpatterns=[
path('register/',views.register,name='register'),
path('login/',views.login,name='login'),
path('logout/',views.logout,name='logout'),
path('activate/<uidb64>/<token>/',views.activate,name='activate'),
path('forgetpassword/',views.forgetpassword,name='forgetpassword'),
path('resetpassword/<uidb64>/<token>/',views.resetpassword,name='resetpassword'),
path('submitpassword/',views.submitpassword,name='submitpassword'),


path('',views.dashbord,name='dashbord'),
path('my_orders/',views.my_orders,name='my_orders'),
path('edit_profile/',views.edit_profile,name='edit_profile'),
path('change_password/',views.change_password,name='change_password'),
path('order_details/<int:order_id>/',views.order_details,name='order_details'),
]
