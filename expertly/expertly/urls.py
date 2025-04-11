# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/", include("api.urls")),
#     path("api/accounts/", include("accounts.urls")),
#     path("api/scheduling/", include("scheduling.urls")),
#     path("api/appointment/", include("appointment.urls")),
#     path("api/chat/", include("chat.urls")),
#     path("api/payments/", include("payments.urls")),
#     path('api/notification/', include('notification.urls')),
#     path('api/feedback/', include('feedback.urls')),
# ]


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/", include("api.urls")),
    path("accounts/", include("accounts.urls")),
    path("scheduling/", include("scheduling.urls")),
    path("appointment/", include("appointment.urls")),
    path("chat/", include("chat.urls")),
    path("payments/", include("payments.urls")),
    path('notification/', include('notification.urls')),
    path('feedback/', include('feedback.urls')),
]
