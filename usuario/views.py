from django.shortcuts import render, redirect, HttpResponse
from .models import Usuario
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps
from .forms import UsuarioForm


# Create your views here.
def is_superuser(user):
    return user.is_superuser


def admin_or_superadmin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario está autenticado y si es admin o superadmin
        if request.user.is_authenticated:
            if request.user.is_superadmin or request.user.is_staff:
                # Si es admin o superadmin, permitir acceso a la vista
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('inicio')) 
        else:
            return HttpResponseRedirect(reverse('login')) 
    return wrapper


@login_required(login_url='login')
@admin_or_superadmin_required
def usuario(request):
    usuarios = Usuario.objects.all()
    elementos_por_pagina = 10

    paginator = Paginator(usuarios, elementos_por_pagina)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/usuario/usuario.html', {'page_obj': page_obj})


@login_required(login_url='login')
@admin_or_superadmin_required
def agregarUsuario(request):
    form = UsuarioForm()
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            departamento = request.POST.get('departamento')

        # Utiliza el método create_user del UsuarioManager para crear el usuario
            usuario_manager = Usuario.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,  # Aquí todavía está como texto plano, lo corregiremos enseguida
                departamento=departamento
            )
        
        # Hashea la contraseña antes de guardarla
            usuario_manager.password = make_password(password)
            usuario_manager.save()
            messages.success(request, "Usuario agregado con éxito.")

        return redirect('usuario')
    context = {
        'form': form
    }
    return render(request, 'admin/usuario/usuario.html', context)


@login_required(login_url='login')
@admin_or_superadmin_required
def cambiar_estado_usuario(request, user_id):
    if request.method == 'POST':
        usuario = Usuario.objects.get(id=user_id)

        # Obtener los valores enviados desde el formulario
        is_admin = request.POST.getlist('admin')
        is_staff = request.POST.getlist('staff')
        is_active = request.POST.getlist('active')
        is_superadmin = request.POST.getlist('superadmin')

        # Convertir los valores a booleanos
        usuario.is_admin = bool(is_admin)
        usuario.is_staff = bool(is_staff)
        usuario.is_active = bool(is_active)
        usuario.is_superadmin = bool(is_superadmin)

        usuario.save()
        messages.success(request, "Estado de Usuario editado con éxito.")

        return redirect('usuario')

    return render(request, 'admin/usuario/usuario.html', {'user_id': user_id})


@login_required(login_url='login')
@admin_or_superadmin_required
def editar_usuario(request, user_id):
    usuarios = Usuario.objects.get(id=user_id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        departamento= request.POST.get('departamento')

        usuarios.first_name = first_name
        usuarios.last_name = last_name
        usuarios.username = username
        if password:
            usuarios.password = make_password(password)
        usuarios.departamento = departamento
        usuarios.save()
        messages.success(request, "Usuario editado con éxito.")
        return redirect('usuario')
    return render(request, 'admin/usuario/usuario.html',{'usuarios': usuarios})


def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superadmin:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("No tienes permiso para eliminar este usuario.")
    return _wrapped_view


@login_required(login_url='login')
@admin_or_superadmin_required
@superuser_required
def eliminar_usuario(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
        # Verifica si el usuario que intentas eliminar no es el superusuario.
        if not usuario.is_superadmin:
            usuario.delete()
            messages.success(request, "Usuario eliminado con éxito.")
        else:
            messages.error(request, "No puedes eliminar al superusuario.")
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")

    return redirect('usuario') 