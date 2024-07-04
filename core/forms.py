from django import forms
from .models import Ticket, Comentarios, Profile, Area, Criticidad, Tipo, Estado
    

# Formularios Ticket
class FormCrearTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['cliente', 'ejecutivo', 'area', 'tipo', 'criticidad', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Profile.objects.filter(group=3)
        self.fields['ejecutivo'].queryset = Profile.objects.filter(group=2)

class FormEditarTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ejecutivo','area','estado', 'descripcion']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ejecutivo'].queryset = Profile.objects.filter(group=2)

#form crear area
class FormCrearArea(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre_area']
        widgets = {
            'nombre_area: ': forms.TextInput(attrs={
                'placeholder': 'Nombre del Area'
                'required'
            })
        }
        labels = {
            'nombre_area': 'Nombre del Area'
        }

#form crear criticidad
class FormCrearCriticidad(forms.ModelForm):
    class Meta:
        model = Criticidad
        fields = ['nombre_criticidad']
        widgets = {
            'nombre_criticidad: ': forms.TextInput(attrs={
                'placeholder': 'nivel Criticidad'
                'required'
            })
        }
        labels = {
            'nombre_criticidad': 'nivel criticidad'
        }

#form crear tipo
class FormCrearTipo(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['tipo_ticket']
        widgets = {
            'tipo_ticket: ': forms.TextInput(attrs={
                'placeholder': 'tipo ticket'
                'required'
            })
        }
        labels = {
            'tipo_ticket': 'Tipo Ticket'
        }

#form crear estado
class FormCrearEstado(forms.ModelForm):
    class Meta:
        model = Estado
        fields = ['estado_ticket']
        widgets = {
            'estado_ticket: ': forms.TextInput(attrs={
                'placeholder': 'Estado Ticket'
                'required'
            })
        }
        labels = {
            'estado_ticket': 'Estado Ticket'
        }



# Formulario de Comentario (x desarrollar)
class FormCrearComentario(forms.ModelForm):
    class Meta:
        model = Comentarios
        fields = ['comentario', 'user']
        

# Formulario de Configuracion de Perfiles
class FormConfigProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nombre','apellido', 'email', 'group','location' ]



