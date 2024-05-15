from django import forms
from .models import Usuario, Ticket

# Formularios Usuarios
class FormCrearUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'contrasena', 'rol']
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
        self.fields['cliente'].queryset = Usuario.objects.filter(rol='Cliente')
        self.fields['ejecutivo'].queryset = Usuario.objects.filter(rol='Ejecutivo')

class FormEditarTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['area', 'tipo', 'criticidad', 'estado', 'descripcion', 'observaciones']
