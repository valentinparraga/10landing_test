from rest_framework import serializers
from .models import Branch, Service, Professional, ProfessionalUnavailability, ProfessionalSchedule


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
    schedules_by_branch = serializers.SerializerMethodField()
    
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
            'schedules_by_branch',
            'total_appointments',
            'completed_appointments',
            'average_rating',
            'total_reviews',
            'is_active',
        ]
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_schedules_by_branch(self, obj):
        """Retorna horarios agrupados por sucursal"""
        schedules = obj.schedules.filter(is_active=True).select_related('branch')
        
        # Agrupar por sucursal
        result = {}
        for schedule in schedules:
            branch_id = schedule.branch.id
            branch_name = schedule.branch.name
            
            if branch_id not in result:
                result[branch_id] = {
                    'branch_id': branch_id,
                    'branch_name': branch_name,
                    'schedules': []
                }
            
            result[branch_id]['schedules'].append({
                'weekday': schedule.weekday,
                'weekday_display': schedule.get_weekday_display(),
                'start_time': schedule.start_time.strftime('%H:%M'),
                'end_time': schedule.end_time.strftime('%H:%M'),
            })
        
        return list(result.values())


class ProfessionalScheduleSerializer(serializers.ModelSerializer):
    """Serializer para horarios de profesionales"""
    
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = ProfessionalSchedule
        fields = [
            'id',
            'professional',
            'branch',
            'branch_name',
            'weekday',
            'weekday_display',
            'start_time',
            'end_time',
            'is_active',
        ]
    
    def validate(self, data):
        """Validaciones personalizadas"""
        # Validar que end_time sea mayor que start_time
        if 'start_time' in data and 'end_time' in data:
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError({
                    'end_time': 'La hora de fin debe ser posterior a la hora de inicio.'
                })
        
        # Validar que el profesional esté asignado a esa sucursal
        if 'professional' in data and 'branch' in data:
            if not data['professional'].branches.filter(id=data['branch'].id).exists():
                raise serializers.ValidationError({
                    'branch': f'El profesional no está asignado a esta sucursal.'
                })
        
        return data


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
    
    def validate(self, data):
        """Validaciones personalizadas"""
        # Validar que end_date sea mayor o igual a start_date
        if 'start_date' in data and 'end_date' in data:
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError({
                    'end_date': 'La fecha de fin no puede ser anterior a la fecha de inicio.'
                })
        
        # Validar horarios si no es día completo
        if 'start_time' in data and 'end_time' in data:
            if data['start_time'] and data['end_time']:
                if data['end_time'] <= data['start_time']:
                    raise serializers.ValidationError({
                        'end_time': 'La hora de fin debe ser posterior a la hora de inicio.'
                    })
        
        return data