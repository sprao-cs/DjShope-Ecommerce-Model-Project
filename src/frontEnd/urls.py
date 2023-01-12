from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('login', login, name="login"),
    path('register', signup, name="register"),
    path('logout', logout, name="logout"),
    path('search-product', search, name="search-product"),
    path('view-products/<int:id>', viewProduct, name="view-product"),
    path('<slug:category_slug>/', searchCategory, name='category')
]
