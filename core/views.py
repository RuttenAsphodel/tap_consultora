from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

from core.forms import FormCrearUsuario, FormEditarUsuario, FormCrearTicket, FormEditarTicket
from .models import Usuario, Ticket

# Create your views here.
# Decorator login_required para validar el usuario antes de ejecutar la vista Usuarios
#@login_required
# Vista de inicio


def ticket_contar(request):
    contar_todos = Ticket.objects.all().count()
    contar_pendiente = Ticket.objects.filter(estado='Pendiente').count()
    contar_cerrados = Ticket.objects.filter(estado='Cerrado').count()
    
    context_contar = {
        'contar_todos':contar_todos,
        'contar_pendiente': contar_pendiente,
        'contar_cerrados': contar_cerrados,
    }

    return {'ticket_contar': context_contar}
    
def ticket_contar_prioridad(request):
    prioridad_alta = Ticket.objects.filter(criticidad = 'Alta').count()
    prioridad_media = Ticket.objects.filter(criticidad = 'Media').count()
    prioridad_baja = Ticket.objects.filter(criticidad = 'Baja').count()
       
    
    contar_prioridad= {
        'prioridad_alta': prioridad_alta,
        'prioridad_media': prioridad_media,
        'prioridad_baja': prioridad_baja,
    }
    
    return {'ticket_contar_prioridad': contar_prioridad}
    

def ticket_prioridad(request):
    ticket_prioridad = Ticket.objects.filter(criticidad = 'Alta').order_by('-fecha_creacion')[:5]
    return {'ticket_prioridad': ticket_prioridad}

def ticket_pendiente(request):
    ticket_pendiente = Ticket.objects.filter(estado = 'Pendiente').order_by('-fecha_creacion')[:5]
    return {'ticket_pendiente': ticket_pendiente}


def home(request):
    context_a = ticket_contar(request)
    context_b = ticket_contar_prioridad(request)
    context_c = ticket_prioridad(request)
    context_d = ticket_pendiente(request)
       
    context = {**context_a, **context_b,**context_c, **context_d}
    return render(request, 'core/home.html', context)


# Decorator login_required para validar el usuario antes de ejecutar la vista Usuarios
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

# Decorator login_required para validar el usuario antes de ejecutar la vista Tickets
@login_required
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