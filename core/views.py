from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import CreateView, UpdateVsiew, DetailView, ListView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

from .forms import FormCrearUsuario, FormEditarUsuario, FormCrearTicket, FormEditarTicket, FormConfigProfile, FormCrearArea, FormCrearCriticidad, FormCrearTipo, FormCrearEstado #FormCrearComentario
from .models import Usuario, Ticket, Profile, Area, Criticidad, Tipo, Estado #Comentarios


# Create your views here.
# Decorator login_required para validar el usuario antes de ejecutar la vista Usuarios
#@login_required
# Vista de inicio


def ticket_contar(request):
    contar_todos = Ticket.objects.all().count()
    contar_pendiente = Ticket.objects.filter(estado=1).count()
    contar_cerrados = Ticket.objects.filter(estado=4).count()
    
    context_contar = {
        'contar_todos':contar_todos,
        'contar_pendiente': contar_pendiente,
        'contar_cerrados': contar_cerrados,
    }

    return {'ticket_contar': context_contar}
    
def ticket_contar_prioridad(request):
    prioridad_alta = Ticket.objects.filter(criticidad = 1).count()
    prioridad_media = Ticket.objects.filter(criticidad = 2).count()
    prioridad_baja = Ticket.objects.filter(criticidad = 3).count()
       
    
    contar_prioridad= {
        'prioridad_alta': prioridad_alta,
        'prioridad_media': prioridad_media,
        'prioridad_baja': prioridad_baja,
    }
    
    return {'ticket_contar_prioridad': contar_prioridad}
    

def ticket_prioridad(request):
    ticket_prioridad = Ticket.objects.filter(criticidad = 1).order_by('-fecha_creacion')[:5]
    return {'ticket_prioridad': ticket_prioridad}

def ticket_pendiente(request):
    ticket_pendiente = Ticket.objects.filter(estado = 1).order_by('-fecha_creacion')[:5]
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
    profiles = Profile.objects.filter(is_active=True)
    return render(request, 'core/usuarios/listar_usuarios.html', {'profiles': profiles})
    

# Vista Configuracion Perfil de Usuarios
def vista_crear_usuario(request, id):
    profile = get_object_or_404(Profile, id=id)

    if request.method == 'POST':
        form = FormConfigProfile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = FormConfigProfile()

    return render(request, 'core/usuarios/crear_usuario.html', {'form': form, 'profile': profile})

# Vista Detalle de Usuario
def vista_detalle_usuario(request, id):
    profile = get_object_or_404(Profile, id=id)
    return render(request, 'core/usuarios/detalle_usuario.html', {'profile': profile})


# Vista Eliminar Usuario
def eliminar_usuario_logico(request, id):
    usuario = get_object_or_404(Profile, id=id)
    if usuario.is_active:
        usuario.is_active = False
        usuario.save()
        messages.success(request, 'Usuario eliminado exitosamente.')
    else:
        messages.error(request, 'El usuario ya está eliminado.')
    return redirect('listar_usuarios')

# Vistas Ticket
# Vista Mostrar Tickets
# Decorator login_required para validar el usuario antes de ejecutar la vista Tickets

@login_required
def vista_listar_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'core/tickets/listar_tickets.html', {'tickets': tickets})
    
# Decorator login_required para validar el usuario antes de ejecutar la vista Tickets
@login_required
def vista_detalle_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'core/tickets/detalle_ticket.html', {'ticket': ticket})

@login_required
def vista_crear_ticket(request):
    if request.method == 'POST':
        # Filtrar ejecutivos disponibles solo si el usuario es cliente
        # if request.usuario.rol == 'Cliente':
        #     form = FormCrearTicket(request.POST, cliente=request.usuario)
        # else:
        form = FormCrearTicket(request.POST)
        if form.is_valid():
            # Guardamos el ticket en BD sin confirmar aun
            nuevo_ticket = form.save(commit=False)
            # Asignamos el ticket al usuario autenticado
            nuevo_ticket.user = request.user
            # Guardamos el ticket con el usuario autenticado
            nuevo_ticket.save()
            # Redirige a la lista de tickets
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


# class TicketDetailView(LoginRequiredMixin, DetailView):
#     model = Ticket
#     template_name = 'core/tickets/detalle_ticket.html'
#     context_object_name = 'ticket'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comentarios'] = self.object.comentario_set.all() # Obtener todos los comentarios del ticket
#         context['comentario_form'] = FormCrearComentario()
#         return context

# @login_required
# def crear_comentario(request, pk):
#     ticket = get_object_or_404(Ticket, pk=pk)
#     if request.method == 'POST':
#         form = FormCrearComentario(request.POST)
#         if form.is_valid():
#             comentario = form.save(commit=False)
#             comentario.ticket = ticket
#             comentario.usuario = request.user
#             comentario.save()
#             return redirect('detalle_ticket', pk=pk)
#     else:
#         form = FormCrearComentario()
#     return render(request, 'core/tickets/comentario_form.html', {'form': form})

def exit(request):
    logout(request)
    return redirect('home')

# Vista de Login
def login_view(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('home')
    # Verificamos si se envió el formulario
    if request.method == 'POST':
        # Creamos un formulario con los datos enviados
        form = AuthenticationForm(request, data=request.POST)
        # Verificamos si el formulario es válido
        if form.is_valid():
            # Autenticamos al usuario
            user = form.get_user()
            # Iniciamos sesión
            login(request, user)
            # Obtenemos la URL a la que se debe redireccionar
            next_url = request.GET.get('next', '/home/')
            # Redireccionamos a la página principal o a la URL
            return redirect(next_url)
    else:
        # Creamos un formulario vacío
        form = AuthenticationForm(request)
    # Creamos el contenido de la respuesta
    context = {'form': form}
    # Creamos la respuesta
    return render(request, 'registration/login.html', context)

# Vista de Registro de Usuario
def register_view(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('home')
    # Verificamos si se envió el formulario
    if request.method == 'POST':
        # Creamos un formulario con los datos enviados
        form = UserCreationForm(request.POST)
        # Verificamos si el formulario es válido
        if form.is_valid():
            # Guardamos el usuario
            form.save()
            # Redirigimos al usuario a la página de inicio de sesión
            return redirect('login')
    else:
        # Creamos un formulario vacío
        form = UserCreationForm()
    # Creamos el contenido de la respuesta
    context = {'form': form}
    # Creamos la respuesta
    return render(request, 'registration/register.html', context)

# Vistas para Gabriel Mena

# Vistas CRUD Area

@login_required
def vista_crear_area(request):
    if request.method == 'POST':

        form_area = FormCrearArea(request.POST)
        if form_area.is_valid():
            nuevo_area = form_area.save(commit=False)
            nuevo_area.user = request.user
            nuevo_area.save()
            return redirect('listar_area')
    else:
        form_area = FormCrearArea()

    return render(request, 'core/areas/crear_area.html', {'form_area': form_area})

@login_required
def vista_listar_area(request):
    listado_area = Area.objects.all()
    return render(request, 'core/areas/listar_areas.html', {'listado_area': listado_area})

    

# Vistas CRUD Criticidad

def vista_crear_criticidad(request):
    if request.method == 'POST':

        form = FormCrearCriticidad(request.POST)
        if form.is_valid():
            nuevo_criticidad = form.save(commit=False)
            nuevo_criticidad.user = request.user
            nuevo_criticidad.save()
            return redirect('tickets')
    else:
        form = FormCrearCriticidad()

    return render(request, 'core/tickets/crear_ticket.html', {'form': form})



# Vistas CRUD Tipo
def vista_crear_tipo(request):
    if request.method == 'POST':

        form = FormCrearTipo(request.POST)
        if form.is_valid():
            nuevo_tipo = form.save(commit=False)
            nuevo_tipo.user = request.user
            nuevo_tipo.save()
            return redirect('tickets')
    else:
        form = FormCrearTipo()

    return render(request, 'core/tickets/crear_ticket.html', {'form': form})

# Vistas CRUD Estado
def vista_crear_estado(request):
    if request.method == 'POST':

        form = FormCrearEstado(request.POST)
        if form.is_valid():
            nuevo_estado = form.save(commit=False)
            nuevo_estado.user = request.user
            nuevo_estado.save()
            return redirect('tickets')
    else:
        form = FormCrearEstado()

    return render(request, 'core/tickets/crear_ticket.html', {'form': form})

# Terminos y Condiciones
def terminos_y_condiciones(request):
    return render(request, 'core/terminos_y_condiciones.html')