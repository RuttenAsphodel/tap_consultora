from django.urls import path
from .views import home, vista_listar_tickets, vista_listar_usuarios, vista_crear_usuario, vista_detalle_usuario, eliminar_usuario_logico,vista_crear_ticket, vista_detalle_ticket,vista_editar_ticket ,exit, login_view, register_view, vista_crear_area, vista_listar_area, terminos_y_condiciones

urlpatterns = [
    path('', home, name = 'home'),
    
    # Urls Tickets
    path('tickets/', vista_listar_tickets, name='tickets'),
    path('crear_ticket/', vista_crear_ticket, name='crear_ticket'),
    path('<int:id>/detalle_ticket', vista_detalle_ticket, name='detalle_ticket'),    
    path('<int:id>/editar_ticket', vista_editar_ticket, name='editar_ticket'),
    

    # Urls Usuarios
    path('listar_usuarios/', vista_listar_usuarios, name='listar_usuarios'),
    path('<int:id>/crear_usuario/', vista_crear_usuario, name='crear_usuario'),
    path('<int:id>/detalle_usuario', vista_detalle_usuario, name='detalle_usuario'),
    path('<int:id>/eliminar_usuario', eliminar_usuario_logico, name='eliminar_usuario'),
    
    # Urls Login
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', exit, name='exit'),    
    
    # Urls Terminos y Condiciones
    path('terminos-y-condiciones/', terminos_y_condiciones, name='terminos_y_condiciones'),
    
    # Urls Mantenedores
    # Areas
    path('listar_area/', vista_listar_area, name='listar_area'),
    path('crear_area/', vista_crear_area, name='crear_area'),
    
]
