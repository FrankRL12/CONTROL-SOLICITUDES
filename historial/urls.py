from django.urls import path
from .import views

urlpatterns = [
    path('', views.historial, name='historial'),
    path('opciones_historial/<int:historial_id>',views.opciones_historial, name='opciones_historial'),
    path('eliminar_historial/<int:historial_id>',views.eliminar_historial, name='eliminar_historial'),
    path('generar_pdf/<int:historial_id>',views.generar_pdf, name='generar_pdf'),
]