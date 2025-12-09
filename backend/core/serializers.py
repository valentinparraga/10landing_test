from rest_framework import serializers
from .models import Branch, Service, Professional, ProfessionalUnavailability


class BranchSerializer(serializers.ModelSerializer):
    """Serializer para Sucursales"""
    
    working_days = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = [
            'id',
            'name',
            'address',
            'phone',
            'email',
            'opening_time',
            'closing_time',
            'monday_open',
            'tuesday_open',
            'wednesday_open',
            'thursday_open',
            'friday_open',
            'saturday_open',
            'sunday_open',
            'working_days',
            'latitude',
            'longitude',
            'total_chairs',
            'is_active',
            'image',
            'description',
        ]
    
    def get_working_days(self, obj):
        """Retorna lista de días que está abierta"""
        return obj.get_working_days()


class BranchListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar sucursales"""
    
    class Meta:
        model = Branch
        fields = [
            'id',
            'name',
            'address',
            'phone',
            'image',
            'is_active',
        ]


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer para Servicios"""
    
    duration_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'description',
            'price',
            'duration_minutes',
            'duration_display',
            'image',
            'requires_deposit',
            'deposit_amount',
            'points_earned',
            'is_active',
        ]
    
    def get_duration_display(self, obj):
        """Duración en formato legible"""
        return obj.get_duration_display()


class ServiceListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar servicios"""
    
    duration_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'price',
            'duration_minutes',
            'duration_display',
            'image',
        ]
    
    def get_duration_display(self, obj):
        return obj.get_duration_display()


class ProfessionalSerializer(serializers.ModelSerializer):
    """Serializer para Profesionales"""
    
    full_name = serializers.SerializerMethodField()
    branches_data = BranchListSerializer(source='branches', many=True, read_only=True)
    services_data = ServiceListSerializer(source='services', many=True, read_only=True)
    
    class Meta:
        model = Professional
        fields = [
            'id',
            'full_name',
            'first_name',
            'last_name',
            'email',
            'phone',
            'bio',
            'specialties',
            'experience_years',
            'profile_picture',
            'branches_data',
            'services_data',
            'average_rating',
            'total_reviews',
            'is_active',
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class ProfessionalListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar profesionales"""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Professional
        fields = [
            'id',
            'full_name',
            'profile_picture',
            'specialties',
            'average_rating',
            'total_reviews',
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class ProfessionalDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para un profesional específico"""
    
    full_name = serializers.SerializerMethodField()
    branches_data = BranchListSerializer(source='branches', many=True, read_only=True)
    services_data = ServiceSerializer(source='services', many=True, read_only=True)
    working_schedule = serializers.SerializerMethodField()
    
    class Meta:
        model = Professional
        fields = [
            'id',
            'full_name',
            'first_name',
            'last_name',
            'bio',
            'specialties',
            'experience_years',
            'profile_picture',
            'branches_data',
            'services_data',
            'working_schedule',
            'total_appointments',
            'completed_appointments',
            'average_rating',
            'total_reviews',
            'is_active',
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_working_schedule(self, obj):
        """Retorna el horario de trabajo por día"""
        days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        schedule = []
        
        for i, day_name in enumerate(days):
            start, end = obj.get_working_hours(i)
            if start and end:
                schedule.append({
                    'day': day_name,
                    'start': start.strftime('%H:%M'),
                    'end': end.strftime('%H:%M'),
                })
        
        return schedule


class ProfessionalUnavailabilitySerializer(serializers.ModelSerializer):
    """Serializer para indisponibilidades de profesionales"""
    
    professional_name = serializers.CharField(source='professional.get_full_name', read_only=True)
    reason_display = serializers.CharField(source='get_reason_display', read_only=True)
    is_full_day = serializers.SerializerMethodField()
    
    class Meta:
        model = ProfessionalUnavailability
        fields = [
            'id',
            'professional',
            'professional_name',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'reason',
            'reason_display',
            'notes',
            'is_full_day',
            'created_at',
        ]
    
    def get_is_full_day(self, obj):
        return obj.is_full_day()