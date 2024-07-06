import django_filters
from .models import Ticket
from django import forms
from datetime import datetime

class TicketFilter(django_filters.FilterSet):

    fecha_creacion = django_filters.DateFilter(
        field_name='fecha_creacion', 
        lookup_expr='exact', 
        initial=datetime.now().date()
    )


    class Meta:
        model = Ticket
        fields = {
            'fecha_creacion': ['exact'],
        }
    
             
class FiltroEjecutivo(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'ejecutivo':['exact'], 
            'estado':['exact'], 
            'area':['exact'],
        }