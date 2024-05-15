from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from core.forms import FormCrearUsuario, FormEditarUsuario, FormCrearTicket, FormEditarTicket
from .models import Usuario, Ticket

# Create your views here.

# Vista de inicio
def home(request):
    return render(request, 'core/home.html')


# Decorator login_required para validar el usuario antes de ejecutar la vista products
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


# Vista Eliminar Usuario
def eliminar_usuario_logico(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if usuario.is_active:
        usuario.is_active = False
        usuario.save()
        messages.success(request, 'Usuario eliminado exitosamente.')
    else:
        messages.error(request, 'El usuario ya está eliminado.')
    return redirect('listar_usuarios')


# Vistas Ticket
# Vista Mostrar Tickets

def vista_listar_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'core/tickets/listar_tickets.html', {'tickets': tickets})

def vista_detalle_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'core/tickets/detalle_ticket.html', {'ticket': ticket})


def vista_crear_ticket(request):
    if request.method == 'POST':
        # Filtrar ejecutivos disponibles solo si el usuario es cliente
        # if request.usuario.rol == 'Cliente':
        #     form = FormCrearTicket(request.POST, cliente=request.usuario)
        # else:
        form = FormCrearTicket(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tickets')
    else:
        # Filtrar ejecutivos disponibles solo si el usuario es cliente
        # if request.Usuario.rol == 'Cliente':
        #     form = FormCrearTicket(cliente=request.usuario)
        # else:
        form = FormCrearTicket()

    return render(request, 'core/tickets/crear_ticket.html', {'form': form})

@login_required
def vista_editar_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    # Permitir edición solo al ejecutivo asignado o al cliente creador
    # if request.usuario == ticket.ejecutivo or request.usuario == ticket.cliente:
    if request.method == 'POST':
        form = FormEditarTicket(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('tickets')
    else:
        form = FormEditarTicket(instance=ticket)
    #else:
    #   return redirect('listar_tickets')  # Redirigir si no tiene permiso

    return render(request, 'core/tickets/editar_ticket.html', {'form': form, 'ticket': ticket})


def exit(request):
    logout(request)
    return redirect('home')