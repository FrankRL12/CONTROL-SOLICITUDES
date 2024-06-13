from django.urls import path
from .import views

urlpatterns = [
    path('', views.usuario, name='usuario'), 
    path('agregarUsuario', views.agregarUsuario, name='agregarUsuario'),
    path('cambiar_estado_usuario/<int:user_id>/', views.cambiar_estado_usuario, name='cambiar_estado_usuario'),
    path('editar_usuario/<int:user_id>',views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>',views.eliminar_usuario, name='eliminar_usuario'),
]