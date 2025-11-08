from django.shortcuts import render, redirect
from django.views import View
from django.db import transaction

from .forms import IntakeForm
from .models import StudyRequest, Attachment, Service


class IntakeView(View):
    template_name = "intake/intake_form.html"

    def get(self, request):
        form = IntakeForm()
        return render(request, self.template_name, {"form": form})

    @transaction.atomic
    def post(self, request):
        form = IntakeForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        # Crear la solicitud de estudio
        req = StudyRequest.objects.create(
            dni=form.cleaned_data["dni"],
            last_name=form.cleaned_data["last_name"],
            first_name=form.cleaned_data["first_name"],
            email=form.cleaned_data.get("email") or "",
            phone=form.cleaned_data.get("phone") or "",
            doctor=form.cleaned_data.get("doctor"),
            service=form.cleaned_data.get("service"),
            notes=form.cleaned_data.get("notes") or "",
        )

        # Guardar adjuntos (múltiples)
        for f in request.FILES.getlist("files"):
            Attachment.objects.create(study_request=req, file=f)

        # Redirigir al panel (o podrías renderizar un "gracias")
        return redirect("panel")


class PanelView(View):
    template_name = "intake/panel.html"

    def get(self, request, service_slug=None):
        services = Service.objects.order_by("name")
        qs = StudyRequest.objects.select_related("service", "doctor").order_by("-created_at")
        selected_service = None

        if service_slug:
            selected_service = Service.objects.filter(slug=service_slug).first()
            if selected_service:
                qs = qs.filter(service=selected_service)

        ctx = {
            "services": services,
            "requests": qs,
            "selected_service": selected_service,
        }
        return render(request, self.template_name, ctx)
