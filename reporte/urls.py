from django.urls import path
from .import views


urlpatterns = [
    path('', views.reporte, name='reporte'), 
    path('opciones_reportes/<int:reporte_id>',views.opciones_reportes, name='opciones_reportes'),
    path('eliminar_reporte/<int:reporte_id>',views.eliminar_reporte, name='eliminar_reporte'),
    path('mover_historial/<int:reporte_id>',views.mover_historial, name='mover_historial'),
]