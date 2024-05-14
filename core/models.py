from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    rol = models.CharField(max_length=50, choices=[('Administrador', 'Administrador'), ('Ejecutivo', 'Ejecutivo'), ('Cliente', 'Cliente')])
    is_active = models.BooleanField(default=True)

class Ticket(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tickets_creados')
    ejecutivo = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='tickets_asignados')
    area = models.CharField(max_length=255, choices=[('ejecutivo', 'Ejecutivo Telefonico'), ('soporte', 'Soporte'), ('cliente', 'Atencion al Cliente'), ('nivel2', 'Soporte Nivel 2')])
    tipo = models.CharField(max_length=255, choices=[('incidente', 'Incidente'), ('solicitud', 'Solicitud'), ('cambio', 'Cambio')])
    criticidad = models.CharField(max_length=255, choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')])
    estado = models.CharField(max_length=255, choices=[('pendiente', 'Pendiente'), ('solucionado', 'Solucionado'), ('validado', 'Validado'), ('cerrado', 'Cerrado')])
    descripcion = models.TextField()
    observaciones = models.TextField(blank=True)
