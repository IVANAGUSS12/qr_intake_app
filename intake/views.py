from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .forms import IntakeForm
from .models import Patient, StudyRequest, Attachment, Doctor, Service

class IntakeView(View):
    template_name = "intake/intake_form.html"

    def get(self, request):
        form = IntakeForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = IntakeForm(request.POST, request.FILES)
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            p, _ = Patient.objects.get_or_create(
                dni=dni,
                defaults={
                    "last_name": form.cleaned_data["last_name"].strip().upper(),
                    "first_name": form.cleaned_data["first_name"].strip().upper(),
                    "email": form.cleaned_data.get("email"),
                    "phone": form.cleaned_data.get("phone"),
                },
            )
            p.last_name = form.cleaned_data["last_name"].strip().upper()
            p.first_name = form.cleaned_data["first_name"].strip().upper()
            p.email = form.cleaned_data.get("email")
            p.phone = form.cleaned_data.get("phone")
            p.save()

            req = StudyRequest.objects.create(
                patient=p,
                doctor=form.cleaned_data.get("doctor"),
                service=form.cleaned_data.get("service"),
                notes=form.cleaned_data.get("notes") or "",
            )

            for f in form.cleaned_data.get("files", []):
                Attachment.objects.create(study_request=req, file=f)

            return redirect("panel")
        return render(request, self.template_name, {"form": form})

class PanelView(View):
    template_name = "intake/panel.html"

    def get_queryset(self, request, service_slug=None):
        q = request.GET.get("q", "").strip()
        doctor_id = request.GET.get("doctor")
        queryset = StudyRequest.objects.select_related("patient","doctor","service").order_by("-id")
        if q:
            queryset = queryset.filter(
                Q(patient__dni__icontains=q) |
                Q(patient__last_name__icontains=q) |
                Q(patient__first_name__icontains=q)
            )
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        service_obj = None
        if service_slug:
            service_obj = get_object_or_404(Service, slug=service_slug)
            queryset = queryset.filter(service=service_obj)
        return queryset, q, doctor_id, service_obj

    def get(self, request, service_slug=None):
        queryset, q, doctor_id, service_obj = self.get_queryset(request, service_slug)

        counts = (StudyRequest.objects
                  .values("service__id", "service__name", "service__slug")
                  .annotate(total=Count("id"))
                  .order_by("service__name"))
        services = Service.objects.all().order_by("name")

        paginator = Paginator(queryset, 20)
        page = request.GET.get("page", 1)
        page_obj = paginator.get_page(page)
        context = {
            "page_obj": page_obj,
            "q": q,
            "doctors": Doctor.objects.all().order_by("full_name"),
            "doctor_selected": doctor_id or "",
            "services": services,
            "service_current": service_obj,
            "service_counts": {c["service__slug"] or "": c["total"] for c in counts},
        }
        return render(request, self.template_name, context)
