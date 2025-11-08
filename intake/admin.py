from django.contrib import admin
from .models import Patient, StudyRequest, Attachment, Doctor, Service

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("dni","last_name","first_name","email","phone","created_at")
    search_fields = ("dni","last_name","first_name","email")

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    search_fields = ("full_name",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0

@admin.register(StudyRequest)
class StudyRequestAdmin(admin.ModelAdmin):
    list_display = ("id","patient","doctor","service","created_at")
    list_filter = ("service","doctor","created_at")
    inlines = [AttachmentInline]
