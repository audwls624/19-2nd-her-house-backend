from django.urls import path, include

from products.views import CategoryView, ProductListView

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('', ProductListView.as_view()),
]