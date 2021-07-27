from django.urls import path

from users.views import SignupView, SigninView, UserView, KakaoSigninView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view()),
    path('/signin/kakao', KakaoSigninView.as_view()),
    path('/info', UserView.as_view()),
]