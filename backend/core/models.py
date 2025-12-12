from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Branch(models.Model):
    """Modelo de Sucursal"""
    
    name = models.CharField('Nombre', max_length=100)
    address = models.CharField('Dirección', max_length=255)
    phone = models.CharField('Teléfono', max_length=20)
    email = models.EmailField('Email', blank=True)
    
    # Horarios
    opening_time = models.TimeField('Hora de apertura', default='09:00')
    closing_time = models.TimeField('Hora de cierre', default='19:00')
    
    # Días de atención
    monday_open = models.BooleanField('Abierto lunes', default=True)
    tuesday_open = models.BooleanField('Abierto martes', default=True)
    wednesday_open = models.BooleanField('Abierto miércoles', default=True)
    thursday_open = models.BooleanField('Abierto jueves', default=True)
    friday_open = models.BooleanField('Abierto viernes', default=True)
    saturday_open = models.BooleanField('Abierto sábado', default=True)
    sunday_open = models.BooleanField('Abierto domingo', default=False)
    
    # Ubicación GPS
    latitude = models.DecimalField(
        'Latitud',
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text='Coordenada GPS para el mapa'
    )
    longitude = models.DecimalField(
        'Longitud',
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text='Coordenada GPS para el mapa'
    )
    
    # Capacidad
    total_chairs = models.PositiveIntegerField(
        'Cantidad de sillas',
        default=5,
        validators=[MinValueValidator(1)]
    )
    
    # Estado
    is_active = models.BooleanField('Activa', default=True)
    
    # Imagen
    image = models.ImageField(
        'Imagen de la sucursal',
        upload_to='branches/',
        null=True,
        blank=True
    )
    
    # Descripción
    description = models.TextField('Descripción', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_working_days(self):
        """Retorna los días que la sucursal está abierta"""
        days = []
        if self.monday_open:
            days.append('Lunes')
        if self.tuesday_open:
            days.append('Martes')
        if self.wednesday_open:
            days.append('Miércoles')
        if self.thursday_open:
            days.append('Jueves')
        if self.friday_open:
            days.append('Viernes')
        if self.saturday_open:
            days.append('Sábado')
        if self.sunday_open:
            days.append('Domingo')
        return days
    
    def is_open_on_day(self, day_number):
        """
        Verifica si está abierto un día específico
        day_number: 0=Lunes, 1=Martes, ..., 6=Domingo
        """
        days_map = {
            0: self.monday_open,
            1: self.tuesday_open,
            2: self.wednesday_open,
            3: self.thursday_open,
            4: self.friday_open,
            5: self.saturday_open,
            6: self.sunday_open,
        }
        return days_map.get(day_number, False)


class Service(models.Model):
    """Modelo de Servicio (Corte, Barba, Color, etc.)"""
    
    name = models.CharField('Nombre', max_length=150)
    description = models.TextField('Descripción')
    
    # Precio y duración
    price = models.DecimalField(
        'Precio',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    duration_minutes = models.PositiveIntegerField(
        'Duración (minutos)',
        validators=[MinValueValidator(5)]
    )
    
    # Imagen
    image = models.ImageField(
        'Imagen del servicio',
        upload_to='services/',
        null=True,
        blank=True
    )
    
    # Configuración
    requires_deposit = models.BooleanField(
        'Requiere seña',
        default=False,
        help_text='Si requiere pago de seña para reservar'
    )
    deposit_amount = models.DecimalField(
        'Monto de seña',
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Puntos
    points_earned = models.PositiveIntegerField(
        'Puntos que otorga',
        default=0,
        help_text='Puntos que gana el cliente al completar este servicio'
    )
    
    # Estado
    is_active = models.BooleanField('Activo', default=True)
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    def get_duration_display(self):
        """Retorna duración en formato legible"""
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        
        if hours > 0 and minutes > 0:
            return f"{hours}h {minutes}min"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}min"


class Professional(models.Model):
    """Modelo de Profesional/Barbero/Peluquero"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='professional_profile',
        verbose_name='Usuario',
        null=True,
        blank=True,
        help_text='Usuario asociado (si tiene cuenta en el sistema)'
    )
    
    # Datos básicos
    first_name = models.CharField('Nombre', max_length=100)
    last_name = models.CharField('Apellido', max_length=100)
    email = models.EmailField('Email', blank=True)
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    
    # Perfil profesional
    bio = models.TextField('Biografía', blank=True)
    specialties = models.TextField(
        'Especialidades',
        blank=True,
        help_text='Ej: Cortes modernos, Barba, Coloración'
    )
    experience_years = models.PositiveIntegerField(
        'Años de experiencia',
        default=0
    )
    
    # Foto
    profile_picture = models.ImageField(
        'Foto de perfil',
        upload_to='professionals/',
        null=True,
        blank=True
    )
    
    # Relaciones
    branches = models.ManyToManyField(
        Branch,
        related_name='professionals',
        verbose_name='Sucursales donde trabaja',
        blank=True
    )
    
    services = models.ManyToManyField(
        Service,
        related_name='professionals',
        verbose_name='Servicios que ofrece',
        blank=True
    )
    
    # Nota: Los horarios ahora se manejan por sucursal en ProfessionalSchedule
    
    # Estadísticas
    total_appointments = models.PositiveIntegerField('Total de turnos', default=0)
    completed_appointments = models.PositiveIntegerField('Turnos completados', default=0)
    average_rating = models.DecimalField(
        'Calificación promedio',
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.PositiveIntegerField('Total de reseñas', default=0)
    
    # Estado
    is_active = models.BooleanField('Activo', default=True)
    
    # Timestamps
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        """Retorna nombre completo"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_schedules_by_branch(self, branch):
        """Retorna horarios para una sucursal específica"""
        return self.schedules.filter(branch=branch)
    
    def update_rating(self):
        """Actualiza la calificación promedio (después crearemos el modelo de reseñas)"""
        # TODO: Calcular desde las reseñas reales
        pass


class ProfessionalUnavailability(models.Model):
    """Bloqueos de horario del profesional (vacaciones, ausencias, etc.)"""
    
    REASON_CHOICES = [
        ('vacation', 'Vacaciones'),
        ('sick', 'Enfermedad'),
        ('personal', 'Personal'),
        ('training', 'Capacitación'),
        ('other', 'Otro'),
    ]
    
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='unavailabilities',
        verbose_name='Profesional'
    )
    
    start_date = models.DateField('Fecha inicio')
    end_date = models.DateField('Fecha fin')
    
    start_time = models.TimeField(
        'Hora inicio',
        null=True,
        blank=True,
        help_text='Dejar vacío para bloquear día completo'
    )
    end_time = models.TimeField(
        'Hora fin',
        null=True,
        blank=True,
        help_text='Dejar vacío para bloquear día completo'
    )
    
    reason = models.CharField(
        'Motivo',
        max_length=20,
        choices=REASON_CHOICES,
        default='other'
    )
    notes = models.TextField('Notas', blank=True)
    
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Indisponibilidad de Profesional'
        verbose_name_plural = 'Indisponibilidades de Profesionales'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.professional.get_full_name()} - {self.start_date} a {self.end_date}"
    
    def is_full_day(self):
        """Verifica si es un bloqueo de día completo"""
        return self.start_time is None or self.end_time is None
    
    def clean(self):
        """Validaciones personalizadas"""
        from django.core.exceptions import ValidationError
        
        # Validar que end_date sea mayor o igual a start_date
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    'end_date': 'La fecha de fin no puede ser anterior a la fecha de inicio.'
                })
            
            # Validar horarios si es un solo dia
            if self.end_date == self.start_date:
                if self.start_time and self.end_time:
                    if self.end_time <= self.start_time:
                        raise ValidationError({
                            'end_time': 'La hora de fin debe ser posterior a la hora de inicio.'
                        })
        
    def save(self, *args, **kwargs):
        """Ejecutar validaciones antes de guardar"""
        self.clean()
        super().save(*args, **kwargs)


class ProfessionalSchedule(models.Model):
    """Horarios de trabajo del profesional por sucursal"""
    
    WEEKDAY_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Profesional'
    )
    
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='professional_schedules',
        verbose_name='Sucursal'
    )
    
    weekday = models.IntegerField(
        'Día de la semana',
        choices=WEEKDAY_CHOICES,
        help_text='0=Lunes, 6=Domingo'
    )
    
    start_time = models.TimeField('Hora de inicio')
    end_time = models.TimeField('Hora de fin')
    
    is_active = models.BooleanField('Activo', default=True)
    
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Horario de Profesional'
        verbose_name_plural = 'Horarios de Profesionales'
        ordering = ['professional', 'branch', 'weekday']
        unique_together = ['professional', 'branch', 'weekday']
    
    def __str__(self):
        return f"{self.professional.get_full_name()} - {self.branch.name} - {self.get_weekday_display()}: {self.start_time}-{self.end_time}"
    
    def get_duration_hours(self):
        """Calcula la duración del turno en horas"""
        from datetime import datetime, timedelta
        
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        
        duration = end - start
        return duration.total_seconds() / 3600
    
    def clean(self):
        """Validaciones personalizadas"""
        from django.core.exceptions import ValidationError
        
        # Validar que end_time sea mayor que start_time
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError({
                    'end_time': 'La hora de fin debe ser posterior a la hora de inicio.'
                })
        
        # Validar que el profesional esté asignado a esa sucursal
        if self.professional and self.branch:
            if not self.professional.branches.filter(id=self.branch.id).exists():
                raise ValidationError({
                    'branch': f'El profesional {self.professional.get_full_name()} no está asignado a la sucursal {self.branch.name}.'
                })
    
    def save(self, *args, **kwargs):
        """Ejecutar validaciones antes de guardar"""
        self.clean()
        super().save(*args, **kwargs)