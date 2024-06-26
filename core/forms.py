from django import forms
from .models import Usuario, Ticket, Comentarios, Profile, Area, Criticidad, Tipo, Estado

# Formularios Usuarios no usar
class FormCrearUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'contrasena', 'group']
        widgets = {
            'nombre: ': forms.TextInput(attrs={
                'placeholder': 'Nombre del Usuario'
                'required'
                
            }),
            
            'apellido: ': forms.TextInput(attrs={
                'placeholder': 'Apellido del Usuario'
                'required'

            }),
            
            'email: ': forms.TextInput(attrs={
                'placeholder': 'Email del Usuario',
                'type':'email'
                'required'

            }),
            
            'contrasena': forms.TextInput(attrs={
                'type':'password'
                'required'
                }
            )
        }
        labels = {
            'nombre': 'Nombre del Usuario',
            'apellido': 'Apellido del Usuario', 
            'email': 'Correo Electronico',
            'contrasena':'Contraseña',
            'rol':'Rol de Usuario:'
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo electrónico ya está registrado.')
        return email

class FormEditarUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'rol']
        
        widgets = {
            'nombre: ': forms.TextInput(attrs={
                'placeholder': 'Nombre del Usuario'
                'required'
                
            }),
            
            'apellido: ': forms.TextInput(attrs={
                'placeholder': 'Apellido del Usuario'
                'required'

            }),
            
            'email: ': forms.TextInput(attrs={
                'placeholder': 'Email del Usuario',
                'type':'email'
                'required'

            }),
            
            'contrasena': forms.TextInput(attrs={
                'type':'password'
                'required'
                }
            )
        }
        
        labels = {
            'nombre': 'Nombre del Usuario',
            'apellido': 'Apellido del Usuario', 
            'email': 'Correo Electronico',
            'contrasena':'Contraseña',
            'rol':'Rol de Usuario:'
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        usuario_actual = self.instance
        if Usuario.objects.filter(email=email).exclude(id=usuario_actual.id).exists():
            raise forms.ValidationError('El correo electrónico ya está registrado.')
        return email
    

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
        fields = ['ejecutivo','estado', 'descripcion', 'observaciones']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ejecutivo'].queryset = Profile.objects.filter(group=2)

#form crear area
class FormCrearArea(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre']
        widgets = {
            'nombre: ': forms.TextInput(attrs={
                'placeholder': 'Nombre del Area'
                'required'
            })
        }
        labels = {
            'nombre': 'Nombre del Area'
        }

#form crear criticidad
class FormCrearCriticidad(forms.ModelForm):
    class Meta:
        model = Criticidad
        fields = ['nivel']
        widgets = {
            'nivel: ': forms.TextInput(attrs={
                'placeholder': 'nivel Criticidad'
                'required'
            })
        }
        labels = {
            'nivel': 'nivel criticidad'
        }

#form crear tipo
class FormCrearTipo(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['tipo']
        widgets = {
            'tipo: ': forms.TextInput(attrs={
                'placeholder': 'tipo ticket'
                'required'
            })
        }
        labels = {
            'tipo': 'tipo ticket'
        }

#form crear estado
class FormCrearEstado(forms.ModelForm):
    class Meta:
        model = Estado
        fields = ['estado']
        widgets = {
            'estado: ': forms.TextInput(attrs={
                'placeholder': 'Estado ticket'
                'required'
            })
        }
        labels = {
            'estado': 'Estado ticket'
        }



# Formulario de Comentario (x desarrollar)
class FormCrearComentario(forms.ModelForm):
    class Meta:
        model = Comentarios
        fields = ['ticket','user','comentario']
        

# Formulario de Configuracion de Perfiles
class FormConfigProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nombre','apellido', 'email', 'group','location' ]



