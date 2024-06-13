from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from datetime import datetime, timedelta
from .models import Historial
from django.core.paginator import Paginator, Page
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps
from django.template.loader import render_to_string
from xhtml2pdf import pisa
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
                return HttpResponseRedirect(reverse('inicio'))  
        else:
            # Si el usuario no está autenticado, redirigir a la página de inicio de sesión
            return HttpResponseRedirect(reverse('login'))  

    return wrapper


@login_required(login_url='login')
@admin_or_superadmin_required
def historial(request):
    historiales = Historial.objects.all()

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        historiales = historiales.filter(fecha__range=(start_date, end_date))
        messages.info(request, 'Se están mostrando historiales antiguos.')
    else:
        # Si no se especifica un rango de fechas, filtramos los registros de las últimas 24 horas
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        historiales = historiales.filter(fecha__gte=twenty_four_hours_ago)

    elementos_por_pagina = 10
    paginator = Paginator(historiales, elementos_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/historial/listar_historial.html', {'page_obj': page_obj})



@login_required(login_url='login')
@admin_or_superadmin_required
def opciones_historial(request, historial_id):
    historiales = Historial.objects.get(id=historial_id)

    if request.method == 'POST':
        servicio_solicitado = request.POST.get('servicio_solicitado')
        servicio_realizado = request.POST.get('servicio_realizado')
        observacion= request.POST.get('observacion')
        tecnico=request.POST.get('tecnico')
        estado = request.POST.get('estado')
        prioridad= request.POST.get('prioridad')

        historiales.servicio_solicitado = servicio_solicitado
        historiales.servicio_realizado = servicio_realizado
        historiales.observacion = observacion
        historiales.tecnico = tecnico
        historiales.estado = estado
        historiales.prioridad = prioridad
        historiales.save()
        return redirect('historial')
    return render(request, 'admin/solicitud/listar_solicitud.html', {'historiales':historiales})


@login_required(login_url='login')
@admin_or_superadmin_required
def eliminar_historial(request,  historial_id):
    historiales = get_object_or_404(Historial, id=historial_id)
    historiales.delete()
    return redirect('historial')


def generar_pdf(request, historial_id):
    historial = get_object_or_404(Historial, pk=historial_id)
    template_path = 'pdf/pdf_template.html'
    context = {'historial': historial}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = f'attachment; filename="historial_{historial.id}.pdf"'

    template = render_to_string(template_path, context)
    # Create a PDF object, and render the template content into the PDF file
    pisa_status = pisa.CreatePDF(template, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response