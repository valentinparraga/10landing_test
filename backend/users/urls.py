from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    CurrentUserView,
    UpdateProfileView,
    UpdateProfilePreferencesView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    UserSessionsView,
    CloseAllSessionsView,
    EmailVerificationView,
    UserProfileView,
)

app_name = 'users'

urlpatterns = [
    # Autenticación
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Usuario actual
    path('me/', CurrentUserView.as_view(), name='current_user'),
    
    # Perfil
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/preferences/', UpdateProfilePreferencesView.as_view(), name='update_preferences'),
    
    # Contraseñas
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Sesiones
    path('sessions/', UserSessionsView.as_view(), name='user_sessions'),
    path('sessions/close-all/', CloseAllSessionsView.as_view(), name='close_all_sessions'),
    
    # Verificación de email
    path('verify-email/', EmailVerificationView.as_view(), name='verify_email'),
]