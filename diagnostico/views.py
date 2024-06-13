from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Diagnostico
from django.core.paginator import Paginator, Page
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from .forms import DiagnosticoForm
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
def diagnostico(request):
    diagnosticos = Diagnostico.objects.all()
    elementos_por_pagina = 10
    paginator = Paginator(diagnosticos, elementos_por_pagina)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/diagnostico/listar_diagnostico.html', {'page_obj': page_obj})


@login_required(login_url='login')
@admin_or_superadmin_required
def crear_diagnostico(request):
    form = DiagnosticoForm()
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            nombre = request.POST['nombre']
            marca = request.POST['marca']
            n_serie = request.POST['n_serie']
            modelo = request.POST['modelo']
            ubicacion = request.POST['ubicacion']
            diagnostico = request.POST['diagnostico']
            solucion = request.POST['solucion']
            estado = request.POST['estado']
            agregar_diagnostico = Diagnostico(nombre=nombre, marca=marca, n_serie=n_serie,
                                        modelo=modelo, ubicacion=ubicacion, diagnostico=diagnostico,
                                        solucion=solucion, estado=estado)
            agregar_diagnostico.save()
            messages.success(request, "Diagnostico agregado con éxito.")
            
        return redirect('diagnostico')
    context = {
        'form': form
    }
    return render(request, 'admin/diagnostico/listar_diagnostico.html', context)


@login_required(login_url='login')
@admin_or_superadmin_required
def editar_diagnostico(request, diagnostico_id):
    diagnost =Diagnostico.objects.get(id=diagnostico_id)

    if request.method == 'POST':
        nombre=request.POST['nombre']
        marca=request.POST['marca']
        n_serie=request.POST['n_serie']
        modelo=request.POST['modelo']
        ubicacion=request.POST['ubicacion']
        diagnostico=request.POST['diagnostico']
        solucion=request.POST['solucion']
        estado=request.POST['estado']

        diagnost.nombre=nombre
        diagnost.marca=marca
        diagnost.n_serie=n_serie
        diagnost.modelo=modelo
        diagnost.ubicacion=ubicacion
        diagnost.diagnostico=diagnostico
        diagnost.solucion=solucion
        diagnost.estado=estado

        diagnost.save()
        messages.success(request, "Diagnostico editado con éxito.")
        return redirect('diagnostico')
    return render(request, 'admin/diagnostico/modal_editar.html', {'diagnost':diagnost})


@login_required(login_url='login')
@admin_or_superadmin_required
def eliminar_diagnostico(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
    diagnostico.delete()
    messages.success(request, 'El diagnóstico se ha eliminado correctamente.')
    return redirect('diagnostico')



def diagnostico_pdf(request, diagnosticos_id):
    diagnosticos = get_object_or_404(Diagnostico, pk=diagnosticos_id)
    template_path = 'pdf/pdf_diagnostico.html'
    context = {'diagnosticos': diagnosticos}
    response = HttpResponse(content_type='application/pdf')


    template = render_to_string(template_path, context)
    
    pisa_status = pisa.CreatePDF(template, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    return response