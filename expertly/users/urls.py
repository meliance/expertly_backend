from django.urls import path
from . import views

urlpatterns = [
  path('', views.user_list_create_api_view, name='user-list-create'),
  path('<int:pk>/', views.UserDetailApiView.as_view(), name='user-detail')
]