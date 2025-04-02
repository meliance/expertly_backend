from django.urls import path
from .views import ExpertDocumentListCreateView, ExpertDocumentDetailView

urlpatterns = [
    path(
        'experts/<int:expert_id>/documents/',
        ExpertDocumentListCreateView.as_view(),
        name='expert-document-list'
    ),
    path(
        'documents/<int:pk>/',
        ExpertDocumentDetailView.as_view(),
        name='expert-document-detail'
    ),
]