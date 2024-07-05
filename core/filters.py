import django_filters
from .models import Ticket

class TicketFilter(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'fecha_creacion': ['exact'],
        }


class FiltroEjecutivo(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'ejecutivo':['exact']
        }