from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from core.forms import FormCrearUsuario, FormEditarUsuario
from .models import Usuario

# Create your views here.

# Vista de inicio
def home(request):
    return render(request, 'core/home.html')


# Decorator login_required para validar el usuario antes de ejecutar la vista products
@login_required 

# Vista Tickets
def vista_listar_tickets(request):
    return render(request, 'core/tickets/listar_tickets.html')

@login_required
# Vista Listar Usuarios
def vista_listar_usuarios(request):
    usuarios = Usuario.objects.filter(is_active=True)
    return render(request, 'core/usuarios/listar_usuarios.html', {'usuarios': usuarios})


# Vista Creacion Usuarios
def vista_crear_usuario(request):
    if request.method == 'POST':
        form = FormCrearUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = FormCrearUsuario()

    return render(request, 'core/usuarios/crear_usuario.html', {'form': form})


# Vista Detalle de Usuario
def vista_detalle_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    return render(request, 'core/usuarios/detalle_usuario.html', {'usuario': usuario})


def exit(request):
    logout(request)
    return redirect('home')