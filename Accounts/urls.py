from django.urls import path
from Accounts.views import UserRegistrationView, UserLoginView, UserLogoutView, PasswordResetView, Home

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('home/', Home.as_view(), name='homepage'),
]
