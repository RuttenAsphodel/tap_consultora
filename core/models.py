from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
    
  
# Modelo de datos Tickets
class Ticket(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Enlazados a Modelo Profile
    cliente = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='tickets_creados') 
    ejecutivo = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='tickets_asignados')
    # Enlazado a Modelo Area
    area = models.ForeignKey("Area", on_delete=models.CASCADE, verbose_name="Area", default = 'Ejecutivo Telefonico')
    # Enlazado a Modelo Tipo
    tipo = models.ForeignKey("Tipo", on_delete=models.CASCADE, verbose_name="Tipo",default='Solicitud')
    # Enlazado a Modelo Criticidad
    criticidad = models.ForeignKey("Criticidad", on_delete=models.CASCADE, verbose_name="Criticidad",default='Media')
    # Enlazado a Modelo EstadoTicket
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE, verbose_name="Estado", default=1)
    descripcion = models.TextField()
    observaciones = models.TextField(blank=True)
    fecha_cierre = models.DateTimeField(auto_now=True)
    
    # Enlazado al modelo User de Django. 
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Usuario', null=True)

        
        
# -----------------------------------------------------------------------------------------------------------------
# Estos modelos se deben enlazar a vistas para que podamos manejarlos desde la aplicacion, y podamos crear estados, areas, criticidad (prioridad), tipos y estados de los tickets

# Modelo de Datos Area 
class Area(models.Model):
    nombre_area = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.nombre_area
    #oye crsitian, estaba viendo los datos que teniamos antes y no emaparece anda con vista, lo mas cercanos seria "departamento"
    #pero viendo la linea 23 muestra como "ejecutivo telefonico"entonces seria el area que acepta el ticket, el que lo envia o alguna wea asi?
    
    # Ejecutivo Telefonico es el valor por defecto que se muestra en el formulario de Ingreso de los Tickets
    
    
    #y lo que tenemos marcado como "departamento" tendria solo "id_departamento" y "nombre", habria que ponerle alguna cuestion ams aparte de eso?
    
    
    # Gabriel con area me refiero adonde va derivado, no al departamento de origen del ticket. 
    # Llamese Ejecutivo Telefonico, Soporte Nivel 1, Soporte Nivel 2, Atencion Publico Entre otros, el de Departamento va enlazado al modelo de usuarios, pero ese lo vamos a encadenar al nuevo modelo llamado Profile, que toma el modelo de usuarios de Django.  


# Modelo de datos Tipo
class Tipo(models.Model):
    tipo_ticket = models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        return self.tipo_ticket
    #aca esta marcado en la linea 24 como "solicitud", si mal no recuerdo anotamos 4 estados para los ticket consulta, felicitacion, reclamo y problema
    
    # Solicitud es el valor por defecto, tal como el modelo de arriba, es como se va a a mostar al momento de ingresar los tickets.  


   
# Modelo de Datos Criticidad
class Criticidad(models.Model):
    nombre_criticidad = models.CharField(max_length=255, blank=False)
    
    def __str__(self):
        return self.nombre_criticidad
    
    #aca esta marcada en la linea 25 como "media", creo que eran 3, en este caso habria que asociarles un valor numerico a cada una(onda, 1, 2 y 3?)
    #y aca en criticidad habria que crear 3 lineas dandoles el valor a cada una?
    #ademasn, en la info que teniamos antes se llama "prioridad", con 2 valores:"id_prioridad" y "prioridad"

    # Mismo caso que lo que mencione arriba
    
# Modelo de datos EstadoTicket
class Estado(models.Model):
    estado_ticket = models.CharField(max_length=55, blank=False)

    
    def __str__(self):
        return self.estado_ticket


# -------- No tocar estos modelos ------------

# Modelo de Comentarios no tocar.
class Comentarios(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comentarios' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    comentario = models.TextField(max_length=255, blank=True, verbose_name='Comentario')
    fecha_comentario = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    
    def __str__(self):
        return self.comentario


# Perfil de usuario extendido Django
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    apellido = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Rol', default=2, null=True)
    is_active = models.BooleanField(default=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    
    

    def __str__(self):
        return self.nombre + ' ' + self.apellido

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
