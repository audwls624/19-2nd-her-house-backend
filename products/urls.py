from django.urls import path, include

from products.views import CategoryView, ProductListView, ProductDetailView, ProductReviewView

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/review/<int:product_id>', ProductReviewView.as_view())
]