from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Area)
admin.site.register(Tipo)
admin.site.register(Criticidad)
admin.site.register(Estado)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 
                    'usuario', 
                    'fecha_creacion',
                    'cliente',
                    'ejecutivo',
                    'estado')

admin.site.register(Ticket, TicketAdmin)
