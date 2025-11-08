from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self): return self.name

class Doctor(models.Model):
    full_name = models.CharField(max_length=160, unique=True)
    def __str__(self): return self.full_name

class Patient(models.Model):
    dni = models.CharField(max_length=20, db_index=True)
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["dni"])]
        unique_together = ("dni", "created_at")

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.dni})"

class StudyRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="requests")
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Req #{self.id} - {self.patient}"

def upload_to(instance, filename):
    return f"uploads/request_{instance.study_request_id}/{filename}"

class Attachment(models.Model):
    study_request = models.ForeignKey(StudyRequest, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
