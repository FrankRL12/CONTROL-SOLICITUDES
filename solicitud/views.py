from django.shortcuts import render, redirect, get_object_or_404
from .models import Solicitar
from django.core.paginator import Paginator, Page
from reporte .models import Reporte
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps
from django.contrib import messages
from .forms import ReporteForm



# Create your views here.
def admin_or_superadmin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario está autenticado y si es superadmin o admin
        if request.user.is_authenticated:
            if request.user.is_superadmin or request.user.is_staff or request.user.is_admin:
                # Si es superadmin, admin o admin normal, permitir acceso a la vista
                return view_func(request, *args, **kwargs)
            else:
                # Si no es superadmin o admin, redirigir a la página de inicio
                return HttpResponseRedirect(reverse('inicio'))  # Reemplaza 'inicio' con el nombre de la vista de inicio en tus urls
        else:
            # Si el usuario no está autenticado, redirigir a la página de inicio de sesión
            return HttpResponseRedirect(reverse('login'))  # Reemplaza 'login' con el nombre de la vista de inicio de sesión en tus urls

    return wrapper



@login_required(login_url='login')
@admin_or_superadmin_required
def solicitar(request):
    solicitudes = Solicitar.objects.all().order_by('-fecha')
    
    elementos_por_pagina = 10
    paginator = Paginator(solicitudes, elementos_por_pagina)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/solicitud/listar_solicitud.html', {'page_obj': page_obj})



@login_required(login_url='login')
@admin_or_superadmin_required
def crear_reporte(request, solicitud_id):
    form = ReporteForm()
    solicitud = Solicitar.objects.get(id=solicitud_id)
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            servicio_realizado = request.POST['servicio_realizado']
            observacion =  request.POST['observacion']
            tecnico = request.POST['tecnico']
            servicio_solicitado = request.POST['servicio_solicitado']
            nuevo_estado = request.POST['estado']

            reporte = Reporte(
                usuario=solicitud.usuario, nombre_completo=f"{solicitud.nombre} {solicitud.apellido}", departamento =solicitud.departamento,
                servicio_solicitado=servicio_solicitado, servicio_realizado= servicio_realizado,
                observacion = observacion, tecnico = tecnico, hora=solicitud.hora, fecha=solicitud.fecha, estado=nuevo_estado,
                prioridad= solicitud.prioridad,
        )
            reporte.save()
            solicitud.delete()
        return redirect('solicitar')
    conntex = {
        'form': form,
        'solicitud': solicitud,
    }
    return render(request, 'admin/solicitud/listar_solicitud.html', conntex)


@login_required(login_url='login')
@admin_or_superadmin_required
def opciones_solicitudes(request, solicitud_id):
    solicitudes = Solicitar.objects.get(id=solicitud_id)

    if request.method == 'POST':
        estado = request.POST.get('estado')
        prioridad= request.POST.get('prioridad')

        solicitudes.estado = estado
        solicitudes.prioridad = prioridad
        solicitudes.save()
        messages.success(request, 'Opciones editada correctamente.')
        return redirect('solicitar')
    return render(request, 'admin/solicitud/listar_solicitud.html', {'solicitudes':solicitudes})


@login_required(login_url='login')
@admin_or_superadmin_required
def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitar, id=solicitud_id)
    solicitud.delete()
    messages.success(request, 'La solicitud se ha eliminado correctamente.')
    return redirect('solicitar')