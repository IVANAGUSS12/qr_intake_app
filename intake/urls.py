from django.urls import path
from .views import IntakeView, PanelView

urlpatterns = [
    path("", PanelView.as_view(), name="panel"),
    path("panel/", PanelView.as_view(), name="panel"),
    path("panel/<slug:service_slug>/", PanelView.as_view(), name="panel_service"),
    path("qr/intake/", IntakeView.as_view(), name="intake"),
]
