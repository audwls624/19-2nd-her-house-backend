from django.urls import path, include

from products.views import CategoryView 

urlpatterns = [
    path('/category', CategoryView.as_view())
]