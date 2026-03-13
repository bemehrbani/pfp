"""
URLs for Users app API.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .otp_views import OTPLoginView

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('otp-login/', OTPLoginView.as_view(), name='otp_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # User management
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('telegram/link/', views.TelegramLinkView.as_view(), name='telegram_link'),

    # Admin only
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]