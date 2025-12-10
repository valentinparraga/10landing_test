from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Branch, Service, Professional, ProfessionalUnavailability
from .serializers import (
    BranchSerializer,
    BranchListSerializer,
    ServiceSerializer,
    ServiceListSerializer,
    ProfessionalSerializer,
    ProfessionalListSerializer,
    ProfessionalDetailSerializer,
    ProfessionalUnavailabilitySerializer,
)


# ========== SUCURSALES ==========

class BranchListView(generics.ListAPIView):
    """
    Lista todas las sucursales activas
    GET /api/branches/
    """
    queryset = Branch.objects.filter(is_active=True)
    serializer_class = BranchListSerializer
    permission_classes = [permissions.AllowAny]


class BranchDetailView(generics.RetrieveAPIView):
    """
    Detalle de una sucursal específica
    GET /api/branches/{id}/
    """
    queryset = Branch.objects.filter(is_active=True)
    serializer_class = BranchSerializer
    permission_classes = [permissions.AllowAny]


# ========== SERVICIOS ==========

class ServiceListView(generics.ListAPIView):
    """
    Lista todos los servicios activos
    GET /api/services/
    Filtros disponibles: ?search={texto}
    """
    serializer_class = ServiceListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'duration_minutes']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True)
        return queryset


class ServiceDetailView(generics.RetrieveAPIView):
    """
    Detalle de un servicio específico
    GET /api/services/{id}/
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]


# ========== PROFESIONALES ==========

class ProfessionalListView(generics.ListAPIView):
    """
    Lista todos los profesionales activos
    GET /api/professionals/
    Filtros: ?branch={id}, ?service={id}
    """
    serializer_class = ProfessionalListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'specialties']
    ordering_fields = ['average_rating', 'experience_years']
    ordering = ['-average_rating']
    
    def get_queryset(self):
        queryset = Professional.objects.filter(is_active=True)
        
        # Filtrar por sucursal
        branch_id = self.request.query_params.get('branch', None)
        if branch_id:
            queryset = queryset.filter(branches__id=branch_id)
        
        # Filtrar por servicio
        service_id = self.request.query_params.get('service', None)
        if service_id:
            queryset = queryset.filter(services__id=service_id)
        
        return queryset.distinct()


class ProfessionalDetailView(generics.RetrieveAPIView):
    """
    Detalle de un profesional específico
    GET /api/professionals/{id}/
    """
    queryset = Professional.objects.filter(is_active=True)
    serializer_class = ProfessionalDetailSerializer
    permission_classes = [permissions.AllowAny]


class ProfessionalsByBranchView(generics.ListAPIView):
    """
    Lista profesionales de una sucursal específica
    GET /api/branches/{branch_id}/professionals/
    """
    serializer_class = ProfessionalListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        branch_id = self.kwargs.get('branch_id')
        return Professional.objects.filter(
            is_active=True,
            branches__id=branch_id
        ).distinct()


class ProfessionalsByServiceView(generics.ListAPIView):
    """
    Lista profesionales que ofrecen un servicio específico
    GET /api/services/{service_id}/professionals/
    """
    serializer_class = ProfessionalListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        service_id = self.kwargs.get('service_id')
        return Professional.objects.filter(
            is_active=True,
            services__id=service_id
        ).distinct()


# ========== VISTAS DE INFORMACIÓN GENERAL ==========

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def services_summary(request):
    """
    Resumen de servicios para el home
    GET /api/services/summary/
    """
    services = Service.objects.filter(is_active=True)
    
    return Response({
        'total_services': services.count(),
        'services': ServiceSerializer(services[:10], many=True).data,
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def professionals_summary(request):
    """
    Resumen de profesionales para el home
    GET /api/professionals/summary/
    """
    professionals = Professional.objects.filter(is_active=True)
    
    return Response({
        'total_professionals': professionals.count(),
        'professionals': ProfessionalListSerializer(professionals[:10], many=True).data,
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def home_data(request):
    """
    Datos completos para la página de inicio
    GET /api/home/
    """
    # Sucursales activas
    branches = Branch.objects.filter(is_active=True)
    
    # Servicios activos
    services = Service.objects.filter(is_active=True)[:10]
    
    # Profesionales activos
    professionals = Professional.objects.filter(is_active=True)[:10]
    
    return Response({
        'branches': BranchListSerializer(branches, many=True).data,
        'services': ServiceSerializer(services, many=True).data,
        'professionals': ProfessionalListSerializer(professionals, many=True).data,
    })