from django.urls import path
from .views import home, vista_listar_tickets, vista_listar_usuarios, vista_crear_usuario, vista_detalle_usuario, exit

urlpatterns = [
    path('', home, name = 'home'),
    
    # Urls Tickets
    path('tickets/', vista_listar_tickets, name='tickets'),
    
    # Urls Usuarios
    path('listar_usuarios/', vista_listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', vista_crear_usuario, name='crear_usuario'),
    path('<int:id>/detalle_usuario', vista_detalle_usuario, name='detalle_usuario'),
    
    path('logout/', exit, name='exit')    
]
