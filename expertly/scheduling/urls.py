from django.urls import path
from .views import (
    ScheduleListView, ScheduleDetailView,
    ExpertScheduleListView, TimeOffListView, TimeOffDetailView
)

urlpatterns = [
    path('schedules/', ScheduleListView.as_view(), name='schedule-list'),
    path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),
    path('experts/<int:expert_id>/schedules/', ExpertScheduleListView.as_view(), name='expert-schedule-list'),
    path('time-offs/', TimeOffListView.as_view(), name='time-off-list'),
    path('time-offs/<int:pk>/', TimeOffDetailView.as_view(), name='time-off-detail'),
]