from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.index,name='home'),
    path('post_by_tag/<int:myid>', views.post_by_tag, name='post_by_tag'),
    path('usersignup/',views.usersignup,name='usersignup'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('userregister/', views.userregister, name='userregister'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('productviews/', views.productview, name='productviews'),
    path('produpdate/<int:myid>', views.produpdate, name='produpdate'),
    path('prodelete/<int:myid>', views.prodelete, name='prodelete'),
    path('order/', views.orders, name='orders'),
    #path('products/', views.products, name='products'),
    path('userlogout/',views.userlogout,name='userlogout'),
]



