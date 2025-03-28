from django.urls import path
from . import views

urlpatterns = [
  path('', views.user_list_create_api_view, name='user-list-create'),
  path('clients/<int:pk>/', views.client_detail_api_view, name='client-detail'),
  path('experts/<int:pk>/', views.expert_detail_api_view, name='expert-detail'),
]