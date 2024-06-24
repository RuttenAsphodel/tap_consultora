from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
    
# Modelo de datos Usuarios
class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, choices=[('Administrador', 'Administrador'), ('Ejecutivo', 'Ejecutivo'), ('Cliente', 'Cliente')])
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Rol', default=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre + " " + self.apellido

    
    
    
# Modelo de datos Tickets
class Ticket(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='tickets_creados')
    ejecutivo = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='tickets_asignados')
    area = models.ForeignKey("Area", on_delete=models.CASCADE, verbose_name="Area", default = 'Ejecutivo Telefonico')
    tipo = models.ForeignKey("Tipo", on_delete=models.CASCADE, verbose_name="Tipo",default='Solicitud')
    criticidad = models.ForeignKey("Criticidad", on_delete=models.CASCADE, verbose_name="Criticidad",default='Media')
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE, verbose_name="Estado", default=1)
    descripcion = models.TextField()
    observaciones = models.TextField(blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Usuario', null=True)
    


# Modelo de Datos Area 
class Area(models.Model):
    nombre_area = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.nombre_area


# Modelo de datos Tipo
class Tipo(models.Model):
    tipo_ticket = models.CharField(max_length=50, blank=False)
    
    def __str__(self) :
        return self.tipo_ticket
    
    
# Modelo de Datos Criticidad
class Criticidad(models.Model):
    nombre_criticidad = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.nombre_criticidad


# Modelo de datos EstadoTicket
class Estado(models.Model):
    estado_ticket = models.CharField(max_length=55, blank=False)
    
    def __str__(self):
        return self.estado_ticket


class Comentarios(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=255, blank=True, verbose_name='Comentario')
    fecha_comentario = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')


# Prueba de edicion de perfil de usuario Django
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True)
    apellido = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Rol', default=2)
    is_active = models.BooleanField(default=True)
    location = models.CharField(max_length=30, blank=True)
    
    

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()