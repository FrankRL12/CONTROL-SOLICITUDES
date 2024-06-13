from django.urls import path
from .import views

urlpatterns = [
    path('', views.diagnostico, name='diagnostico'),
    path('crear_diagnostico/', views.crear_diagnostico, name='crear_diagnostico'),
    path('editar_diagnostico/<int:diagnostico_id>',views.editar_diagnostico, name='editar_diagnostico'),
    path('eliminar_diagnostico/<int:diagnostico_id>',views.eliminar_diagnostico, name='eliminar_diagnostico'),
    path('diagnostico_pdf/<int:diagnosticos_id>',views.diagnostico_pdf, name='diagnostico_pdf'),
]