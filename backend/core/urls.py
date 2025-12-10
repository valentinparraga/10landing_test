from django.urls import path
from .views import (
    # Sucursales
    BranchListView,
    BranchDetailView,
    
    # Servicios
    ServiceListView,
    ServiceDetailView,
    
    # Profesionales
    ProfessionalListView,
    ProfessionalDetailView,
    ProfessionalsByBranchView,
    ProfessionalsByServiceView,
    
    # Resúmenes
    services_summary,
    professionals_summary,
    home_data,
)

app_name = 'core'

urlpatterns = [
    # Home
    path('home/', home_data, name='home_data'),
    
    # Sucursales
    path('branches/', BranchListView.as_view(), name='branch_list'),
    path('branches/<int:pk>/', BranchDetailView.as_view(), name='branch_detail'),
    path('branches/<int:branch_id>/professionals/', ProfessionalsByBranchView.as_view(), name='professionals_by_branch'),
    
    # Servicios
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/summary/', services_summary, name='services_summary'),
    path('services/<int:service_id>/professionals/', ProfessionalsByServiceView.as_view(), name='professionals_by_service'),
    
    # Profesionales
    path('professionals/', ProfessionalListView.as_view(), name='professional_list'),
    path('professionals/<int:pk>/', ProfessionalDetailView.as_view(), name='professional_detail'),
    path('professionals/summary/', professionals_summary, name='professionals_summary'),
]