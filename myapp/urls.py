from django .urls import path
from .views import *
urlpatterns = [
    path('',index_view,name='index_page'),
    path('about/',about_view,name='about_page'),
    path('login/',login_view,name='login_page'),
     path('register/',register_view,name='register_page'),
     path('logout/',logout_view,name='logout_page'),
     path('forget/',forget_view,name='forget_page'),
     path('add_to_cart/<int:product_id>/',add_to_cart_view,name='add_to_cart'),
     path('cart_count/',cart_count,name='cart_count'),
     path('cartItems/',cart_items,name='cart_items'),
     path('viewdetails/<int:product_id>/',view_details,name='view_details'),
     path('update_cart/<int:id>/<str:action>/',update_cart,name='update_cart')
]
