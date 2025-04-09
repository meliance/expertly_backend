from django.urls import path
from .views import ExpertSearchView  # Correct import

urlpatterns = [
    path('api/search/', ExpertSearchView.as_view(), name='expert_search'),
]