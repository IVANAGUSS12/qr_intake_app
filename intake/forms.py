from django import forms
from .models import Doctor, Service

# 👇 Widget que sí permite múltiples archivos
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class IntakeForm(forms.Form):
    dni = forms.CharField(label="DNI", max_length=20)
    last_name = forms.CharField(label="Apellido", max_length=120)
    first_name = forms.CharField(label="Nombre", max_length=120)
    email = forms.EmailField(label="Correo", required=False)
    phone = forms.CharField(label="Teléfono", required=False)
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), required=False, label="Médico solicitante")
    service = forms.ModelChoiceField(queryset=Service.objects.all(), required=False, label="Servicio")
    notes = forms.CharField(label="Notas", widget=forms.Textarea, required=False)

    # 👇 ahora sí: input múltiple
    files = forms.FileField(
        label="Archivos (PDF/JPG/PNG)",
        widget=MultiFileInput(attrs={"multiple": True}),
        required=False,
    )

    def clean_files(self):
        # Con múltiples archivos, los obtenemos desde self.files
        files = self.files.getlist("files")
        for f in files:
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError(f"'{f.name}' excede 5MB.")
        return files
