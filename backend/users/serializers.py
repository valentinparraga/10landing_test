from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, UserSession
import uuid

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil del usuario."""

    level_display = serializers.CharField(source='get_level_display', read_only=True)
    cancellation_rate = serializers.SerializerMethodField()
    no_show_rate = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'preferred_branch',
            'preferred_professional',
            'notification_preferences',
            'appointment_reminders',
            'points',
            'total_points_earned',
            'total_points_redeemed',
            'level',
            'level_display',
            'total_appointments',
            'completed_appointments',
            'cancelled_appointments',
            'no_show_count',
            'current_streak',
            'longest_streak',
            'last_visit_date',
            'cancellation_rate',
            'no_show_rate',
        ] 

        read_only_fields = [
            'points',
            'total_points_earned',
            'total_points_redeemed',
            'level',
            'total_appointments',
            'completed_appointments',
            'cancelled_appointments',
            'no_show_count',
            'current_streak',
            'longest_streak',
            'last_visit_date',
        ]

    def get_cancellation_rate(self, obj):
        return round(obj.get_cancellation_rate(), 2)
    
    def get_no_show_rate(self, obj):
        return round(obj.get_no_show_rate(), 2)
    
class UserSerializer(serializers.ModelSerializer):
    """Serializer principal del usuario"""
    
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone',
            'birth_date',
            'profile_picture',
            'wants_promotions',
            'is_email_verified',
            'created_at',
            'profile',
        ]
        read_only_fields = ['id', 'created_at', 'is_email_verified']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    accepted_terms = serializers.BooleanField(required=True)
    accepted_privacy = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'phone',
            'birth_date',
            'accepted_terms',
            'accepted_privacy',
            'wants_promotions',
        ]
    
    def validate(self, attrs):
        """Validación de datos"""
        # Verificar que las contraseñas coincidan
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password': 'Las contraseñas no coinciden.'
            })
        
        # Verificar que aceptó términos y privacidad
        if not attrs.get('accepted_terms'):
            raise serializers.ValidationError({
                'accepted_terms': 'Debe aceptar los términos y condiciones.'
            })
        
        if not attrs.get('accepted_privacy'):
            raise serializers.ValidationError({
                'accepted_privacy': 'Debe aceptar la política de privacidad.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Crear usuario y perfil"""
        # Remover campos que no son del modelo User
        validated_data.pop('password_confirm')
        
        # Extraer password
        password = validated_data.pop('password')
        
        # Crear usuario
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        # Generar token de verificación de email
        user.email_verification_token = str(uuid.uuid4())
        user.save()
        
        # Crear perfil automáticamente
        UserProfile.objects.create(user=user)
        
        # TODO: Enviar email de verificación
        # send_verification_email(user)
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña"""
    
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Validar que las contraseñas nuevas coincidan"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password': 'Las contraseñas no coinciden.'
            })
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer para solicitar reseteo de contraseña"""
    
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer para confirmar reseteo de contraseña"""
    
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Validar que las contraseñas coincidan"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password': 'Las contraseñas no coinciden.'
            })
        return attrs


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Serializer para actualizar datos del usuario"""
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'birth_date',
            'profile_picture',
            'wants_promotions',
        ]
    
    def validate_phone(self, value):
        """Validar formato de teléfono"""
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError('Formato de teléfono inválido.')
        return value


class UpdateProfilePreferencesSerializer(serializers.ModelSerializer):
    """Serializer para actualizar preferencias del perfil"""
    
    class Meta:
        model = UserProfile
        fields = [
            'preferred_branch',
            'preferred_professional',
            'notification_preferences',
            'appointment_reminders',
        ]


class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer para sesiones de usuario"""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserSession
        fields = [
            'id',
            'user_email',
            'ip_address',
            'device_info',
            'created_at',
            'last_activity',
            'is_active',
        ]
        read_only_fields = ['id', 'created_at', 'last_activity']


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer para verificación de email"""
    
    token = serializers.CharField(required=True)