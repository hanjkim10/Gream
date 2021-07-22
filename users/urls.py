from django.urls import path

from users.views import SignupView, SigninView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view()),
    path('/signin/kakao', SigninView.as_view()),
]
