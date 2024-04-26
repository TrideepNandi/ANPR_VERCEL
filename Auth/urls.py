# Auth/urls.py
from django.urls import path
from .views import (
    SendOTPView, VerifyOTPView, LogoutView,
    CustomUserCreateView, CustomUserListView,
    CustomUserDetailView, CustomUserUpdateView,
    CustomUserDeleteView, CheckPasswordView
)

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-user/', CustomUserCreateView.as_view(), name='create_user'),
    path('list-users/', CustomUserListView.as_view(), name='list_users'),
    path('detail-user/<int:pk>/', CustomUserDetailView.as_view(), name='detail_user'),
    path('update-user/<int:pk>/', CustomUserUpdateView.as_view(), name='update_user'),
    path('delete-user/<int:pk>/', CustomUserDeleteView.as_view(), name='delete_user'),
    path('check-password/', CheckPasswordView.as_view(), name='check_password'),
]
