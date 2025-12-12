from django.contrib import admin
from django.utils.html import format_html
from .models import Branch, Service, Professional, ProfessionalUnavailability, ProfessionalSchedule


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
    actions = ['create_default_schedules']
    
    # Inlines para gestionar horarios desde el mismo formulario
    inlines = []
    
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
            'fields': ('branches', 'services'),
            'description': 'Primero selecciona las sucursales, luego configura los horarios abajo.'
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
    
    def get_inline_instances(self, request, obj=None):
        """
        Mostrar inline solo si el profesional ya existe
        (no en la creación inicial)
        """
        if obj is None:
            return []
        return [inline(self.model, self.admin_site) for inline in self.inlines]
    
    def create_default_schedules(self, request, queryset):
        """
        Action para crear horarios por defecto (Lunes a Viernes, 9:00-18:00)
        para todas las sucursales asignadas
        """
        from datetime import time
        
        total_created = 0
        
        for professional in queryset:
            branches = professional.branches.all()
            
            if not branches:
                self.message_user(
                    request,
                    f'{professional.get_full_name()} no tiene sucursales asignadas.',
                    level='warning'
                )
                continue
            
            for branch in branches:
                # Crear horarios de Lunes a Viernes (0-4)
                for weekday in range(5):
                    schedule, created = ProfessionalSchedule.objects.get_or_create(
                        professional=professional,
                        branch=branch,
                        weekday=weekday,
                        defaults={
                            'start_time': time(9, 0),
                            'end_time': time(18, 0),
                            'is_active': True
                        }
                    )
                    if created:
                        total_created += 1
        
        self.message_user(
            request,
            f'Se crearon {total_created} horarios por defecto (L-V, 9:00-18:00).'
        )
    
    create_default_schedules.short_description = 'Crear horarios por defecto (L-V 9-18hs)'
    
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


class ProfessionalScheduleInline(admin.TabularInline):
    """Inline para gestionar horarios desde el formulario de Profesional"""
    model = ProfessionalSchedule
    extra = 1
    fields = ['branch', 'weekday', 'start_time', 'end_time']
    ordering = ['branch', 'weekday']
    
    def get_formset(self, request, obj = ..., **kwargs):
        """
        Establecer valores por defecto cuando se agrega un nuevo horario
        """
        FormSet = super().get_formset(request, obj, **kwargs)

        class DefaultForm(FormSet.form):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                if not self.instance.pk:
                    self.fields['start_time'].initial = "09:30"
                    self.fields['end_time'].initial = "18:00"

        FormSet.form = DefaultForm
        return FormSet

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtrar las sucursales para mostrar solo aquellas
        a las que el profesional está asignado
        """
        if db_field.name == "branch":
            # Obtener el profesional actual desde la URL
            professional_id = request.resolver_match.kwargs.get('object_id')
            if professional_id:
                try:
                    professional = Professional.objects.get(id=professional_id)
                    kwargs["queryset"] = professional.branches.all()
                except Professional.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Agregar el inline al ProfessionalAdmin
ProfessionalAdmin.inlines = [ProfessionalScheduleInline]


@admin.register(ProfessionalSchedule)
class ProfessionalScheduleAdmin(admin.ModelAdmin):
    """Administración de Horarios de Profesionales por Sucursal"""
    
    list_display = [
        'professional',
        'branch',
        'weekday_display',
        'start_time',
        'end_time',
        'is_active',
    ]
    
    list_filter = ['branch', 'weekday', 'is_active']
    search_fields = ['professional__first_name', 'professional__last_name', 'branch__name']
    ordering = ['professional', 'branch', 'weekday']
    
    fieldsets = (
        ('Asignación', {
            'fields': ('professional', 'branch')
        }),
        ('Horario', {
            'fields': ('weekday', 'start_time', 'end_time')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
    )
    
    def weekday_display(self, obj):
        return obj.get_weekday_display()
    weekday_display.short_description = 'Día'
    weekday_display.admin_order_field = 'weekday'


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