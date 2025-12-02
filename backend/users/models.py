from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
import uuid


class UserManager(BaseUserManager):
    """Manager personalizado para el mdoelo User."""

    def create_user(self, email, password=None, **extra_fields):
        """Crea y retorna un usuario regular."""
        if not email:
            raise ValueError('El email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y retorna un superusuario."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    """Modelo de usuario personalizado."""

    # Saco campo username
    username = None
    email = models.EmailField('Email', unique=True, db_index=True)

    # Datos personales
    first_name = models.CharField('Nombre', max_length=30)
    last_name = models.CharField('Apellido', max_length=30)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe tener el formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    phone = models.CharField('Telefono', validators=[phone_regex], max_length=17, blank=True)
    birth_date = models.DateField('Fecha de nacimiento', null=True, blank=True)
    profile_picture = models.ImageField(
        'Foto de perfil',
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )
    
    # Consentimientos
    accepted_terms = models.BooleanField('Aceptó términos y condiciones', default=False)
    accepted_privacy = models.BooleanField('Aceptó política de privacidad', default=False)
    
    # Fechas
    created_at = models.DateTimeField('Fecha de registro', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    # Email verification
    is_email_verified = models.BooleanField('Email verificado', default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    
    # Password reset
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_token_created = models.DateTimeField(null=True, blank=True)
    
    # Social login
    google_id = models.CharField(max_length=255, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        """Retorna el nombre completo del usuario."""
        return f"{self.first_name} {self.last_name}".strip() 
    
class UserProfile(models.Model):
    """Perfil extendido del usuario con preferencias y sistema de puntos"""
    
    NOTIFICATION_CHOICES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('push', 'Push Notification'),
    ]
    
    LEVEL_CHOICES = [
        ('bronze', 'Bronce'),
        ('silver', 'Plata'),
        ('gold', 'Oro'),
        ('platinum', 'Platino'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuario'
    )
    
    # Preferencias
    preferred_branch = models.ForeignKey(
        'core.Branch',  # Lo creamos después
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_by_users',
        verbose_name='Sucursal preferida'
    )
    
    preferred_professional = models.ForeignKey(
        'core.Professional',  # Lo creamos después
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_by_users',
        verbose_name='Profesional preferido'
    )
    
    # Notificaciones
    notification_preferences = models.JSONField(
        'Preferencias de notificación',
        default=dict,
        blank=True,
        help_text='Canales de notificación preferidos'
    )
    
    appointment_reminders = models.BooleanField(
        'Recordatorios de turno',
        default=True
    )
    
    # Sistema de puntos
    points = models.IntegerField('Puntos', default=0)
    total_points_earned = models.IntegerField('Puntos totales ganados', default=0)
    total_points_redeemed = models.IntegerField('Puntos totales canjeados', default=0)
    
    level = models.CharField(
        'Nivel',
        max_length=20,
        choices=LEVEL_CHOICES,
        default='bronze'
    )
    
    # Estadísticas
    total_appointments = models.IntegerField('Total de turnos', default=0)
    completed_appointments = models.IntegerField('Turnos completados', default=0)
    cancelled_appointments = models.IntegerField('Turnos cancelados', default=0)
    no_show_count = models.IntegerField('Inasistencias', default=0)
    
    # Gamificación
    current_streak = models.IntegerField('Racha actual (meses)', default=0)
    longest_streak = models.IntegerField('Racha más larga (meses)', default=0)
    last_visit_date = models.DateField('Última visita', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"
    
    def update_level(self):
        """Actualiza el nivel del usuario según sus puntos"""
        if self.points >= 1001:
            self.level = 'platinum'
        elif self.points >= 501:
            self.level = 'gold'
        elif self.points >= 101:
            self.level = 'silver'
        else:
            self.level = 'bronze'
        self.save()
    
    def add_points(self, points, description=''):
        """Agrega puntos al usuario"""
        self.points += points
        self.total_points_earned += points
        self.update_level()
        
        # Crear registro de transacción (después)
        # PointTransaction.objects.create(
        #     user=self.user,
        #     points=points,
        #     transaction_type='earn',
        #     description=description
        # )
    
    def redeem_points(self, points, description=''):
        """Canjea puntos del usuario"""
        if self.points >= points:
            self.points -= points
            self.total_points_redeemed += points
            self.update_level()
            
            # Crear registro de transacción
            # PointTransaction.objects.create(
            #     user=self.user,
            #     points=points,
            #     transaction_type='redeem',
            #     description=description
            # )
            return True
        return False
    
    def get_cancellation_rate(self):
        """Calcula el porcentaje de cancelaciones"""
        if self.total_appointments == 0:
            return 0
        return (self.cancelled_appointments / self.total_appointments) * 100
    
    def get_no_show_rate(self):
        """Calcula el porcentaje de inasistencias"""
        if self.total_appointments == 0:
            return 0
        return (self.no_show_count / self.total_appointments) * 100


class UserSession(models.Model):
    """Registro de sesiones activas del usuario"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name='Usuario'
    )
    
    session_key = models.CharField('Clave de sesión', max_length=255, unique=True)
    ip_address = models.GenericIPAddressField('Dirección IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    device_info = models.CharField('Información del dispositivo', max_length=255, blank=True)
    
    created_at = models.DateTimeField('Inicio de sesión', auto_now_add=True)
    last_activity = models.DateTimeField('Última actividad', auto_now=True)
    is_active = models.BooleanField('Activa', default=True)
    
    class Meta:
        verbose_name = 'Sesión de Usuario'
        verbose_name_plural = 'Sesiones de Usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Sesión de {self.user.email} - {self.created_at}"