from django.urls import path
from .import views

urlpatterns = [
    path('', views.solicitar, name='solicitar'),
    path('crear_reporte/<int:solicitud_id>',views.crear_reporte, name='crear_reporte'),
    path('opciones_solicitudes/<int:solicitud_id>',views.opciones_solicitudes, name='opciones_solicitudes'),
    path('eliminar_solicitud/<int:solicitud_id>',views.eliminar_solicitud, name='eliminar_solicitud'),
]