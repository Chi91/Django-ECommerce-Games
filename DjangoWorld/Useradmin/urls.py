from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.MySignUpView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
]
