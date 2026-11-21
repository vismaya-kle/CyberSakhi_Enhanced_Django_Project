from django.contrib import admin
from .models import IncidentReport, AwarenessArticle, SavedArticle, SafetyChecklist

@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ("reference_id", "title", "category", "user", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("reference_id", "title", "description", "user__username")
    readonly_fields = ("reference_id", "created_at")

@admin.register(AwarenessArticle)
class AwarenessArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    search_fields = ("title", "category", "summary")

admin.site.register(SavedArticle)
admin.site.register(SafetyChecklist)
