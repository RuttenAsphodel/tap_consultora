from django.urls import path
from .views import home, vista_listar_tickets, vista_listar_usuarios, vista_crear_usuario, vista_detalle_usuario, eliminar_usuario_logico,vista_crear_ticket, vista_detalle_ticket,vista_editar_ticket ,exit

urlpatterns = [
    path('', home, name = 'home'),
    
    # Urls Tickets
    path('tickets/', vista_listar_tickets, name='tickets'),
    path('crear_ticket/', vista_crear_ticket, name='crear_ticket'),
    path('<int:id>/detalle_ticket', vista_detalle_ticket, name='detalle_ticket'),    
    path('<int:id>/editar_ticket', vista_editar_ticket, name='editar_ticket'),
    
    
    # Urls Usuarios
    path('listar_usuarios/', vista_listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', vista_crear_usuario, name='crear_usuario'),
    path('<int:id>/detalle_usuario', vista_detalle_usuario, name='detalle_usuario'),
    path('<int:id>/eliminar_usuario', eliminar_usuario_logico, name='eliminar_usuario'),
    
    path('logout/', exit, name='exit')    
]
