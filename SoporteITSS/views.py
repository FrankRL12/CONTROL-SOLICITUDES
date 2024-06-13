from django.shortcuts import render, get_object_or_404, redirect
from solicitud .models import Solicitar
from reporte .models import Reporte
from historial .models import Historial
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
import requests
from .forms import SolicitudForm
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from plyer import notification


@login_required(login_url='login')
def inicio(request):
    solicitudes = Solicitar.objects.filter(usuario=request.user)
    reportes = Reporte.objects.filter(usuario=request.user)
    return render(request, 'views/solicitar.html', {'solicitudes':solicitudes, 'reportes': reportes})


@login_required(login_url='login')
def crear_solicitud(request):
    form = SolicitudForm()
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            detalle_equipo = form.cleaned_data['detalle_equipo']
            descripcion = form.cleaned_data['descripcion']
            mantenimiento = form.cleaned_data['mantenimiento']
            estado = 'En espera'

            usuario_actual = request.user
            departamento = usuario_actual.departamento
            nombre = usuario_actual.first_name
            apellido = usuario_actual.last_name

            solicitud = Solicitar(usuario=usuario_actual, nombre=nombre, apellido=apellido, departamento=departamento, detalle_equipo=detalle_equipo,
                            descripcion=descripcion, mantenimiento=mantenimiento,  estado=estado)
            solicitud.save()
            messages.success(request, 'Solicitud Craeda Exitosamente!')

            # Envía una notificación
            notification.notify(
                title='Nueva Solicitud',
                message='Se ha creado una nueva solicitud de mantenimiento.',
                app_name='solicitud'
            )
        return redirect('inicio')
    context = {
        'form': form
    }
    return render(request, 'views/solicitar.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Has iniciado sesión exitosamente')

            # Redirigir al superusuario si es uno
            if user.is_superadmin:
                return redirect('administrador')
            elif user.is_admin:
                return redirect('administrador')
            else:
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                    return redirect('inicio')
            
        else:
            messages.error(request, 'Las credenciales son incorrectas')
            return redirect('login')  
        
    return render(request, 'views/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Has salido de sesion')

    return redirect('login')


@login_required(login_url='login')
def cancelar_solicitud(request, solicitud_id):
    solicitudes = get_object_or_404(Solicitar, id=solicitud_id)
    solicitudes.delete()
    messages.success(request, 'La solicitud ha sido cancelada exitosamente.')
    return redirect('inicio')


@login_required(login_url='login')
def historial_cliente(request):
    historiales = Historial.objects.filter(usuario=request.user)

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

    return render(request, 'views/historial.html', {'page_obj': page_obj})