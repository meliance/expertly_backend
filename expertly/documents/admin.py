from django.contrib import admin
from .models import ExpertDocument

@admin.register(ExpertDocument)
class ExpertDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'expert', 'get_document_type_display', 'version', 'title', 'is_verified', 'uploaded_at')
    list_filter = ('document_type', 'is_verified', 'uploaded_at')
    search_fields = ('expert__user__username', 'title', 'description')
    readonly_fields = ('version', 'uploaded_at', 'updated_at')
    list_editable = ('is_verified',)
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('expert', 'document_type', 'version')
        }),
        ('Document Info', {
            'fields': ('title', 'description', 'file')
        }),
        ('Status', {
            'fields': ('is_verified',)
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_document_type_display(self, obj):
        return obj.get_document_type_display()
    get_document_type_display.short_description = 'Document Type'