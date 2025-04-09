from django.contrib import admin
from django.utils import timezone
from .models import User, Expert

admin.site.register(User)

@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = (
        'user_email',
        'full_name',
        'specialization',
        'consultation_fields_display',
        'experience_level',
        'display_rate',
        'rating',
        'is_approved'
    )
    list_filter = (
        'is_approved',
        'specialization',
        'consultation_fields',
    )
    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'specialization',
    )
    list_editable = ('is_approved',)
    readonly_fields = (
        'rating',
        'total_sessions',
        'approval_date',
        'consultation_fields_display',
        'experience_level',
        'display_rate'
    )
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'user_email')
        }),
        ('Professional Details', {
            'fields': (
                'specialization',
                'consultation_fields',
                'qualifications',
                'experience_years',
                'hourly_rate',
                'display_rate'
            )
        }),
        ('Status & Ratings', {
            'fields': (
                'is_approved',
                'approval_date',
                'rating',
                'total_sessions'
            )
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Name'
    full_name.admin_order_field = 'user__first_name'

    def consultation_fields_display(self, obj):
        return obj.get_consultation_fields_display()
    consultation_fields_display.short_description = 'Consultation Fields'

    def save_model(self, request, obj, form, change):
        if obj.is_approved and not obj.approval_date:
            obj.approval_date = timezone.now()
        super().save_model(request, obj, form, change)