from django.contrib.auth.models import User
from django.db import models
    
# Modelo de datos Usuarios
class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, choices=[('Administrador', 'Administrador'), ('Ejecutivo', 'Ejecutivo'), ('Cliente', 'Cliente')])
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre + " " + self.apellido    


    
# Modelo de datos Tickets
class Ticket(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tickets_creados')
    ejecutivo = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tickets_asignados')
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
    #oye crsitian, estaba viendo los datos que teniamos antes y no emaparece anda con vista, lo mas cercanos seria "departamento"
    #pero viendo la linea 23 muestra como "ejecutivo telefonico"entonces seria el area que acepta el ticket, el que lo envia o alguna wea asi?
    #y lo que tenemos marcado como "departamento" tendria solo "id_departamento" y "nombre", habria que ponerle alguna cuestion ams aparte de eso?
    


# Modelo de datos Tipo
class Tipo(models.Model):
    tipo_ticket = models.CharField(max_length=50, blank=False)
    #aca esta marcado en la linea 24 como "solicitud", si mal no recuerdo anotamos 4 estados para los ticket consulta, felicitacion, reclamo y problema 



    
# Modelo de Datos Criticidad
class Criticidad(models.Model):
    nombre_criticidad = models.CharField(max_length=255, blank=False)
    #aca esta marcada en la linea 25 como "media", creo que eran 3, en este caso habria que asociarles un valor numerico a cada una(onda, 1, 2 y 3?)
    #y aca en criticidad habria que crear 3 lineas dandoles el valor a cada una?
    #ademasn, en la info que teniamos antes se llama "prioridad", con 2 valores:"id_prioridad" y "prioridad"

    
# Modelo de datos EstadoTicket
class Estado(models.Model):
    estado_ticket = models.CharField(max_length=55, blank=False)
    #aca ya estan marcados los estados con valores, encontre el valor "1" y el "4" en views.py(lineas 18, 19 y 49)
    #tambien lo que tenemos guardado marca este con 2 datos,"id_estado" y "estado"



