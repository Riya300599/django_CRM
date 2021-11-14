from django.forms import ModelForm
from .models import Order, Customer, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'status']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'discription', 'tags']
