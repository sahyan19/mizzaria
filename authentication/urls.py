from django.urls import path
from .views import ActivateAccountView, PasswordResetConfirmView, RegisterView, LoginView, UserProfileView, LogoutView, PasswordResetView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate_account'),
]