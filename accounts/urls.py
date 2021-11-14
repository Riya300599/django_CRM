from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView, name='login'),
    path('register/', views.RegisterView, name='register'),
    path('logout/', views.LogoutView, name='logout'),

    # url for role == admin
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),

    path('create_order/<str:pk>/', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),

    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<str:pk>/', views.update_product, name='update_product'),
    path('delete_product/<str:pk>/', views.delete_product, name='delete_product'),


    # url for role == customer
    path('user/', views.user_page, name='user'),
    path('account/', views.account_settings, name='account'),
]
