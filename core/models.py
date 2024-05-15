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
    area = models.CharField(max_length=255, choices=[('Ejecutivo Telefonico', 'Ejecutivo Telefonico'), ('Soporte', 'Soporte'), ('Atencion al Cliente', 'Atencion al Cliente'), ('Soporte Nivel 2', 'Soporte Nivel 2')])
    tipo = models.CharField(max_length=255, choices=[('Incidente', 'Incidente'), ('Solicitud', 'Solicitud'), ('Cambio', 'Cambio')])
    criticidad = models.CharField(max_length=255, choices=[('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')])
    estado = models.CharField(max_length=255, choices=[('Pendiente', 'Pendiente'), ('Solucionado', 'Solucionado'), ('Validado', 'Validado'), ('Cerrado', 'Cerrado')], default='Pendiente')
    descripcion = models.TextField()
    observaciones = models.TextField(blank=True)
