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
