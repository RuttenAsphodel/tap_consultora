from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from django_filters.views import FilterView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .filters import TicketFilter, FiltroEjecutivo
from .forms import FormCrearTicket, FormEditarTicket, FormConfigProfile, FormCrearArea, FormCrearCriticidad, FormCrearTipo, FormCrearEstado, FormCrearComentario
from .models import Ticket, Profile, Area, Criticidad, Tipo, Estado, Comentarios

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


# Vista Eliminar Usuario Logico
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

# Decorator login_required para validar el usuario antes de ejecutar la vista Tickets
@login_required

# Vista Mostrar Tickets
def vista_listar_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'core/tickets/listar_tickets.html', {'tickets': tickets})
    
# Decorator login_required para validar el usuario antes de ejecutar la vista Tickets
@login_required
# Vista de Detalle de Tickets
def vista_detalle_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    comentarios = ticket.comentarios.all().order_by('-fecha_comentario')
    
    if request.method =='POST':
        form_comentario = FormCrearComentario(request.POST)
        if form_comentario.is_valid():
            nuevo_comentario = form_comentario.save(commit=False)
            nuevo_comentario.ticket = ticket
            nuevo_comentario.save()
            return redirect('detalle_ticket', id=ticket.id)
    else:
        form_comentario = FormCrearComentario
        
    
    return render(request, 'core/tickets/detalle_ticket.html', {
        'ticket' : ticket,
        'comentarios': comentarios,
        'form_comentario': form_comentario,
    })

# return render(request, 'core/tickets/detalle_ticket.html', {'ticket': ticket})



@login_required
# Vista de Creacion del Ticket
def vista_crear_ticket(request):
    if request.method == 'POST':
        # Filtrar ejecutivos disponibles solo si el usuario es cliente
        # if request.profile.group == 'Cliente':
        #     form = FormCrearTicket(request.POST, cliente=request.profile)
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
        # if request.profile.group == 'Cliente':
        #     form = FormCrearTicket(cliente=request.profile)
        # else:
        form = FormCrearTicket()

    return render(request, 'core/tickets/crear_ticket.html', {'form': form})

# Vista de Actualizacion del Ticket
@login_required
def vista_editar_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    # Permitir edición solo al ejecutivo asignado o al cliente creador
    # if request.user == ticket.ejecutivo or request.user == ticket.cliente:
    if request.method == 'POST':
        form = FormEditarTicket(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('tickets')
    else:
        form = FormEditarTicket(instance=ticket)
    #else:
    #   return redirect('listar_tickets')  # Redirigir si no tiene permiso

    comentarios = ticket.comentarios.all().order_by('-fecha_comentario')
    
    if request.method =='POST':
        form_comentario = FormCrearComentario(request.POST)
        if form_comentario.is_valid():
            nuevo_comentario = form_comentario.save(commit=False)
            nuevo_comentario.ticket = ticket
            nuevo_comentario.save()
            return redirect('editar_ticket', id=ticket.id)
    else:
        form_comentario = FormCrearComentario
        
    
    return render(request, 'core/tickets/editar_ticket.html', {
        'ticket' : ticket,
        'form' : form,
        'comentarios': comentarios,
        'form_comentario': form_comentario,
        
    })
#    return render(request, 'core/tickets/editar_ticket.html', {'form': form, 'ticket': ticket})

# Vistas de Informes

#Modificar vista para realizar informes
def vista_informe_x_ejecutivos(request):
    # ticket = Ticket.objects.all()
    
    # # obtener el valor del formulario de búsqueda si existe
    # ejecutivos_query = request.GET.get('ejecutivo')
    # if ejecutivos_query:
    #     ticket = ticket.filter(ejecutivo__profile__icontains=ejecutivos_query)

#     page = request.GET.get('page', 1)
#     paginator = Paginator(equipos, 20)
    
#     try:
#         equipos = paginator.page(page)
#     except PageNotAnInteger:
#         equipos = paginator.page(1)
#     except EmptyPage:
#         equipos = paginator.page(paginator.num_pages)
        
    filtro_ejecutivo = FiltroEjecutivo(request.GET, queryset=Ticket.objects.all())
    return render(request, 'core/informes/informe_x_ejecutivos.html', {'filtro_ejecutivo': filtro_ejecutivo})


def vista_informe_diario(request):
    ticket_filter = TicketFilter(request.GET, queryset=Ticket.objects.all())
    return render(request, 'core/informes/informe_diario.html', {'filter': ticket_filter})


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

    

@login_required
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


@login_required
# Vistas CRUD Tipo
def vista_crear_tipo(request):
    if request.method == 'POST':

        form_tipo = FormCrearTipo(request.POST)
        if form_tipo.is_valid():
            nuevo_tipo = form_tipo.save(commit=False)
            nuevo_tipo.user = request.user
            nuevo_tipo.save()
            return redirect('listar_tipo')
    else:
        form_tipo = FormCrearTipo()

    return render(request, 'core/tipos/crear_tipo.html', {'form_tipo': form_tipo})

@login_required
def vista_listar_tipo(request):
    listado_tipo = Tipo.objects.all()
    return render(request, 'core/tipos/listar_tipo.html', {'listado_tipo': listado_tipo})

@login_required
# Vistas CRUD Estado
def vista_crear_estado(request):
    if request.method == 'POST':

        form_estado = FormCrearEstado(request.POST)
        if form_estado.is_valid():
            nuevo_estado = form_estado.save(commit=False)
            nuevo_estado.user = request.user
            nuevo_estado.save()
            return redirect('listar_estado')
    else:
        form_estado = FormCrearEstado()

    return render(request, 'core/estados/crear_estado.html', {'form_estado': form_estado})

@login_required
def vista_listar_estado(request):
    listado_estado = Estado.objects.all()
    return render(request, 'core/estados/listar_estado.html', {'listado_estado': listado_estado})


# Terminos y Condiciones
def terminos_y_condiciones(request):
    return render(request, 'core/terminos_y_condiciones.html')