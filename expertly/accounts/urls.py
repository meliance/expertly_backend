from django.urls import path
from .views import (
    user_list_create_api_view,
    client_detail_api_view,
    expert_detail_api_view,
    expert_registration_api_view,
    client_registration_api_view  # Make sure this is imported
)

urlpatterns = [
    path('', user_list_create_api_view, name='user-list'),
    path('clients/<int:pk>/', client_detail_api_view, name='client-detail'),
    path('clients/me/', client_detail_api_view, name='client-me'),
    path('experts/<int:pk>/', expert_detail_api_view, name='expert-detail'),
    path('experts/me/', expert_detail_api_view, name='expert-me'),
    path('experts/register/', expert_registration_api_view, name='expert-register'),
    path('clients/register/', client_registration_api_view, name='client-register'),  # Added client registration
]