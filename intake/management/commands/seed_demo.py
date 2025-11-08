from django.core.management.base import BaseCommand
from intake.models import Service, Doctor

SERVICES = ["Cardiología", "Traumatología", "Diagnóstico por Imágenes", "Laboratorio", "Clínica Médica"]
DOCTORS = ["Dr. Juan Pérez", "Dra. Ana Gómez", "Dr. Mario Rossi", "Dra. Sofía Díaz"]

class Command(BaseCommand):
    help = "Crea servicios y médicos de ejemplo"

    def handle(self, *args, **kwargs):
        for s in SERVICES:
            Service.objects.get_or_create(name=s)
        for d in DOCTORS:
            Doctor.objects.get_or_create(full_name=d)
        self.stdout.write(self.style.SUCCESS("Servicios y médicos creados (o ya existían)."))
