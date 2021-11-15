from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView, name='login'),
    path('register/', RegisterView, name='register'),
    path('logout/', LogoutView, name='logout'),

    # url for role == admin
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('customer/<str:pk>/', customer, name='customer'),

    path('create_order/<str:pk>/', create_order, name='create_order'),
    path('update_order/<str:pk>/', update_order, name='update_order'),
    path('delete_order/<str:pk>/', delete_order, name='delete_order'),

    path('create_product/', create_product, name='create_product'),
    path('update_product/<str:pk>/', update_product, name='update_product'),
    path('delete_product/<str:pk>/', delete_product, name='delete_product'),


    # url for role == customer
    path('user/', user_page, name='user'),
    path('account/', account_settings, name='account'),
]
