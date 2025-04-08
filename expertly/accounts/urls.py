from django.urls import path
from .views import (
    RegisterView, LoginView, UserProfileView,UserListView, 
    ClientProfileView, ExpertProfileView, ChangePasswordView,
    ExpertListView, ExpertDetailView, ExpertApprovalView,
    AdminUserListView, AdminUserDetailView, ClientDetailView,
    ExpertPublicProfileView, ExpertAdminDetailView,
    ExpertDocumentListView, ExpertDocumentDetailView,
    ExpertDocumentVerificationView
)

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    path('users/', UserListView.as_view(), name='user-list'),

    # Profile management
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/client/', ClientProfileView.as_view(), name='client-profile'),
    path('profile/expert/', ExpertProfileView.as_view(), name='expert-profile'),
    
    # Client URLs
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    
    # Expert URLs
    path('experts/', ExpertListView.as_view(), name='expert-list'),
    path('experts/<int:pk>/', ExpertDetailView.as_view(), name='expert-detail'),
    path('experts/public/<int:pk>/', ExpertPublicProfileView.as_view(), name='expert-public-profile'),
    path('experts/admin/<int:pk>/', ExpertAdminDetailView.as_view(), name='expert-admin-detail'),
    path('admin/experts/<int:pk>/approve/', ExpertApprovalView.as_view(), name='expert-approve'),
    # Expert document URLs
    path('experts/<int:expert_id>/documents/', ExpertDocumentListView.as_view(), name='expert-document-list'),
    path('documents/<int:pk>/', ExpertDocumentDetailView.as_view(), name='expert-document-detail'),
    path('documents/<int:pk>/verify/', ExpertDocumentVerificationView.as_view(), name='expert-document-verify'),
    
    # Admin URLs
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
]