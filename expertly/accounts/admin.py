from django.contrib import admin
from .models import Expert

class ExpertAdmin(admin.ModelAdmin):
    list_display = ('get_user_email', 'get_full_name', 'specialization', 'is_approved')
    list_filter = ('is_approved', 'specialization')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'
    get_user_email.admin_order_field = 'user__email'
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'user__last_name'

admin.site.register(Expert, ExpertAdmin)