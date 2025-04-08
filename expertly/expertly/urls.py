from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
<<<<<<< Updated upstream
    path("api/", include("api.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/scheduling/", include("scheduling.urls")),
    path("api/appointment/", include("appointment.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/payments/", include("payments.urls")),
    path('api/notification/', include('notification.urls')),
    path('api/feedback/', include('feedback.urls')),
]
=======
    path('api/', include('api.urls')),
    path('api/accounts/', include('accounts.urls')),  # Added trailing slash
    path('api/documents/', include('documents.urls')),
   path('api/', include('scheduling.urls')),  # Replace 'your_app_name' with the actual name of your app

]
>>>>>>> Stashed changes
