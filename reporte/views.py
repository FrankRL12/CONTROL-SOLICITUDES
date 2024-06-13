from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from reporte .models import Reporte
from historial .models import Historial
from django.core.paginator import Paginator, Page
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps
from django.contrib import messages

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
def reporte(request):
    reportes = Reporte.objects.all()
    elementos_por_pagina = 10
    paginator = Paginator(reportes, elementos_por_pagina)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/reportes/listar_reportes.html', {'page_obj': page_obj})


@login_required(login_url='login')
@admin_or_superadmin_required
def opciones_reportes(request, reporte_id):
    reportes = Reporte.objects.get(id=reporte_id)

    if request.method == 'POST':
        estado = request.POST.get('estado')
        prioridad= request.POST.get('prioridad')

        reportes.estado = estado
        reportes.prioridad = prioridad
        reportes.save()
        messages.success(request, 'Opciones editada correctamente.')
        return redirect('reporte')
    return render(request, 'admin/reportes/listar_reportes.html', {'reportes':reportes}) 


@login_required(login_url='login')
@admin_or_superadmin_required
def eliminar_reporte(request, reporte_id):
    reporte = get_object_or_404(Reporte, id=reporte_id)
    reporte.delete()
    messages.success(request, 'El reporte se ha eliminado correctamente.')
    return redirect('reporte')

@login_required(login_url='login')
@admin_or_superadmin_required
def mover_historial(request, reporte_id):
    try:
        reporte = Reporte.objects.get(id=reporte_id)

        historial = Historial(
            usuario=reporte.usuario,
            nombre_completo=reporte.nombre_completo,
            departamento=reporte.departamento,
            servicio_solicitado=reporte.servicio_solicitado,
            servicio_realizado=reporte.servicio_realizado,
            observacion=reporte.observacion,
            tecnico=reporte.tecnico,
            fecha=reporte.fecha,
            hora=reporte.hora,
            fecha_final=datetime.now().date(),
            hora_final=datetime.now().time(),
            estado=reporte.estado,
            prioridad=reporte.prioridad
        )

        historial.save()

        reporte.delete()

        return redirect('reporte')

    except Reporte.DoesNotExist:
        return HttpResponse("El reporte no existe.")