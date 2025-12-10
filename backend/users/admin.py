from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile, UserSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administracion personalizada del modelo User."""

    list_display = [
        'email',
        'full_name_display',
        'phone',
        'is_active',
        'is_email_verified',
        'created_at',
        'profile_picture_display',
    ]

    list_filter = [
        'is_active',
        'is_staff',
        'is_superuser',
        'is_email_verified',
        'wants_promotions',
        'created_at',
    ]

    search_fields = ['email', 'first_name', 'last_name', 'phone']

    ordering = ['-created_at']

    fieldsets = (
        ('credenciales', {
            'fields' : ('email', 'password')
        }),
        ('Información Personal',{
            'fields': ('first_name', 'last_name', 'phone', 'birth_date', 'profile_picture')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Consentimientos', {
            'fields': ('accepted_terms', 'accepted_privacy', 'wants_promotions')
        }),
        ('Verificacion', {
            'fields': ('is_email_verified', 'email_verification_token')
        }),
        ('Social Login', {
            'fields': ('google_id', 'facebook_id'),
            'classes': ('collapse',)
        }),
        ('Fechas Importantes', {
            'fields': ('created_at', 'updated_at', 'last_login'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        ('Crear Nuevo USuario', {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'phone',
                'is_active',
                'is_staff',
            ),
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'last_login']

    def full_name_display(self, obj):
        """Mostrar nombre completo."""
        return obj.get_full_name()
    
    full_name_display.short_description = 'Nombre Completo'

    def profile_picture_display(self, obj):
        """Mostrar miniatura de la foto de perfil."""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return '-'
    profile_picture_display.short_description = 'Foto'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Administración del perfil de usuario"""
    
    list_display = [
        'user_email',
        'user_name',
        'points',
        'level',
        'total_appointments',
        'completed_appointments',
        'current_streak',
    ]
    
    list_filter = [
        'level',
        'appointment_reminders',
    ]
    
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
    ]
    
    readonly_fields = [
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
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Preferencias', {
            'fields': (
                'preferred_branch',
                'preferred_professional',
                'notification_preferences',
                'appointment_reminders',
            )
        }),
        ('Sistema de Puntos', {
            'fields': (
                'points',
                'total_points_earned',
                'total_points_redeemed',
                'level',
            )
        }),
        ('Estadísticas', {
            'fields': (
                'total_appointments',
                'completed_appointments',
                'cancelled_appointments',
                'no_show_count',
            )
        }),
        ('Gamificación', {
            'fields': (
                'current_streak',
                'longest_streak',
                'last_visit_date',
            )
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'
    
    def user_name(self, obj):
        return obj.user.get_full_name()
    user_name.short_description = 'Nombre'
    user_name.admin_order_field = 'user__first_name'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """Administración de sesiones de usuario"""
    
    list_display = [
        'user_email',
        'ip_address',
        'device_info',
        'created_at',
        'last_activity',
        'is_active',
    ]
    
    list_filter = [
        'is_active',
        'device_info',
        'created_at',
    ]
    
    search_fields = [
        'user__email',
        'ip_address',
        'session_key',
    ]
    
    readonly_fields = [
        'user',
        'session_key',
        'ip_address',
        'user_agent',
        'device_info',
        'created_at',
        'last_activity',
    ]
    
    ordering = ['-created_at']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Usuario'
    user_email.admin_order_field = 'user__email'
    
    def has_add_permission(self, request):
        """No permitir crear sesiones manualmente"""
        return False


# Personalizar el sitio de administración
admin.site.site_header = '10PELUQUERIA.COM - Administración'
admin.site.site_title = '10PELUQUERIA.COM'
admin.site.index_title = 'Panel de Control'