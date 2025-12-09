from django.contrib import admin
from django.utils.html import format_html
from .models import Branch, Service, Professional, ProfessionalUnavailability


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """Administración de Sucursales"""
    
    list_display = [
        'name',
        'address',
        'phone',
        'total_chairs',
        'is_active',
        'image_display',
    ]
    
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'address', 'phone']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'address', 'phone', 'email', 'description', 'image')
        }),
        ('Horarios', {
            'fields': (
                'opening_time',
                'closing_time',
                ('monday_open', 'tuesday_open', 'wednesday_open'),
                ('thursday_open', 'friday_open', 'saturday_open', 'sunday_open'),
            )
        }),
        ('Ubicación GPS', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Capacidad', {
            'fields': ('total_chairs',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def image_display(self, obj):
        """Mostrar miniatura de la imagen"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_display.short_description = 'Imagen'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Administración de Servicios"""
    
    list_display = [
        'name',
        'price_display',
        'duration_minutes',
        'points_earned',
        'is_active',
        'image_display',
    ]
    
    list_filter = ['is_active', 'requires_deposit']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'image')
        }),
        ('Precio y Duración', {
            'fields': ('price', 'duration_minutes')
        }),
        ('Seña/Depósito', {
            'fields': ('requires_deposit', 'deposit_amount'),
            'classes': ('collapse',)
        }),
        ('Gamificación', {
            'fields': ('points_earned',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def price_display(self, obj):
        """Mostrar precio formateado"""
        return f"${obj.price}"
    price_display.short_description = 'Precio'
    price_display.admin_order_field = 'price'
    
    def image_display(self, obj):
        """Mostrar miniatura de la imagen"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_display.short_description = 'Imagen'


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    """Administración de Profesionales"""
    
    list_display = [
        'full_name_display',
        'email',
        'phone',
        'experience_years',
        'average_rating',
        'is_active',
        'photo_display',
    ]
    
    list_filter = ['is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'specialties']
    ordering = ['first_name', 'last_name']
    
    filter_horizontal = ['branches', 'services']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_picture')
        }),
        ('Usuario del Sistema', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
        ('Perfil Profesional', {
            'fields': ('bio', 'specialties', 'experience_years')
        }),
        ('Relaciones', {
            'fields': ('branches', 'services')
        }),
        ('Horario - Lunes', {
            'fields': ('monday_start', 'monday_end'),
            'classes': ('collapse',)
        }),
        ('Horario - Martes', {
            'fields': ('tuesday_start', 'tuesday_end'),
            'classes': ('collapse',)
        }),
        ('Horario - Miércoles', {
            'fields': ('wednesday_start', 'wednesday_end'),
            'classes': ('collapse',)
        }),
        ('Horario - Jueves', {
            'fields': ('thursday_start', 'thursday_end'),
            'classes': ('collapse',)
        }),
        ('Horario - Viernes', {
            'fields': ('friday_start', 'friday_end'),
            'classes': ('collapse',)
        }),
        ('Horario - Sábado', {
            'fields': ('saturday_start', 'saturday_end'),
            'classes': ('collapse',)
        }),
        ('Horario - Domingo', {
            'fields': ('sunday_start', 'sunday_end'),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': (
                'total_appointments',
                'completed_appointments',
                'average_rating',
                'total_reviews',
            ),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = [
        'total_appointments',
        'completed_appointments',
        'average_rating',
        'total_reviews',
        'created_at',
        'updated_at',
    ]
    
    def full_name_display(self, obj):
        """Mostrar nombre completo"""
        return obj.get_full_name()
    full_name_display.short_description = 'Nombre Completo'
    full_name_display.admin_order_field = 'first_name'
    
    def photo_display(self, obj):
        """Mostrar foto de perfil"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return '-'
    photo_display.short_description = 'Foto'


@admin.register(ProfessionalUnavailability)
class ProfessionalUnavailabilityAdmin(admin.ModelAdmin):
    """Administración de Indisponibilidades de Profesionales"""
    
    list_display = [
        'professional',
        'start_date',
        'end_date',
        'reason',
        'is_full_day_display',
    ]
    
    list_filter = ['reason', 'start_date']
    search_fields = ['professional__first_name', 'professional__last_name', 'notes']
    ordering = ['-start_date']
    
    fieldsets = (
        ('Profesional', {
            'fields': ('professional',)
        }),
        ('Periodo', {
            'fields': (
                ('start_date', 'end_date'),
                ('start_time', 'end_time'),
            )
        }),
        ('Detalles', {
            'fields': ('reason', 'notes')
        }),
    )
    
    readonly_fields = ['created_at']
    
    def is_full_day_display(self, obj):
        """Mostrar si es día completo"""
        return '✓ Día completo' if obj.is_full_day() else '✗ Parcial'
    is_full_day_display.short_description = 'Tipo'