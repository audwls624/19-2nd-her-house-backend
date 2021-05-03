from django.urls import path, include

from products.views import CategoryView, ProductListView, ProductDetailView

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]