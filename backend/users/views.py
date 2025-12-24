from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import uuid

from .models import User, UserProfile, UserSession
from .serializers import(
    UserSerializer,
    RegisterSerializer, 
    LoginSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UpdateProfileSerializer,
    UpdateProfilePreferencesSerializer,
    UserProfileSerializer,
    UserSessionSerializer,
    EmailVerificationSerializer,
)

class RegisterView(generics.CreateAPIView):
    """
    Vista para registro de nuevos usuarios.
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)

        return Response(
            {
                "message": "Usuario registrado exitosamente.",
                "user": user_serializer.data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )
    
class LoginView(APIView):
    """
    Vista para login de usuarios.
    POST api/auth/login
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Autenticar usuario
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({
                'error': 'Credenciales invalidas'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({
                'error': 'Usuario inactivo'
            }, status=status.HTTP_403_FORBIDDEN)

        # Generar tokens
        refresh = RefreshToken.for_user(user)

        # Crear sesion
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = self.get_client_ip(request)

        UserSession.objects.create(
            user=user,
            session_key=str(refresh.access_token),
            ip_address=ip_address,
            user_agent=user_agent[:255],
            device_info=self.get_device_info(user_agent)
        )

        # Serializar usuario
        user_serializer = UserSerializer(user)

        return Response({
            'message': 'Login exitoso',
            'user': user_serializer.data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        }, status=status.HTTP_200_OK)
    
    def get_client_ip(self, request):
        """Obtener IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_device_info(self, user_agent):
        """Extraer información básica del dispositivo"""
        user_agent_lower = user_agent.lower()
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
            return 'Mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'Tablet'
        else:
            return 'Desktop'

class LogoutView(APIView):
    """
    Vista para logout
    POST /api/auth/logout/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            # Obtener el token de refresh
            refresh_token = request.data.get('refresh_token')
            
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Marcar sesiones como inactivas
            UserSession.objects.filter(
                user=request.user,
                is_active=True
            ).update(is_active=False)
            
            return Response({
                'message': 'Logout exitoso'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'Error al cerrar sesión'
            }, status=status.HTTP_400_BAD_REQUEST)
        
class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    Vista para obtener y actualizar el usuario actual
    GET/PUT /api/auth/me/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
class UpdateProfileView(generics.UpdateAPIView):
    """
    Vista para actualizar datos del perfil
    PUT/PATCH /api/auth/profile/update/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateProfileSerializer
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Retornar usuario completo
        user_serializer = UserSerializer(instance)
        return Response({
            'message': 'Perfil actualizado exitosamente',
            'user': user_serializer.data
        })

class UpdateProfilePreferencesView(generics.UpdateAPIView):
    """
    Vista para actualizar preferencias del perfil
    PUT/PATCH /api/auth/profile/preferences/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateProfilePreferencesSerializer
    
    def get_object(self):
        return self.request.user.profile
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Preferencias actualizadas exitosamente',
            'profile': serializer.data
        })
    
class ChangePasswordView(APIView):
    """
    Vista para cambiar contraseña
    POST /api/auth/change-password/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Verificar contraseña actual
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error': 'Contraseña actual incorrecta'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Establecer nueva contraseña
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Cerrar todas las sesiones activas excepto la actual
        UserSession.objects.filter(
            user=user,
            is_active=True
        ).update(is_active=False)
        
        return Response({
            'message': 'Contraseña cambiada exitosamente'
        }, status=status.HTTP_200_OK)
    
class PasswordResetRequestView(APIView):
    """
    Vista para solicitar reseteo de contraseña
    POST /api/auth/password-reset/
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            
            # Generar token de reseteo
            user.password_reset_token = str(uuid.uuid4())
            user.password_reset_token_created = timezone.now()
            user.save()
            
            # TODO: Enviar email con el token
            # send_password_reset_email(user)
            
            return Response({
                'message': 'Se ha enviado un código de verificación a tu email'
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            # Por seguridad, no revelar si el email existe o no
            return Response({
                'message': 'Se ha enviado un código de verificación a tu email'
            }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Vista para confirmar reseteo de contraseña
    POST /api/auth/password-reset-confirm/
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = User.objects.get(password_reset_token=token)
            
            # Verificar que el token no haya expirado (30 minutos)
            if user.password_reset_token_created:
                expiration_time = user.password_reset_token_created + timedelta(minutes=30)
                
                if timezone.now() > expiration_time:
                    return Response({
                        'error': 'El código de verificación ha expirado'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Cambiar contraseña
            user.set_password(new_password)
            user.password_reset_token = None
            user.password_reset_token_created = None
            user.save()
            
            # Cerrar todas las sesiones
            UserSession.objects.filter(
                user=user,
                is_active=True
            ).update(is_active=False)
            
            return Response({
                'message': 'Contraseña restablecida exitosamente'
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({
                'error': 'Código de verificación inválido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
class UserSessionsView(generics.ListAPIView):
    """
    Vista para listar sesiones activas del usuario
    GET /api/auth/sessions/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSessionSerializer
    
    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user,
            is_active=True
        )


class CloseAllSessionsView(APIView):
    """
    Vista para cerrar todas las sesiones activas
    POST /api/auth/sessions/close-all/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        UserSession.objects.filter(
            user=request.user,
            is_active=True
        ).update(is_active=False)
        
        return Response({
            'message': 'Todas las sesiones han sido cerradas'
        }, status=status.HTTP_200_OK)


class EmailVerificationView(APIView):
    """
    Vista para verificar email
    POST /api/auth/verify-email/
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            user = User.objects.get(email_verification_token=token)
            user.is_email_verified = True
            user.email_verification_token = None
            user.save()
            
            return Response({
                'message': 'Email verificado exitosamente'
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({
                'error': 'Token de verificación inválido'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """
    Vista para obtener el perfil completo del usuario
    GET /api/auth/profile/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user.profile