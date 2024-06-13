from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps

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
def administrador(request):
    return render(request, 'admin/dashboard/dashboard.html')