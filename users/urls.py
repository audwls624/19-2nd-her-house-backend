from django.urls import path
from .views      import KakaoSigninView, KakaoSignupView

urlpatterns = [
    path('/kakao-signin', KakaoSigninView.as_view()),
    path('/kakao-signup', KakaoSignupView.as_view())
]