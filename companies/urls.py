from django.urls import path

from .views import CompanyMainView

urlpatterns = [
    path('', CompanyMainView.as_view())
]
