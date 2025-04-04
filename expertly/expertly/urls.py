from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('api.urls')),
    path('api/accounts/', include('accounts.urls')),  # Added trailing slash
    path('api/documents/', include('documents.urls')),
]